import json
import pickle
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import source.base_api as base_api
from source.machine_learning.subject_area import get_data


def model_training(data: pd.DataFrame):
    # data=pd.get_dummies(data, columns=["subtopic"],drop_first=True)
    data = data[["subject","year", "count_subtopic"]]
    # print(data.set_index(["year", "subtopic"]))
    
    data = data.groupby(['subject', 'year'], as_index=False).agg({'count_subtopic': 'sum'})
    
    data = data.rename(columns={'count_subtopic': 'count_subject'})
    
    all_combinations = pd.MultiIndex.from_product(
        [data["subject"].unique(), data["year"].unique()],
        names=["subject", "year"],
    )

    data = (
        data.set_index(["subject", "year"])
        .reindex(all_combinations, fill_value=0)
        .reset_index()
    )

    total_count = (
        data.groupby("subject")
        .sum(numeric_only=True)
        .reset_index()
    )

    for subject_name in total_count["subject"]:
        subject = data[data["subject"] == subject_name]
        X = subject[["year"]] 
        y = subject["count_subject"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        lr_regressor = LinearRegression()
        lr_regressor.fit(X_train, y_train)
        y_pred = lr_regressor.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Subject: {subject_name}")
        print("MSE:", mse)
        print("R2:", r2)

        with open(
            base_api.relative_to_abs(
                [
                    "source",
                    "machine_learning",
                    "model",
                    "subject",
                    "Subject_{}.pkl".format(subject_name),
                ]
            ),
            "wb",
        ) as file:
            pickle.dump(lr_regressor, file)


if __name__ == "__main__":
    data = get_data()
    model_training(data)

import json
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import source.base_api as base_api
from source.machine_learning.subject_area import get_data

NUMBER_OF_TOP = 20
MINIMUM_YEARS = 3


def model_training(data: pd.DataFrame):
    # data=pd.get_dummies(data, columns=["subtopic"],drop_first=True)
    data = data[["subtopic_code", "count_subtopic", "year"]]
    # print(data.set_index(["year", "subtopic"]))

    all_combinations = pd.MultiIndex.from_product(
        [data["subtopic_code"].unique(), data["year"].unique()],
        names=["subtopic_code", "year"],
    )

    data = (
        data.set_index(["subtopic_code", "year"])
        .reindex(all_combinations, fill_value=0)
        .reset_index()
    )

    total_count = (
        data.groupby("subtopic_code")
        .sum(numeric_only=True)
        .sort_values(by=["count_subtopic"], ascending=False)
        .reset_index()
    )

    count = 0

    for subtopic_code in total_count["subtopic_code"]:
        if count > NUMBER_OF_TOP:
            break
        subtopic_data = data[data["subtopic_code"] == subtopic_code]
        if (subtopic_data["year"] != 0).sum() < MINIMUM_YEARS:
            continue
        count += 1
        X = subtopic_data[["year"]]  # have to be 2d for training
        y = subtopic_data["count_subtopic"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        rf_regressor = RandomForestRegressor(
            n_estimators=100, max_depth=None, random_state=42
        )
        rf_regressor.fit(X_train, y_train)
        y_pred = rf_regressor.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print("mse:", mse)
        print("r2", r2)

        with open(
            base_api.relative_to_abs(
                [
                    "source",
                    "machine_learning",
                    "model",
                    "subtopic",
                    "{}.pkl".format(subtopic_code),
                ]
            ),
            "wb",
        ) as file:
            pickle.dump(rf_regressor, file)


if __name__ == "__main__":
    data = get_data()
    model_training(data)

import json
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error ,r2_score
from sklearn.model_selection import train_test_split 
import source.base_api as base_api
from source.machine_learning.subject_area import get_data

# lang_column = "abstracts-retrieval-response.language.@xml:lang"
# def transform(file) :
#     data = json.load(file)
#     df = pd.json_normalize(data)
#     print(df.columns)
#     return df.drop(columns=df.columns.difference([lang_column]))
def model_training(data) :  
    #: only include $ , @abbrev
    X_model1 = data.pop("year")
    y = data.drop(columns=["$" , "@abbrev"])
    
    #: train test split
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X_model1, y, test_size=0.2, random_state=42)
    
    #: model
    rf_regressor = RandomForestRegressor(n_estimators=100, max_depth=None, random_state=42)
    rf_regressor.fit(X_train1, y_train1)
    y_pred = rf_regressor.predict(X_test1)
    
    #:elevate model
    mse = mean_squared_error(y_test1, y_pred)
    r2 = r2_score(y_test1, y_pred)
    
    with open('random_forest_model.pkl', 'wb') as file:
        pickle.dump(rf_regressor, file)

if __name__ == "__main__":
    # df = get_data()
    # print(df)
    data = get_data()
    model_training(data)
import os
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
import mlflow
from mlflow.models.signature import infer_signature
import logging
import mlflow.sklearn
from urllib.parse import urlparse


os.environ["MLFLOW_TRACKING_URI"] = "http://ec2-107-21-195-23.compute-1.amazonaws.com:5000/"

logging.basicConfig(level=logging.WARN)
logger=logging.getLogger(__name__)

def eval_metrics(actual,pred):
    rmse=np.sqrt(mean_squared_error(actual,pred))
    mae=mean_absolute_error(actual,pred)
    r2=r2_score(actual,pred)
    return rmse,mae,r2

if __name__=="__main__":

    ## Data Ingestion
    data =pd.read_csv("diabetes.csv")

    ## split the data into train and test

    train,test=train_test_split(data)

    train_x=train.drop(['Outcome'],axis=1)
    test_x=test.drop(['Outcome'],axis=1)
    train_y=train[['Outcome']]
    test_y=test[['Outcome']]

    ## For elastic net we have to use "alpha", "L1 ratio"
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio=float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    ## Mlflow start

    with mlflow.start_run():
        lr=ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=42)
        lr.fit(train_x,train_y)

        predicted_outcome= lr.predict(test_x)
        (rmse, mae, r2)= eval_metrics(test_y, predicted_outcome)

        print("elastic model (alpha= {:f}, l1_ratio={:f}:".format(alpha, l1_ratio))
        print(" RMSE: %s" % rmse)
        print("l1_ratio: %s" % l1_ratio)
        print("MAE: %s" % mae)
        print("R2: %s" % r2)


        ## Seting Up the remote server AWS

        remote_server_uris="http://ec2-107-21-195-23.compute-1.amazonaws.com:5000/"
        mlflow.set_tracking_uri(remote_server_uris)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme


        if tracking_url_type_store!="file":
            mlflow.sklearn.log_model(
                lr,"model",registered_model_name="ElasticnetdiabetesModel"
            ) 
        else:
            mlflow.sklearn.log_model(lr,"model")
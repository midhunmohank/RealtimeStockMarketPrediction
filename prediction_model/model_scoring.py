import json
import numpy as np
import pandas as pd
import joblib


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory.
    """
    global model
    # Load the serialized model file from the model folder
    model_path = 'model.pkl'
    model = joblib.load(model_path)


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    It expects a JSON input with a "data" field that contains an array of data.
    """
    # Load the input data from JSON format
    input_data = json.loads(raw_data)['data']
    # Convert the input data to a pandas DataFrame
    input_df = pd.DataFrame.from_records(input_data, columns=None)
    # Make the predictions
    predictions = model.predict(input_df)
    # Convert the predictions to a list
    predictions_list = predictions.tolist()
    # Return the predictions as JSON
    return json.dumps(predictions_list)

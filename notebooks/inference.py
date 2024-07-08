import os
import pickle
import pandas as pd
import io

def model_fn(model_dir):
    """Load model from the model_dir directory"""
    model_path = os.path.join(model_dir, 'model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def input_fn(request_body, request_content_type):
    """Deserialize the request body into a pandas DataFrame"""
    if request_content_type == 'text/csv':
        return pd.read_csv(io.StringIO(request_body))
    else:
        raise ValueError("This model only supports CSV input")

def predict_fn(input_data, model):
    """Make predictions using the loaded model"""
    return model.predict(input_data)

def output_fn(prediction, content_type):
    """Serialize the prediction output"""
    if content_type == 'text/csv':
        return ','.join(map(str, prediction))
    else:
        raise ValueError("This model only supports CSV output")

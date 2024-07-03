import nbformat
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor
import boto3
import pandas as pd
from datetime import datetime
import io

# Load the notebook
with open("notebooks/test_notebook.ipynb") as f:
    nb = nbformat.read(f, as_version=4)

# Execute the notebook
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})

# Extract the result from the notebook
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "Inference result" in cell.outputs[0].text:
            result = eval(cell.outputs[0].text.split(': ')[1])

# Convert result to DataFrame
payload = {"data": [[0.00632, 18.00, 2.31, 0.0, 0.538, 6.575, 65.2, 4.0900, 1, 296.0, 15.3, 396.90, 4.98]]}
inference_data = {
    "input": [payload["data"]],
    "prediction": [result]
}
df = pd.DataFrame(inference_data)

# Save DataFrame as CSV
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)

# Upload CSV to S3
s3_client = boto3.client('s3')
bucket_name = 'justin-automation-output'
csv_file_name = f'inferences_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

s3_client.put_object(
    Bucket=bucket_name,
    Key=csv_file_name,
    Body=csv_buffer.getvalue()
)

print(f"Inference results saved to S3 bucket '{bucket_name}' with file name '{csv_file_name}'.")

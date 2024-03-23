from google.cloud import storage
from pathlib import Path

bucket_name = "dados_rox"
local_dir = Path("caminho/da/pasta/local/contendo/os/arquivos/fornecidos/pelo/teste")
client = storage.Client()
bucket = client.bucket(bucket_name)

def upload_csv(filename):
    blob = bucket.blob(filename)
    blob.upload_from_filename(local_dir / filename)

csv_files = list(local_dir.glob("*.csv"))

for filename in csv_files:
    upload_csv(filename.name)

import gsutil
import schedule
import time

def upload_file():
    local_file_path = CAMINHO_LOCAL_DOS_ARQUIVOS"
    bucket_name = "ing_dad_bronze"
    destination_file_path = "CAMINHO_NA_NUVEM_DOS_ARQUIVOS"

    # Fazer upload do arquivo para o Cloud Storage
    gsutil.cp(local_file_path, f"gs://{bucket_name}/{destination_file_path}")

# Agendar a execução da função upload_file() diariamente às 00:00
schedule.every().day.at("00:00").do(upload_file)

# Iniciar o loop de agendamento
while True:
    schedule.run_pending()
    time.sleep(1)

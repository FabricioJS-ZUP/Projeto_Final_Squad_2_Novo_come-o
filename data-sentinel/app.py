import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from src.s3_uploader import S3Uploader
from src.csv_processor import CSVProcessor
from src.sensitive_data_identifier import SensitiveDataIdentifier
from src.stackspot_quick_command_client import StackSpotQuickCommandClient
from src.dynamodb_repository import DynamoDBRepository
from src.email_notifier import EmailNotifier
from src.process_result import ProcessResult
from pydantic import EmailStr

app = FastAPI()

s3_uploader = S3Uploader(bucket_name="bucket-auditoria-do-projeto")
stackspot_client = StackSpotQuickCommandClient(api_url="SUA_URL", token="SEU_TOKEN")
sensitive_data_identifier = SensitiveDataIdentifier(stackspot_client)
csv_processor = CSVProcessor(sensitive_data_identifier)
dynamo_repo = DynamoDBRepository(table_name="sua-tabela")
email_notifier = EmailNotifier(sender_email="seu@email.com")

logging.basicConfig(level=logging.INFO)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), user_email: EmailStr = "usuario@email.com"):
    try:
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        logging.info("Arquivo salvo localmente em %s", file_location)
        
        s3_uploader.upload_file(file_location, file.filename, user_email)
        logging.info("Arquivo enviado para o S3 com sucesso.")
        
        result_data = csv_processor.process("bucket-auditoria-do-projeto", file.filename)
        logging.info("Processamento do CSV concluído.")
        
        process_result = ProcessResult(file.filename, result_data, status="processed")
        dynamo_repo.save_result(process_result.to_dict())
        logging.info("Resultado salvo no DynamoDB.")
        
        email_notifier.send_email(user_email, "Processamento concluído", f"Resultado: {result_data}")
        logging.info("E-mail de notificação enviado com sucesso.")
        
        return {"message": "Arquivo enviado e processado com sucesso", "result": result_data}
    except Exception as e:
        logging.error("Erro durante o processamento: %s", str(e))
        raise HTTPException(status_code=500, detail="Erro no processamento do arquivo.")
import azure.functions as func
import logging
import aspose.words as aw
from azure.storage.blob import BlobServiceClient

# Initialize the Function App
app = func.FunctionApp()

# Connection string for Azure Storage Account
STORAGE_CONNECTION_STRING = "your_storage_account_connection_string"

@app.blob_trigger(arg_name="myblob", path="input-dotx/{name}", connection="AzureWebJobsStorage")
def convert_dotx_to_pdf(myblob: func.InputStream, name: str):
    logging.info(f"Processing blob: Name: {myblob.name}, Size: {myblob.length} bytes")

    # Step 1: Save the incoming .dotx file to a temporary location
    temp_dotx_path = f"/tmp/{name}"
    with open(temp_dotx_path, "wb") as temp_file:
        temp_file.write(myblob.read())

    # Step 2: Convert .dotx to .pdf using Aspose
    output_pdf_path = f"/tmp/{name.replace('.dotx', '.pdf')}"
    try:
        doc = aw.Document(temp_dotx_path)
        doc.save(output_pdf_path)
        logging.info(f"Converted file saved locally at {output_pdf_path}")
    except Exception as e:
        logging.error(f"Error converting .dotx to .pdf: {e}")
        raise

    # Step 3: Upload the .pdf file to the 'output-dotx' container
    try:
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        output_container_name = "output-dotx"
        blob_client = blob_service_client.get_blob_client(container=output_container_name, blob=name.replace(".dotx", ".pdf"))

        with open(output_pdf_path, "rb") as pdf_file:
            blob_client.upload_blob(pdf_file, overwrite=True)
        logging.info(f"Uploaded PDF to container '{output_container_name}' with name '{name.replace('.dotx', '.pdf')}'")
    except Exception as e:
        logging.error(f"Error uploading .pdf to output container: {e}")
        raise

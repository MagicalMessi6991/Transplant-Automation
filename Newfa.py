import azure.functions as func
import logging
import aspose.words as aw
from azure.storage.blob import BlobServiceClient

def main(myblob: func.InputStream, outputBlob: func.Out[bytes]):
    logging.info(f"Processing blob: Name: {myblob.name}, Size: {myblob.length} bytes")

    # Save input blob (.dotx) to a temporary file
    temp_dotx_path = "/tmp/temp.dotx"
    with open(temp_dotx_path, "wb") as temp_file:
        temp_file.write(myblob.read())

    # Convert .dotx to .pdf
    temp_pdf_path = "/tmp/converted.pdf"
    try:
        doc = aw.Document(temp_dotx_path)
        doc.save(temp_pdf_path)
        logging.info("File successfully converted to PDF.")
    except Exception as e:
        logging.error(f"Error converting .dotx to .pdf: {e}")
        raise

    # Write the converted .pdf back to the output blob
    with open(temp_pdf_path, "rb") as pdf_file:
        outputBlob.set(pdf_file.read())

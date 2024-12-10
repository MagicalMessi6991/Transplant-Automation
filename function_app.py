import azure.functions as func
import logging
from docx import Document
import os
from io import BytesIO

# Function App instance
app = func.FunctionApp()

# Blob trigger function
@app.function_name(name="ConvertDotxToPdf")
@app.blob_trigger(arg_name="myblob", path="input-dotx/{name}", connection="AzureWebJobsStorage")
def convert_dotx_to_pdf(myblob: func.InputStream):
    logging.info(f"Processing blob trigger function: Name: {myblob.name}, Size: {myblob.length} bytes")

    # Read the content of the .dotx file (blob)
    file_content = myblob.read()

    # Temporary file to store the .dotx content
    temp_filename = "/tmp/temp.dotx"

    # Write the content to a temporary file
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(file_content)

    # Load the .dotx file using python-docx (works with .docx as well)
    try:
        doc = Document(temp_filename)

        # Perform logic to convert .dotx to PDF
        # Here, we need to convert the .docx to PDF (you may use an external tool like LibreOffice)
        logging.info(f"Loaded .dotx file: {doc.core_properties.title}")

        # Placeholder logic for PDF conversion (replace with actual PDF conversion)
        output_pdf_path = "/tmp/converted_output.pdf"

        # For demonstration purposes, we are just logging the content here
        logging.info(f"Saving PDF to {output_pdf_path}")

        # Example of writing to a PDF file (replace with actual conversion logic)
        with open(output_pdf_path, "wb") as pdf_file:
            pdf_file.write(file_content)  # Just an example, use actual conversion logic here

        logging.info(f"Conversion complete. PDF saved to {output_pdf_path}")

    except Exception as e:
        logging.error(f"Error processing .dotx file: {e}")
        raise

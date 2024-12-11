import azure.functions as func
import logging
import aspose.words as aw

# Initialize the Function App
app = func.FunctionApp()

@app.function_name(name="ConvertDotxToPdf")
@app.blob_trigger(arg_name="myblob", path="input-dotx/{name}", connection="AzureWebJobsStorage")
def convert_dotx_to_pdf(myblob: func.InputStream):
    logging.info(f"Processing blob: Name: {myblob.name}, Size: {myblob.length} bytes")

    # Save the blob content to a temporary file
    temp_dotx_path = "/tmp/temp.dotx"
    with open(temp_dotx_path, "wb") as temp_file:
        temp_file.write(myblob.read())

    # Convert .dotx to .pdf using Aspose
    output_pdf_path = "/tmp/converted.pdf"
    try:
        doc = aw.Document(temp_dotx_path)
        doc.save(output_pdf_path)
        logging.info(f"Converted file saved at {output_pdf_path}")
    except Exception as e:
        logging.error(f"Error converting .dotx to .pdf: {e}")
        raise

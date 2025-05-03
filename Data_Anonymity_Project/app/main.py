from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from anonymizer import anonymize_csv, anonymize_text
import pandas as pd
import io
import mimetypes
import logging
import fitz  
from docx import Document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

@app.post("/anonymize")
async def anonymize_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        mime_type, _ = mimetypes.guess_type(file.filename)

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
            anon_df = anonymize_csv(df)
            output = io.StringIO()
            anon_df.to_csv(output, index=False)
            return JSONResponse(content={"anonymized_csv": output.getvalue()})

        elif file.filename.endswith('.pdf'):
            pdf_document = fitz.open(stream=contents, filetype="pdf")
            text = ""
            for page in pdf_document:
                text += page.get_text()
            anonymized_text = anonymize_text(text)
            return JSONResponse(content={"anonymized_text": anonymized_text})

        elif file.filename.endswith('.docx'):
            doc = Document(io.BytesIO(contents))
            text = "\n".join([para.text for para in doc.paragraphs])
            anonymized_text = anonymize_text(text)
            return JSONResponse(content={"anonymized_text": anonymized_text})

        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported file format"})

    except Exception as e:
        logging.error(f"Error occurred while anonymizing the file: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

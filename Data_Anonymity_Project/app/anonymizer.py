import re
from faker import Faker
import pandas as pd
from fastapi import HTTPException

fake = Faker()

EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+'
PHONE_PATTERN = r'\b\+?\d{1,3}[\s.-]?\d{3}[\s.-]?\d{3,4}\b'
IP_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'

def anonymize_text(text: str):
    try:
        text = re.sub(EMAIL_PATTERN, lambda _: fake.email(), text)
        text = re.sub(PHONE_PATTERN, lambda _: fake.phone_number(), text)
        text = re.sub(IP_PATTERN, lambda _: fake.ipv4(), text)
        text = re.sub(SSN_PATTERN, lambda _: fake.ssn(), text)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error anonymizing text: {str(e)}")

def anonymize_csv(df: pd.DataFrame) -> pd.DataFrame:
    try:
        for column in df.columns:
            df[column] = df[column].astype(str).apply(anonymize_text)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

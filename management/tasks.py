from pathlib import Path
import pandas as pd

from django.db.transaction import atomic

from celery import shared_task


@shared_task(bind=True)
def process_excel(file_path:Path):
    df = pd.read_excel(file_path,usecols="B:E",skiprows=2,engine="openpyxl")
    
    for _,row in df.iterrows():
        with atomic():
            print("lkasjdlksajdklsajd")
        
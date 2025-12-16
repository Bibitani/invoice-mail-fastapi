import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

VENDOR_FILE = os.path.join(DATA_DIR, "FINAL_VENDOR_MASTER_FILLED.xlsx")
INVOICE_FILE = os.path.join(DATA_DIR, "INVOICE_VALIDATED_OUTPUT.xlsx")

def load_data():
    vendor_df = pd.read_excel(VENDOR_FILE)
    invoice_df = pd.read_excel(INVOICE_FILE)
    return vendor_df, invoice_df

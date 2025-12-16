import pandas as pd

# -------------------------------------------------------
# PATHS (keep same for now)
# -------------------------------------------------------
BASE_PATH = r"C:\Users\bibiy\Desktop\L n T\mock_mail"

VENDOR_FILE = rf"{BASE_PATH}\FINAL_VENDOR_MASTER_FILLED.xlsx"
INVOICE_FILE = rf"{BASE_PATH}\INVOICE_VALIDATED_OUTPUT.xlsx"


def load_data():
    """
    Loads vendor and invoice Excel files.
    Returns:
        vendor_df (DataFrame)
        invoice_df (DataFrame)
    """
    vendor_df = pd.read_excel(VENDOR_FILE)
    invoice_df = pd.read_excel(INVOICE_FILE)
    return vendor_df, invoice_df

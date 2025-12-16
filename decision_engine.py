def build_email_content(invoice_row):
    """
    Builds email subject and body based on invoice status.
    """
    if invoice_row["Status"] == "PASS":
        subject = f"Invoice Verification SUCCESS – {invoice_row['Invoice_No']}"
        body = f"""
Dear Vendor,

Your invoice {invoice_row['Invoice_No']} has been successfully verified.

Amount: ₹{invoice_row['Invoice_Amount']}
Bank: {invoice_row['Bank_Name']}
Date: {invoice_row['Invoice_Date']}

Regards,
Automated Verification System
"""
    else:
        subject = f"Invoice Verification FAILED – {invoice_row['Invoice_No']}"
        body = f"""
Dear Treasury,

Invoice {invoice_row['Invoice_No']} has FAILED verification.

Reason:
{invoice_row['Reason_For_Failure (Gemini Generated)']}

Mismatch Summary:
{invoice_row['Mismatch_Summary (Gemini Generated)']}

Regards,
Automated Verification System
"""

    return subject, body


def decide_recipients(invoice_row, vendor_row):
    """
    Decides TO and CC lists based on PASS / FAIL.
    """
    if invoice_row["Status"] == "PASS":
        to_list = [vendor_row["Vendor_Email"]]
        cc_list = [
            vendor_row["Vendor_Manager_Email"],
            vendor_row["Treasury_Email"]
        ]
    else:
        to_list = [vendor_row["Treasury_Email"]]
        cc_list = [
            vendor_row["Vendor_Manager_Email"],
            vendor_row["Vendor_Email"]
        ]

    return to_list, cc_list

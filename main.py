from fastapi import FastAPI, HTTPException
import traceback

from excel_loader import load_data
from decision_engine import build_email_content, decide_recipients
from email_sender import send_email

app = FastAPI()

@app.post("/process-invoices")
def process_invoices():
    try:
        print("🚀 /process-invoices endpoint HIT")

        vendor_df, invoice_df = load_data()
        print("✅ Excel files loaded")

        results = []

        for _, invoice in invoice_df.iterrows():
            print(f"🔍 Processing invoice {invoice['Invoice_No']}")

            vendor = vendor_df[
                vendor_df["Vendor_ID"] == invoice["Vendor_ID"]
            ].iloc[0]

            subject, body = build_email_content(invoice)
            to_list, cc_list = decide_recipients(invoice, vendor)

            send_email(subject, body, to_list, cc_list)

            results.append({
                "invoice_no": invoice["Invoice_No"],
                "status": invoice["Status"],
                "email_sent_to": to_list
            })

        return {
            "message": "Invoices processed and emails sent",
            "results": results
        }

    except Exception as e:
        print("❌ ERROR OCCURRED")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

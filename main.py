from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback
from excel_loader import load_data
from decision_engine import build_email_content, decide_recipients
from email_sender import send_email

# OpenAPI metadata
app = FastAPI(
    title="Invoice Email Automation API",
    description="""
    Automated invoice verification and email notification system.
    
    This API processes vendor invoices, verifies their status (PASS/FAIL), 
    and automatically sends email notifications to relevant stakeholders.
    
    ## Features
    - Processes invoices from Excel files
    - Sends success emails to vendors
    - Sends failure alerts to treasury
    - Includes CC notifications to managers
    """,
    version="1.0.0",
    contact={
        "name": "Invoice System Support",
        "email": "support@yourcompany.com"
    },
    servers=[
        {
            "url": "https://invoice-mail-fastapi.onrender.com",
            "description": "Production server"
        }
    ]
)

# Add CORS middleware for Azure AI Foundry
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for anonymous connection
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Response models
class EmailResult(BaseModel):
    invoice_no: str
    status: str
    email_sent_to: list[str]
    success: bool = True
    error: str = None

class ProcessInvoicesResponse(BaseModel):
    message: str
    results: list[EmailResult]
    total_processed: int
    successful: int
    failed: int

class HealthResponse(BaseModel):
    status: str
    message: str
    endpoints: dict

class TestEmailRequest(BaseModel):
    email: str

class TestEmailResponse(BaseModel):
    status: str
    message: str

# Endpoints
@app.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and view available endpoints",
    tags=["Health"]
)
def root():
    """Health check endpoint that returns API status and available endpoints"""
    return {
        "status": "ok",
        "message": "Invoice Email System is running",
        "endpoints": {
            "process_invoices": "/process-invoices (POST)",
            "test_email": "/test-email (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Status",
    description="Alternative health check endpoint",
    tags=["Health"]
)
def health():
    """Alternative health check endpoint"""
    return {
        "status": "healthy",
        "message": "All systems operational",
        "endpoints": {}
    }

@app.post(
    "/process-invoices",
    response_model=ProcessInvoicesResponse,
    summary="Process All Invoices",
    description="""
    Processes all invoices from the Excel files and sends appropriate emails.
    
    **For PASS invoices:**
    - TO: Vendor email
    - CC: Vendor manager, Treasury
    
    **For FAIL invoices:**
    - TO: Treasury email
    - CC: Vendor manager, Vendor email
    
    Returns a list of all processed invoices with their email delivery status.
    """,
    tags=["Invoice Processing"],
    responses={
        200: {
            "description": "Invoices processed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invoices processed and emails sent",
                        "results": [
                            {
                                "invoice_no": "INV-001",
                                "status": "PASS",
                                "email_sent_to": ["vendor@example.com"],
                                "success": True
                            }
                        ],
                        "total_processed": 10,
                        "successful": 9,
                        "failed": 1
                    }
                }
            }
        },
        500: {
            "description": "Internal server error during processing"
        }
    }
)
def process_invoices():
    """
    Process all invoices and send emails based on their verification status.
    
    This endpoint:
    1. Loads vendor and invoice data from Excel files
    2. Matches invoices with vendor information
    3. Builds appropriate email content based on PASS/FAIL status
    4. Sends emails to correct recipients with proper CC lists
    5. Returns detailed results for each invoice
    """
    try:
        print("🚀 /process-invoices endpoint HIT")
        vendor_df, invoice_df = load_data()
        print("✅ Excel files loaded")
        
        results = []
        successful = 0
        failed = 0
        
        for _, invoice in invoice_df.iterrows():
            try:
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
                    "email_sent_to": to_list,
                    "success": True
                })
                successful += 1
                
            except Exception as e:
                print(f"❌ Error processing invoice {invoice['Invoice_No']}: {str(e)}")
                results.append({
                    "invoice_no": invoice["Invoice_No"],
                    "status": invoice.get("Status", "UNKNOWN"),
                    "email_sent_to": [],
                    "success": False,
                    "error": str(e)
                })
                failed += 1
        
        return {
            "message": "Invoices processed and emails sent",
            "results": results,
            "total_processed": len(results),
            "successful": successful,
            "failed": failed
        }
        
    except Exception as e:
        print("❌ ERROR OCCURRED")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/test-email",
    response_model=TestEmailResponse,
    summary="Send Test Email",
    description="""
    Sends a test email to verify SendGrid configuration.
    
    Use this endpoint to test if your email system is working correctly
    before processing actual invoices.
    """,
    tags=["Testing"],
    responses={
        200: {
            "description": "Test email sent successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Test email sent to test@example.com"
                    }
                }
            }
        },
        500: {
            "description": "Failed to send test email"
        }
    }
)
def test_email(request: TestEmailRequest):
    """
    Send a test email to verify email functionality.
    
    Args:
        request: JSON body containing the recipient email address
        
    Returns:
        Success/failure status of the test email
    """
    try:
        from email_sender import send_email
        
        send_email(
            subject="Test Email - Invoice Verification System",
            body="This is a test email from your invoice verification system. If you receive this, everything is working correctly!",
            to_list=[request.email],
            cc_list=[]
        )
        
        return {
            "status": "success",
            "message": f"Test email sent to {request.email}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send test email: {str(e)}"
        )

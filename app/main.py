from fastapi import FastAPI, HTTPException, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime
import uuid
from fastapi.responses import JSONResponse
import os
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk

from .models import Lead, LeadData, LeadResponse
from .services.lead_classifier import classify_lead
from .services.crm_integration import update_crm
from .services.ml_predictor import LeadPredictor
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Lead Qualification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "https://your-other-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == os.getenv("WEBHOOK_API_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid API Key"
    )

def process_lead_async(lead: Lead):
    # Move the CRM update to background task
    try:
        await update_crm(lead)
    except Exception as e:
        # Log the error but don't raise it
        print(f"Error updating CRM: {str(e)}")

@app.post("/webhook/leads", response_model=LeadResponse)
async def receive_lead(
    lead_data: LeadData,
    background_tasks: BackgroundTasks,
    api_key: str = Security(get_api_key)
):
    try:
        # Create lead object with engagement metrics
        lead = Lead(
            id=str(uuid.uuid4()),
            email=lead_data.email,
            name=lead_data.name,
            company=lead_data.company,
            source=lead_data.source or "webhook",
            engagement_metrics={
                "website_visits": lead_data.visits or 0,
                "time_on_site": lead_data.time_on_site or 0,
                "pages_viewed": lead_data.pages_viewed or 0,
                "downloaded_resources": lead_data.downloads or 0,
                "email_interactions": lead_data.email_interactions or 0,
            },
            created_at=datetime.utcnow(),
            status="Cold",
            score=0
        )

        # Classify the lead
        classification = await classify_lead(lead)
        lead.status = classification.status
        lead.score = classification.score

        # Move CRM update to background task
        background_tasks.add_task(process_lead_async, lead)

        return LeadResponse(
            success=True,
            lead={
                "id": lead.id,
                "status": lead.status,
                "score": lead.score
            }
        )
    except Exception as e:
        # Return 500 to trigger Zapier retry
        raise HTTPException(status_code=500, detail=str(e))

# Add this new endpoint for testing
@app.get("/webhook/test")
async def test_webhook():
    return JSONResponse({
        "status": "active",
        "message": "Webhook endpoint is ready to receive leads"
    })

class TrainingData(BaseModel):
    leads: List[dict]
    converted: List[int]  # 1 for converted, 0 for not converted

predictor = LeadPredictor()

@app.post("/train-model")
async def train_model(
    data: TrainingData,
    api_key: str = Security(get_api_key)
):
    try:
        await predictor.train(data.leads, data.converted)
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to train model: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "crm_type": os.getenv("CRM_TYPE"),
        "ml_model_loaded": predictor.model is not None
    }

if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=os.getenv("ENVIRONMENT", "production"),
        traces_sample_rate=1.0
    )
    app.add_middleware(SentryAsgiMiddleware) 
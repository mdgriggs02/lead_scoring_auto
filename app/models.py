from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Literal
from datetime import datetime

class EngagementMetrics(BaseModel):
    website_visits: int
    time_on_site: int
    pages_viewed: int
    downloaded_resources: int
    email_interactions: int

class Lead(BaseModel):
    id: str
    email: EmailStr
    name: str
    company: Optional[str] = None
    source: str
    engagement_metrics: EngagementMetrics
    created_at: datetime
    status: Literal["Hot", "Warm", "Cold"]
    score: int

class LeadData(BaseModel):
    email: EmailStr
    name: str
    company: Optional[str] = None
    source: Optional[str] = None
    visits: Optional[int] = 0
    time_on_site: Optional[int] = 0
    pages_viewed: Optional[int] = 0
    downloads: Optional[int] = 0
    email_interactions: Optional[int] = 0

class LeadClassificationResult(BaseModel):
    status: Literal["Hot", "Warm", "Cold"]
    score: int
    confidence: float

class LeadResponse(BaseModel):
    success: bool
    lead: Dict 
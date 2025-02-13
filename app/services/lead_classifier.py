from ..models import Lead, LeadClassificationResult, EngagementMetrics
from .ml_predictor import LeadPredictor

# Initialize the predictor
lead_predictor = LeadPredictor()

async def classify_lead(lead: Lead) -> LeadClassificationResult:
    # Get conversion probability from ML model
    conversion_prob = await lead_predictor.predict_conversion(
        lead.engagement_metrics.dict()
    )
    
    # Calculate score (0-100)
    score = round(conversion_prob * 100)
    
    # Determine lead status based on score
    if score >= 80:
        status = "Hot"
    elif score >= 50:
        status = "Warm"
    else:
        status = "Cold"

    return LeadClassificationResult(
        status=status,
        score=score,
        confidence=calculate_confidence(score)
    )

def calculate_engagement_score(metrics: EngagementMetrics) -> int:
    weights = {
        "website_visits": 10,
        "time_on_site": 15,
        "pages_viewed": 20,
        "downloaded_resources": 30,
        "email_interactions": 25
    }

    normalized_score = (
        metrics.website_visits * weights["website_visits"] +
        min(metrics.time_on_site / 300, 1) * weights["time_on_site"] +
        metrics.pages_viewed * weights["pages_viewed"] +
        metrics.downloaded_resources * weights["downloaded_resources"] +
        metrics.email_interactions * weights["email_interactions"]
    )

    return min(round(normalized_score), 100)

def calculate_confidence(score: int) -> float:
    threshold = 80 if score >= 80 else 50 if score >= 50 else 0
    distance = abs(score - threshold)
    return max(0.6, min(0.95, 0.6 + (distance / 100))) 
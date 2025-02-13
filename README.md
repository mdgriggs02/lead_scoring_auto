 AI-Powered Lead Qualification System

An intelligent lead qualification system that automatically scores and classifies incoming leads using machine learning, integrates with popular CRMs, and provides real-time lead insights.

## Features:

- **Automated Lead Scoring**: ML-powered scoring system using engagement metrics
- **Intelligent Classification**: Automatically categorizes leads as Hot/Warm/Cold
- **CRM Integration**: Seamless integration with HubSpot and Salesforce
- **Zapier Integration**: Easy connection to 1000+ apps via webhooks
- **ML Model Training**: Self-improving system that learns from historical data
- **Real-time Processing**: Instant lead qualification and CRM updates
- **Performance Monitoring**: Built-in analytics and visualization
- **Secure API**: API key authentication and error handling
- **Multiple Deployment Options**: AWS Lambda, Vercel, or DigitalOcean

## Quick Start:

1. **Clone and Install**
   
Do these steps:

git clone https://github.com/yourusername/lead-qualification-system
cd lead-qualification-system
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

2. **Configure Environment**
Create a `.env` file:
CRM Configuration
CRM_TYPE=hubspot # or salesforce
API Security
WEBHOOK_API_KEY=your_secure_webhook_key
HubSpot Configuration
HUBSPOT_API_KEY=your_hubspot_api_key
Salesforce Configuration
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_TOKEN=your_salesforce_token
Optional Monitoring
SENTRY_DSN=your_sentry_dsn
ENVIRONMENT=production
LOG_LEVEL=INFO

##  System Architecture

### 1. Lead Processing Pipeline
Lead Data → Webhook → ML Scoring → Classification → CRM Update

### 2. Key Components

- **Webhook Endpoint** (`app/main.py`):
  - Receives lead data
  - Validates input
  - Triggers processing pipeline

- **ML Predictor** (`app/services/ml_predictor.py`):
  - Scores leads based on engagement metrics
  - Uses RandomForest classifier
  - Provides confidence scores
  - Auto-retraining capability

- **CRM Integration** (`app/services/crm/`):
  - Adapter pattern for multiple CRMs
  - Automatic lead creation/update
  - Task creation for hot leads
  - Error handling and retry logic

## Lead Scoring Metrics

The system uses these engagement metrics:
- Website visits
- Time on site
- Pages viewed
- Resources downloaded
- Email interactions

Scoring weights:
weights = {
"website_visits": 10,
"time_on_site": 15,
"pages_viewed": 20,
"downloaded_resources": 30,
"email_interactions": 25
}

## CRM Setup

### HubSpot Setup
1. Create API key in HubSpot Settings → Integrations
2. Add custom properties:
   - lead_score (number)
   - lead_status (single-line text)
   - website_visits (number)
   - time_on_site (number)
   - pages_viewed (number)
   - downloaded_resources (number)
   - email_interactions (number)

### Salesforce Setup
1. Create Connected App
2. Add custom fields to Lead object:
   - Lead_Score__c (Number)
   - Website_Visits__c (Number)
   - Time_On_Site__c (Number)
   - Pages_Viewed__c (Number)
   - Downloaded_Resources__c (Number)
   - Email_Interactions__c (Number)

## Zapier Integration

1. Create new Zap
2. Configure webhook action:
URL: https://your-api-domain.com/webhook/leads
Method: POST
Headers:
Content-Type: application/json
X-API-Key: your_webhook_api_key
3. Data mapping:
   {
"email": "{{lead_email}}",
"name": "{{lead_name}}",
"company": "{{lead_company}}",
"source": "zapier",
"visits": "{{website_visits}}",
"time_on_site": "{{time_spent}}",
"pages_viewed": "{{pages_viewed}}",
"downloads": "{{resource_downloads}}",
"email_interactions": "{{email_opens}}"
}

## Deployment Options

### Vercel Deployment
./deploy.sh vercel
### AWS Lambda Deployment
./deploy.sh aws
### DigitalOcean Deployment
./deploy.sh digitalocean

## Monitoring

Run the performance analysis:
python scripts/monitor_performance.py

This generates:
- Conversion rate visualization
- Performance metrics
- Lead status distribution

## Testing

Run the test suite:
python tests/test_api.py

## API Documentation

### Endpoints

1. **Receive Lead**
   POST /webhook/leads
2. **Train Model**
   POST /train-model
3. **Health Check**
   GET /health
# Security

- API key authentication
- Environment variable protection
- CRM credential security
- Input validation
- Error handling

##  Customization

### Adding New CRM
1. Create new adapter in `app/services/crm/`
2. Implement CRMAdapter interface
3. Add to CRMIntegration factory

### Modifying Scoring
1. Update weights in `app/services/ml_predictor.py`
2. Retrain model with new parameters

## Performance Metrics

The system tracks:
- Lead conversion rates by status
- ML model accuracy
- CRM sync success rate
- API response times

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request


## Support

For questions or support:
1. Open an issue
2. Check documentation
3. Review existing issues

## Future Enhancements

- Additional CRM integrations
- Advanced ML models
- Real-time dashboard
- A/B testing capability
- Multi-tenant support

---

Built with FastAPI, scikit-learn, and Python
This project is currently unlicensed. If you wish to use it, please contact me.

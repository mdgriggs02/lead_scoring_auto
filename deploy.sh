#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Function to display usage
usage() {
    echo "Usage: $0 [vercel|aws|digitalocean]"
    exit 1
}

# Check if platform argument is provided
if [ $# -eq 0 ]; then
    usage
fi

PLATFORM=$1

case $PLATFORM in
    vercel)
        echo "Deploying to Vercel..."
        # Set up Vercel secrets
        vercel secrets add webhook_api_key "$WEBHOOK_API_KEY"
        vercel secrets add hubspot_api_key "$HUBSPOT_API_KEY"
        vercel secrets add salesforce_username "$SALESFORCE_USERNAME"
        vercel secrets add salesforce_password "$SALESFORCE_PASSWORD"
        vercel secrets add salesforce_token "$SALESFORCE_TOKEN"
        
        # Deploy
        vercel --prod
        ;;
        
    aws)
        echo "Deploying to AWS Lambda..."
        # Install serverless plugins
        serverless plugin install -n serverless-python-requirements
        
        # Deploy
        serverless deploy --stage prod
        ;;
        
    digitalocean)
        echo "Deploying to DigitalOcean..."
        # Create app
        doctl apps create --spec app.yaml
        
        # Get app ID
        APP_ID=$(doctl apps list --format ID --no-header)
        
        # Deploy updates
        doctl apps update $APP_ID --spec app.yaml
        ;;
        
    *)
        usage
        ;;
esac 
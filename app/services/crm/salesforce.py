from simple_salesforce import Salesforce
from typing import Dict, Any
import os
from .base import CRMAdapter
from ...models import Lead

class SalesforceAdapter(CRMAdapter):
    def __init__(self):
        self.sf = Salesforce(
            username=os.getenv("SALESFORCE_USERNAME"),
            password=os.getenv("SALESFORCE_PASSWORD"),
            security_token=os.getenv("SALESFORCE_TOKEN"),
            domain='login'  # or 'test' for sandbox
        )

    async def update_lead(self, lead: Lead) -> bool:
        try:
            # Prepare lead data
            lead_data = {
                'Email': lead.email,
                'FirstName': lead.name.split()[0],
                'LastName': lead.name.split()[-1] if len(lead.name.split()) > 1 else "",
                'Company': lead.company,
                'LeadSource': lead.source,
                'Rating': lead.status,  # Hot/Warm/Cold maps to Salesforce Rating
                'Lead_Score__c': lead.score,
                'Website_Visits__c': lead.engagement_metrics["website_visits"],
                'Time_On_Site__c': lead.engagement_metrics["time_on_site"],
                'Pages_Viewed__c': lead.engagement_metrics["pages_viewed"],
                'Downloaded_Resources__c': lead.engagement_metrics["downloaded_resources"],
                'Email_Interactions__c': lead.engagement_metrics["email_interactions"]
            }

            # Check if lead exists
            existing_lead = self.sf.query(
                f"SELECT Id FROM Lead WHERE Email = '{lead.email}'"
            )

            if existing_lead['totalSize'] > 0:
                # Update existing lead
                lead_id = existing_lead['records'][0]['Id']
                self.sf.Lead.update(lead_id, lead_data)
            else:
                # Create new lead
                self.sf.Lead.create(lead_data)

            # Create task for hot leads
            if lead.status == "Hot":
                await self.create_task(lead)

            return True

        except Exception as e:
            print(f"Salesforce Error: {str(e)}")
            return False

    async def get_lead(self, email: str) -> Dict[str, Any]:
        try:
            result = self.sf.query(
                f"SELECT Id, FirstName, LastName, Company, Rating, Lead_Score__c "
                f"FROM Lead WHERE Email = '{email}'"
            )
            return result['records'][0] if result['totalSize'] > 0 else {}
        except Exception:
            return {}

    async def create_task(self, lead: Lead) -> bool:
        try:
            # Find the lead ID
            lead_query = self.sf.query(
                f"SELECT Id FROM Lead WHERE Email = '{lead.email}'"
            )
            if lead_query['totalSize'] == 0:
                return False

            lead_id = lead_query['records'][0]['Id']

            # Create task
            self.sf.Task.create({
                'Subject': f'Follow up with {lead.name} (Hot Lead)',
                'Priority': 'High',
                'Status': 'Not Started',
                'WhoId': lead_id,
                'Type': 'Call'
            })
            return True
        except Exception as e:
            print(f"Error creating Salesforce task: {str(e)}")
            return False 
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
from typing import Dict, Any
import os
from .base import CRMAdapter
from ...models import Lead

class HubSpotAdapter(CRMAdapter):
    def __init__(self):
        self.client = hubspot.Client.create(
            access_token=os.getenv("HUBSPOT_API_KEY")
        )

    async def update_lead(self, lead: Lead) -> bool:
        try:
            # Prepare lead properties
            properties = {
                "email": lead.email,
                "firstname": lead.name.split()[0],
                "lastname": lead.name.split()[-1] if len(lead.name.split()) > 1 else "",
                "company": lead.company,
                "lead_source": lead.source,
                "lead_score": str(lead.score),
                "lead_status": lead.status.lower(),
                "website_visits": str(lead.engagement_metrics["website_visits"]),
                "time_on_site": str(lead.engagement_metrics["time_on_site"]),
                "pages_viewed": str(lead.engagement_metrics["pages_viewed"]),
                "downloaded_resources": str(lead.engagement_metrics["downloaded_resources"]),
                "email_interactions": str(lead.engagement_metrics["email_interactions"])
            }

            # Check if contact exists
            try:
                contact = self.client.crm.contacts.basic_api.get_by_id(
                    contact_id=lead.email
                )
                # Update existing contact
                self.client.crm.contacts.basic_api.update(
                    contact_id=contact.id,
                    simple_public_object_input=SimplePublicObjectInput(
                        properties=properties
                    )
                )
            except ApiException:
                # Create new contact
                self.client.crm.contacts.basic_api.create(
                    simple_public_object_input=SimplePublicObjectInput(
                        properties=properties
                    )
                )

            # Create task for hot leads
            if lead.status == "Hot":
                await self.create_task(lead)

            return True

        except Exception as e:
            print(f"HubSpot Error: {str(e)}")
            return False

    async def get_lead(self, email: str) -> Dict[str, Any]:
        try:
            contact = self.client.crm.contacts.basic_api.get_by_id(
                contact_id=email
            )
            return contact.properties
        except ApiException:
            return {}

    async def create_task(self, lead: Lead) -> bool:
        try:
            task_properties = {
                "hs_task_subject": f"Follow up with {lead.name} (Hot Lead)",
                "hs_task_priority": "HIGH",
                "hs_task_status": "NOT_STARTED",
                "hs_task_type": "SALES_OUTREACH",
                "hs_timestamp": str(int(lead.created_at.timestamp() * 1000))
            }

            self.client.crm.tasks.basic_api.create(
                simple_public_object_input=SimplePublicObjectInput(
                    properties=task_properties
                )
            )
            return True
        except Exception as e:
            print(f"Error creating HubSpot task: {str(e)}")
            return False 
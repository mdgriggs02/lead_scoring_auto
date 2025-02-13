import os
from typing import Optional
from .crm.base import CRMAdapter
from .crm.hubspot import HubSpotAdapter
from .crm.salesforce import SalesforceAdapter
from ..models import Lead

class CRMIntegration:
    def __init__(self):
        self.crm_adapter: Optional[CRMAdapter] = None
        self._initialize_adapter()

    def _initialize_adapter(self):
        crm_type = os.getenv("CRM_TYPE", "").lower()
        if crm_type == "hubspot":
            self.crm_adapter = HubSpotAdapter()
        elif crm_type == "salesforce":
            self.crm_adapter = SalesforceAdapter()
        else:
            raise ValueError(f"Unsupported CRM type: {crm_type}")

    async def update_crm(self, lead: Lead) -> bool:
        """Update lead information in the CRM"""
        if not self.crm_adapter:
            raise ValueError("CRM adapter not initialized")
        
        try:
            # Update lead in CRM
            success = await self.crm_adapter.update_lead(lead)
            
            if not success:
                print(f"Failed to update lead {lead.email} in CRM")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error updating CRM: {str(e)}")
            return False

# Create singleton instance
crm_integration = CRMIntegration()

async def update_crm(lead: Lead) -> bool:
    """Convenience function to update CRM"""
    return await crm_integration.update_crm(lead) 
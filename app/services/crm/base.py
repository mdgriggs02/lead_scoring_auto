from abc import ABC, abstractmethod
from typing import Dict, Any
from ...models import Lead

class CRMAdapter(ABC):
    """Base CRM adapter class that defines the interface for CRM integrations"""
    
    @abstractmethod
    async def update_lead(self, lead: Lead) -> bool:
        """Update or create a lead in the CRM"""
        pass

    @abstractmethod
    async def get_lead(self, email: str) -> Dict[str, Any]:
        """Retrieve lead information from CRM"""
        pass

    @abstractmethod
    async def create_task(self, lead: Lead) -> bool:
        """Create a follow-up task in CRM"""
        pass 
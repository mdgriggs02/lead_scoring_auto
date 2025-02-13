import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from app.services.crm.base import CRMAdapter
from app.services.crm_integration import crm_integration

async def analyze_performance(days=30):
    """Analyze lead qualification performance"""
    
    # Get CRM data
    crm = crm_integration.crm_adapter
    
    # Calculate conversion rates by lead status
    hot_leads = 0
    warm_leads = 0
    cold_leads = 0
    hot_conversions = 0
    warm_conversions = 0
    cold_conversions = 0
    
    # Your CRM-specific logic here to get conversion data
    # This is a placeholder for the actual implementation
    
    # Calculate conversion rates
    conversion_rates = {
        'Hot': hot_conversions / hot_leads if hot_leads > 0 else 0,
        'Warm': warm_conversions / warm_leads if warm_leads > 0 else 0,
        'Cold': cold_conversions / cold_leads if cold_leads > 0 else 0
    }
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.bar(conversion_rates.keys(), conversion_rates.values())
    plt.title('Lead Conversion Rates by Status')
    plt.ylabel('Conversion Rate')
    plt.savefig('conversion_rates.png')
    
    # Print summary
    print("\nLead Qualification Performance Summary")
    print("=====================================")
    print(f"Period: Last {days} days")
    print(f"Total Leads: {hot_leads + warm_leads + cold_leads}")
    print(f"Hot Lead Conversion Rate: {conversion_rates['Hot']:.2%}")
    print(f"Warm Lead Conversion Rate: {conversion_rates['Warm']:.2%}")
    print(f"Cold Lead Conversion Rate: {conversion_rates['Cold']:.2%}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_performance()) 
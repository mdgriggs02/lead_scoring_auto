import { NextResponse } from 'next/server';
import { Lead, LeadStatus } from '@/app/types';
import { classifyLead } from '@/app/utils/leadClassifier';
import { updateCRM } from '@/app/utils/crmIntegration';

export async function POST(req: Request) {
    try {
        const leadData = await req.json();

        // Validate incoming data
        if (!leadData.email || !leadData.name) {
            return NextResponse.json(
                { error: 'Missing required fields' },
                { status: 400 }
            );
        }

        // Process engagement metrics
        const engagementMetrics = {
            websiteVisits: leadData.visits || 0,
            timeOnSite: leadData.timeOnSite || 0,
            pagesViewed: leadData.pagesViewed || 0,
            downloadedResources: leadData.downloads || 0,
            emailInteractions: leadData.emailInteractions || 0,
        };

        // Create lead object
        const lead: Lead = {
            id: crypto.randomUUID(),
            email: leadData.email,
            name: leadData.name,
            company: leadData.company,
            source: leadData.source || 'webhook',
            engagementMetrics,
            createdAt: new Date(),
            status: 'Cold', // Default status
            score: 0,
        };

        // Classify the lead
        const classification = await classifyLead(lead);
        lead.status = classification.status;
        lead.score = classification.score;

        // Update CRM
        await updateCRM(lead);

        return NextResponse.json({
            success: true,
            lead: {
                id: lead.id,
                status: lead.status,
                score: lead.score,
            },
        });
    } catch (error) {
        console.error('Error processing lead:', error);
        return NextResponse.json(
            { error: 'Failed to process lead' },
            { status: 500 }
        );
    }
} 
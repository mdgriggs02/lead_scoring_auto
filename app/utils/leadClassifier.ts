import { Lead, LeadClassificationResult, LeadStatus } from '@/app/types';

export async function classifyLead(lead: Lead): Promise<LeadClassificationResult> {
    // Calculate base score from engagement metrics
    const score = calculateEngagementScore(lead.engagementMetrics);

    // Determine lead status based on score
    let status: LeadStatus;
    if (score >= 80) {
        status = 'Hot';
    } else if (score >= 50) {
        status = 'Warm';
    } else {
        status = 'Cold';
    }

    return {
        status,
        score,
        confidence: calculateConfidence(score),
    };
}

function calculateEngagementScore(metrics: Lead['engagementMetrics']): number {
    const weights = {
        websiteVisits: 10,
        timeOnSite: 15,
        pagesViewed: 20,
        downloadedResources: 30,
        emailInteractions: 25,
    };

    const normalizedScore =
        (metrics.websiteVisits * weights.websiteVisits) +
        (Math.min(metrics.timeOnSite / 300, 1) * weights.timeOnSite) + // Normalize time on site (in seconds)
        (metrics.pagesViewed * weights.pagesViewed) +
        (metrics.downloadedResources * weights.downloadedResources) +
        (metrics.emailInteractions * weights.emailInteractions);

    return Math.min(Math.round(normalizedScore), 100);
}

function calculateConfidence(score: number): number {
    // Simple confidence calculation based on score variance from thresholds
    const threshold = score >= 80 ? 80 : score >= 50 ? 50 : 0;
    const distance = Math.abs(score - threshold);
    return Math.max(0.6, Math.min(0.95, 0.6 + (distance / 100)));
} 
export interface Message {
    role: 'user' | 'assistant';
    content: string;
    recommendations?: Recommendation[];
}

export interface Recommendation {
    title: string;
    description: string;
}

export interface Lead {
    id: string;
    email: string;
    name: string;
    company?: string;
    source: string;
    engagementMetrics: EngagementMetrics;
    createdAt: Date;
    status: LeadStatus;
    score: number;
}

export interface EngagementMetrics {
    websiteVisits: number;
    timeOnSite: number;
    pagesViewed: number;
    downloadedResources: number;
    emailInteractions: number;
}

export type LeadStatus = 'Hot' | 'Warm' | 'Cold';

export interface LeadClassificationResult {
    status: LeadStatus;
    score: number;
    confidence: number;
} 
import { NextResponse } from 'next/server';
import { Configuration, OpenAIApi } from 'openai';
import { PineconeClient } from '@pinecone-database/pinecone';
import { Message } from '@/types';

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});

const openai = new OpenAIApi(configuration);
const pinecone = new PineconeClient();

export async function POST(req: Request) {
    try {
        const { message, history } = await req.json();

        // Initialize Pinecone
        await pinecone.init({
            environment: process.env.PINECONE_ENVIRONMENT!,
            apiKey: process.env.PINECONE_API_KEY!,
        });

        // Get embeddings for the user's message
        const embedding = await openai.createEmbedding({
            model: 'text-embedding-ada-002',
            input: message,
        });

        // Query Pinecone for similar content
        const index = pinecone.Index(process.env.PINECONE_INDEX!);
        const queryResponse = await index.query({
            vector: embedding.data.data[0].embedding,
            topK: 5,
            includeMetadata: true,
        });

        // Generate response using GPT-4
        const completion = await openai.createChatCompletion({
            model: 'gpt-4',
            messages: [
                ...history,
                { role: 'user', content: message },
                {
                    role: 'system',
                    content: `Based on the user's message and these similar items: ${JSON.stringify(
                        queryResponse.matches?.map(m => m.metadata)
                    )}, provide personalized recommendations.`,
                },
            ],
        });

        return NextResponse.json({
            message: completion.data.choices[0].message?.content,
            recommendations: queryResponse.matches?.map(match => ({
                title: match.metadata?.title,
                description: match.metadata?.description,
            })),
        });
    } catch (error) {
        console.error('Error:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
} 
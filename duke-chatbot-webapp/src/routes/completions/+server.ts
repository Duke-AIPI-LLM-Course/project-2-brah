import { json } from '@sveltejs/kit';
import { v4 as uuidv4 } from 'uuid';
import { env } from '$env/dynamic/private';

interface Message {
    role: string;
    content: string;
    id: string;
}

interface RequestEvent {
    request: Request;
}

const API_URL = env.API_BASE_URL || 'http://localhost:8000';

export async function POST(event: RequestEvent) {
    const { messages } = await event.request.json();
    
    // Get the last user message
    const lastUserMessage = messages[0];
    
    if (!lastUserMessage) {
        return json({ messages });
    }

    try {
        // Call the API
        const response = await fetch(`${API_URL}/ask?question=${encodeURIComponent(lastUserMessage.content)}`);
        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }
        
        const { answer } = await response.json();
        
        return json({
            messages: [{
                role: "assistant",
                content: answer,
                id: uuidv4(),
            }, ...messages],
        });
    } catch (error) {
        console.error('Error calling API:', error);
        return json({
            messages: [{
                role: "assistant",
                content: "Sorry, I encountered an error while processing your request.",
                id: uuidv4(),
            }, ...messages],
        });
    }
}

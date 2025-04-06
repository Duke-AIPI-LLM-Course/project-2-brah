import { json } from '@sveltejs/kit';
import { v4 as uuidv4 } from 'uuid';

export async function POST(event) {
    const { messages } = await event.request.json();
    return json({
        messages: [{
            role: "assistant",
            content: "Hello, world!",
            id: uuidv4(),
        }, ...messages],
    });
}

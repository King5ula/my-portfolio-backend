import { GoogleGenAI } from '@google/genai';
import { config } from './../config/env.js';

const client = new GoogleGenAI({
    apiKey: config.geminiApiKey
});

export const getGeminiChatResponse = async (userMessage) => {
    try {
        console.log('Calling Gemini with message:', userMessage.substring(0, 50));
        
        // Simple test call first
        const response = await client.models.generateContent({
            model: 'gemini-pro',
            contents: [{
                role: 'user',
                parts: [{
                    text: userMessage
                }]
            }]
        });
        
        console.log('Raw response:', response);
        
        // Extract text from response
        let text;
        if (typeof response.text === 'function') {
            text = response.text();
        } else if (response.text) {
            text = response.text;
        } else if (response.candidates?.[0]?.content?.parts?.[0]?.text) {
            text = response.candidates[0].content.parts[0].text;
        }
        
        if (!text) {
            throw new Error('No text in response: ' + JSON.stringify(response));
        }
        
        return text;
    } catch (error) {
        console.error('Gemini error details:', {
            message: error.message,
            status: error.status,
            statusText: error.statusText,
            stack: error.stack
        });
        throw error;
    }
};  
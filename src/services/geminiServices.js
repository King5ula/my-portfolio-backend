import { GoogleGenAI } from '@google/genai';
import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

const client = new GoogleGenAI({
    apiKey: config.geminiApiKey
});

export const getGeminiChatResponse = async (userMessage) => {
    try {
        console.log('Starting Gemini API call with message:', userMessage.substring(0, 50));
        console.log('API Key exists:', !!config.geminiApiKey);
        
        const response = await client.models.generateContent({
            model: 'gemini-1.5-flash',
            contents: [{
                role: 'user',
                parts: [{
                    text: `${DAVID_PROMPT}\n\nUser: ${userMessage}`
                }]
            }]
        });
        
        console.log('Response received:', response);
        
        // Try different ways to get the text
        if (response.text && typeof response.text === 'function') {
            return response.text();
        } else if (response.text && typeof response.text === 'string') {
            return response.text;
        } else if (response.candidates && response.candidates[0]) {
            const part = response.candidates[0].content?.parts?.[0];
            if (part?.text) return part.text;
        }
        
        console.error('Could not extract text from response:', JSON.stringify(response));
        throw new Error('Could not extract text from Gemini response');
    } catch (error) {
        console.error('Full Gemini error:', error);
        throw error;
    }
};  
import { GoogleGenAI } from '@google/genai';
import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

const client = new GoogleGenAI({
    apiKey: config.geminiApiKey
});

export const getGeminiChatResponse = async (userMessage) => {
    try {
        const fullPrompt = `${DAVID_PROMPT}\n\nUser: ${userMessage}`;
        
        const response = await client.models.generateContent({
            model: 'models/gemini-1.5-flash',
            contents: [{
                role: 'user',
                parts: [{ text: fullPrompt }]
            }]
        });
        
        if (response.candidates && response.candidates[0] && response.candidates[0].content && response.candidates[0].content.parts && response.candidates[0].content.parts[0]) {
            return response.candidates[0].content.parts[0].text;
        }
        
        throw new Error('Invalid response structure from Gemini');
    } catch (error) {
        console.error('Gemini API Error:', error.message || error);
        throw new Error(`Gemini API failed: ${error.message}`);
    }
};  
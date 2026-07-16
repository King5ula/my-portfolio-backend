import { GoogleGenAI } from '@google/genai';
import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

const ai = new GoogleGenAI({ apiKey: config.geminiApiKey })

export const getGeminiChatResponse = async (userMessage) => {
    try {
        const response = await ai.models.generateContent({
            model: 'gemini-1.5-flash',
            contents: [{
                role: 'user',
                parts: [{text: `${DAVID_PROMPT}\n\nUser: ${userMessage}`}]
            }],
            generationConfig: {
                temperature: 0.4,
                maxOutputTokens: 1024
            }
        });
        
        if (response && response.text) {
            return response.text();
        }
        throw new Error('No text in response');
    } catch (error) {
        console.error('Gemini API Error:', error);
        throw error;
    }
};  
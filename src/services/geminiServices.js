import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

export const getGeminiChatResponse = async (userMessage) => {
    try {
        console.log('Calling Gemini API with message:', userMessage.substring(0, 50));
        
        const apiKey = config.geminiApiKey;
        if (!apiKey) {
            throw new Error('GEMINI_API_KEY not configured');
        }
        
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `${DAVID_PROMPT}\n\nUser: ${userMessage}`
                    }]
                }],
                generationConfig: {
                    temperature: 0.4,
                    maxOutputTokens: 1024
                }
            })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Gemini API error:', errorData);
            throw new Error(`Gemini API error: ${response.status} - ${JSON.stringify(errorData)}`);
        }
        
        const data = await response.json();
        console.log('Gemini response:', data);
        
        // Extract the text from the response
        const candidates = data.candidates;
        if (candidates && candidates.length > 0) {
            const content = candidates[0].content;
            if (content && content.parts && content.parts.length > 0) {
                return content.parts[0].text;
            }
        }
        
        throw new Error('No text found in Gemini response: ' + JSON.stringify(data));
    } catch (error) {
        console.error('Gemini service error:', error);
        throw error;
    }
};  
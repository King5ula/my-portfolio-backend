import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

export const getGeminiChatResponse = async (userMessage) => {
    try {
        console.log('🤖 Calling Gemini API...');

        const apiKey = config.geminiApiKey;
        if (!apiKey) {
            throw new Error('GEMINI_API_KEY not configured');
        }

        // Use REST API directly
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent`;

        const response = await fetch(`${url}?key=${apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                systemInstruction: {
                    parts: [{ text: DAVID_PROMPT }]
                },
                contents: [{
                    parts: [{
                        text: userMessage
                    }]
                }]
            })
        });
        
        console.log('📨 API Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('❌ Gemini API error response:', errorData);
            throw new Error(`Gemini API (${response.status}): ${JSON.stringify(errorData.error || 'Unknown error')}`);
        }
        
        const data = await response.json();
        console.log('✅ Gemini response received');
        
        // Extract the text from the response
        if (data.candidates?.[0]?.content?.parts?.[0]?.text) {
            return data.candidates[0].content.parts[0].text;
        }
        
        throw new Error('No text in response: ' + JSON.stringify(data));
    } catch (error) {
        console.error('🚨 Gemini service error:', error.message);
        throw error;
    }
};  
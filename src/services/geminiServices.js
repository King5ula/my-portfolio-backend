import { GoogleGenAI } from '@google/genai';
import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

const ai = new GoogleGenAI({ apiKey: config.geminiApiKey })

export const getGeminiChatResponse = async (userMessage) => {
    const response = await ai.models.generateContent({
        model: 'gemini-3.5-flash',
        contents: userMessage,
        config: {
            systemInstruction: DAVID_PROMPT,
            temperature: 0.4
        }
    });
    return response.text;
};  
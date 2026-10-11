import { config } from './../config/env.js';
import { DAVID_PROMPT } from '../prompts/davidPrompt.js';

const callOpenRouter = async (model, userMessage, apiKey) => {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model,
            messages: [
                { role: 'system', content: DAVID_PROMPT },
                { role: 'user', content: userMessage }
            ]
        })
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`OpenRouter API (${response.status}): ${JSON.stringify(errorData.error || 'Unknown error')}`);
    }

    const data = await response.json();
    if (!data.choices?.[0]?.message?.content) {
        throw new Error('No text in response: ' + JSON.stringify(data));
    }

    return data.choices[0].message.content;
};

export const getChatResponse = async (userMessage) => {
    const apiKey = config.openRouterApiKey;
    if (!apiKey) {
        throw new Error('OPENROUTER_API_KEY not configured');
    }

    const models = config.openRouterModels;
    let lastError;

    for (const model of models) {
        try {
            console.log(`🤖 Calling OpenRouter API with model: ${model}...`);
            const reply = await callOpenRouter(model, userMessage, apiKey);
            console.log('✅ OpenRouter response received');
            return reply;
        } catch (error) {
            console.warn(`⚠️ Model ${model} failed: ${error.message}`);
            lastError = error;
        }
    }

    console.error('🚨 All OpenRouter models failed:', lastError.message);
    throw lastError;
};

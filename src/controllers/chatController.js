import { getGeminiChatResponse } from "../services/geminiServices.js";

export const handleChatResponse = async (req, res) => {
    try {
        const { userMessage } = req.body;

        if (!userMessage) {
            return res.status(400).json({ error: "Message content cannot be blank."});
        }

        const reply = await getGeminiChatResponse(userMessage);
        return res.status(200).json({ reply });
    } catch (error) {
        console.error("Chat controller Error:", error.message);
        console.error("Full error:", error);
        return res.status(500).json({ error: `Internal server error: ${error.message}`});
    }
};
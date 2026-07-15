import { Router } from 'express';
import { rateLimit } from 'express-rate-limit';
import { handleChatResponse } from '../controllers/chatController.js';
import { handleContactForm } from '../controllers/contactController.js';

export const chatRouter = Router();

const aiChatLimiter = rateLimit({
    windowMs: 20 * 6 * 1000,
    max: 20,
    message: {
        error: "Too many requests sent to David's AI clone. Please slow down and try again shortly."
    },
    standardHeaders: true,
    legacyHeaders: false,
});

const contactLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
  max: 5,
  message: { error: "Too many messages sent from this device. Please try again later." }
});

chatRouter.post('/chat', aiChatLimiter, handleChatResponse);
chatRouter.post('/contact', contactLimiter, handleContactForm);
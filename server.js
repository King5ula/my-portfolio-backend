import express from 'express';
import cors from 'cors';
import { config } from './src/config/env.js';
import { chatRouter } from './src/routes/chatRoutes.js'; // Clean named object binding

const app = express();

app.use(cors({
    origin: [
        'http://localhost:5173',
        'https://my-portfolio-frontend-rd8rfk620-domn8r.vercel.app',
        'https://my-portfolio-frontend-kg5dpdn5v-domn8r.vercel.app',
        'https://my-portfolio-frontend-domn8r.vercel.app'
    ],
    methods: ['GET', 'POST', 'OPTIONS'],
    credentials: true,
    allowedHeaders: ['Content-Type'],
    optionsSuccessStatus: 200
}));
app.use(express.json());

// Seamless mounting engine
app.use('/api', chatRouter);

app.listen(config.port, () => console.log(`Running on ${config.port}`));

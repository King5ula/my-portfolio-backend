import express from 'express';
import cors from 'cors';
import { config } from './src/config/env.js';
import { chatRouter } from './src/routes/chatRoutes.js'; // Clean named object binding

const app = express();

app.use(cors({
    origin: [
        'http://localhost:5173',
        'https://vercel.app'
    ],
    methods: ['GET', 'POST'],
    credentials: true,
}));
app.use(express.json());

// Seamless mounting engine
app.use('/api', chatRouter);

app.listen(config.port, () => console.log(`Running on ${config.port}`));

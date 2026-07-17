import express from 'express';
import cors from 'cors';
import { config } from './src/config/env.js';
import { chatRouter } from './src/routes/chatRoutes.js'; // Clean named object binding

const app = express();

const allowedOriginPattern = /^http:\/\/localhost:5173$|^https:\/\/my-portfolio-frontend(-[a-z0-9]+)*\.vercel\.app$/;

app.use(cors({
    origin: (origin, callback) => {
        if (!origin || allowedOriginPattern.test(origin)) {
            return callback(null, true);
        }
        callback(new Error(`Not allowed by CORS: ${origin}`));
    },
    methods: ['GET', 'POST', 'OPTIONS'],
    credentials: true,
    allowedHeaders: ['Content-Type'],
    optionsSuccessStatus: 200
}));
app.use(express.json());

// Seamless mounting engine
app.use('/api', chatRouter);

app.listen(config.port, () => console.log(`Running on ${config.port}`));

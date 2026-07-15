import 'dotenv/config';

export const config = {
    port: process.env.PORT || 5000,
    geminiApiKey: process.env.GEMINI_API_KEY,
    emailHost: process.env.EMAIL_HOST || 'smtp.gmail.com',
    emailPort: parseInt(process.env.EMAIL_PORT || '465', 10),
    emailUser: process.env.EMAIL_USER,
    emailPass: process.env.EMAIL_PASS,
    emailReceiver: process.env.EMAIL_RECEIVER
};

if (!config.geminiApiKey) {
    console.error("CRITICAL ERROR: GEMINI_API_KEY is missing from environment variables.")
    process.exit(1);
}

if (!config.emailUser || !config.emailPass) {
  console.warn("WARNING: Email user or password credentials are blank. Contact form will fail.");
}
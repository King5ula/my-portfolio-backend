import 'dotenv/config';

export const config = {
    port: process.env.PORT || 5000,
    openRouterApiKey: process.env.OPENROUTER_API_KEY,
    openRouterModels: (process.env.OPENROUTER_MODELS || 'nvidia/nemotron-3.5-lightning:free,liquid/lfm-2.5-2.6b:free,poolside/laguna-s-2.1:free')
        .split(',')
        .map(model => model.trim())
        .filter(Boolean),
    emailHost: process.env.EMAIL_HOST || 'smtp.gmail.com',
    emailPort: parseInt(process.env.EMAIL_PORT || '465', 10),
    emailUser: process.env.EMAIL_USER,
    emailPass: process.env.EMAIL_PASS,
    emailReceiver: process.env.EMAIL_RECEIVER
};

if (!config.openRouterApiKey) {
    console.error("CRITICAL ERROR: OPENROUTER_API_KEY is missing from environment variables.")
    process.exit(1);
}

if (!config.emailUser || !config.emailPass) {
  console.warn("WARNING: Email user or password credentials are blank. Contact form will fail.");
}
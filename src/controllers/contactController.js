import { sendContactEmail } from '../services/emailService.js';

export const handleContactForm = async (req, res) => {
  try {
    const { name, email, message } = req.body;

    // Simple sanitization & validation checks
    if (!name || !email || !message) {
      return res.status(400).json({ error: "All contact fields are required." });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: "Please enter a valid email address." });
    }

    // Hand execution to our background mail worker
    await sendContactEmail({ name, email, message });

    return res.status(200).json({ success: "Your message has been delivered successfully!" });
  } catch (error) {
    console.error("Contact Form Controller Error:", error);
    return res.status(500).json({ error: "Failed to forward your message. Please try again later." });
  }
};

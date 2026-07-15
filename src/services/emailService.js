import nodemailer from 'nodemailer';
import { config } from '../config/env.js';

const transporter = nodemailer.createTransport({
  host: config.emailHost,      
  port: config.emailPort, 
  secure: true, 
  auth: {
    user: config.emailUser,
    pass: config.emailPass,
  },
});
export const sendContactEmail = async ({ name, email, message }) => {
  const mailOptions = {
    from: `"Portfolio Contact" <${config.emailUser}>`, 
    to: config.emailReceiver, 
    replyTo: email, 
    subject: `💼 New Portfolio Message from ${name}`,
    text: `You received a message via your portfolio site contact form:\n\nName: ${name}\nEmail: ${email}\n\nMessage:\n${message}`,
    html: `
      <div style="font-family: sans-serif; padding: 20px; color: #333;">
        <h2 style="color: #4f46e5; border-bottom: 1px solid #ddd; padding-bottom: 10px;">New Portfolio Contact</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> <a href="mailto:${email}">${email}</a></p>
        <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #4f46e5;">
          <p style="white-space: pre-wrap; margin: 0;">${message}</p>
        </div>
      </div>
    `,
  };

  return await transporter.sendMail(mailOptions);
};
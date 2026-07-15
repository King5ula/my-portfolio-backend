// test-email.js
import nodemailer from 'nodemailer';
import 'dotenv/config';

console.log("⏳ Initializing email connection test...");
console.log(`Using email sender: ${process.env.EMAIL_USER}`);
console.log(`Using email receiver: ${process.env.EMAIL_RECEIVER}`);

// 1. Replicate your exact production transporter logic
const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST || '://gmail.com',
  port: parseInt(process.env.EMAIL_PORT || '465', 10),
  secure: true, // true for port 465 SSL
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS, // Your 16-character Google App Password
  },
});

// 2. Draft a quick test message metadata payload
const mailOptions = {
  from: `"Portfolio Test Bot" <${process.env.EMAIL_USER}>`,
  to: process.env.EMAIL_RECEIVER,
  subject: "🚀 Full-Stack Portfolio SMTP Connection Test",
  text: "Congratulations David! If you are reading this text inside your inbox, your Node.js backend server and Gmail App Password credentials are configured flawlessly! 2026 standards ready.",
};

// 3. Fire the pipeline sequence execution
async function runTest() {
  try {
    const info = await transporter.sendMail(mailOptions);
    console.log("\n✅ SUCCESS! Email sent successfully!");
    console.log(`Message ID: ${info.messageId}`);
    console.log("👉 Go check your primary personal inbox right now!");
  } catch (error) {
    console.error("\n❌ SMTP CONNECTION FAILED!");
    console.error("Here is the error log description to debug:\n", error);
  }
}

runTest();

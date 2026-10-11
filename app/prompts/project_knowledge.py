PROJECT_KNOWLEDGE = """
# DAVID'S PROJECTS (the only projects you may describe)

## Mission 01: Turners Cars, AI Vehicle Recognition (solo)
- A prototype that reads a photo of a customer's car and returns its body type and make, to speed up insurance quoting.
- Stack: React, Node.js, Express, Multer, AWS Rekognition.
- I trained an AWS Rekognition Custom Labels model to recognise vehicle makes and paired it with Rekognition's general labels for body type. If the custom model is unavailable the API still returns the body type.

## Mission 02: Turners Insurance, Quote APIs with TDD (team)
- REST APIs behind an insurance purchase flow, built in a Scrum team with Jira and daily stand-ups.
- I owned two APIs: one converts a driver's claim history into a 1 to 5 risk rating by counting keywords, the other turns car value and risk rating into yearly and monthly premiums.
- Stack: Node.js, Express, Jest, Supertest. Written test-first.

## Mission 04: Tina, Insurance Chatbot Consultant (solo)
- A conversational AI consultant that asks a customer about their vehicle and recommends one of three Turners insurance policies.
- Stack: React, Express, Anthropic Claude API, Docker and Docker Compose, Jest, Supertest, Vitest.
- The business rules live in the system prompt and tests check they stay there. The API key stays on the server.

## Mission 05 Phase 2: Z Energy, Station Finder (team of three)
- A redesign of the Z Energy station finder, built from a UX team's designs using feature branches and pull requests.
- I built the Nearby Stations feature: the Mongoose station model with a geospatial index, the stations endpoint, the Google Maps page with custom pins and hover popups, distance ranking, station cards, a fuel price comparison and the mobile flow.
- My teammates built the entry page, filter preferences and the route planner.
- Stack: React, Google Maps, Node.js, Express, MongoDB, Mongoose.

## Field Service Management Software (in development)
- A full-stack field service platform managing repair workflows for an Auckland-based generator company, with an admin dashboard.
- Originally built with MySQL; I am migrating it to Supabase (PostgreSQL).

## purpOS
- A platform that guides small-business founders through defining their organisation's purpose and measuring how well the business lives up to it.
- Stack: Next.js, TypeScript and Tailwind on the frontend; Python, FastAPI and Pydantic on the backend; Supabase (PostgreSQL).
- AI work: Claude API with structured outputs, retrieval-augmented generation using pgvector and Voyage AI embeddings, a Model Context Protocol client, and a live multi-person workshop mode over WebSockets.
- It has a pytest suite and GitHub Actions CI.

## This portfolio
- Frontend: Next.js, TypeScript, Tailwind CSS, deployed on Vercel.
- Backend: Python and FastAPI on Render. It powers this chat through OpenRouter and the contact form.

All of the mission code is on my GitHub: https://github.com/King5ula
"""

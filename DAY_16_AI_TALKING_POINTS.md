# Day 16 AI Talking Points Card

## Groq in Plain English
- **What Groq does:** Groq is the AI engine used by the project to turn plain language prompts into intelligent responses.
- **How it works here:** The app sends a text prompt to the Groq API, which runs the Llama-3.3-70b model and returns a natural-language answer.
- **Why Groq matters:** It lets us keep our AI logic simple while outsourcing the actual language understanding and response generation to a specialized service.
- **Security note:** The Groq API key is stored in environment variables, not in code, to keep secrets safe.

---

## Prompts Explained in Plain English

### `describe_prompt`
- This prompt template tells the AI to take a short task idea and expand it into full developer-ready instructions.
- In other words, it turns a rough requirement into a clear task breakdown with steps, acceptance criteria, and technical details.
- Use it when you want the AI to write a detailed task description for a Kanban board.

### `generate_report_prompt`
- This prompt asks the AI to write a concise sprint report.
- It produces a short executive summary, accomplishments, challenges, metrics, and next steps.
- Use it when you want a polished status report for stakeholders.

### `recommend_prompt`
- This prompt asks the AI to act like a product manager and recommend the next best tasks.
- It prioritizes work by business value, feasibility, risk, and team capacity.
- Use it when planning the next sprint or choosing the best work items.

---

## Security Talking Points
- **API protection:** The service uses an `X-API-Key` on protected endpoints so only authorized systems can access the AI service.
- **Input sanitization:** User text is cleaned before processing to remove scripts and suspicious prompt injection content.
- **Rate limiting:** Requests are limited to prevent abuse and keep the service available under load.
- **Security headers:** The app adds headers like `X-Frame-Options` and `Strict-Transport-Security` to protect from common web attacks.
- **Error handling:** Errors are returned as generic messages so internal details never leak to users.
- **Secrets handling:** All keys (including Groq API key) are loaded from `.env`, not checked into Git.

---

## Technology Snapshot
- **AI backend:** Python Flask with Groq client
- **Model:** Llama-3.3-70b-versatile via Groq API
- **Security middleware:** CORS, rate limiting, input validation, generic error handling
- **Frontend:** React app
- **Integration:** Java backend can call the AI service securely
- **Deployment:** Docker-based container setup

---

## GitHub Link
https://github.com/srujancshetty/grc-sprint-board-kanban

---

## Demo Use Cases
- **Tell me what this task means:** Use `describe_prompt` to expand task ideas.
- **Show sprint progress:** Use `generate_report_prompt` to create a report summary.
- **Choose the next task:** Use `recommend_prompt` to prioritize work.
- **Ensure security:** Mention the API key, sanitization, and headers in every demo.

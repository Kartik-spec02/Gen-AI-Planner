# 🎉 GenAI Event Planner

A premium, full-stack GenAI-powered planning assistant built for **PromptWars Virtual**. It helps users organize weddings, birthdays, and community events by generating custom budgets, timelines, vendor checklists, and personalized ideas.

## ✨ Features
- **Real GenAI:** Uses Google's `gemini-3.8-flash` model to generate unique, creative plans based on your specific theme.
- **Smart Fallback:** If the AI is offline or rate-limited, a built-in mock engine ensures the app never crashes.
- **Beautiful UI:** Features a modern dark-mode glassmorphism design, animated background blobs, and smooth interactions.
- **Print / PDF Export:** One-click printing with custom CSS so users can take their plans to vendors.
- **Database Persistence:** All generated plans are safely saved to an SQLite database.

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript
- **Backend:** Python 3, FastAPI, Uvicorn
- **Database:** SQLite
- **AI Integration:** Google GenAI SDK (`google-genai`)

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/event-planner.git
   cd event-planner
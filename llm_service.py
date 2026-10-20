import os, json, time
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

try:
    if GEMINI_KEY:
        _client = genai.Client(api_key=GEMINI_KEY)
    else:
        _client = None
except Exception as e:
    print("GenAI setup error:", e)
    _client = None

SYSTEM_PROMPT = """You are an expert event planner. Given an event brief, produce a JSON object with:
- "summary": 2-sentence strategy
- "budget_breakdown": list of {category, percent, amount, notes}
- "timeline": list of {phase, weeks_before, tasks:[...]}
- "vendor_checklist": list of {vendor_type, questions:[...], estimated_cost}
- "personalized_ideas": list of 6 creative, specific ideas tied to the theme
Return ONLY valid JSON. Percentages must sum to 100."""

def _mock_plan(brief: Dict[str, Any]) -> Dict[str, Any]:
    etype = brief.get("event_type", "event").lower()
    budget = float(brief.get("budget", 10000))
    guests = int(brief.get("guests", 50))
    theme = brief.get("theme", "elegant")

    splits = {
        "wedding":  [("Venue", 30), ("Catering", 25), ("Photography", 12), ("Attire & Beauty", 10),
                     ("Flowers & Decor", 10), ("Music & Entertainment", 7), ("Invitations & Stationery", 3), ("Contingency", 3)],
        "birthday": [("Venue", 20), ("Food & Cake", 30), ("Entertainment", 15), ("Decor", 15),
                     ("Photography", 10), ("Favors", 5), ("Contingency", 5)],
        "community": [("Venue & Permits", 20), ("Food & Beverage", 25), ("Speakers/Performers", 15),
                      ("Marketing", 10), ("Equipment & AV", 15), ("Volunteers/Staff", 10), ("Contingency", 5)],
    }
    key = "wedding" if "wed" in etype else "birthday" if "birth" in etype else "community"
    budget_breakdown = [
        {"category": c, "percent": p, "amount": round(budget * p / 100, 2), "notes": "Standard allocation for this category."}
        for c, p in splits[key]
    ]

    timelines = {
        "wedding": [
            {"phase": "Foundation", "weeks_before": 48, "tasks": ["Set budget", "Draft guest list", "Choose date & venue"]},
            {"phase": "Vendors",     "weeks_before": 36, "tasks": ["Book photographer", "Hire caterer", "Select florist"]},
            {"phase": "Details",     "weeks_before": 20, "tasks": ["Send save-the-dates", "Order attire", "Plan menu tasting"]},
            {"phase": "Logistics",   "weeks_before": 8,  "tasks": ["Send invitations", "Finalize seating", "Confirm vendors"]},
            {"phase": "Final",       "weeks_before": 2,  "tasks": ["Rehearsal", "Pack day-of kit", "Confirm timeline"]},
        ],
        "birthday": [
            {"phase": "Concept",     "weeks_before": 8, "tasks": ["Pick theme", "Set guest list", "Choose venue"]},
            {"phase": "Booking",     "weeks_before": 6, "tasks": ["Book entertainer", "Order cake", "Send invites"]},
            {"phase": "Prep",        "weeks_before": 3, "tasks": ["Buy decor", "Plan food", "Order favors"]},
            {"phase": "Final",       "weeks_before": 1, "tasks": ["Confirm RSVPs", "Prep playlist", "Pack party kit"]},
        ],
        "community": [
            {"phase": "Vision",      "weeks_before": 16, "tasks": ["Define purpose & audience", "Form committee", "Secure permits"]},
            {"phase": "Partners",    "weeks_before": 12, "tasks": ["Recruit sponsors", "Book venue", "Confirm speakers"]},
            {"phase": "Promote",     "weeks_before": 6,  "tasks": ["Launch marketing", "Open registration", "Recruit volunteers"]},
            {"phase": "Execute",     "weeks_before": 2,  "tasks": ["Final logistics", "Safety briefing", "Run sheet"]},
        ],
    }
    vendor_map = {
        "wedding":  ["Venue", "Caterer", "Photographer", "Florist", "DJ/Band", "Officiant", "Hair & Makeup"],
        "birthday": ["Venue", "Baker", "Entertainer", "Balloon/Decor Artist", "Photographer"],
        "community":["Venue", "AV Company", "Security", "Food Trucks", "Print/Marketing"],
    }
    vendor_checklist = [
        {"vendor_type": v,
         "questions": ["What's included?", "Deposit & cancellation policy?", "Insurance/licensing?", "Backup plan?"],
         "estimated_cost": round(budget * 0.08, 2)}
        for v in vendor_map[key]
    ]

    ideas = [
        f"Build a {theme}-themed welcome station with a custom scent.",
        "Create a shared memory wall where guests leave voice notes via QR code.",
        "Personalize place cards with a one-line 'fun fact' about each guest.",
        "Hire a roaming polaroid photographer for candid keepsakes.",
        "Design a signature drink or mocktail tied to your story.",
        "Send a post-event GenAI-generated recap video/summary to guests.",
    ]
    return {
        "summary": f"A {guests}-guest {etype} anchored in a {theme} theme, prioritizing guest experience while keeping {budget:,.0f} budget in balance.",
        "budget_breakdown": budget_breakdown,
        "timeline": timelines[key],
        "vendor_checklist": vendor_checklist,
        "personalized_ideas": ideas,
    }

def generate_plan(brief: Dict[str, Any]) -> Dict[str, Any]:
    if _client is None:
        return _mock_plan(brief)

    prompt = f"""{SYSTEM_PROMPT}
    
    Event type: {brief.get('event_type')}
    Theme: {brief.get('theme')}
    Budget (USD): {brief.get('budget')}
    Guests: {brief.get('guests')}
    Date: {brief.get('date')}
    Location: {brief.get('location')}
    Notes: {brief.get('notes','')}
    """

    for attempt in range(3):
        try:
            response = _client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            print(f"API Error: {e}")
            if "503" in str(e) and attempt < 2:
                time.sleep(3)
            else:
                return _mock_plan(brief)
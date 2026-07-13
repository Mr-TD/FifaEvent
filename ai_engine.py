"""
StadiumIQ — GenAI Engine
Powered by Google Gemini API with smart fallback
"""

import hashlib
import json
import logging
import random
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai

    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class StadiumAI:
    """AI engine for StadiumIQ — wraps Google Gemini with fallback mock responses."""

    SYSTEM_PROMPT = """You are StadiumIQ, an AI assistant for the FIFA World Cup 2026.
You help fans, staff, and organizers with:
- Stadium navigation and finding points of interest (food, restrooms, exits, medical, merchandise)
- Match schedules, team info, and live updates
- Multilingual assistance (you speak 12+ languages fluently)
- Accessibility guidance (wheelchair routes, audio descriptions, sensory-friendly spaces)
- Transportation and parking info
- Crowd management recommendations (for staff)
- Sustainability tips and eco-friendly actions

You are friendly, concise, and helpful. Use emojis sparingly for warmth.
Keep responses under 200 words unless the user asks for details.
Always prioritize safety information when relevant.
The tournament spans 16 venues across the United States, Mexico, and Canada from June 11 to July 19, 2026."""

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key
        self.model = None
        self.use_gemini = False
        self.cache: Dict[str, str] = {}

        if api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=self.SYSTEM_PROMPT)
                self.use_gemini = True
                logger.info("GenAI model initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize GenAI model: {e}")
                self.use_gemini = False

    def _get_cache_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode("utf-8")).hexdigest()

    def chat(self, message: str, language: str = "en", context: str = "") -> str:
        """Conversational fan assistant."""
        if self.use_gemini and self.model:
            try:
                prompt = f"User language: {language}\nContext: {context}\nUser: {message}"
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return self._mock_chat(message, language)
        return self._mock_chat(message, language)

    def translate(self, text: str, source_lang: str = "en", target_lang: str = "es") -> str:
        """Translate text between languages with caching."""
        prompt = f"Translate the following text from {source_lang} to {target_lang}. Return ONLY the translation, nothing else.\n\nText: {text}"
        cache_key = self._get_cache_key(prompt)
        
        if cache_key in self.cache:
            return self.cache[cache_key]

        if self.use_gemini and self.model:
            try:
                response = self.model.generate_content(prompt)
                self.cache[cache_key] = response.text
                return response.text
            except Exception as e:
                logger.error(f"Translation error: {e}")
                return self._mock_translate(text, target_lang)
        return self._mock_translate(text, target_lang)

    def generate_match_preview(self, match_data: Dict[str, Any]) -> str:
        """Generate AI match preview."""
        prompt = f"""Generate an exciting 2-3 sentence match preview for this FIFA World Cup 2026 game:
{match_data.get('team_a')} vs {match_data.get('team_b')}
Stage: {match_data.get('stage')}
Venue: {match_data.get('stadium_name', 'TBD')}
Date: {match_data.get('match_date', 'TBD')}

Make it engaging and informative. Include key storylines or rivalries if applicable."""
        cache_key = self._get_cache_key(prompt)
        
        if cache_key in self.cache:
            return self.cache[cache_key]

        if self.use_gemini and self.model:
            try:
                response = self.model.generate_content(prompt)
                self.cache[cache_key] = response.text
                return response.text
            except Exception as e:
                logger.error(f"Match preview error: {e}")
                return self._mock_match_preview(match_data)
        return self._mock_match_preview(match_data)

    def crowd_recommendation(self, crowd_data: Dict[str, Any]) -> str:
        """Generate operational recommendations based on crowd data using structured output."""
        if self.use_gemini and self.model:
            try:
                prompt = f"""As a crowd management AI for FIFA World Cup 2026, analyze this stadium crowd data and provide 3-4 actionable recommendations.
IMPORTANT: Your response MUST be valid JSON in this exact format:
{{"recommendations": ["rec 1", "rec 2"]}}

Stadium: {crowd_data.get('stadium_name', 'Unknown')}
Zone Data: {crowd_data.get('zones', [])}
Overall Capacity: {crowd_data.get('overall_density', 0)}%
Time: {crowd_data.get('time', 'N/A')}
"""
                response = self.model.generate_content(prompt)
                text_out = response.text.strip()
                if text_out.startswith("```json"):
                    text_out = text_out[7:]
                if text_out.endswith("```"):
                    text_out = text_out[:-3]
                
                try:
                    data = json.loads(text_out.strip())
                    recs = data.get("recommendations", [])
                    if recs:
                        return "**AI Operational Recommendations:**\n" + "\n".join([f"1. **Action:** {r}" for r in recs])
                except json.JSONDecodeError:
                    logger.warning("Failed to decode JSON from AI crowd recommendation.")
                    return response.text
            except Exception as e:
                logger.error(f"Crowd recommendation error: {e}")
                return self._mock_crowd_recommendation(crowd_data)
        return self._mock_crowd_recommendation(crowd_data)

    def accessibility_guide(self, user_needs: str, destination: str) -> str:
        """Personalized accessible route guidance."""
        if self.use_gemini and self.model:
            try:
                prompt = f"""Provide accessible navigation guidance for a FIFA World Cup 2026 stadium visitor:

User accessibility needs: {user_needs}
Destination: {destination}

Provide step-by-step guidance that is clear, reassuring, and inclusive. Mention elevators, ramps, accessible entrances, and any assistance points along the way."""
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Accessibility guide error: {e}")
                return self._mock_accessibility_guide(user_needs, destination)
        return self._mock_accessibility_guide(user_needs, destination)

    def sustainability_tip(self, context: str = "general") -> str:
        """Generate eco-friendly suggestions."""
        prompt = f"""Give one specific, actionable sustainability tip for a fan attending the FIFA World Cup 2026.
Context: {context}
Keep it brief (2-3 sentences), positive, and motivating. Include a relevant emoji."""
        cache_key = self._get_cache_key(prompt)
        if cache_key in self.cache:
            return self.cache[cache_key]

        if self.use_gemini and self.model:
            try:
                response = self.model.generate_content(prompt)
                self.cache[cache_key] = response.text
                return response.text
            except Exception as e:
                logger.error(f"Sustainability tip error: {e}")
                return self._mock_sustainability_tip()
        return self._mock_sustainability_tip()

    # ─── Mock/Fallback Responses ──────────────────────────────────────

    def _mock_chat(self, message: str, language: str) -> str:
        """Smart mock responses when Gemini is unavailable."""
        msg = message.lower()

        if any(w in msg for w in ["food", "eat", "hungry", "restaurant", "drink"]):
            return "🍔 Great question! Each stadium has multiple food zones. I recommend checking the **North Food Court** for international cuisine or the **South Plaza** for quick bites. Look for the 🟢 green markers on the stadium map for food locations. Vegetarian and halal options are available at most stalls!"

        elif any(w in msg for w in ["restroom", "bathroom", "toilet", "washroom"]):
            return "🚻 Restrooms are located at every gate entrance and at each corner of every level. The nearest ones are usually at **Gates A, C, E, and G**. Accessible restrooms are marked with ♿ symbols. Check the stadium map for real-time availability!"

        elif any(w in msg for w in ["exit", "leave", "gate", "way out"]):
            return "🚪 Exit gates are located at all four cardinal points of the stadium. For the quickest exit, use the gate closest to your seating section. After the match, **Gates B and D** typically have the least congestion. Follow the illuminated exit signs!"

        elif any(w in msg for w in ["medical", "help", "emergency", "first aid", "doctor"]):
            return "🏥 **Medical stations** are located at Gates A, D, and near Section 200. For emergencies, alert any staff member in a yellow vest or call the stadium emergency line. First aid kits are available at all information desks. Stay calm — help is always nearby!"

        elif any(w in msg for w in ["schedule", "match", "game", "when", "time", "today"]):
            return "⚽ Check the **Schedule** tab for today's matches! The FIFA World Cup 2026 features 104 matches across 16 venues from June 11 to July 19, 2026. You can filter by group, date, or venue. Want me to find a specific team's schedule?"

        elif any(w in msg for w in ["parking", "car", "transport", "bus", "metro", "train"]):
            return "🚗 **Transportation Tips:**\n- **Metro/Subway** is the fastest option — follow signs to the nearest station\n- **Bus shuttles** run every 10 minutes from downtown\n- **Parking** lots open 4 hours before kickoff\n- **Rideshare** drop-off zones are at Gates F and H\n\nWe recommend public transit to reduce congestion!"

        elif any(w in msg for w in ["wheelchair", "accessible", "disability", "blind", "deaf"]):
            return "♿ **Accessibility is our priority!** All FIFA World Cup 2026 venues are fully accessible:\n- Wheelchair-accessible seating in every section\n- Ramps and elevators at all levels\n- Audio description services available\n- Sign language interpreters at info desks\n- Sensory rooms for those who need a quiet break\n\nVisit the **Accessibility** page for personalized guidance!"

        elif any(w in msg for w in ["hello", "hi", "hey", "howdy", "sup"]):
            return "👋 Hello and welcome to **StadiumIQ**! I'm your AI assistant for the FIFA World Cup 2026. I can help you with:\n\n🗺️ Stadium navigation\n⚽ Match schedules\n🍔 Food & facilities\n♿ Accessibility\n🌍 Multilingual support\n🌱 Sustainability tips\n\nWhat can I help you with today?"

        elif any(w in msg for w in ["thank", "thanks", "thx"]):
            return "😊 You're welcome! Enjoy the FIFA World Cup 2026! If you need anything else, I'm always here. ⚽🎉"

        else:
            return '⚽ Thanks for your question! While I\'m currently running in demo mode, here\'s what I can help with:\n\n🗺️ **Navigation** — "Where is the nearest restroom?"\n🍔 **Food** — "What food options are available?"\n📅 **Schedule** — "What matches are today?"\n🚗 **Transport** — "How do I get to the stadium?"\n♿ **Accessibility** — "Wheelchair accessible routes"\n\nTry asking one of these, or set up a **Gemini API key** in the `.env` file for full AI-powered responses!'

    def _mock_translate(self, text: str, target_lang: str) -> str:
        translations = {
            "es": f"[Traducción al español] {text}",
            "fr": f"[Traduction en français] {text}",
            "pt": f"[Tradução em português] {text}",
            "ar": f"[ترجمة عربية] {text}",
            "zh": f"[中文翻译] {text}",
            "hi": f"[हिंदी अनुवाद] {text}",
            "de": f"[Deutsche Übersetzung] {text}",
            "ja": f"[日本語訳] {text}",
            "ko": f"[한국어 번역] {text}",
        }
        return translations.get(target_lang, f"[Translation to {target_lang}] {text}")

    def _mock_match_preview(self, match_data: Dict[str, Any]) -> str:
        previews = [
            f"⚽ An electrifying clash awaits as **{match_data.get('team_a')}** face off against **{match_data.get('team_b')}** in the {match_data.get('stage')}! Both teams have shown incredible form, and this promises to be a match that fans will remember for years. Expect high intensity from kickoff!",
            f"🔥 **{match_data.get('team_a')}** vs **{match_data.get('team_b')}** — a fixture that needs no introduction! With pride and progression on the line in the {match_data.get('stage')}, both squads will leave everything on the pitch. This is the beautiful game at finest!",
            f"🏟️ The stage is set for **{match_data.get('team_a')}** to take on **{match_data.get('team_b')}** in what could be the match of the round! The {match_data.get('stage')} has produced some memorable encounters, and this one looks set to deliver more drama and world-class football.",
        ]
        return random.choice(previews)

    def _mock_crowd_recommendation(self, crowd_data: Dict[str, Any]) -> str:
        density = crowd_data.get("overall_density", 50)
        stadium = crowd_data.get("stadium_name", "the stadium")

        if density > 85:
            return f"""🔴 **HIGH DENSITY ALERT — {stadium}**

1. **Activate overflow protocols** — Open auxiliary gates (B2, D2) to distribute incoming fans across multiple entry points
2. **Deploy additional staff** to high-density zones, particularly the North Stand and East Concourse
3. **Announce alternative routes** via PA system — direct fans to less crowded sections via the South Corridor
4. **Monitor exits closely** — Ensure all emergency exits remain clear and accessible at all times
5. **Consider staggered food service** — Redirect queues to underutilized vendors in the West Wing"""

        elif density > 60:
            return f"""🟡 **MODERATE DENSITY — {stadium}**

1. **Pre-position staff** at key transition points between levels 1 and 2
2. **Activate digital signage** to show real-time queue lengths at food and restroom facilities
3. **Monitor entry gates** — Gate A showing higher than average throughput; consider opening Lane 2
4. **Remind fans via app** about less crowded concession areas on the upper concourse"""

        else:
            return f"""🟢 **NORMAL OPERATIONS — {stadium}**

1. **Maintain standard staffing levels** across all zones
2. **Good time for maintenance** — Schedule restroom cleaning rotations
3. **Engagement opportunity** — Activate fan zone activities in the lower concourse
4. **Prepare for surge** — Pre-match rush expected in approximately 45 minutes"""

    def _mock_accessibility_guide(self, user_needs: str, destination: str) -> str:
        return f"""♿ **Accessible Route to {destination}**

Based on your needs ({user_needs}), here's your personalized route:

1. **Enter via Gate A** (fully accessible entrance with automatic doors)
2. **Take the elevator** located 20 meters to your right — it goes to all levels
3. **Follow the blue accessibility markers** on the floor to {destination}
4. **Assistance point** is available midway — look for the purple "Help" desk

📍 **Estimated time:** 5-7 minutes
♿ **Route features:** Ramp access, wide corridors, tactile paving
🆘 **Need help?** Press any yellow assistance button or ask staff in green vests

All FIFA World Cup 2026 venues meet the highest accessibility standards. Enjoy the match! 🎉"""

    def _mock_sustainability_tip(self) -> str:
        tips = [
            "🌱 **Bring a reusable water bottle!** All FIFA World Cup 2026 stadiums have free water refill stations. You'll save an average of 3 plastic bottles per visit — that's a real impact when multiplied by millions of fans!",
            "🚌 **Take public transit to the stadium!** Each fan who uses the metro instead of driving saves approximately 4.5 kg of CO₂ emissions per trip. Plus, you'll avoid parking stress!",
            "♻️ **Use the color-coded recycling bins** throughout the stadium — Blue for recyclables, Green for compostables, Black for waste. FIFA 2026 aims to recycle 90% of stadium waste!",
            "🌍 **Go digital with your tickets and programs!** Choosing digital over paper saves trees and reduces waste. The FIFA app has everything you need — from tickets to stadium maps!",
            "🍽️ **Choose locally sourced food options** marked with the 🌿 green leaf at food stalls. They have a lower carbon footprint and support local communities around each venue!",
            "💡 **Did you know?** FIFA World Cup 2026 stadiums use 100% renewable energy. By attending, you're supporting one of the most sustainable sporting events ever. Spread the word! ⚡",
        ]
        return random.choice(tips)

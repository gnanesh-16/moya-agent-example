"""
Dynamic prompt fetcher using OpenAI API
Replaces static/fake prompts with AI-generated contextual prompts
"""

import os
import openai
from typing import List, Dict, Any
from datetime import datetime
import json
import random


class PromptFetcher:
    """Fetches dynamic travel prompts using OpenAI API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self._cached_prompts = []
        self._last_fetch_time = None
        self._cache_duration = 300  # 5 minutes in seconds
    
    def fetch_travel_prompts(self, count: int = 8, category: str = "general") -> List[str]:
        """
        Fetch dynamic travel prompts from OpenAI API
        
        Args:
            count: Number of prompts to generate
            category: Category of prompts (general, planning, information, budget, etc.)
            
        Returns:
            List of generated travel prompts
        """
        # Check cache first
        if self._should_use_cache():
            return self._get_cached_prompts(count)
        
        try:
            current_month = datetime.now().strftime("%B")
            current_year = datetime.now().year
            
            system_prompt = f"""You are a travel planning assistant. Generate {count} realistic and diverse travel planning prompts that users might ask. 
            
            The prompts should be:
            - Practical and realistic
            - Varied in scope (short trips, long trips, different budgets, different destinations)
            - Include different types of requests (planning, information, suggestions)
            - Consider current time context (it's {current_month} {current_year})
            - Mix of domestic and international destinations
            - Different travel styles (family, solo, romantic, business, adventure)
            
            Focus on category: {category}
            
            Return only a JSON array of strings, no other text."""
            
            user_prompt = self._get_category_specific_prompt(category, count)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.8
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the JSON response
            try:
                prompts = json.loads(content)
                if isinstance(prompts, list):
                    # Cache the results
                    self._cached_prompts = prompts
                    self._last_fetch_time = datetime.now()
                    return prompts[:count]
            except json.JSONDecodeError:
                # Fallback: try to extract prompts from text
                prompts = self._extract_prompts_from_text(content)
                if prompts:
                    self._cached_prompts = prompts
                    self._last_fetch_time = datetime.now()
                    return prompts[:count]
            
        except Exception as e:
            print(f"Error fetching prompts from API: {e}")
            # Fallback to minimal prompts if API fails
            return self._get_fallback_prompts(count)
        
        return self._get_fallback_prompts(count)
    
    def _get_category_specific_prompt(self, category: str, count: int) -> str:
        """Get category-specific prompt for generating travel prompts"""
        category_prompts = {
            "general": f"Generate {count} diverse travel planning prompts covering various aspects like itinerary planning, destination research, budget planning, and travel tips.",
            "planning": f"Generate {count} travel planning prompts focused on itinerary creation, trip organization, and travel logistics.",
            "information": f"Generate {count} travel information prompts about destinations, weather, attractions, and cultural insights.",
            "budget": f"Generate {count} budget-focused travel prompts about cost estimation, money-saving tips, and financial planning for trips.",
            "accommodation": f"Generate {count} accommodation-related travel prompts about hotels, booking, and lodging recommendations.",
            "activities": f"Generate {count} activity-focused travel prompts about attractions, tours, and things to do at destinations."
        }
        
        return category_prompts.get(category, category_prompts["general"])
    
    def _should_use_cache(self) -> bool:
        """Check if cached prompts should be used"""
        if not self._cached_prompts or not self._last_fetch_time:
            return False
        
        time_diff = (datetime.now() - self._last_fetch_time).total_seconds()
        return time_diff < self._cache_duration
    
    def _get_cached_prompts(self, count: int) -> List[str]:
        """Get prompts from cache"""
        if len(self._cached_prompts) >= count:
            return random.sample(self._cached_prompts, count)
        return self._cached_prompts
    
    def _extract_prompts_from_text(self, text: str) -> List[str]:
        """Extract prompts from text if JSON parsing fails"""
        lines = text.split('\n')
        prompts = []
        
        for line in lines:
            line = line.strip()
            # Remove numbering, bullets, quotes
            line = line.lstrip('1234567890.- "\'')
            line = line.rstrip('"\'')
            
            if len(line) > 10 and '?' in line or 'plan' in line.lower() or 'trip' in line.lower():
                prompts.append(line)
        
        return prompts[:20]  # Limit to reasonable number
    
    def _get_fallback_prompts(self, count: int) -> List[str]:
        """Fallback prompts if API fails"""
        fallback_prompts = [
            "Plan a weekend getaway for two people with a moderate budget",
            "What are the best attractions in Paris for first-time visitors?",
            "Create a 7-day itinerary for Japan in spring",
            "Suggest budget-friendly accommodations in Barcelona",
            "What's the weather like in Thailand during monsoon season?",
            "Plan a family trip to Disney World for 5 days",
            "Recommend restaurants in Rome for food lovers",
            "Create a packing list for a winter trip to Iceland",
            "Suggest activities in New York City for art enthusiasts",
            "Plan a romantic getaway to Santorini for a couple",
            "What are the visa requirements for traveling to India?",
            "Create a budget estimate for a month-long backpacking trip in Europe"
        ]
        
        return random.sample(fallback_prompts, min(count, len(fallback_prompts)))
    
    def get_contextual_prompts(self, user_preferences: Dict[str, Any], count: int = 5) -> List[str]:
        """Generate prompts based on user preferences"""
        try:
            preferences_text = ""
            if user_preferences:
                if user_preferences.get("preferred_destinations"):
                    preferences_text += f"Interested in destinations: {user_preferences['preferred_destinations']}. "
                if user_preferences.get("budget_level"):
                    preferences_text += f"Budget level: {user_preferences['budget_level']}. "
                if user_preferences.get("travel_style"):
                    preferences_text += f"Travel style: {user_preferences['travel_style']}. "
                if user_preferences.get("interests"):
                    preferences_text += f"Interests: {', '.join(user_preferences['interests'])}. "
            
            system_prompt = f"""Generate {count} personalized travel prompts based on the user's preferences: {preferences_text}
            
            The prompts should be relevant to their interests and preferences. Return only a JSON array of strings."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create {count} travel prompts that match my preferences."}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            prompts = json.loads(content)
            
            if isinstance(prompts, list):
                return prompts[:count]
            
        except Exception as e:
            print(f"Error generating contextual prompts: {e}")
        
        return self.fetch_travel_prompts(count, "general")
    
    def refresh_cache(self):
        """Force refresh of cached prompts"""
        self._cached_prompts = []
        self._last_fetch_time = None


# Global instance
prompt_fetcher = None

def get_prompt_fetcher() -> PromptFetcher:
    """Get or create global prompt fetcher instance"""
    global prompt_fetcher
    if prompt_fetcher is None:
        prompt_fetcher = PromptFetcher()
    return prompt_fetcher

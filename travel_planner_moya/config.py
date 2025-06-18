"""
Configuration file for Travel Planner Multi-Agent System
"""

import os
from typing import Dict, List, Any

class Config:
    """Configuration settings for the travel planner system"""
      # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-openai-api-key-here")
    
    # Agent Configuration
    AGENT_SETTINGS = {
        "info_agent": {
            "name": "InfoAgent",
            "description": "Gathers travel information and destination details",
            "max_retries": 3,
            "timeout": 30
        },
        "travel_agent": {
            "name": "TravelAgent", 
            "description": "Creates travel plans and assists with booking decisions",
            "max_retries": 3,
            "timeout": 30
        }
    }
    
    # Memory Configuration
    MEMORY_SETTINGS = {
        "max_conversation_history": 50,
        "max_search_history": 20,
        "context_window": 10
    }
    
    # Classifier Keywords
    CLASSIFIER_KEYWORDS = {
        "info": [
            "weather", "climate", "temperature", "forecast",
            "attractions", "places", "things to do", "sightseeing",
            "culture", "history", "museums", "landmarks",
            "tips", "advice", "customs", "local",
            "currency", "money", "exchange", "payment",
            "information", "about", "describe", "tell me"
        ],
        "travel": [
            "itinerary", "plan", "schedule", "organize",
            "accommodation", "hotel", "stay", "lodging",
            "transport", "flight", "train", "bus", "travel",
            "budget", "cost", "price", "expense", "money",
            "pack", "packing", "luggage", "bring",
            "book", "booking", "reserve", "reservation"
        ]
    }
    
    # UI Configuration
    STREAMLIT_CONFIG = {
        "page_title": "Travel Planner AI",
        "page_icon": "✈️",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # Sample destinations for context extraction
    COMMON_DESTINATIONS = [
        "paris", "london", "tokyo", "new york", "rome", "barcelona", 
        "amsterdam", "berlin", "prague", "vienna", "budapest", "lisbon",
        "dublin", "edinburgh", "venice", "florence", "milan", "madrid",
        "athens", "istanbul", "dubai", "singapore", "hong kong", "sydney",
        "los angeles", "san francisco", "chicago", "washington dc", "boston",
        "mumbai", "delhi", "bangalore", "bangkok", "seoul", "beijing"
    ]
    
    # Budget levels
    BUDGET_LEVELS = {
        "budget": {
            "accommodation": 40,
            "food": 25, 
            "activities": 15,
            "transport": 10
        },
        "medium": {
            "accommodation": 80,
            "food": 45,
            "activities": 30, 
            "transport": 20
        },
        "luxury": {
            "accommodation": 150,
            "food": 80,
            "activities": 60,
            "transport": 40
        }
    }
      # Dynamic prompt configuration
    PROMPT_CONFIG = {
        "enabled": True,
        "cache_duration": 300,  # 5 minutes
        "default_count": 8,
        "categories": ["general", "planning", "information", "budget", "accommodation", "activities"],
        "fallback_enabled": True
    }
    
    @classmethod
    def get_agent_config(cls, agent_name: str) -> Dict[str, Any]:
        """Get configuration for a specific agent"""
        return cls.AGENT_SETTINGS.get(agent_name, {})
    
    @classmethod
    def get_budget_config(cls, budget_level: str) -> Dict[str, int]:
        """Get budget configuration for a specific level"""
        return cls.BUDGET_LEVELS.get(budget_level, cls.BUDGET_LEVELS["medium"])

    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "sk-your-openai-api-key-here":
            print("⚠️  Warning: OPENAI_API_KEY not properly configured")
            return False
        
        required_agents = ["info_agent", "travel_agent"]
        for agent in required_agents:
            if agent not in cls.AGENT_SETTINGS:
                print(f"⚠️  Warning: Missing configuration for {agent}")
                return False
        
        return True

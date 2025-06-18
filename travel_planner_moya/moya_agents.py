"""
Travel Planner Multi-Agent System
Implements OpenAI agents for travel planning without MOYA framework dependency
"""

import os
import openai
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Import our custom tools
from tools.travel_tools import (
    get_destination_info,
    get_weather_info,
    search_attractions,
    get_travel_tips,
    get_currency_info,
    create_itinerary,
    suggest_accommodations,
    estimate_budget,
    generate_packing_list
)

class TravelPlannerSystem:
    """Travel Planner System using OpenAI directly"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Simple conversation memory
        self.conversation_history = {}
        
        # Agent configurations
        self.info_agent_config = {
            "name": "InfoAgent",
            "system_prompt": """You are an expert travel information agent specialized in providing comprehensive destination details, weather information, and cultural insights.

Your capabilities include:
- Providing detailed destination information and cultural context
- Fetching current weather conditions and forecasts
- Finding attractions, activities, and points of interest
- Offering practical travel tips and local customs advice
- Providing currency and payment information

When responding:
1. Be informative and detailed while remaining concise
2. Provide practical, actionable advice
3. Focus on safety and cultural sensitivity
4. Format responses clearly with proper structure

Always provide helpful, accurate, and up-to-date travel information."""
        }
        
        self.travel_agent_config = {
            "name": "TravelAgent", 
            "system_prompt": """You are an expert travel planning agent specialized in creating detailed itineraries, suggesting accommodations, and providing comprehensive travel plans.

Your capabilities include:
- Creating detailed day-by-day itineraries
- Suggesting accommodations based on preferences and budget
- Estimating travel budgets and costs
- Generating personalized packing lists
- Planning transportation and logistics

When responding:
1. Create structured, easy-to-follow itineraries
2. Consider budget constraints and preferences
3. Provide realistic time estimates and logistics
4. Include practical tips and recommendations

Always create practical, well-organized travel plans."""
        }
    
    def _classify_request(self, message: str) -> str:
        """Simple keyword-based classification of user requests"""
        message_lower = message.lower()
        
        # Keywords for info agent
        info_keywords = [
            "weather", "climate", "temperature", "forecast",
            "attractions", "places", "things to do", "sightseeing",
            "culture", "history", "museums", "landmarks",
            "tips", "advice", "customs", "local",
            "currency", "money", "exchange", "payment",
            "information", "about", "describe", "tell me",
            "what", "where", "when", "how"
        ]
        
        # Keywords for travel agent
        travel_keywords = [
            "itinerary", "plan", "schedule", "organize",
            "accommodation", "hotel", "stay", "lodging",
            "transport", "flight", "train", "bus", "travel",
            "budget", "cost", "price", "expense", "estimate",
            "pack", "packing", "luggage", "bring",
            "book", "booking", "reserve", "reservation",
            "create", "suggest", "recommend"
        ]
        
        info_score = sum(1 for keyword in info_keywords if keyword in message_lower)
        travel_score = sum(1 for keyword in travel_keywords if keyword in message_lower)
        
        # If scores are equal or low, default to travel agent for planning
        if travel_score > info_score:
            return "travel_agent"
        elif info_score > travel_score:
            return "info_agent"
        else:
            return "travel_agent"  # Default to travel planning
    
    def handle_message(self, message: str, user_id: str = "default") -> str:
        """Handle user message and route to appropriate agent"""
        try:
            # Store user message
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            self.conversation_history[user_id].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Classify the request
            agent_type = self._classify_request(message)
            
            # Get appropriate agent config
            if agent_type == "info_agent":
                config = self.info_agent_config
            else:
                config = self.travel_agent_config
            
            # Prepare conversation context
            recent_history = self.conversation_history[user_id][-10:]  # Last 10 messages
            messages = [
                {"role": "system", "content": config["system_prompt"]}
            ]
            
            # Add recent conversation history
            for entry in recent_history:
                if entry["role"] in ["user", "assistant"]:
                    messages.append({
                        "role": entry["role"],
                        "content": entry["content"]
                    })
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using more cost-effective model
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Store assistant response
            self.conversation_history[user_id].append({
                "role": "assistant", 
                "content": assistant_response,
                "timestamp": datetime.now().isoformat(),
                "agent": config["name"]
            })
            
            return assistant_response
            
        except Exception as e:
            error_msg = f"I encountered an error while processing your request: {str(e)}"
            if user_id in self.conversation_history:
                self.conversation_history[user_id].append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().isoformat(),
                    "agent": "System"
                })
            return error_msg
    
    def get_conversation_history(self, user_id: str = "default", limit: int = 10) -> List[Dict]:
        """Get conversation history for user"""
        if user_id not in self.conversation_history:
            return []
        return self.conversation_history[user_id][-limit:]
    
    def clear_conversation(self, user_id: str = "default"):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
    
    def get_available_capabilities(self) -> Dict[str, List[str]]:
        """Get available agent capabilities"""
        return {
            "InfoAgent": [
                "Get destination information and cultural context",
                "Check weather conditions and forecasts", 
                "Find attractions, activities, and points of interest",
                "Provide travel tips and local customs advice",
                "Currency and payment information"
            ],
            "TravelAgent": [
                "Create detailed day-by-day itineraries",
                "Suggest accommodations based on preferences",
                "Estimate travel budgets and costs",
                "Generate personalized packing lists", 
                "Plan transportation and logistics"
            ]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        total_conversations = len(self.conversation_history)
        total_messages = sum(len(history) for history in self.conversation_history.values())
        
        return {
            "agents_registered": 2,  # InfoAgent and TravelAgent
            "tools_available": 9,    # Number of travel tools
            "memory_enabled": True,
            "api_configured": bool(self.api_key),
            "total_conversations": total_conversations,
            "total_messages": total_messages
        }

# Global instance for the application
travel_system = None

def get_travel_system() -> TravelPlannerSystem:
    """Get or create global travel system instance"""
    global travel_system
    if travel_system is None:
        travel_system = TravelPlannerSystem()
    return travel_system

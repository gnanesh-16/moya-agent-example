"""
Travel Planner Orchestrator
Coordinates between InfoAgent and TravelAgent using MOYA framework patterns
"""

import os
import re
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

from agents.info_agent import info_agent
from agents.travel_agent import travel_agent
from tools.memory import travel_memory


class TravelPlannerOrchestrator:
    """Main orchestrator for the travel planning multi-agent system"""
    
    def __init__(self):
        self.memory = travel_memory
        self.agents = {
            "info_agent": info_agent,
            "travel_agent": travel_agent
        }
        
        # Setup classifier
        self.setup_classifier()
        
    def setup_classifier(self):
        """Setup the keyword classifier for routing requests"""
        self.classifier_keywords = {
            "info_agent": [
                "weather", "climate", "temperature", "forecast",
                "attractions", "places", "things to do", "sightseeing",
                "culture", "history", "museums", "landmarks",
                "tips", "advice", "customs", "local",
                "currency", "money", "exchange", "payment",
                "information", "about", "describe", "tell me",
                "what", "where", "when", "how"
            ],
            "travel_agent": [
                "itinerary", "plan", "schedule", "organize",
                "accommodation", "hotel", "stay", "lodging",
                "transport", "flight", "train", "bus", "travel",
                "budget", "cost", "price", "expense", "estimate",
                "pack", "packing", "luggage", "bring",
                "book", "booking", "reserve", "reservation",
                "create", "suggest", "recommend"
            ]
        }
    
    def classify_request(self, request: str) -> str:
        """Classify user request to determine which agent should handle it"""
        request_lower = request.lower()
        
        info_score = 0
        travel_score = 0
        
        # Count keyword matches
        for keyword in self.classifier_keywords["info_agent"]:
            if keyword in request_lower:
                info_score += 1
        
        for keyword in self.classifier_keywords["travel_agent"]:
            if keyword in request_lower:
                travel_score += 1
        
        # Determine best agent
        if travel_score > info_score:
            return "travel_agent"
        else:
            return "info_agent"
    
    def extract_context(self, request: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Extract context from request and conversation history"""
        context = {}
        
        # Extract basic information from request
        request_lower = request.lower()
        
        # Look for destinations
        common_destinations = [
            "paris", "london", "tokyo", "new york", "rome", "barcelona", 
            "amsterdam", "berlin", "prague", "vienna", "budapest", "lisbon",
            "dublin", "edinburgh", "venice", "florence", "milan", "madrid",
            "athens", "istanbul", "dubai", "singapore", "hong kong", "sydney",
            "los angeles", "san francisco", "chicago", "washington dc", "boston",
            "mumbai", "delhi", "bangalore", "bangkok", "seoul", "beijing"
        ]
        
        for destination in common_destinations:
            if destination in request_lower:
                context["destination"] = destination.title()
                break
        
        # Look for dates (simplified pattern matching)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}',
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2}'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, request_lower)
            if dates:
                context["travel_date"] = dates[0]
                break
        
        # Look for duration
        duration_patterns = [
            r'(\d+)\s+days?',
            r'(\d+)\s+weeks?',
            r'(\d+)\s+months?'
        ]
        
        for pattern in duration_patterns:
            duration = re.findall(pattern, request_lower)
            if duration:
                context["duration"] = int(duration[0])
                break
        
        # Look for budget indicators
        budget_keywords = {
            "budget": ["budget", "cheap", "affordable", "low cost"],
            "medium": ["moderate", "mid-range", "reasonable"],
            "luxury": ["luxury", "premium", "high-end", "expensive"]
        }
        
        for budget_level, keywords in budget_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                context["budget_level"] = budget_level
                break
        
        # Look for number of travelers
        traveler_patterns = [
            r'(\d+)\s+people',
            r'(\d+)\s+travelers?',
            r'(\d+)\s+persons?',
            r'group\s+of\s+(\d+)'
        ]
        
        for pattern in traveler_patterns:
            travelers = re.findall(pattern, request_lower)
            if travelers:
                context["travelers"] = int(travelers[0])
                break
        
        # Add memory context
        if self.memory.travel_context:
            context.update(self.memory.travel_context)
        
        # Add user preferences
        if self.memory.user_preferences:
            context.update(self.memory.user_preferences)
        
        return context
    
    def process_request(self, user_request: str, user_id: str = "default") -> Dict[str, Any]:
        """Main method to process user requests"""
        try:
            # Log conversation
            self.memory.add_conversation("user", user_request)
            
            # Extract context
            context = self.extract_context(user_request)
            
            # Classify request to determine agent
            agent_choice = self.classify_request(user_request)
            
            # Route to appropriate agent
            response = self.agents[agent_choice].process_request(user_request, context)
            
            # Prepare result
            result = {
                "user_request": user_request,
                "agent_used": agent_choice,
                "extracted_context": context,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "conversation_context": self.memory.get_conversation_context(5)
            }
            
            return result
            
        except Exception as e:
            # Fallback error handling
            result = {
                "user_request": user_request,
                "agent_used": "error",
                "extracted_context": {},
                "response": f"I encountered an error while processing your request: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            
            return result
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation and current context"""
        return {
            "conversation_history": self.memory.conversation_history[-10:],
            "user_preferences": self.memory.user_preferences,
            "travel_context": self.memory.travel_context,
            "total_interactions": len(self.memory.conversation_history)
        }
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences in memory"""
        self.memory.update_user_preferences(preferences)
    
    def clear_session(self):
        """Clear the current session"""
        self.memory.clear_context()
    
    def get_available_capabilities(self) -> Dict[str, List[str]]:
        """Get list of available capabilities"""
        return {
            "InfoAgent": [
                "Get destination information",
                "Check weather conditions",
                "Find attractions and activities",
                "Provide travel tips and advice",
                "Currency and payment information"
            ],
            "TravelAgent": [
                "Create detailed itineraries",
                "Suggest accommodations",
                "Plan transportation",
                "Estimate travel budgets",
                "Generate packing lists"
            ]
        }
    
    def handle_multi_agent_workflow(self, request: str) -> Dict[str, Any]:
        """Handle complex requests that might need multiple agents"""
        try:
            # For complex travel planning, we might need both agents
            if any(word in request.lower() for word in ["complete", "full", "everything", "comprehensive"]):
                context = self.extract_context(request)
                
                # First get destination info
                info_response = self.agents["info_agent"].process_request(
                    f"Tell me about {context.get('destination', 'the destination')} including weather, attractions, and travel tips",
                    context
                )
                
                # Then create travel plan
                travel_response = self.agents["travel_agent"].process_request(
                    f"Create a complete travel plan for {context.get('destination', 'the destination')} including itinerary, accommodations, and budget",
                    context
                )
                
                combined_response = {
                    "type": "multi_agent_response",
                    "destination_info": info_response,
                    "travel_plan": travel_response,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
                
                return combined_response
            
            # For single requests, use normal processing
            return self.process_request(request)
            
        except Exception as e:
            # Fallback to single agent processing
            return self.process_request(request)


# Create global orchestrator instance
travel_orchestrator = TravelPlannerOrchestrator()

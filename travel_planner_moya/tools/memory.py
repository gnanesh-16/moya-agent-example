"""
Memory Tool for Travel Planner Multi-Agent System
Handles conversation context, user preferences, and travel history
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class TravelMemory:
    """Memory system for maintaining travel planning context and preferences"""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.travel_context: Dict[str, Any] = {}
        self.search_history: List[Dict[str, Any]] = []
        
    def add_conversation(self, role: str, message: str, agent: Optional[str] = None):
        """Add a conversation entry to memory"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "message": message,
            "agent": agent
        }
        self.conversation_history.append(entry)
        
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user travel preferences"""
        self.user_preferences.update(preferences)
        
    def set_travel_context(self, context: Dict[str, Any]):
        """Set current travel planning context"""
        self.travel_context.update(context)
        
    def add_search_result(self, query: str, results: Any, agent: str):
        """Store search results for reference"""
        search_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results": results,
            "agent": agent
        }
        self.search_history.append(search_entry)
        
    def get_conversation_context(self, last_n: int = 10) -> str:
        """Get recent conversation context as string"""
        recent = self.conversation_history[-last_n:] if len(self.conversation_history) > last_n else self.conversation_history
        context = "Recent conversation:\n"
        for entry in recent:
            agent_info = f" ({entry['agent']})" if entry['agent'] else ""
            context += f"{entry['role']}{agent_info}: {entry['message']}\n"
        return context
        
    def get_user_preferences_context(self) -> str:
        """Get user preferences as context string"""
        if not self.user_preferences:
            return "No user preferences stored yet."
        
        context = "User preferences:\n"
        for key, value in self.user_preferences.items():
            context += f"- {key}: {value}\n"
        return context
        
    def get_travel_context(self) -> str:
        """Get current travel context as string"""
        if not self.travel_context:
            return "No current travel planning context."
            
        context = "Current travel planning context:\n"
        for key, value in self.travel_context.items():
            context += f"- {key}: {value}\n"
        return context
        
    def clear_context(self):
        """Clear all memory contexts"""
        self.conversation_history.clear()
        self.user_preferences.clear()
        self.travel_context.clear()
        self.search_history.clear()
        
    def export_memory(self) -> Dict[str, Any]:
        """Export memory state as dictionary"""
        return {
            "conversation_history": self.conversation_history,
            "user_preferences": self.user_preferences,
            "travel_context": self.travel_context,
            "search_history": self.search_history
        }
        
    def import_memory(self, memory_data: Dict[str, Any]):
        """Import memory state from dictionary"""
        self.conversation_history = memory_data.get("conversation_history", [])
        self.user_preferences = memory_data.get("user_preferences", {})
        self.travel_context = memory_data.get("travel_context", {})
        self.search_history = memory_data.get("search_history", [])


# Global memory instance
travel_memory = TravelMemory()

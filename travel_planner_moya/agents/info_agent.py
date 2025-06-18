"""
Info Agent - Responsible for gathering travel information, weather data, and destination details
Uses MOYA framework components for agent functionality
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Import travel tools
from tools.travel_tools import (
    get_destination_info,
    get_weather_info,
    search_attractions,
    get_travel_tips,
    get_currency_info
)
from tools.memory import travel_memory


class InfoAgent:
    """Agent specialized in gathering travel information and destination details"""
    
    def __init__(self):
        self.name = "InfoAgent"
        self.description = "Gathers travel information, weather data, and destination details"
        self.memory = travel_memory
        self.tools = self.setup_tools()
        
    def setup_tools(self):
        """Setup available tools for the info agent"""
        return {
            "get_destination_info": get_destination_info,
            "get_weather_info": get_weather_info,
            "search_attractions": search_attractions,
            "get_travel_tips": get_travel_tips,
            "get_currency_info": get_currency_info
        }
    
    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a travel information request"""
        self.memory.add_conversation("user", request, "InfoAgent")
        
        # Simple keyword-based routing
        request_lower = request.lower()
        context = context or {}
        
        try:
            if "weather" in request_lower:
                destination = context.get("destination", "Unknown")
                travel_date = context.get("travel_date")
                result = self.tools["get_weather_info"](destination, travel_date)
                
                # Store in memory
                self.memory.add_search_result(
                    query=f"weather_{destination}_{travel_date}",
                    results=result,
                    agent="InfoAgent"
                )
                
                response = f"🌤️ Weather information for {destination}:\n\n"
                if "error" not in result:
                    response += f"📅 Date: {result['date']}\n"
                    response += f"🌡️ Temperature: {result['current_temperature']} (Range: {result['temperature_range']})\n"
                    response += f"☁️ Conditions: {result['conditions']}\n"
                    response += f"💧 Humidity: {result['humidity']}\n"
                    response += f"🌧️ Precipitation: {result['precipitation']}\n"
                    response += f"💨 Wind: {result['wind']}\n"
                    response += f"☀️ UV Index: {result['uv_index']}\n\n"
                    response += "📋 Recommendations:\n"
                    for rec in result['recommendations']:
                        response += f"• {rec}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            elif "attractions" in request_lower or "things to do" in request_lower:
                destination = context.get("destination", "Unknown")
                interests = context.get("interests", [])
                result = self.tools["search_attractions"](destination, interests)
                
                self.memory.add_search_result(
                    query=f"attractions_{destination}",
                    results=result,
                    agent="InfoAgent"
                )
                
                response = f"🎯 Attractions in {destination}:\n\n"
                if "error" not in result:
                    response += f"Found {result['total_found']} attractions"
                    if interests:
                        response += f" matching your interests: {', '.join(interests)}"
                    response += "\n\n"
                    
                    for i, attraction in enumerate(result['attractions'][:5], 1):  # Show top 5
                        response += f"{i}. **{attraction['name']}** ({attraction['type']})\n"
                        response += f"   ⭐ Rating: {attraction['rating']}/5\n"
                        response += f"   📝 {attraction['description']}\n"
                        response += f"   ⏱️ Duration: {attraction['estimated_time']}\n"
                        response += f"   💰 Cost: {attraction['cost']}\n"
                        response += f"   📍 {attraction.get('address', 'Location varies')}\n\n"
                    
                    response += "💡 Planning Tips:\n"
                    for tip in result.get('planning_tips', []):
                        response += f"• {tip}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            elif "tips" in request_lower or "advice" in request_lower:
                destination = context.get("destination", "Unknown")
                result = self.tools["get_travel_tips"](destination)
                
                self.memory.add_search_result(
                    query=f"travel_tips_{destination}",
                    results=result,
                    agent="InfoAgent"
                )
                
                response = f"💡 Travel Tips for {destination}:\n\n"
                if "error" not in result:
                    sections = [
                        ("🏛️ Cultural Tips", result['cultural_tips']),
                        ("🛡️ Safety Tips", result['safety_tips']),
                        ("💰 Money Tips", result['money_tips']),
                        ("🎒 Practical Tips", result['practical_tips'])
                    ]
                    
                    for section_title, tips in sections:
                        response += f"{section_title}:\n"
                        for tip in tips:
                            response += f"• {tip}\n"
                        response += "\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            elif "currency" in request_lower or "money" in request_lower:
                country = context.get("destination", "Unknown")
                result = self.tools["get_currency_info"](country)
                
                self.memory.add_search_result(
                    query=f"currency_{country}",
                    results=result,
                    agent="InfoAgent"
                )
                
                response = f"💱 Currency Information for {country}:\n\n"
                if "error" not in result:
                    response += f"💰 Currency: {result['currency_name']} ({result['currency_code']})\n"
                    response += f"💱 Exchange Rate: {result['exchange_rate']}\n"
                    response += f"📅 Last Updated: {result['last_updated']}\n\n"
                    
                    response += "💳 Payment Methods:\n"
                    for method, info in result['payment_methods'].items():
                        response += f"• {method.replace('_', ' ').title()}: {info}\n"
                    
                    response += "\n🏧 ATM Information:\n"
                    for key, info in result['atm_availability'].items():
                        response += f"• {key.replace('_', ' ').title()}: {info}\n"
                    
                    response += "\n💸 Tipping Culture:\n"
                    for service, tip in result['tipping_culture'].items():
                        response += f"• {service.replace('_', ' ').title()}: {tip}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            else:
                destination = context.get("destination", "Unknown")
                result = self.tools["get_destination_info"](destination)
                
                self.memory.add_search_result(
                    query=f"destination_info_{destination}",
                    results=result,
                    agent="InfoAgent"
                )
                
                response = f"📍 Information about {destination}:\n\n"
                if "error" not in result:
                    response += f"📝 Description: {result['description']}\n\n"
                    response += f"🌅 Best Time to Visit: {result['best_time_to_visit']}\n"
                    response += f"🗣️ Language: {result['local_language']}\n"
                    response += f"🕐 Timezone: {result['time_zone']}\n"
                    response += f"📋 Visa Requirements: {result['visa_requirements']}\n"
                    response += f"🆘 Emergency Contacts: {result['emergency_contacts']}\n"
                    response += f"💰 Currency: {result['currency']}\n"
                    response += f"🌡️ Climate: {result['climate']}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
            
            self.memory.add_conversation("assistant", response, "InfoAgent")
            return response
            
        except Exception as e:
            error_response = f"I encountered an error while processing your request: {str(e)}"
            self.memory.add_conversation("assistant", error_response, "InfoAgent")
            return error_response


# Create global instance
info_agent = InfoAgent()

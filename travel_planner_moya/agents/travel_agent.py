"""
Travel Agent - Responsible for travel planning, itinerary creation, and booking assistance
Uses MOYA framework components for agent functionality
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Import travel tools
from tools.travel_tools import (
    create_itinerary,
    suggest_accommodations,
    estimate_budget,
    generate_packing_list
)
from tools.memory import travel_memory


class TravelAgent:
    """Agent specialized in travel planning, itinerary creation, and booking assistance"""
    
    def __init__(self):
        self.name = "TravelAgent"
        self.description = "Creates travel plans, itineraries, and assists with booking decisions"
        self.memory = travel_memory
        self.tools = self.setup_tools()
        
    def setup_tools(self):
        """Setup available tools for the travel agent"""
        return {
            "create_itinerary": create_itinerary,
            "suggest_accommodations": suggest_accommodations,
            "estimate_budget": estimate_budget,
            "generate_packing_list": generate_packing_list
        }
    
    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a travel planning request"""
        self.memory.add_conversation("user", request, "TravelAgent")
        
        request_lower = request.lower()
        context = context or {}
        
        try:
            if "itinerary" in request_lower or "plan" in request_lower:
                travel_details = {
                    "destination": context.get("destination", "Unknown"),
                    "duration": context.get("duration", 3),
                    "start_date": context.get("travel_date", datetime.now().strftime("%Y-%m-%d")),
                    "interests": context.get("interests", []),
                    "budget_level": context.get("budget_level", "medium"),
                    "travelers": context.get("travelers", 2)
                }
                
                result = self.tools["create_itinerary"](travel_details)
                
                # Store in memory
                self.memory.add_search_result(
                    query=f"itinerary_{travel_details['destination']}_{travel_details['start_date']}",
                    results=result,
                    agent="TravelAgent"
                )
                
                response = f"✈️ Travel Itinerary for {travel_details['destination']}:\n\n"
                if "error" not in result:
                    response += f"📅 Duration: {result['duration']}\n"
                    response += f"👥 Travelers: {result['travelers']}\n"
                    response += f"💰 Budget Level: {result['budget_level']}\n"
                    response += f"🎯 Interests: {', '.join(result.get('interests', ['General']))}\n\n"
                    
                    for day_plan in result['daily_plans']:
                        response += f"📅 **Day {day_plan['day']} - {day_plan['date']}**\n"
                        response += f"🎭 Theme: {day_plan['theme']}\n\n"
                        
                        for activity in day_plan['activities']:
                            response += f"  ⏰ {activity['time']} - {activity['activity']}\n"
                            response += f"      ⏱️ Duration: {activity['duration']} | 💰 Cost: {activity['cost']}\n"
                        
                        response += f"\n  📊 Daily Budget: {day_plan['estimated_daily_cost']}\n"
                        response += "  💡 Tips:\n"
                        for tip in day_plan['travel_tips']:
                            response += f"    • {tip}\n"
                        response += "\n"
                    
                    response += f"📈 **Trip Summary:**\n"
                    response += f"• Total Activities: {result['summary']['total_activities']}\n"
                    response += f"• Estimated Cost: {result['summary']['estimated_cost']}\n"
                    response += f"• Top Highlights: {', '.join(result['summary']['highlights'])}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            elif "accommodation" in request_lower or "hotel" in request_lower:
                travel_details = {
                    "destination": context.get("destination", "Unknown"),
                    "budget_level": context.get("budget_level", "medium"),
                    "travelers": context.get("travelers", 2),
                    "duration": context.get("duration", 3)
                }
                
                result = self.tools["suggest_accommodations"](travel_details)
                
                self.memory.add_search_result(
                    query=f"accommodations_{travel_details['destination']}",
                    results=result,
                    agent="TravelAgent"
                )
                
                response = f"🏨 Accommodation Suggestions for {travel_details['destination']}:\n\n"
                if "error" not in result:
                    for i, option in enumerate(result['options'], 1):
                        response += f"{i}. **{option['name']}** ({option['type']})\n"
                        response += f"   ⭐ Rating: {option['rating']}/5 ({option['category']})\n"
                        response += f"   💰 Price: {option['price_per_night']} per night\n"
                        response += f"   💳 Total Cost: {option['total_cost']} for {travel_details['duration']} nights\n"
                        response += f"   📍 Location: {option['location']}\n"
                        response += f"   🚶 Distance to Center: {option['distance_to_center']}\n"
                        response += f"   🚇 Transport: {option['transport_access']}\n"
                        response += f"   🎯 Amenities: {', '.join(option['amenities'])}\n"
                        response += f"   💬 Guest Rating: {option['guest_rating']}\n"
                        response += f"   ✅ Pros: {', '.join(option['pros'])}\n"
                        response += f"   ⚠️ Cons: {', '.join(option['cons'])}\n\n"
                    
                    response += "💡 **Booking Tips:**\n"
                    for tip in result['booking_recommendations']:
                        response += f"• {tip}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            elif "budget" in request_lower or "cost" in request_lower:
                travel_details = {
                    "destination": context.get("destination", "Unknown"),
                    "duration": context.get("duration", 3),
                    "travelers": context.get("travelers", 1),
                    "budget_level": context.get("budget_level", "medium")
                }
                
                result = self.tools["estimate_budget"](travel_details)
                
                self.memory.add_search_result(
                    query=f"budget_{travel_details['destination']}_{travel_details['duration']}days",
                    results=result,
                    agent="TravelAgent"
                )
                
                response = f"💰 Budget Estimate for {travel_details['destination']}:\n\n"
                if "error" not in result:
                    response += f"📅 Duration: {result['duration']}\n"
                    response += f"👥 Travelers: {result['travelers']}\n"
                    response += f"💎 Budget Level: {result['budget_level']}\n\n"
                    
                    response += "📊 **Daily Breakdown:**\n"
                    for category, details in result['detailed_breakdown']['daily_costs'].items():
                        response += f"• {category.replace('_', ' ').title()}: {details['amount']} per day → {details['total']} total\n"
                        response += f"  └─ {details['description']}\n"
                    
                    response += "\n💸 **One-time Costs:**\n"
                    for category, cost in result['detailed_breakdown']['one_time_costs'].items():
                        response += f"• {category.replace('_', ' ').title()}: {cost}\n"
                    
                    response += f"\n📈 **Total Summary:**\n"
                    response += f"• Daily Average: {result['totals']['daily_average']}\n"
                    response += f"• Trip Total (before flights): {result['totals']['trip_total_before_flights']}\n"
                    response += f"• Flights & Fees: {result['totals']['flights_and_fees']}\n"
                    response += f"• **Grand Total per Person: {result['totals']['grand_total_per_person']}**\n"
                    response += f"• **Grand Total for Group: {result['totals']['grand_total_for_group']}**\n"
                    
                    response += f"\n🚨 **Emergency Fund:** {result['emergency_fund']['recommended']}\n"
                    response += f"({result['emergency_fund']['description']})\n"
                    
                    response += "\n💡 **Money-Saving Tips:**\n"
                    for tip in result['budget_tips']['save_money']:
                        response += f"• {tip}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            elif "pack" in request_lower:
                travel_details = {
                    "destination": context.get("destination", "Unknown"),
                    "duration": context.get("duration", 3),
                    "season": "spring",  # Default season, could be extracted from context
                    "planned_activities": context.get("interests", []),
                    "budget_level": context.get("budget_level", "medium")
                }
                
                result = self.tools["generate_packing_list"](travel_details)
                
                self.memory.add_search_result(
                    query=f"packing_list_{travel_details['destination']}_{travel_details['season']}",
                    results=result,
                    agent="TravelAgent"
                )
                
                response = f"🎒 Packing List for {travel_details['destination']}:\n\n"
                if "error" not in result:
                    response += f"📅 Duration: {result['duration']}\n"
                    response += f"🌤️ Season: {result['season']}\n"
                    response += f"🎯 Activities: {', '.join(result.get('activities', ['General travel']))}\n\n"
                    
                    # Essentials
                    response += "📋 **Essential Documents:**\n"
                    for doc in result['categories']['essentials']['documents']:
                        response += f"• {doc}\n"
                    
                    response += "\n💳 **Money & Cards:**\n"
                    for item in result['categories']['essentials']['money_and_cards']:
                        response += f"• {item}\n"
                    
                    # Clothing
                    response += "\n👔 **Clothing Basics:**\n"
                    for item in result['categories']['clothing']['basics']:
                        response += f"• {item}\n"
                    
                    if result['categories']['clothing']['weather_specific']:
                        response += f"\n🌦️ **Weather-Specific ({result['season']}):**\n"
                        for item in result['categories']['clothing']['weather_specific']:
                            response += f"• {item}\n"
                    
                    if result['categories']['clothing']['activity_specific']:
                        response += "\n🎯 **Activity-Specific:**\n"
                        for item in result['categories']['clothing']['activity_specific']:
                            response += f"• {item}\n"
                    
                    # Other categories
                    categories = [
                        ("🧴 Health & Hygiene", result['categories']['health_and_hygiene']),
                        ("🔌 Electronics", result['categories']['electronics']),
                        ("🎒 Comfort & Convenience", result['categories']['comfort_and_convenience'])
                    ]
                    
                    for cat_title, items in categories:
                        response += f"\n{cat_title}:\n"
                        for item in items:
                            response += f"• {item}\n"
                    
                    response += "\n💡 **Packing Tips:**\n"
                    for tip in result['packing_tips']:
                        response += f"• {tip}\n"
                else:
                    response += result.get('error', 'Unknown error occurred')
                
            else:
                response = "I can help you with travel planning! 🎯\n\n"
                response += "Here's what I can do for you:\n"
                response += "✈️ **Create detailed itineraries** - Just ask me to plan your trip!\n"
                response += "🏨 **Suggest accommodations** - I'll find places to stay within your budget\n"
                response += "💰 **Estimate budgets** - Get detailed cost breakdowns for your trip\n"
                response += "🎒 **Generate packing lists** - Never forget essentials again\n\n"
                response += "Try asking me something like:\n"
                response += '• "Create an itinerary for Paris"\n'
                response += '• "Suggest hotels in Tokyo"\n'
                response += '• "Estimate budget for a week in Rome"\n'
                response += '• "Generate packing list for winter travel"\n'
            
            self.memory.add_conversation("assistant", response, "TravelAgent")
            return response
            
        except Exception as e:
            error_response = f"I encountered an error while processing your travel planning request: {str(e)}"
            self.memory.add_conversation("assistant", error_response, "TravelAgent")
            return error_response


# Create global instance
travel_agent = TravelAgent()

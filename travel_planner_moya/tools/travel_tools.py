"""
Travel Tools for MOYA Framework
Collection of tools for travel information and planning
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json


def get_destination_info(destination: str) -> Dict[str, Any]:
    """Get general information about a destination"""
    try:
        # Simulate API call for destination info
        # In real implementation, this would call actual travel APIs
        info = {
            "destination": destination,
            "description": f"A wonderful destination with rich culture and history. {destination} offers visitors a unique blend of traditional and modern experiences.",
            "best_time_to_visit": "Spring and Fall are ideal for pleasant weather and fewer crowds",
            "local_language": "Local language varies by region",
            "time_zone": "Local timezone information",
            "visa_requirements": "Check visa requirements based on your nationality - most countries require valid passport",
            "emergency_contacts": "Emergency: 911 (or local equivalent), Tourist Police available",
            "currency": "Local currency accepted, major credit cards widely accepted",
            "climate": "Temperate climate with seasonal variations"
        }
        
        return info
    except Exception as e:
        return {"error": f"Failed to get destination info: {str(e)}"}


def get_weather_info(destination: str, travel_date: Optional[str] = None) -> Dict[str, Any]:
    """Get weather information for destination"""
    try:
        # Simulate weather API call
        # In real implementation, use OpenWeatherMap or similar API

        # EXAMPLE PROMPT AND ITS EXPECTED OUTPUT RESPONSE  
        weather_info = {
            "destination": destination,
            "date": travel_date or datetime.now().strftime("%Y-%m-%d"),
            "current_temperature": "22°C (72°F)", 
            "temperature_range": "18-26°C (64-79°F)",
            "conditions": "Partly cloudy with occasional sunshine",
            "humidity": "65%",
            "precipitation": "20% chance of light rain",
            "wind": "Light breeze 10-15 km/h",
            "uv_index": "Moderate (5/10)",
            "recommendations": [
                "Pack light layers for temperature changes",
                "Bring a light rain jacket or umbrella",
                "Sunscreen recommended for outdoor activities",
                "Comfortable walking shoes are essential"
            ],
            "7_day_forecast": [
                {"day": "Today", "high": "26°C", "low": "18°C", "condition": "Partly cloudy"},
                {"day": "Tomorrow", "high": "24°C", "low": "17°C", "condition": "Sunny"},
                {"day": "Day 3", "high": "25°C", "low": "19°C", "condition": "Light rain"},
                {"day": "Day 4", "high": "23°C", "low": "16°C", "condition": "Cloudy"},
                {"day": "Day 5", "high": "27°C", "low": "20°C", "condition": "Sunny"},
                {"day": "Day 6", "high": "25°C", "low": "18°C", "condition": "Partly cloudy"},
                {"day": "Day 7", "high": "24°C", "low": "17°C", "condition": "Sunny"}
            ]
        }
        
        return weather_info
    except Exception as e:
        return {"error": f"Failed to get weather info: {str(e)}"}


def search_attractions(destination: str, interests: Optional[List[str]] = None) -> Dict[str, Any]:
    """Search for attractions based on destination and interests"""
    try:
        # Sample attractions database
        all_attractions = [
            {
                "name": "Historic City Center",
                "type": "Historical",
                "category": "history",
                "rating": 4.5,
                "description": "Beautiful historic architecture and cultural sites dating back centuries",
                "estimated_time": "2-3 hours",
                "cost": "Free",
                "opening_hours": "24/7 (outdoor)",
                "address": "City Center District",
                "highlights": ["Ancient architecture", "Walking tours", "Photo opportunities"]
            },
            {
                "name": "National Art Museum",
                "type": "Cultural",
                "category": "art",
                "rating": 4.3,
                "description": "Extensive collection of local and international art spanning multiple centuries",
                "estimated_time": "2-3 hours",
                "cost": "$15-25 per person",
                "opening_hours": "9:00 AM - 6:00 PM (Closed Mondays)",
                "address": "Museum District",
                "highlights": ["Classical paintings", "Modern art", "Sculpture garden"]
            },
            {
                "name": "Scenic Viewpoint",
                "type": "Nature",
                "category": "nature",
                "rating": 4.7,
                "description": "Panoramic views of the city and surrounding landscape, perfect for sunrise/sunset",
                "estimated_time": "1-2 hours",
                "cost": "Free",
                "opening_hours": "5:00 AM - 10:00 PM",
                "address": "Hill District",
                "highlights": ["City panorama", "Sunset views", "Photography"]
            },
            {
                "name": "Central Food Market",
                "type": "Culinary",
                "category": "food",
                "rating": 4.4,
                "description": "Bustling local market with authentic street food and local delicacies",
                "estimated_time": "1-2 hours",
                "cost": "$10-30 per meal",
                "opening_hours": "7:00 AM - 9:00 PM",
                "address": "Market Square",
                "highlights": ["Local cuisine", "Fresh ingredients", "Cultural experience"]
            },
            {
                "name": "Adventure Park",
                "type": "Recreation",
                "category": "adventure",
                "rating": 4.2,
                "description": "Outdoor adventure activities including hiking trails and zip-lining",
                "estimated_time": "Half day",
                "cost": "$30-50 per person",
                "opening_hours": "8:00 AM - 6:00 PM",
                "address": "Forest District",
                "highlights": ["Zip-lining", "Hiking trails", "Nature walks"]
            },
            {
                "name": "Local Cultural Center",
                "type": "Cultural",
                "category": "culture",
                "rating": 4.1,
                "description": "Learn about local traditions, customs, and cultural heritage",
                "estimated_time": "1-2 hours",
                "cost": "$8-15 per person",
                "opening_hours": "10:00 AM - 5:00 PM",
                "address": "Cultural District",
                "highlights": ["Traditional crafts", "Cultural shows", "Local history"]
            }
        ]
        
        # Filter by interests if provided
        filtered_attractions = all_attractions
        if interests:
            filtered_attractions = []
            for attraction in all_attractions:
                for interest in interests:
                    if (interest.lower() in attraction["category"].lower() or 
                        interest.lower() in attraction["type"].lower() or 
                        interest.lower() in attraction["description"].lower()):
                        filtered_attractions.append(attraction)
                        break
        
        result = {
            "destination": destination,
            "interests_filter": interests or [],
            "attractions": filtered_attractions,
            "total_found": len(filtered_attractions),
            "categories_available": list(set([attr["category"] for attr in all_attractions])),
            "planning_tips": [
                "Book tickets in advance for popular attractions",
                "Check opening hours before visiting",
                "Consider purchasing city tourist passes for discounts",
                "Group nearby attractions for efficient touring"
            ]
        }
        
        return result
    except Exception as e:
        return {"error": f"Failed to search attractions: {str(e)}"}


def get_travel_tips(destination: str) -> Dict[str, Any]:
    """Get travel tips and local customs information"""
    try:
        tips = {
            "destination": destination,
            "cultural_tips": [
                "Respect local customs and traditions",
                "Learn basic phrases in the local language (Hello, Thank you, Please, Excuse me)",
                "Dress appropriately for religious sites and cultural venues",
                "Remove shoes when entering homes or certain establishments",
                "Be patient and polite in all interactions",
                "Show interest in local culture and ask questions respectfully"
            ],
            "safety_tips": [
                "Keep copies of important documents (passport, visa, insurance)",
                "Store emergency contact information in multiple places",
                "Stay aware of your surroundings, especially in crowded areas",
                "Use reputable transportation services and official taxis",
                "Avoid displaying expensive items or large amounts of cash",
                "Trust your instincts and leave situations that feel unsafe",
                "Register with your embassy if staying for extended periods"
            ],
            "money_tips": [
                "Notify your bank of travel plans to avoid card blocks",
                "Keep cash in multiple locations (wallet, bag, hotel safe)",
                "Understand local tipping customs and practices",
                "Learn current exchange rates and common scams",
                "Use ATMs affiliated with major banks when possible",
                "Keep receipts for major purchases for tax refunds",
                "Budget extra for unexpected expenses and souvenirs"
            ],
            "practical_tips": [
                "Download offline maps and translation apps",
                "Pack a portable charger and universal adapter",
                "Research local transportation options and apps",
                "Learn about local dining etiquette and meal times",
                "Pack appropriate clothing for weather and activities",
                "Bring necessary medications with prescriptions",
                "Consider travel insurance for health and trip coverage"
            ],
            "communication": [
                "Download language translation apps",
                "Learn basic local phrases before arrival",
                "Carry hotel address written in local language",
                "Use gestures and patience when language barriers exist",
                "Tourist information centers usually have English speakers"
            ],
            "health_and_wellness": [
                "Check if vaccinations are required or recommended",
                "Bring a basic first aid kit",
                "Research local healthcare options",
                "Stay hydrated and eat safely prepared food",
                "Get adequate rest to avoid travel fatigue"
            ]
        }
        
        return tips
    except Exception as e:
        return {"error": f"Failed to get travel tips: {str(e)}"}


def get_currency_info(destination_country: str) -> Dict[str, Any]:
    """Get currency information for the destination"""
    try:
        # Simulate currency API call
        currency_info = {
            "country": destination_country,
            "currency_name": "Local Currency",
            "currency_code": "LC",
            "symbol": "₤",
            "exchange_rate": "1 USD = 1.20 LC (approximate - rates change daily)",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "payment_methods": {
                "cash": "Widely accepted, essential for small vendors and markets",
                "credit_cards": "Visa and Mastercard accepted at most hotels and restaurants",
                "debit_cards": "Accepted at ATMs and many establishments",
                "mobile_payments": "Apple Pay, Google Pay available in major cities",
                "traveler_checks": "Limited acceptance, not recommended"
            },
            "atm_availability": {
                "urban_areas": "ATMs readily available in cities and towns",
                "rural_areas": "Limited availability, plan ahead",
                "fees": "Expect $3-5 withdrawal fees plus currency conversion",
                "daily_limits": "Usually $200-500 USD equivalent per day"
            },
            "tipping_culture": {
                "restaurants": "10-15% for good service, sometimes included in bill",
                "taxis": "Round up fare or 10%",
                "hotels": "$1-2 per bag for porters, $2-5 per day for housekeeping",
                "tour_guides": "$5-10 per day per person",
                "general": "Not mandatory but appreciated for good service"
            },
            "money_saving_tips": [
                "Use bank ATMs instead of currency exchange shops for better rates",
                "Pay in local currency when possible to avoid conversion fees",
                "Compare exchange rates at different locations",
                "Avoid airport currency exchanges (usually poor rates)",
                "Consider getting some local currency before departure"
            ],
            "budgeting_guidance": {
                "budget_traveler": "$30-50 per day",
                "mid_range": "$50-100 per day", 
                "luxury": "$100+ per day",
                "categories": "Accommodation, food, transport, activities, shopping"
            }
        }
        
        return currency_info
    except Exception as e:
        return {"error": f"Failed to get currency info: {str(e)}"}


def create_itinerary(travel_details: Dict[str, Any]) -> Dict[str, Any]:
    """Create a detailed travel itinerary"""
    try:
        destination = travel_details.get("destination", "Unknown")
        duration = travel_details.get("duration", 3)
        start_date = travel_details.get("start_date")
        interests = travel_details.get("interests", [])
        budget_level = travel_details.get("budget_level", "medium")
        travelers = travel_details.get("travelers", 2)
        
        # Create comprehensive itinerary
        itinerary = {
            "destination": destination,
            "duration": f"{duration} days",
            "start_date": start_date,
            "travelers": travelers,
            "budget_level": budget_level,
            "interests": interests,
            "daily_plans": [],
            "summary": {
                "total_activities": 0,
                "estimated_cost": "$0",
                "highlights": []
            }
        }
        
        # Sample activities by day
        daily_activities = {
            1: [
                {"time": "09:00", "activity": "Arrival and hotel check-in", "duration": "2 hours", "cost": "$0", "type": "logistics"},
                {"time": "11:00", "activity": "Welcome city walking tour", "duration": "3 hours", "cost": "$25", "type": "sightseeing"},
                {"time": "14:00", "activity": "Lunch at traditional local restaurant", "duration": "1.5 hours", "cost": "$35", "type": "dining"},
                {"time": "16:00", "activity": "Visit historic city center", "duration": "2 hours", "cost": "$10", "type": "culture"},
                {"time": "19:00", "activity": "Dinner and evening stroll", "duration": "3 hours", "cost": "$45", "type": "dining"}
            ],
            2: [
                {"time": "09:00", "activity": "Visit national museum", "duration": "3 hours", "cost": "$20", "type": "culture"},
                {"time": "12:30", "activity": "Lunch break", "duration": "1 hour", "cost": "$25", "type": "dining"},
                {"time": "14:00", "activity": "Explore local markets", "duration": "2 hours", "cost": "$30", "type": "shopping"},
                {"time": "16:30", "activity": "Scenic viewpoint visit", "duration": "1.5 hours", "cost": "$0", "type": "nature"},
                {"time": "19:00", "activity": "Traditional dinner experience", "duration": "2.5 hours", "cost": "$50", "type": "dining"}
            ],
            3: [
                {"time": "09:00", "activity": "Day trip adventure activity", "duration": "4 hours", "cost": "$60", "type": "adventure"},
                {"time": "13:00", "activity": "Picnic lunch", "duration": "1 hour", "cost": "$15", "type": "dining"},
                {"time": "15:00", "activity": "Cultural workshop", "duration": "2 hours", "cost": "$40", "type": "culture"},
                {"time": "18:00", "activity": "Farewell dinner", "duration": "2 hours", "cost": "$55", "type": "dining"},
                {"time": "20:30", "activity": "Evening entertainment", "duration": "2 hours", "cost": "$30", "type": "entertainment"}
            ]
        }
        
        # Generate daily plans
        total_cost = 0
        total_activities = 0
        
        for day in range(1, duration + 1):
            activities = daily_activities.get(day, daily_activities[3])  # Use day 3 as template for longer trips
            
            day_plan = {
                "day": day,
                "date": (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day-1)).strftime("%Y-%m-%d") if start_date else f"Day {day}",
                "theme": f"Day {day} - {'Arrival & Exploration' if day == 1 else 'Cultural Immersion' if day == 2 else 'Adventure & Farewell'}",
                "activities": activities,
                "estimated_daily_cost": f"${sum([int(act['cost'].replace('$', '')) for act in activities])}",
                "travel_tips": [
                    "Start early to avoid crowds",
                    "Stay hydrated and take breaks",
                    "Keep important documents secure"
                ]
            }
            
            total_activities += len(activities)
            total_cost += sum([int(act['cost'].replace('$', '')) for act in activities])
            
            itinerary["daily_plans"].append(day_plan)
        
        # Update summary
        itinerary["summary"] = {
            "total_activities": total_activities,
            "estimated_cost": f"${total_cost}",
            "highlights": [
                "Historic city center exploration",
                "Local culinary experiences", 
                "Cultural immersion activities",
                "Scenic viewpoints and nature"
            ],
            "recommendations": [
                "Book popular attractions in advance",
                "Carry comfortable walking shoes",
                "Keep some cash for small vendors",
                "Take photos but respect local photography rules"
            ]
        }
        
        return itinerary
        
    except Exception as e:
        return {"error": f"Failed to create itinerary: {str(e)}"}


def suggest_accommodations(travel_details: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest accommodation options"""
    try:
        destination = travel_details.get("destination", "Unknown")
        budget_level = travel_details.get("budget_level", "medium")
        travelers = travel_details.get("travelers", 2)
        duration = travel_details.get("duration", 3)
        preferences = travel_details.get("preferences", [])
        
        # Budget-based accommodation options
        budget_ranges = {
            "budget": {"min": 30, "max": 80},
            "medium": {"min": 80, "max": 200},
            "luxury": {"min": 200, "max": 500}
        }
        
        price_range = budget_ranges.get(budget_level, budget_ranges["medium"])
        
        accommodations = {
            "destination": destination,
            "budget_level": budget_level,
            "travelers": travelers,
            "duration": f"{duration} nights",
            "options": [
                {
                    "name": "Grand City Hotel",
                    "type": "Hotel",
                    "category": "4-star",
                    "rating": 4.3,
                    "price_per_night": f"${price_range['min'] + 50}-{price_range['max'] - 20}",
                    "total_cost": f"${(price_range['min'] + 50) * duration}-{(price_range['max'] - 20) * duration}",
                    "amenities": [
                        "Free WiFi",
                        "Breakfast included",
                        "Fitness center",
                        "24/7 reception",
                        "Room service",
                        "Business center"
                    ],
                    "location": "City center - walking distance to main attractions",
                    "distance_to_center": "0.3 km",
                    "transport_access": "Metro station 2 min walk",
                    "guest_rating": "Excellent location, professional service, clean rooms",
                    "pros": ["Prime location", "Professional service", "Good facilities"],
                    "cons": ["Can be busy", "Street noise possible"]
                },
                {
                    "name": "Cozy Downtown Apartment",
                    "type": "Apartment/Airbnb",
                    "category": "Local experience",
                    "rating": 4.6,
                    "price_per_night": f"${price_range['min']}-{price_range['min'] + 40}",
                    "total_cost": f"${price_range['min'] * duration}-{(price_range['min'] + 40) * duration}",
                    "amenities": [
                        "Full kitchen",
                        "WiFi",
                        "Washing machine",
                        "Local host support",
                        "Living area",
                        "Private bathroom"
                    ],
                    "location": "Residential neighborhood - authentic local area",
                    "distance_to_center": "1.5 km",
                    "transport_access": "Bus stop 5 min walk",
                    "guest_rating": "Authentic experience, great value, helpful host",
                    "pros": ["Local experience", "Cost-effective", "Kitchen facilities"],
                    "cons": ["Further from center", "Limited hotel services"]
                },
                {
                    "name": "Boutique Heritage B&B",
                    "type": "Bed & Breakfast",
                    "category": "Boutique",
                    "rating": 4.7,
                    "price_per_night": f"${price_range['min'] + 30}-{price_range['max'] - 50}",
                    "total_cost": f"${(price_range['min'] + 30) * duration}-{(price_range['max'] - 50) * duration}",
                    "amenities": [
                        "Gourmet breakfast included",
                        "Personalized service",
                        "Garden terrace",
                        "WiFi",
                        "Concierge service",
                        "Historic building"
                    ],
                    "location": "Historic quarter - charming neighborhood",
                    "distance_to_center": "0.8 km",
                    "transport_access": "Walking distance to attractions",
                    "guest_rating": "Exceptional breakfast, personal touch, beautiful building",
                    "pros": ["Personal service", "Excellent breakfast", "Unique character"],
                    "cons": ["Limited rooms", "May book up quickly"]
                }
            ],
            "booking_recommendations": [
                "Book 2-4 weeks in advance for better rates",
                "Check cancellation policies carefully",
                "Read recent guest reviews for current conditions",
                "Consider location vs. budget trade-offs",
                "Look for package deals including breakfast or tours",
                "Verify amenities that are important to you"
            ],
            "neighborhood_guide": {
                "city_center": "Convenient but can be busy and expensive",
                "historic_quarter": "Charming atmosphere, walkable to attractions",
                "residential_areas": "Authentic local experience, better value",
                "business_district": "Modern amenities, good transport links"
            },
            "seasonal_considerations": [
                "Peak season: Book early, expect higher prices",
                "Off-season: Better rates, fewer crowds",
                "Shoulder season: Good balance of weather and prices",
                "Local events: Check for festivals that might affect availability"
            ]
        }
        
        return accommodations
        
    except Exception as e:
        return {"error": f"Failed to suggest accommodations: {str(e)}"}


def estimate_budget(travel_details: Dict[str, Any]) -> Dict[str, Any]:
    """Estimate comprehensive travel budget"""
    try:
        destination = travel_details.get("destination", "Unknown")
        duration = travel_details.get("duration", 3)
        travelers = travel_details.get("travelers", 1)
        budget_level = travel_details.get("budget_level", "medium")
        activities = travel_details.get("planned_activities", [])
        
        # Detailed daily costs by budget level
        daily_costs = {
            "budget": {
                "accommodation": 45,
                "meals": 30,
                "local_transport": 8,
                "attractions": 15,
                "shopping": 10,
                "miscellaneous": 12
            },
            "medium": {
                "accommodation": 120,
                "meals": 55,
                "local_transport": 15,
                "attractions": 25,
                "shopping": 20,
                "miscellaneous": 20
            },
            "luxury": {
                "accommodation": 250,
                "meals": 100,
                "local_transport": 30,
                "attractions": 50,
                "shopping": 50,
                "miscellaneous": 40
            }
        }
        
        base_costs = daily_costs.get(budget_level, daily_costs["medium"])
        
        # Additional one-time costs
        one_time_costs = {
            "flights": {
                "budget": 400,
                "medium": 600,
                "luxury": 1200
            },
            "travel_insurance": 50,
            "visa_fees": 30,
            "airport_transfers": 40
        }
        
        # Calculate totals
        daily_total = sum(base_costs.values())
        trip_total = daily_total * duration
        flight_cost = one_time_costs["flights"][budget_level]
        other_costs = one_time_costs["travel_insurance"] + one_time_costs["visa_fees"] + one_time_costs["airport_transfers"]
        
        budget_estimate = {
            "destination": destination,
            "duration": f"{duration} days",
            "travelers": travelers,
            "budget_level": budget_level,
            "detailed_breakdown": {
                "daily_costs": {
                    "accommodation": {
                        "amount": f"${base_costs['accommodation']}",
                        "description": "Hotel/lodging per night",
                        "total": f"${base_costs['accommodation'] * duration}"
                    },
                    "meals": {
                        "amount": f"${base_costs['meals']}",
                        "description": "Breakfast, lunch, dinner per day",
                        "total": f"${base_costs['meals'] * duration}"
                    },
                    "local_transport": {
                        "amount": f"${base_costs['local_transport']}",
                        "description": "Metro, buses, taxis per day",
                        "total": f"${base_costs['local_transport'] * duration}"
                    },
                    "attractions": {
                        "amount": f"${base_costs['attractions']}",
                        "description": "Museums, tours, activities per day",
                        "total": f"${base_costs['attractions'] * duration}"
                    },
                    "shopping": {
                        "amount": f"${base_costs['shopping']}",
                        "description": "Souvenirs, personal items per day",
                        "total": f"${base_costs['shopping'] * duration}"
                    },
                    "miscellaneous": {
                        "amount": f"${base_costs['miscellaneous']}",
                        "description": "Tips, snacks, extras per day",
                        "total": f"${base_costs['miscellaneous'] * duration}"
                    }
                },
                "one_time_costs": {
                    "flights": f"${flight_cost}",
                    "travel_insurance": f"${one_time_costs['travel_insurance']}",
                    "visa_fees": f"${one_time_costs['visa_fees']}",
                    "airport_transfers": f"${one_time_costs['airport_transfers']}"
                }
            },
            "totals": {
                "daily_average": f"${daily_total}",
                "trip_total_before_flights": f"${trip_total}",
                "flights_and_fees": f"${flight_cost + other_costs}",
                "grand_total_per_person": f"${trip_total + flight_cost + other_costs}",
                "grand_total_for_group": f"${(trip_total + flight_cost + other_costs) * travelers}"
            },
            "budget_tips": {
                "save_money": [
                    "Book flights 6-8 weeks in advance",
                    "Stay in local neighborhoods vs tourist areas",
                    "Eat at local restaurants and markets",
                    "Use public transportation",
                    "Look for free walking tours and activities",
                    "Travel during shoulder season",
                    "Cook some meals if staying in apartment"
                ],
                "splurge_worthwhile": [
                    "Good location accommodation",
                    "One special dining experience",
                    "Professional guided tour of highlights",
                    "Quality travel insurance",
                    "Comfortable walking shoes"
                ]
            },
            "emergency_fund": {
                "recommended": f"${int((trip_total + flight_cost + other_costs) * 0.15)}",
                "description": "15% of total budget for unexpected expenses"
            },
            "payment_recommendations": [
                "Notify bank of travel dates",
                "Bring mix of cash and cards",
                "Have backup payment method",
                "Research ATM fees and locations",
                "Consider travel-friendly credit cards"
            ]
        }
        
        return budget_estimate
        
    except Exception as e:
        return {"error": f"Failed to estimate budget: {str(e)}"}


def generate_packing_list(travel_details: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive personalized packing list"""
    try:
        destination = travel_details.get("destination", "Unknown")
        duration = travel_details.get("duration", 3)
        season = travel_details.get("season", "spring")
        activities = travel_details.get("planned_activities", [])
        budget_level = travel_details.get("budget_level", "medium")
        
        # Base packing list by category
        base_categories = {
            "essentials": {
                "documents": [
                    "Passport (valid for 6+ months)",
                    "Visa (if required)",
                    "Travel insurance documents",
                    "Flight tickets/boarding passes",
                    "Hotel confirmations",
                    "Emergency contact information",
                    "Copies of important documents (stored separately)",
                    "Travel itinerary",
                    "Local embassy contact info"
                ],
                "money_and_cards": [
                    "Credit cards (2 different types)",
                    "Debit card",
                    "Cash (local currency + USD)",
                    "Money belt or hidden wallet",
                    "Backup cards (stored separately)"
                ]
            },
            "clothing": {
                "basics": [
                    f"Underwear for {duration + 2} days",
                    f"Socks for {duration + 2} days",
                    "Comfortable walking shoes",
                    "Casual pants/jeans (2 pairs)",
                    "Comfortable shirts/tops (3-4)",
                    "One dressy outfit",
                    "Sleepwear",
                    "Light jacket or sweater"
                ],
                "weather_specific": [],  # Will be filled based on season
                "activity_specific": []   # Will be filled based on activities
            },
            "health_and_hygiene": [
                "Prescription medications (in original containers)",
                "Basic first aid kit",
                "Toothbrush and toothpaste",
                "Shampoo and conditioner (travel size)",
                "Body wash or soap",
                "Deodorant",
                "Sunscreen (SPF 30+)",
                "Hand sanitizer",
                "Personal hygiene items",
                "Any special medical needs"
            ],
            "electronics": [
                "Phone and charger",
                "Portable battery pack/power bank",
                "Universal power adapter",
                "Camera (optional)",
                "Headphones",
                "Tablet/e-reader (optional)",
                "Portable speaker (small, optional)"
            ],
            "comfort_and_convenience": [
                "Reusable water bottle",
                "Day backpack or daypack",
                "Travel pillow",
                "Eye mask and earplugs",
                "Snacks for travel day",
                "Entertainment (book, downloaded movies)",
                "Pen and small notebook",
                "Tissues/napkins",
                "Plastic bags (for dirty clothes, wet items)"
            ]
        }
        
        # Add weather-specific items
        weather_items = {
            "winter": [
                "Heavy winter coat",
                "Warm hat and gloves",
                "Thermal underwear",
                "Warm socks",
                "Waterproof boots",
                "Scarf",
                "Hot packs/warmers"
            ],
            "spring": [
                "Light rain jacket",
                "Layers for temperature changes",
                "Light sweater",
                "Umbrella (compact)",
                "Mix of short and long sleeves"
            ],
            "summer": [
                "Sun hat",
                "Sunglasses",
                "Light, breathable clothing",
                "Sandals or breathable shoes",
                "Swimwear",
                "Light cover-up",
                "Cooling towel"
            ],
            "fall": [
                "Warm layers",
                "Medium weight jacket",
                "Comfortable boots",
                "Rain protection",
                "Mix of clothing weights"
            ]
        }
        
        base_categories["clothing"]["weather_specific"] = weather_items.get(season, weather_items["spring"])
        
        # Add activity-specific items
        activity_items = []
        activity_list = [activity.lower() for activity in activities]
        
        if any(word in activity_list for word in ["hiking", "walking", "trek"]):
            activity_items.extend([
                "Sturdy hiking boots",
                "Moisture-wicking clothing",
                "Daypack with water bottle holder",
                "Trail snacks",
                "Hiking socks",
                "Quick-dry towel"
            ])
        
        if any(word in activity_list for word in ["swimming", "beach", "water"]):
            activity_items.extend([
                "Swimwear (2 sets)",
                "Beach towel",
                "Waterproof bag",
                "Flip-flops",
                "Snorkeling gear (optional)"
            ])
        
        if any(word in activity_list for word in ["business", "meeting", "conference"]):
            activity_items.extend([
                "Business attire (2-3 outfits)",
                "Dress shoes",
                "Laptop and charger",
                "Business cards",
                "Professional bag"
            ])
        
        if any(word in activity_list for word in ["formal", "dinner", "theater"]):
            activity_items.extend([
                "Formal wear",
                "Dress shoes",
                "Accessories (jewelry, ties, etc.)",
                "Small purse/evening bag"
            ])
        
        base_categories["clothing"]["activity_specific"] = activity_items
        
        # Packing tips based on duration and budget
        packing_tips = [
            "Roll clothes instead of folding to save space",
            "Pack heaviest items closest to your back in backpack",
            "Wear heaviest shoes and jacket while traveling",
            "Leave room for souvenirs (pack 20% less than capacity)",
            "Pack essentials in carry-on bag",
            "Check airline baggage restrictions and fees"
        ]
        
        if duration <= 3:
            packing_tips.append("Consider carry-on only for short trips")
        if duration >= 7:
            packing_tips.append("Pack for laundry every 5-7 days")
        
        # Final packing list structure
        packing_list = {
            "destination": destination,
            "duration": f"{duration} days",
            "season": season,
            "budget_level": budget_level,
            "activities": activities,
            "categories": base_categories,
            "packing_tips": packing_tips,
            "weight_considerations": {
                "carry_on_limit": "Usually 7-10 kg (15-22 lbs)",
                "checked_bag_limit": "Usually 23 kg (50 lbs)",
                "personal_item": "Small bag that fits under seat"
            },
            "last_minute_checklist": [
                "Check weather forecast before packing",
                "Confirm airline baggage policies",
                "Leave emergency contact with someone at home",
                "Set out-of-office messages",
                "Arrange mail/package holds",
                "Charge all electronic devices",
                "Download offline maps and translation apps"
            ],
            "packing_strategy": {
                "week_before": "Gather all items, check expiration dates",
                "few_days_before": "Do laundry, start packing non-essentials",
                "day_before": "Pack essentials, prepare carry-on",
                "day_of": "Final checks, pack last-minute items"
            }
        }
        
        return packing_list
        
    except Exception as e:
        return {"error": f"Failed to generate packing list: {str(e)}"}

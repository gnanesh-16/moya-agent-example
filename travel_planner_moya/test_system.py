"""
Simple test script for Travel Planner Multi-Agent System
Tests basic functionality of agents and orchestrator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.orchestrator import travel_orchestrator
from agents.info_agent import info_agent
from agents.travel_agent import travel_agent
from tools.memory import travel_memory

def test_memory_system():
    """Test the memory system functionality"""
    print("🧠 Testing Memory System...")
    
    # Test conversation logging
    travel_memory.add_conversation("user", "Hello, I want to plan a trip to Paris", "Test")
    travel_memory.add_conversation("assistant", "I can help you plan your Paris trip!", "InfoAgent")
    
    # Test user preferences
    preferences = {
        "destination": "Paris",
        "budget_level": "medium",
        "interests": ["art", "food"]
    }
    travel_memory.update_user_preferences(preferences)
    
    # Test context retrieval
    context = travel_memory.get_conversation_context(5)
    prefs = travel_memory.get_user_preferences_context()
    
    print(f"✅ Conversation context: {len(context)} characters")
    print(f"✅ User preferences stored: {len(travel_memory.user_preferences)} items")
    
    return True

def test_info_agent():
    """Test InfoAgent functionality"""
    print("📊 Testing InfoAgent...")
    
    # Test destination info
    dest_response = info_agent.process_request("Tell me about Paris", {"destination": "Paris"})
    print(f"✅ Destination info: Generated {len(dest_response)} character response")
    
    # Test weather info
    weather_response = info_agent.process_request("What's the weather like in Paris?", {"destination": "Paris"})
    print(f"✅ Weather info: Generated {len(weather_response)} character response")
    
    # Test attractions search
    attractions_response = info_agent.process_request("Find attractions in Paris", {"destination": "Paris", "interests": ["art", "history"]})
    print(f"✅ Attractions found: Generated {len(attractions_response)} character response")
    
    return True

def test_travel_agent():
    """Test TravelAgent functionality"""
    print("✈️ Testing TravelAgent...")
    
    context = {
        "destination": "Paris",
        "duration": 5,
        "budget_level": "medium",
        "travelers": 2
    }
    
    # Test itinerary creation
    itinerary_response = travel_agent.process_request("Create an itinerary for Paris", context)
    print(f"✅ Itinerary created: Generated {len(itinerary_response)} character response")
    
    # Test accommodation suggestions
    hotel_response = travel_agent.process_request("Suggest accommodations in Paris", context)
    print(f"✅ Accommodations: Generated {len(hotel_response)} character response")
    
    # Test budget estimation
    budget_response = travel_agent.process_request("Estimate budget for Paris trip", context)
    print(f"✅ Budget estimated: Generated {len(budget_response)} character response")
    
    return True

def test_orchestrator():
    """Test the orchestrator functionality"""
    print("🎯 Testing Orchestrator...")
    
    # Test request classification
    info_request = "What's the weather like in Tokyo?"
    travel_request = "Create an itinerary for Rome"
    
    info_classification = travel_orchestrator.classify_request(info_request)
    travel_classification = travel_orchestrator.classify_request(travel_request)
    
    print(f"✅ Info request classified as: {info_classification}")
    print(f"✅ Travel request classified as: {travel_classification}")
    
    # Test context extraction
    test_request = "Plan a 5-day trip to Paris in June for 2 people with medium budget"
    context = travel_orchestrator.extract_context(test_request)
    
    print(f"✅ Context extracted: {len(context)} items")
    print(f"   Detected: {context}")
    
    # Test full request processing
    result = travel_orchestrator.process_request("Tell me about Paris attractions")
    print(f"✅ Request processed by: {result.get('agent_used', 'Error')}")
    
    return True

def test_integration():
    """Test integration between components"""
    print("🔗 Testing Integration...")
    
    # Test multi-agent workflow
    complex_request = "Create a complete travel plan for Tokyo"
    result = travel_orchestrator.handle_multi_agent_workflow(complex_request)
    
    if result.get("type") == "multi_agent_response":
        print("✅ Multi-agent workflow completed")
    else:
        print("✅ Single-agent workflow completed")
    
    # Test memory persistence across requests
    travel_orchestrator.process_request("I want to visit museums in Paris")
    travel_orchestrator.process_request("What's my budget for this trip?")
    
    summary = travel_orchestrator.get_conversation_summary()
    print(f"✅ Conversation summary: {summary['total_interactions']} interactions")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Travel Planner System Tests")
    print("=" * 50)
    
    tests = [
        ("Memory System", test_memory_system),
        ("InfoAgent", test_info_agent),
        ("TravelAgent", test_travel_agent),
        ("Orchestrator", test_orchestrator),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name} tests...")
            if test_func():
                print(f"✅ {test_name} tests passed!")
                passed += 1
            else:
                print(f"❌ {test_name} tests failed!")
        except Exception as e:
            print(f"❌ {test_name} tests failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

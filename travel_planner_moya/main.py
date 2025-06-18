"""
Travel Planner Multi-Agent System
Main application using Streamlit for UI and MOYA framework for agent orchestration
"""

import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime, date
import json

# Load environment variables
load_dotenv()

# Import our MOYA-powered travel system
from moya_agents import get_travel_system
from utils.prompt_fetcher import get_prompt_fetcher

# Initialize the travel system with OpenAI integration
travel_system = get_travel_system()
prompt_fetcher = get_prompt_fetcher()

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}
    if 'current_context' not in st.session_state:
        st.session_state.current_context = {}

def display_agent_capabilities():
    """Display available agent capabilities"""
    with st.expander("🤖 Available AI Agents & Capabilities"):
        capabilities = travel_system.get_available_capabilities()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 InfoAgent")
            for capability in capabilities["InfoAgent"]:
                st.write(f"• {capability}")
        
        with col2:
            st.subheader("✈️ TravelAgent") 
            for capability in capabilities["TravelAgent"]:
                st.write(f"• {capability}")

def display_conversation_history():
    """Display conversation history"""
    if st.session_state.conversation_history:
        st.subheader("💬 Conversation History")
        for i, interaction in enumerate(st.session_state.conversation_history[-5:]):  # Show last 5
            with st.expander(f"Interaction {len(st.session_state.conversation_history) - 4 + i}", expanded=False):
                st.write(f"**You:** {interaction['user_request']}")
                st.write(f"**Agent:** {interaction['agent_used']}")
                
                # Display response in a more readable format
                try:
                    response_data = json.loads(interaction['response'])
                    st.json(response_data)
                except (json.JSONDecodeError, TypeError):
                    st.write(f"**Response:** {interaction['response']}")

def format_response_display(response_text: str) -> str:
    """Format response for better display"""
    try:
        # Try to parse as JSON for better formatting
        response_data = json.loads(response_text)
        return json.dumps(response_data, indent=2)
    except (json.JSONDecodeError, TypeError):
        return response_text

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Travel Planner AI",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("✈️ Travel Planner AI")
    st.markdown("**Multi-Agent Travel Planning System powered by MOYA Framework**")
    st.markdown("---")
    
    # Sidebar for user preferences and controls
    with st.sidebar:
        st.header("🎯 Travel Preferences")
        
        # User preferences form
        with st.form("preferences_form"):
            st.subheader("Personal Preferences")
            
            preferred_destinations = st.text_input(
                "Preferred Destinations",
                value=st.session_state.user_preferences.get("preferred_destinations", ""),
                placeholder="e.g., Paris, Tokyo, New York"
            )
            
            budget_level = st.selectbox(
                "Budget Level",
                ["budget", "medium", "luxury"],
                index=["budget", "medium", "luxury"].index(
                    st.session_state.user_preferences.get("budget_level", "medium")
                )
            )
            
            travel_style = st.selectbox(
                "Travel Style",
                ["adventurous", "relaxed", "cultural", "business"],
                index=["adventurous", "relaxed", "cultural", "business"].index(
                    st.session_state.user_preferences.get("travel_style", "relaxed")
                )
            )
            
            interests = st.multiselect(
                "Interests",
                ["history", "art", "food", "nature", "nightlife", "shopping", "museums", "sports"],
                default=st.session_state.user_preferences.get("interests", [])
            )
            
            if st.form_submit_button("Save Preferences"):
                preferences = {
                    "preferred_destinations": preferred_destinations,
                    "budget_level": budget_level,
                    "travel_style": travel_style,
                    "interests": interests,
                    "updated_at": datetime.now().isoformat()
                }
                st.session_state.user_preferences = preferences
                # Note: MOYA system manages its own preferences
                st.success("Preferences saved!")
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            travel_system.clear_conversation()
            st.success("Conversation cleared!")
        
        if st.button("Show System Status"):
            summary = travel_system.get_conversation_history()
            if summary:
                st.write("**Recent Conversation:**")
                for msg in summary[-3:]:  # Show last 3 messages
                    st.write(f"**{msg.get('role', 'unknown').title()}:** {msg.get('content', '')[:200]}...")
            else:
                st.info("No conversation history available")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display agent capabilities
        display_agent_capabilities()
        
        # Chat interface
        st.subheader("💭 Chat with AI Travel Agents")
        
        # Dynamic example prompts from API
        st.write("**Example prompts:**")
        
        # Get user preferences for contextual prompts
        user_prefs = st.session_state.user_preferences
        
        # Fetch dynamic prompts
        try:
            with st.spinner("Loading personalized suggestions..."):
                if user_prefs:
                    example_prompts = prompt_fetcher.get_contextual_prompts(user_prefs, count=5)
                else:
                    example_prompts = prompt_fetcher.fetch_travel_prompts(count=5, category="general")
        except Exception as e:
            st.warning(f"Could not load dynamic prompts: {e}")
            example_prompts = [
                "Plan a weekend trip for two people",
                "What's the weather like in popular destinations?",
                "Suggest budget-friendly travel options"
            ]
        
        # Add refresh button for prompts
        col_prompts, col_refresh = st.columns([4, 1])
        
        with col_refresh:
            if st.button("🔄", help="Refresh prompt suggestions"):
                prompt_fetcher.refresh_cache()
                st.rerun()
        
        with col_prompts:
            selected_example = st.selectbox(
                "Or choose a suggestion:",
                [""] + example_prompts,
                key="example_selector"
            )
        
        # User input
        user_input = st.text_area(
            "Your travel question or request:",
            value=selected_example if selected_example else "",
            height=100,
            placeholder="Ask me anything about travel planning, destinations, weather, or get help creating itineraries..."
        )
        
        # Processing options
        col_submit, col_multi = st.columns(2)
        
        with col_submit:
            submit_button = st.button("Send Message", type="primary")
        
        with col_multi:
            multi_agent_button = st.button("Full Travel Plan", help="Uses multiple agents for comprehensive planning")
        
        # Process user request
        if submit_button and user_input:
            with st.spinner("Processing your request..."):
                try:
                    # Use MOYA system to handle the message
                    result = travel_system.handle_message(user_input)
                    
                    # Store in session state
                    conversation_entry = {
                        "user_input": user_input,
                        "agent_response": result,
                        "timestamp": datetime.now().isoformat()
                    }
                    st.session_state.conversation_history.append(conversation_entry)
                    
                    # Display result
                    st.success("Response from AI Travel Agent")
                    
                    # Format and display response
                    with st.container():
                        st.write("**AI Response:**")
                        st.markdown(result)
                        
                        # Show extracted context
                        if result.get("extracted_context"):
                            with st.expander("Extracted Context"):
                                st.json(result["extracted_context"])
                
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
        
        elif multi_agent_button and user_input:
            with st.spinner("Creating comprehensive travel plan with multiple agents..."):
                try:
                    # Use the MOYA system for multi-agent workflow
                    result = travel_system.handle_message(f"[COMPREHENSIVE PLAN] {user_input}")
                    
                    # Store in session state
                    st.session_state.conversation_history.append({
                        "user_request": user_input,
                        "agent_used": "Multi-Agent",
                        "response": result,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Display multi-agent result
                    st.success("Comprehensive travel plan created using multiple agents!")
                    st.markdown(result)
                
                except Exception as e:
                    st.error(f"Error creating multi-agent plan: {str(e)}")
    
    with col2:
        # Current context and conversation history
        st.subheader("🔍 Current Context")
        if st.session_state.current_context:
            st.json(st.session_state.current_context)
        else:
            st.info("No current context. Start a conversation to see extracted information.")
        
        # Display recent conversation
        display_conversation_history()
        
        # System information
        with st.expander("ℹ️ System Information"):
            st.write("**Framework:** MOYA Multi-Agent System")
            st.write("**Agents Active:** InfoAgent, TravelAgent")
            st.write("**Memory System:** Conversation context and user preferences")
            st.write("**UI Framework:** Streamlit")
            
            # Show system stats
            system_stats = travel_system.get_system_status()
            conversation_history = travel_system.get_conversation_history()
            st.write(f"**Total Interactions:** {len(conversation_history)}")
            st.write(f"**Agents Registered:** {system_stats.get('agents_registered', 0)}")
            st.write(f"**Tools Available:** {system_stats.get('tools_available', 0)}")


if __name__ == "__main__":
    main()

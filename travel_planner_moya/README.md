# Travel Planner Multi-Agent System

## Overview
A sophisticated travel planning system that leverages multiple AI agents to provide comprehensive travel assistance. The system integrates OpenAI's GPT models with specialized travel tools to deliver personalized travel recommendations, itinerary planning, and destination information.

## Task Design

### Primary Task
**Comprehensive Travel Planning and Assistance**

The system is designed to handle complex travel planning scenarios by breaking them down into specialized subtasks handled by different agents. Users can request anything from simple destination information to complete multi-day itinerary planning.

### Task Scope
| Task Category | Description | Examples |
|---------------|-------------|----------|
| **Information Gathering** | Collect destination details, weather, attractions | "What's the weather in Tokyo in spring?" |
| **Itinerary Planning** | Create detailed day-by-day travel plans | "Plan a 5-day trip to Paris for 2 people" |
| **Budget Estimation** | Calculate travel costs and provide budget breakdowns | "Estimate costs for a week in Rome" |
| **Accommodation Suggestions** | Recommend hotels based on preferences | "Find luxury hotels in Barcelona" |
| **Activity Recommendations** | Suggest attractions and activities | "Find art museums in New York" |
| **Travel Logistics** | Handle transportation and packing advice | "Create a packing list for winter Europe travel" |

## Agent Design

### Agent Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                 Multi-Agent System                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   InfoAgent     │    │      TravelAgent            │ │
│  │                 │    │                             │ │
│  │ • Destination   │    │ • Itinerary Creation        │ │
│  │   Information   │    │ • Accommodation Suggestions │ │
│  │ • Weather Data  │    │ • Budget Estimation         │ │
│  │ • Attractions   │    │ • Packing Lists            │ │
│  │ • Cultural Tips │    │ • Transportation Planning   │ │
│  └─────────────────┘    └─────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│               Shared Components                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐│
│  │ Memory Tool │ │ Classifier  │ │    Travel Tools     ││
│  │             │ │             │ │                     ││
│  │ • Context   │ │ • Route     │ │ • Weather API       ││
│  │   Storage   │ │   Requests  │ │ • Destination DB    ││
│  │ • History   │ │ • Agent     │ │ • Budget Calculator ││
│  │   Tracking  │ │   Selection │ │ • Recommendation    ││
│  └─────────────┘ └─────────────┘ └─────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Agent Specifications

#### 1. InfoAgent
| Attribute | Details |
|-----------|---------|
| **Primary Function** | Information gathering and destination research |
| **Model** | GPT-4o |
| **Specialization** | Travel information, weather, cultural insights, attractions |
| **Tools Access** | `get_destination_info`, `get_weather_info`, `search_attractions`, `get_travel_tips`, `get_currency_info` |
| **Response Style** | Informative, detailed, culturally sensitive |

**Capabilities:**
- Provides comprehensive destination information
- Fetches real-time weather conditions and forecasts
- Discovers attractions and points of interest
- Offers cultural tips and local customs advice
- Provides currency and payment information

**Tools:**
- `get_destination_info()` - General destination information
- `get_weather_info()` - Weather data and forecasts
- `search_attractions()` - Activity and attraction recommendations
- `get_travel_tips()` - Cultural and practical advice
- `get_currency_info()` - Financial and payment information

#### 2. TravelAgent
| Attribute | Details |
|-----------|---------|
| **Primary Function** | Travel planning and logistics management |
| **Model** | GPT-4o |
| **Specialization** | Itinerary creation, accommodation, budgeting, logistics |
| **Tools Access** | `create_itinerary`, `suggest_accommodations`, `estimate_budget`, `generate_packing_list` |
| **Response Style** | Structured, practical, detail-oriented |

**Capabilities:**
- Creates detailed day-by-day itineraries
- Suggests accommodations based on preferences and budget
- Estimates comprehensive travel budgets
- Generates personalized packing lists
- Plans transportation and logistics

**Tools:**
- `create_itinerary()` - Day-by-day travel plans
- `suggest_accommodations()` - Lodging recommendations
- `estimate_budget()` - Cost breakdowns and financial planning
- `generate_packing_list()` - Personalized packing recommendations

### Agent Collaboration

| Collaboration Type | Description | Example Scenario |
|-------------------|-------------|------------------|
| **Sequential Processing** | InfoAgent provides context, TravelAgent creates plans | User asks for "complete Paris trip plan" - InfoAgent gathers Paris info, TravelAgent creates itinerary |
| **Parallel Processing** | Both agents work simultaneously on different aspects | Complex queries trigger both agents to provide comprehensive responses |
| **Context Sharing** | Agents share information through memory system | Previous destination research informs subsequent planning requests |

## Framework Integration

### OpenAI Integration
The system integrates with OpenAI's API to power both agents:

| Component | Integration Details |
|-----------|-------------------|
| **API Configuration** | Uses `OPENAI_API_KEY` from environment variables |
| **Model Selection** | GPT-4o for both agents (configurable) |
| **Streaming Support** | Enabled for real-time response generation |
| **Error Handling** | Graceful fallbacks for API limitations |

### System Architecture
```python
# Core System Components
TravelPlannerSystem
├── AgentRegistry (manages agent instances)
├── SimpleKeywordClassifier (routes requests)
├── MemoryTool (context management)
├── ToolRegistry (function registry)
└── Orchestrator (coordinates agent interactions)
```

### Dynamic Prompt System
| Feature | Implementation |
|---------|---------------|
| **Dynamic Generation** | Uses OpenAI API to generate contextual prompts |
| **Caching** | 5-minute cache to optimize API usage |
| **Personalization** | Adapts prompts based on user preferences |
| **Fallback System** | Predefined prompts when API is unavailable |

## Memory Component Implementation

### Memory Architecture

| Memory Type | Purpose | Storage Method | Retention |
|-------------|---------|----------------|-----------|
| **Conversation History** | Track user interactions | In-memory lists | Session-based |
| **User Preferences** | Store travel preferences | Session state | Persistent during session |
| **Context Extraction** | Maintain conversation context | Memory tool | Cross-conversation |
| **Agent State** | Track agent responses | Conversation entries | Historical |
### Memory Features

#### 1. Conversation Context
```python
# Memory Structure
{
    "user_id": "default",
    "messages": [
        {
            "role": "user|assistant",
            "content": "message content",
            "timestamp": "ISO timestamp",
            "agent": "InfoAgent|TravelAgent"
        }
    ],
    "extracted_context": {
        "destinations": ["Paris", "Rome"],
        "budget_level": "medium",
        "travel_dates": "June 2025",
        "preferences": {...}
    }
}
```

#### 2. Context Preservation
| Mechanism | Description | Implementation |
|-----------|-------------|---------------|
| **Message Storage** | Stores all user-agent interactions | `memory_tool.store_message()` |
| **Context Retrieval** | Retrieves relevant historical context | `memory_tool.get_conversation_history()` |
| **Preference Tracking** | Maintains user travel preferences | Session state management |
| **Cross-Agent Sharing** | Allows agents to access shared context | Centralized memory tool |

#### 3. Memory Management
| Feature | Configuration | Purpose |
|---------|--------------|---------|
| **Max History** | 50 conversations | Prevent memory overflow |
| **Context Window** | 10 recent messages | Relevant context retrieval |
| **Search History** | 20 recent searches | Quick access to previous queries |
| **Session Persistence** | Browser session | Maintain state during use |

## Demonstration Strategy

### Testing Approach

#### 1. Unit Testing
| Test Category | Focus Area | Test Cases |
|---------------|------------|------------|
| **Agent Functionality** | Individual agent responses | InfoAgent weather queries, TravelAgent itinerary creation |
| **Tool Integration** | Travel tool functions | Destination info retrieval, budget calculations |
| **Memory Operations** | Context storage/retrieval | Message persistence, conversation history |
| **Prompt Generation** | Dynamic prompt system | API-based prompt fetching, fallback mechanisms |

#### 2. Integration Testing
| Scenario | Test Objective | Expected Outcome |
|----------|---------------|------------------|
| **Multi-Agent Workflow** | Agent collaboration | Seamless handoff between agents |
| **Memory Persistence** | Context maintenance | Conversation history preserved across interactions |
| **Error Handling** | System resilience | Graceful degradation when APIs fail |
| **User Experience** | Interface responsiveness | Smooth Streamlit interface operation |

#### 3. End-to-End Testing

##### Test Scenarios
| Scenario | User Input | Expected Agent Response | Success Criteria |
|----------|------------|----------------------|------------------|
| **Simple Information Query** | "What's the weather in Tokyo?" | InfoAgent provides current weather | Accurate, formatted weather data |
| **Complex Planning Request** | "Plan a 5-day trip to Paris for 2 people, medium budget" | TravelAgent creates detailed itinerary | Complete itinerary with daily activities, budget breakdown |
| **Multi-Turn Conversation** | Follow-up questions about previous destinations | Agents reference conversation history | Contextually aware responses |
| **Preference-Based Recommendations** | Requests based on stored user preferences | Personalized suggestions | Recommendations aligned with preferences |

### Evaluation Metrics

#### 1. Performance Metrics
| Metric | Measurement | Target |
|--------|-------------|--------|
| **Response Time** | Average response generation time | < 10 seconds |
| **Accuracy** | Information correctness | > 90% |
| **Context Retention** | Cross-conversation context preservation | 100% within session |
| **Tool Success Rate** | Successful tool execution | > 95% |

#### 2. User Experience Metrics
| Metric | Measurement Method | Success Indicator |
|--------|-------------------|-------------------|
| **Conversation Flow** | Natural conversation progression | Seamless multi-turn interactions |
| **Personalization** | Preference-based recommendations | Relevant suggestions |
| **Error Recovery** | System behavior during failures | Graceful fallback responses |
| **Interface Usability** | Streamlit UI responsiveness | Intuitive user interactions |

### Demonstration Workflow

#### 1. System Initialization
```bash
# Environment Setup
export OPENAI_API_KEY="your-api-key"
cd travel_planner_moya
pip install -r requirements.txt

# Launch Application
streamlit run main.py
```

#### 2. Feature Demonstration
| Demo Phase | Actions | Demonstrates |
|------------|---------|-------------|
| **Phase 1: Basic Queries** | Weather, destination info requests | InfoAgent capabilities |
| **Phase 2: Planning Tasks** | Itinerary creation, budget estimation | TravelAgent functionality |
| **Phase 3: Memory Features** | Multi-turn conversations, context references | Memory system effectiveness |
| **Phase 4: Personalization** | Preference-based recommendations | Dynamic prompt system |

#### 3. Edge Case Testing
| Test Case | Scenario | Expected Behavior |
|----------|----------|------------------|
| **API Failure** | OpenAI API unavailable | Fallback to cached/default prompts |
| **Invalid Inputs** | Nonsensical travel requests | Graceful error handling |
| **Memory Overflow** | Excessive conversation history | Automatic cleanup, maintained performance |
| **Network Issues** | Intermittent connectivity | Retry mechanisms, user feedback |

## Configuration and Setup

### Environment Variables
| Variable | Purpose | Required |
|----------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API access | Yes |

### Configuration Files
| File | Purpose | Key Settings |
|------|---------|-------------|
| `config.py` | System configuration | Agent settings, memory limits, UI config |
| `.env` | Environment variables | API keys, sensitive configuration |
| `requirements.txt` | Python dependencies | Package versions and requirements |

### Supporting Scripts
| Script | Purpose | Usage |
|--------|---------|-------|
| `main.py` | Streamlit application entry point | `streamlit run main.py` |
| `moya_agents.py` | Agent system implementation | Core system logic |
| `utils/prompt_fetcher.py` | Dynamic prompt generation | API-based prompt fetching |
| `tools/travel_tools.py` | Travel-specific functions | Tool implementations |

## System Advantages

### 1. Scalability
- **Modular Design**: Easy to add new agents or tools
- **Configurable Components**: Adjustable memory limits and API settings
- **Framework Agnostic**: Can integrate with different AI frameworks

### 2. Reliability
- **Fallback Mechanisms**: System continues operating when APIs fail
- **Error Handling**: Comprehensive error management and recovery
- **Memory Management**: Automatic cleanup prevents memory issues

### 3. User Experience
- **Personalization**: Adapts to user preferences and history
- **Context Awareness**: Maintains conversation context across interactions
- **Real-time Responses**: Streaming responses for immediate feedback
- **Intuitive Interface**: Clean, responsive Streamlit UI

### 4. Extensibility
- **Tool Registry**: Easy addition of new travel tools
- **Agent Framework**: Simple agent creation and registration
- **Memory System**: Flexible context storage and retrieval
- **Configuration System**: Extensive customization options

## Future Enhancements

| Enhancement | Description | Implementation Priority |
|-------------|-------------|----------------------|
| **Database Integration** | Persistent storage for user data and preferences | High |
| **Advanced Personalization** | Machine learning-based recommendation engine | Medium |
| **Multi-language Support** | International travel assistance | Medium |
| **Real-time Data Integration** | Live pricing, availability data | High |
| **Voice Interface** | Speech-to-text travel planning | Low |
| **Mobile Application** | Native mobile app development | Medium |

---

## Getting Started

### Quick Start
1. Clone the repository
2. Set up environment variables (`OPENAI_API_KEY`)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `streamlit run main.py`
5. Access the web interface at `http://localhost:8501`

### Example Usage
1. **Set Preferences**: Configure travel style, budget, interests
2. **Ask Questions**: Use natural language for travel queries
3. **Get Recommendations**: Receive personalized travel suggestions
4. **Plan Trips**: Create detailed itineraries with agent assistance
5. **Maintain Context**: Continue conversations with preserved history

This system demonstrates the power of multi-agent collaboration in solving complex, multi-faceted problems while maintaining user context and providing personalized experiences.

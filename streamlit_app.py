import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="Travel Agent Chatbot",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 50%, #FFFFFF 100%);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #3b82f6;
        color: white;
        align-items: flex-end;
    }
    .bot-message {
        background-color: white;
        color: #333;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("⚠️ GROQ_API_KEY not found! Please add it in Streamlit Cloud: Settings → Secrets")
        st.code('GROQ_API_KEY = "your_key_here"')
        st.stop()
    return Groq(api_key=api_key)

try:
    client = get_groq_client()
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("Make sure you added GROQ_API_KEY in Streamlit secrets (⚙️ Settings → Secrets)")
    st.stop()

# Travel keywords
TRAVEL_KEYWORDS = [
    'flight', 'flights', 'airline', 'hotel', 'hotels', 'destination', 'trip', 'travel',
    'tour', 'tourism', 'tourist', 'vacation', 'holiday', 'visa', 'passport', 'booking',
    'bangalore', 'delhi', 'mumbai', 'paris', 'london', 'tokyo', 'europe', 'asia',
    'cheap', 'budget', 'best', 'place', 'visit', 'recommend', 'airport', 'train'
]

GREETING_KEYWORDS = ['hi', 'hello', 'hey', 'hye', 'hii', 'helo', 'greetings']

def is_greeting(message):
    return message.lower().strip() in GREETING_KEYWORDS

def is_travel_related(message):
    return any(keyword in message.lower() for keyword in TRAVEL_KEYWORDS)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! 👋 I'm your travel assistant. Ask me about destinations, flights, hotels, or any travel plans!"}
    ]

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.title("✈️ Travel Agent Chatbot 🌍")
    st.caption("Your AI-powered travel planning assistant")

with col2:
    st.markdown("### Quick Tips")
    st.markdown("🏨 Hotels • ✈️ Flights")
    st.markdown("🗺️ Destinations • 🎫 Bookings")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your travel question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Check greeting
            if is_greeting(prompt):
                response = "Hello! 👋 I'm your travel assistant. How can I help you plan your next adventure? Ask me about flights, hotels, destinations, or any travel plans! ✈️🌍"
            # Check travel-related
            elif not is_travel_related(prompt):
                response = "Sorry! I'm a travel assistant and can only help with travel-related questions. 🌍✈️"
            else:
                # Get AI response
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a friendly travel agent assistant. Help users with flights, hotels, destinations, visas, and travel planning. Keep responses concise (2-4 sentences) and use emojis occasionally. Be enthusiastic about travel!"
                            },
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                        max_tokens=300
                    )
                    response = chat_completion.choices[0].message.content
                except Exception as e:
                    response = "I'm here to help with your travel plans! Ask me about flights, hotels, destinations, or travel tips. 🌍✈️"
            
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

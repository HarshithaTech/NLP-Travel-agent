# Travel Agent Chatbot

A simple web-based chatbot that acts as a travel agent, powered by Google Gemini API.

## Features
- 🌍 Travel-focused chatbot assistant
- ✈️ Answers questions about flights, hotels, destinations, and travel planning
- 🚫 Politely refuses non-travel-related questions
- 💬 Modern, responsive chat interface
- 🎨 Cool landing page

## How the NLP Filtering Works

This project uses a **simple keyword-based intent detection** approach:

1. **Keyword List**: A predefined list of travel-related keywords (flights, hotels, destinations, visa, etc.)

2. **Message Analysis**: When a user sends a message, the `is_travel_related()` function:
   - Converts the message to lowercase
   - Checks if ANY travel keyword appears in the message
   - Returns True if travel-related, False otherwise

3. **Response Logic**:
   - If NOT travel-related → Returns polite refusal message
   - If travel-related → Sends to Google Gemini API with system prompt

4. **Gemini Integration**: The AI model receives:
   - A system prompt defining its role as a travel agent
   - The user's message
   - Generates contextual, helpful travel advice

This approach is beginner-friendly and effective for filtering out non-travel queries while allowing the AI to handle complex travel questions naturally.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   Navigate to: `http://127.0.0.1:5000`

## Project Structure
```
NLP chatbot/
├── app.py              # Flask backend with NLP filtering
├── .env                # API key (keep secure!)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend HTML
└── static/
    └── style.css       # Styling
```

## Usage
1. Click "Start Chatting" on the landing page
2. Ask travel-related questions
3. Get instant AI-powered responses!

## Example Questions
- "What are the best destinations in Europe?"
- "How do I apply for a Schengen visa?"
- "Recommend budget hotels in Tokyo"
- "What's the best time to visit Bali?"

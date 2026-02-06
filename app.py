from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Groq API
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Load system prompt
def load_system_prompt():
    try:
        with open('system_prompt.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "You are a helpful travel agent assistant."

SYSTEM_PROMPT = load_system_prompt()

# Travel-related keywords for intent detection
TRAVEL_KEYWORDS = [
    # Transportation
    'flight', 'flights', 'airline', 'airlines', 'plane', 'aircraft', 'airport', 'airports',
    'train', 'trains', 'railway', 'metro', 'subway', 'bus', 'buses', 'taxi', 'cab', 'uber',
    'ferry', 'cruise', 'ship', 'boat', 'car', 'rental', 'drive', 'road', 'transportation',
    
    # Accommodation
    'hotel', 'hotels', 'motel', 'resort', 'resorts', 'hostel', 'hostels', 'lodge',
    'accommodation', 'stay', 'staying', 'airbnb', 'booking', 'reservation', 'room',
    
    # Travel Activities
    'trip', 'travel', 'tour', 'tours', 'tourism', 'tourist', 'vacation', 'holiday',
    'journey', 'adventure', 'explore', 'visit', 'visiting', 'sightseeing', 'backpack',
    'itinerary', 'package', 'excursion', 'safari', 'trekking', 'hiking', 'camping',
    
    # Documents & Visa
    'visa', 'passport', 'immigration', 'customs', 'border', 'permit', 'document',
    
    # Money & Budget
    'cheap', 'budget', 'expensive', 'price', 'cost', 'currency', 'exchange', 'money',
    'affordable', 'deal', 'discount', 'offer',
    
    # General Travel Terms
    'destination', 'destinations', 'place', 'places', 'country', 'countries', 'city',
    'cities', 'town', 'village', 'island', 'beach', 'beaches', 'mountain', 'mountains',
    'guide', 'map', 'luggage', 'baggage', 'ticket', 'tickets', 'recommend', 'suggestion',
    'best', 'top', 'famous', 'popular', 'must', 'see', 'attraction', 'attractions',
    
    # Flight Types
    'domestic', 'international', 'direct', 'nonstop', 'connecting', 'layover', 'stopover',
    'economy', 'business', 'first', 'class', 'one-way', 'round-trip', 'return',
    
    # Continents & Regions
    'europe', 'asia', 'africa', 'america', 'australia', 'oceania', 'caribbean',
    'middle', 'east', 'southeast', 'south', 'north', 'central', 'western', 'eastern',
    
    # Popular Countries
    'india', 'usa', 'uk', 'france', 'germany', 'italy', 'spain', 'portugal', 'greece',
    'switzerland', 'netherlands', 'belgium', 'austria', 'norway', 'sweden', 'denmark',
    'japan', 'china', 'thailand', 'singapore', 'malaysia', 'indonesia', 'vietnam',
    'philippines', 'korea', 'dubai', 'uae', 'turkey', 'egypt', 'morocco', 'australia',
    'new', 'zealand', 'canada', 'mexico', 'brazil', 'argentina', 'peru', 'chile',
    'russia', 'poland', 'czech', 'hungary', 'croatia', 'iceland', 'ireland', 'scotland',
    
    # Indian Cities
    'bangalore', 'bengaluru', 'delhi', 'mumbai', 'kolkata', 'chennai', 'hyderabad',
    'pune', 'ahmedabad', 'jaipur', 'goa', 'kerala', 'kashmir', 'ladakh', 'manali',
    'shimla', 'udaipur', 'agra', 'varanasi', 'rishikesh', 'darjeeling', 'ooty',
    
    # Famous Cities Worldwide
    'paris', 'london', 'rome', 'barcelona', 'amsterdam', 'berlin', 'vienna', 'prague',
    'budapest', 'venice', 'florence', 'milan', 'madrid', 'lisbon', 'athens', 'santorini',
    'tokyo', 'kyoto', 'osaka', 'bangkok', 'phuket', 'bali', 'hong', 'kong', 'macau',
    'seoul', 'beijing', 'shanghai', 'hanoi', 'manila', 'kuala', 'lumpur', 'jakarta',
    'sydney', 'melbourne', 'auckland', 'toronto', 'vancouver', 'new', 'york', 'los',
    'angeles', 'san', 'francisco', 'las', 'vegas', 'miami', 'chicago', 'boston',
    'washington', 'seattle', 'orlando', 'hawaii', 'cancun', 'rio', 'buenos', 'aires',
    
    # Famous Landmarks & Attractions
    'eiffel', 'tower', 'colosseum', 'louvre', 'vatican', 'sagrada', 'familia',
    'big', 'ben', 'buckingham', 'palace', 'taj', 'mahal', 'great', 'wall', 'pyramids',
    'statue', 'liberty', 'disney', 'disneyland', 'universal', 'studios', 'museum',
    'temple', 'church', 'cathedral', 'mosque', 'fort', 'palace', 'castle', 'park',
    
    # Travel Services
    'makemytrip', 'goibibo', 'cleartrip', 'yatra', 'expedia', 'booking.com', 'agoda',
    'trivago', 'kayak', 'skyscanner', 'google', 'flights', 'tripadvisor',
    
    # Airlines
    'indigo', 'air', 'india', 'spicejet', 'vistara', 'emirates', 'qatar', 'etihad',
    'lufthansa', 'british', 'airways', 'american', 'united', 'delta', 'singapore',
    'cathay', 'pacific', 'ana', 'jal', 'thai', 'malaysia', 'qantas', 'ryanair', 'easyjet',
    
    # Food & Dining
    'restaurant', 'restaurants', 'cafe', 'cafes', 'food', 'cuisine', 'dining', 'eat',
    'breakfast', 'lunch', 'dinner', 'street', 'local', 'dish', 'dishes',
    
    # Weather & Seasons
    'weather', 'climate', 'season', 'summer', 'winter', 'spring', 'autumn', 'fall',
    'monsoon', 'rainy', 'sunny', 'snow', 'temperature', 'when', 'time',
    
    # Travel Tips
    'tip', 'tips', 'advice', 'guide', 'help', 'plan', 'planning', 'prepare', 'pack',
    'packing', 'checklist', 'safety', 'insurance', 'health', 'vaccination', 'vaccine'
]

# Greeting keywords
GREETING_KEYWORDS = ['hi', 'hello', 'hey', 'hye', 'hii', 'helo', 'greetings']

def is_greeting(message):
    """Check if message is a greeting"""
    message_lower = message.lower().strip()
    return message_lower in GREETING_KEYWORDS

def is_travel_related(message):
    """Check if the message contains travel-related keywords"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in TRAVEL_KEYWORDS)

def get_travel_response(user_message):
    """Generate travel responses based on keywords"""
    msg = user_message.lower()
    
    # Flight queries
    if 'flight' in msg or 'airline' in msg:
        if 'bangalore' in msg and 'delhi' in msg:
            return "For flights from Bangalore to Delhi, check IndiGo, Air India, or SpiceJet! ✈️ Flight time is ~2.5 hours. Prices range ₹3,000-8,000. Book on MakeMyTrip or Google Flights for best deals. Tip: Book 2-3 weeks in advance!"
        elif 'cheap' in msg or 'budget' in msg:
            return "Budget airlines for international travel: AirAsia, Scoot, IndiGo (Asia routes), Ryanair & EasyJet (Europe), Spirit & Frontier (USA). ✈️ Book 2-3 months ahead, fly midweek, and use Skyscanner to compare prices!"
        return "For flight bookings, use MakeMyTrip, Goibibo, or Google Flights! ✈️ Pro tips: Book 2-3 weeks ahead for domestic, 2-3 months for international. Fly Tuesday-Thursday for cheaper fares. Clear cookies before booking!"
    
    # Europe destinations
    elif 'europe' in msg or ('place' in msg and 'visit' in msg):
        return "Best places to visit in Europe: 🌍\n1. Paris - Eiffel Tower, Louvre\n2. Rome - Colosseum, Vatican\n3. Barcelona - Sagrada Familia, beaches\n4. Amsterdam - canals, museums\n5. Santorini - stunning sunsets\n\nBest time: April-October. Budget: €50-150/day depending on country!"
    
    # Hotel queries
    elif 'hotel' in msg or 'accommodation' in msg:
        if 'cheap' in msg or 'budget' in msg:
            return "Budget accommodation tips: 🏨 Use Booking.com, Hostelworld, or Airbnb. Stay in hostels (€15-30/night) or budget hotels. Book areas slightly outside city center. Check reviews! Tip: Book directly with hotel for better rates."
        return "For hotels, try Booking.com, Agoda, Hotels.com, or Airbnb! 🏨 Tips: Read reviews, check location on map, book refundable rates when possible. Look for breakfast included deals!"
    
    # Visa queries
    elif 'visa' in msg:
        return "Visa tips: 📝 Check official embassy websites for requirements. Apply 1-2 months before travel. Common docs: passport (6 months validity), photos, bank statements, travel insurance, flight bookings. Schengen visa covers 27 European countries!"
    
    # Best time to visit
    elif 'best time' in msg or 'when to visit' in msg:
        return "Best travel times: 🌞\n- Europe: April-October\n- Southeast Asia: November-March\n- India: October-March\n- Japan: March-May (cherry blossoms)\n- Australia: September-November\n\nAvoid peak season (July-August) for better prices!"
    
    # General travel advice
    else:
        return "I'm here to help with your travel plans! ✈️🌍 Ask me about:\n- Flight bookings & airlines\n- Hotel recommendations\n- Destination suggestions\n- Visa information\n- Travel tips & budgets\n- Best times to visit\n\nWhat would you like to know?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check if message is a greeting
        if is_greeting(user_message):
            return jsonify({
                'response': "Hello! 👋 I'm your travel assistant. How can I help you plan your next adventure? Ask me about flights, hotels, destinations, or any travel plans! ✈️🌍"
            })
        
        # Check if message is travel-related
        if not is_travel_related(user_message):
            return jsonify({
                'response': "Sorry! I'm a travel assistant and can only help with travel-related questions. 🌍✈️"
            })
        
        # Create chat completion with Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly travel agent assistant. Help users with flights, hotels, destinations, visas, and travel planning. Keep responses concise (2-4 sentences) and use emojis occasionally. Be enthusiastic about travel!"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300
        )
        
        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # Fallback to keyword-based response
        bot_response = get_travel_response(user_message)
        return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)

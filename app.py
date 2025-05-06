from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain, Miner, Transaction
from dotenv import load_dotenv
from skyfield.api import load as sky_load
import openai
import os
import requests
import datetime as date

# Load environment variables from .env file
load_dotenv()


# Initialize Flask app
app = Flask(__name__)
blockchain = Blockchain()
miner = Miner("MissionControl_Miner")

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# NASA API credentials
NASA_API_KEY=os.getenv("NASA_API_KEY")

# Space-Track credentials
SPACE_TRACK_USERNAME=os.getenv("SPACE_TRACK_USERNAME")
SPACE_TRACK_PASSWORD=os.getenv("SPACE_TRACK_PASSWORD")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_ai_response():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        ai_output = response.choices[0].message.content

        # Log AI transaction
        tx = Transaction(
            sender="MissionControlAI",
            receiver="Engineer",
            amount=f"Prompt: {prompt} | Response: {ai_output}",
            timestamp=date.datetime.now(),
            content_hash=blockchain.hash_data(prompt + ai_output),
            metadata={"type": "AI_Generated", "model": "gpt-4"}
        )
        blockchain.add_transaction(tx)

        return jsonify({
            "prompt": prompt,
            "response": ai_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mine', methods=['GET'])
def mine_block():
    blockchain.mine_block(miner)
    return jsonify({"message": "Block mined!", "miner_balance": miner.balance})

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": str(block.timestamp),
            "transactions": [
                {
                    "sender": tx.sender,
                    "receiver": tx.receiver,
                    "amount": tx.amount,
                    "timestamp": str(tx.timestamp),
                    "hash": tx.content_hash,
                    "metadata": tx.metadata
                } for tx in block.transactions
            ],
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify(chain_data)

# Real-Time Space Data Routes

@app.route('/nasa-data')
def nasa_data():
    params = {
        'lat': 28.7041,
        'lon': 77.1025,
        'dim': 0.1,
        'api_key': NASA_API_KEY
    }
    try:
        r = requests.get("https://api.nasa.gov/planetary/earth/assets",params=params)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error":str(e)})
    
@app.route('/celestrak')
def celestrak_tle():
    try:
        response = requests.get("https://celestrak.org/NORAD/elements/stations.txt")
        lines = response.text.strip().split("\n")
        return jsonify({"tle_lines":lines})
    except Exception as e:
        return jsonify({"error":str(e)})
    
@app.route('/space-track')
def space_track_data():
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = "https://www.space-track.org/basicspacedata/query/class/satcat/format/json"
    try:
        session = requests.Session()
        session.post(login_url, data={
            'identity': SPACE_TRACK_USERNAME,
            'password': SPACE_TRACK_PASSWORD
        })
        r = session.get(query_url)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get-iss-location', methods=['GET'])
def get_iss_location():
    try:
        # Fetch data from the real-time ISS location API (Open Notify or another provider)
        response = requests.get('http://api.open-notify.org/iss-now.json')
        data = response.json()

        # If data is valid, send it to the front-end
        if data.get("message") == "success":
            iss_location = {
                'latitude': data['iss_position']['latitude'],
                'longitude': data['iss_position']['longitude'],
                'altitude': '400 km',  # Example static value, update with real data if available
                'velocity': '28,000 km/h'  # Example static value, update with real data if available
            }
            return jsonify(iss_location)
        else:
            return jsonify({"error": "Unable to fetch ISS location."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start app
if __name__ == '__main__':
    app.run(debug=True)
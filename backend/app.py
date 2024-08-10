from flask import Flask, request, jsonify
import logging
import requests
from contracts.state_machine_contract import deploy_contract
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Deploy contract
contract = deploy_contract()

# Initialize agent endpoints
supplier_url = "http://127.0.0.1:8001/submit"
manufacturer_url = "http://127.0.0.1:8002/submit"
distributor_url = "http://127.0.0.1:8003/submit"
retailer_url = "http://127.0.0.1:8004/submit"

@app.route('/')
def index():
    return "Supply Chain Management API is running"

@app.route('/order', methods=['POST'])
def place_order():
    try:
        data = request.get_json()
        if 'order' not in data:
            return jsonify({"error": "Missing 'order' in request"}), 400
        order = data['order']
        item = order.get('item')
        quantity = order.get('quantity')
        if not item or not isinstance(quantity, int):
            return jsonify({"error": "Invalid order format"}), 400
        return jsonify({"status": "Order placed"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to place order. Error: {str(e)}"}), 400

@app.route('/send_materials', methods=['POST'])
def send_materials():
    try:
        response = requests.post(supplier_url, json={"order": {"item": "raw materials", "quantity": 100}})
        response.raise_for_status()
        materials = response.json().get('materials')
        if materials:
            return jsonify({"status": "Materials sent to Manufacturer"}), 200
        return jsonify({"error": "Failed to send materials"}), 400
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Supplier Agent failed: {e}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

@app.route('/manufacture_goods', methods=['POST'])
def manufacture_goods():
    try:
        response = requests.post(manufacturer_url, json={"materials": "raw materials"})
        response.raise_for_status()
        message = response.json().get('message')
        if message:
            return jsonify({"status": "Goods manufactured"}), 200
        return jsonify({"error": "Failed to manufacture goods"}), 400
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Manufacturer Agent failed: {e}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

@app.route('/distribute_goods', methods=['POST'])
def distribute_goods():
    try:
        response = requests.post(distributor_url, json={"goods": "manufactured goods"})
        response.raise_for_status()
        message = response.json().get('message')
        if message:
            return jsonify({"status": "Goods distributed"}), 200
        return jsonify({"error": "Failed to distribute goods"}), 400
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Distributor Agent failed: {e}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

@app.route('/receive_goods', methods=['POST'])
def receive_goods():
    try:
        response = requests.post(retailer_url, json={"goods": "distributed goods"})
        response.raise_for_status()
        message = response.json().get('message')
        if message:
            return jsonify({"status": "Goods received"}), 200
        return jsonify({"error": "Failed to receive goods"}), 400
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Retailer Agent failed: {e}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000)

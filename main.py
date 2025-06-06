from flask import Flask, jsonify
from scraper import scrape_events
import os

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_route():
    data = scrape_events()
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Get PORT from Railway
    app.run(host='0.0.0.0', port=port)

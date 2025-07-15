from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
ASSET_FILE = "assets.json"

def load_assets():
    if not os.path.exists(ASSET_FILE):
        with open(ASSET_FILE, 'w') as f:
            json.dump({}, f)
    with open(ASSET_FILE, 'r') as f:
        return json.load(f)

def save_assets(data):
    with open(ASSET_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ''
    if request.method == 'POST':
        serial = request.form['serial'].strip().upper()
        new_location = request.form['location']
        assets = load_assets()

        if serial in assets:
            assets[serial]['location'] = new_location
            msg = f"✅ Serial {serial} moved to '{new_location}'."
        else:
            # Auto-create if not found (optional)
            assets[serial] = {
                "group": "Unknown",
                "location": new_location
            }
            msg = f"➕ Serial {serial} not found. Added and moved to '{new_location}'."

        save_assets(assets)

    return render_template('index.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)


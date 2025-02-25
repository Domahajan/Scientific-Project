from flask import Flask, request, jsonify, render_template
import util
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    locations = [loc.title() for loc in util.get_location_names()]
    response = jsonify({
        'locations': locations
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



@app.route('/predict_price', methods=['POST'])
def predict_price():
    try:
        print("Request Data:", request.form)

        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Ensure the returned value is a Python float
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        estimated_price = float(np.round(estimated_price, 2))  # Convert to standard float

        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print("Error:", str(e))  # Log error
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()
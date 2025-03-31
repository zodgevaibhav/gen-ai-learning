from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

classes = ['setosa', 'versicolor', 'virginica']

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = data.get('features')

    if features is None:
        return jsonify({'error': 'Missing features in request'}), 400
    
    try:
        # Load the model
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)

        # Make prediction
        prediction = model.predict([features])

        return jsonify({'prediction': classes[int(prediction[0])]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8083, debug=True)

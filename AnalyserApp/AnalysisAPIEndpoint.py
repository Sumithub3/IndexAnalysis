from flask import Flask, jsonify
import pickle
from flask_cors import CORS


app = Flask(__name__)
# Configure CORS to allow only specific origins
CORS(app, resources={r"/*": {"origins": "http://allowed-origin.com"}})
@app.route('/', methods=['GET'])
def json_response():
    data = None
    with open(r"D:\IndexDataAnalysisAutomation\AnalysisData.pkl", "rb") as f:
        data = pickle.load(f)
    return jsonify(data)

if __name__ == '__main__':
    # app.run(host='192.168.1.5', port=816)
    app.run(host='0.0.0.0', port=810)


# if __name__ == '__main__':
#     app.run(debug=True)


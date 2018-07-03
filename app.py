from flask import Flask,abort,jsonify,request
import numpy as np
from sklearn.externals import joblib
from flask_cors import CORS


model = joblib.load("./LM_33%_split_model_python3.pkl")

#creating web service running on port 8000, answer POST requests
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://testing-cost-predictor.firebaseapp.com"}})

@app.route("/fitOutCostPrediction", methods=['GET'])

#prediction function
def make_predict():

    if request.method =='GET':
        try:
            #expecting user imput as a json file with a title 'volume'
            data = request.get_json()
            user_data = request.args.get('volume')
                           
        except ValueError:
            return jsonify("error text here")

        #return a single prediction and convert to json
        cost_pred=model.predict(user_data).tolist()
        return json.dumps({'cost':cost_pred});
        #return jsonify({'cost':cost_pred});
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

from flask import Flask, render_template, url_for, request
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import numpy as np
import joblib


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    reflectance_classifier = open('monarchsexclass.pkl','rb')
    clf = joblib.load(reflectance_classifier)

    if request.method == 'POST':
        scan_raw = request.form['scan']
        scan = scan_raw.split(',')
        result = clf.predict(np.array(scan).reshape(1,-1))
        if result == 'F':
            my_prediction = 1
        else:
            my_prediction = 0
    return render_template('result.html', prediction = my_prediction)

if __name__ == '__main__':
    app.run(debug=True)
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

sales = pickle.load(open('sales.pkl', 'rb'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if not username or not email or not password:
                flash("All fields are required!", "error")
                return redirect('/register')
            print(f"Registered user: {username}, {email}")
            flash("Registration successful!", "success")
            return redirect('/login')
        except KeyError:
            flash("Invalid form data!", "error")
            return redirect('/register')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash("All fields are required!", "error")
                return redirect('/login')
            print(f"Login attempt: {username}, {password}")
            flash("Login successful!", "success")
            return redirect('/upload')
        except KeyError:
            flash("Invalid form data!", "error")
            return redirect('/login')
    return render_template('login.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview', methods=["POST"])
def preview():
    if request.method == 'POST':
        try:
            dataset = request.files['datasetfile']
            df = pd.read_csv(dataset, encoding='unicode_escape')
            df.set_index('Id', inplace=True)
            return render_template("preview.html", df_view=df)
        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return redirect('/upload')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods=['POST'])
def predict():
	int_feature = [x for x in request.form.values()]
	print(int_feature)
	int_feature = [float(i) for i in int_feature]
	final_features = [np.array(int_feature)]
	prediction = sales.predict(final_features)

	output =format(float(prediction[0]))
	print(output)  
	result =float(output) * float(output) * float(output)
	return render_template('prediction.html', prediction_text= int(result))


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/logout')
def logout():
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)



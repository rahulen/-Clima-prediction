from flask import Flask,render_template,request,redirect, url_for
import mysql.connector
import json
import pandas as pd
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.metrics import mean_squared_error, r2_score # type: ignore

from flask_cors import CORS, cross_origin

app=Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/regdata')
def regdata():
	nm=request.args['stname']
	em=request.args['email']
	ph=request.args['phone']
	gen=request.args['gender']
	addr=request.args['addr1']
	pwd=request.args['pswd']
	connection = mysql.connector.connect(host='localhost',database='climatedb',user='root',password='')
	sqlquery="insert into userdata(uname,email,phone,gender,addr,pswd) values('"+nm+"','"+em+"','"+ph+"','"+gen+"','"+addr+"','"+pwd+"')"
	print(sqlquery)
	cursor = connection.cursor()
	try:
		cursor.execute(sqlquery)
	except mysql.connector.IntegrityError:
		connection.commit()
		cursor.close()
		connection.close()
		msg="Email already present"
		resp=json.dumps(msg)
		return resp
	connection.commit()
	cursor.close()
	connection.close()
	msg="Data Saved Successfully"
	resp=json.dumps(msg)
	return resp

@app.route('/logdata')
def logdata():
	em=request.args['email']
	pwd=request.args['pswd']
	msg=''
	connection = mysql.connector.connect(host='localhost',database='climatedb',user='root',password='')
	sqlquery="select count(*) from userdata where email='"+em+"' and pswd='"+pwd+"'"
	cursor = connection.cursor()
	cursor.execute(sqlquery)
	data=cursor.fetchall()
	if data[0][0]>0:
		msg='success'
	else:
		msg='failure'
	cursor.close()
	connection.close()
	resp=json.dumps(msg)
	return resp

@app.route('/dashboard')
def dashboard():
    connection = mysql.connector.connect(host='localhost',database='climatedb',user='root',password='')
    sqlquery="select date,meantemp from dataset"
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    rows=cursor.fetchall()
    dt1=[{"date": row[0], "meantemp": float(row[1])} for row in rows]
    sqlquery="select date,humidity from dataset"
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    rows=cursor.fetchall()
    dt2=[{"date": row[0], "humidity": float(row[1])} for row in rows]
    sqlquery="select date,wind_speed from dataset"
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    rows=cursor.fetchall()
    dt3=[{"date": row[0], "wind_speed": float(row[1])} for row in rows]
    sqlquery="select date,meanpressure from dataset"
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    rows=cursor.fetchall()
    dt4=[{"date": row[0], "meanpressure": float(row[1])} for row in rows]
    cursor.close()
    connection.close()
    return render_template('dashboard.html',dt1=dt1,dt2=dt2,dt3=dt3,dt4=dt4)


@app.route('/predictdata')
def predictdata():
    date = request.args['date']
    future_date = pd.to_datetime(date,format="%Y-%m-%d")
    print("-"*50)
    print(f"{future_date}")
    print("-"*50)

    connection = mysql.connector.connect(host='localhost',database='climatedb',user='root',password='')
    sqlquery="select * from dataset"
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    dataset=cursor.fetchall()
    cursor.close()
    connection.close()
    columns = ['date','mean_temp','humidity','wind_speed','meanpressure']
    df = pd.DataFrame(dataset,columns = columns)
    df['date'] = pd.to_datetime(df['date'],format="%Y-%m-%d")
    df[['mean_temp', 'humidity', 'wind_speed', 'meanpressure']] = df[['mean_temp', 'humidity', 'wind_speed', 'meanpressure']].astype(float)
    print(type(df))
    print(df)
    
    X = df[['date']]
    y = df['mean_temp']

    X1 = df[['date']]
    y1 = df['humidity']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.2, random_state=42)
    

    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_regressor1 = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the classifier
    rf_regressor.fit(X_train, y_train)
    rf_regressor1.fit(X_train1, y_train1)
    
    # Make predictions on the test set
    y_pred = rf_regressor.predict(X_test)
    y_pred1 = rf_regressor1.predict(X_test1)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    mse1 = mean_squared_error(y_test1, y_pred1)
    r2 = r2_score(y_test, y_pred)
    r21 = r2_score(y_test1, y_pred1)
    
    # Print the results
    print('-'*50)
    print(f"Mean Squared Error of mean_temp: {mse:.2f}")
    print(f"R-squared Score of mean_temp: {r2:.2f}")
    print('-'*50)
    print(f"Mean Squared Error of humidity: {mse1:.2f}")
    print(f"R-squared Score of humidity: {r21:.2f}")
    print('-'*50)

    # Prediction
    future_date = pd.DataFrame([future_date],columns=['date'])
    pred = rf_regressor.predict(future_date)
    pred1 = rf_regressor1.predict(future_date)
    print(pred)
    print(pred1)
    msg={'mean_temp': pred[0], 'humidity': pred1[0]}
    resp=json.dumps(msg)
    print(resp)
    return resp
    

if __name__=="__main__":
    app.run(debug=True)

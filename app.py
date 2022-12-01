from flask import Flask, redirect,render_template,request,url_for,make_response
import requests
import pandas as pd
import sqlite3


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@app.route('/data',methods=['GET','POST'])
def results():
    cat = request.form.get('category')
    desc = request.form.get('description')
    pri = request.form.get('price')
    co = request.form.get('code')
    to_insert = (cat,desc,pri,co)
    with sqlite3.connect('mydb.db') as con:
        con.execute('CREATE TABLE IF NOT EXISTS product(Category TEXT NOT NULL, Descriptions TEXT NOT NULL,Price INTEGER NOT NULL,Code TEXT NOT NULL UNIQUE)')
        con.commit()
        con.execute("INSERT INTO product VALUES(?,?,?,?)",to_insert)
    return render_template("homepage.html")

@app.route('/tableCreate',methods=['GET','POST'])
def renderTable():
    return render_template('tableRender.html')

@app.route('/tableDisplay',methods=['GET','POST'])
def displayTable():
    cat2 = request.form.get('cat2')
    with sqlite3.connect('mydb.db') as con:
        if(cat2 != ""):
            df = pd.read_sql("SELECT * FROM product WHERE category = ? ",con,params=(cat2,))
        else:
            df = pd.read_sql("SELECT * FROM product",con)
    return render_template('displayData.html',df=df)

if __name__ == '__main__':
    app.run(debug=True,port=8080)
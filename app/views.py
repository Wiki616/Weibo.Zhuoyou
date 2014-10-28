from flask import render_template, flash, redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib

@app.route('/')
@app.route('/index')
def index():
        return render_template("index.html")
<<<<<<< HEAD
@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
<<<<<<< HEAD
        cookie = request.cookies.get('username')
        if (cookie == resp.
=======
        #cookie = request.cookies.get('username')
        #if (cookie == resp.
>>>>>>> d13fdbf11e018e7c6e6afdf21ddcb3772b73dbb0
=======
@app.route('/welcome',methods=['POST','GET'])
def welcome():
>>>>>>> 803f2e15234c4c893ec63498a6a5d8f283b2db25
        if request.method == 'POST':
                resp = make_response(render_template('index.html'))
                resp.set_cookie('username',request.form['username'])
                resp.set_cookie('nickname',request.form['nickname'])
                miss = models.User.query.filter_by(username=request.form['username']).first()
                if miss == None:
                        m = hashlib.md5()
                        m.update(request.form['password'])
                        psw = m.hexdigest()
                        psw = request.form['password']
                        user = models.User(username=request.form['username'] , nickname=request.form['nickname'] ,email='null',password=psw)
                        db.session.add(user)
                        db.session.commit()
                        return render_template("welcome.html",nickname=request.cookies.get('nickname'))
                return render_template("error.html")
        return render_template("welcome.html")
@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
        #return render_template("profile.html",nickname=request.form['nickname'])
        return render_template("profile.html",nickname=request.cookies.get('nickname'))
@app.route('/settings/account')
def account():
        return render_template("account.html")
@app.route('/settings/following')
def following():
        return render_template("following.html")
@app.route('/update',methods=['POST','GET'])
def update():
        if request.method == 'POST':
                ret = request.form['nickname']
                return render_template("profile.html",nickname=ret)
<<<<<<< HEAD
        return render_template("profile.html")
<<<<<<< HEAD
=======
@app.route('/home',methods=['POST','GET'])
def home():
        return render_template("home.html")
>>>>>>> d13fdbf11e018e7c6e6afdf21ddcb3772b73dbb0
=======
        return render_template("error.html")
@app.route('/home',methods=['POST','GET'])
def home():
        if request.method == 'POST':
                resp = make_response(render_template('index.html'))
                resp.set_cookie('username',request.form['username2'])
                m = hashlib.md5()
                m.update(request.form['password2'])
                psw = m.hexdigest()
                psw = request.form['password2']
                miss = models.User.query.filter_by(username=request.form['username2']).first()
                if psw == miss.password:
                        return render_template("home.html",nickname=miss.nickname)
                return render_template("error.html")
        return render_template("error.html")
>>>>>>> 803f2e15234c4c893ec63498a6a5d8f283b2db25

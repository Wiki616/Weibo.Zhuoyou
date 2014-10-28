from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib

def convertmd5(origin):
        m = hashlib.md5()
        m.update(origin)
        psw = m.hexdigest()
        return psw

@app.route('/')
@app.route('/index')
def index():
        return render_template("index.html")
@app.route('/logout')
def logout():
        session.pop('username',None)
        return render_template("index.html")
@app.route('/welcome',methods=['POST','GET'])
def welcome():
        if request.method == 'POST':
                resp = make_response(render_template('index.html'))
                session['username'] = request.form['username']
                miss = models.User.query.filter_by(username=request.form['username']).first()
                if miss == None:
                        psw = convertmd5(request.form['password'])
                        user = models.User(username=request.form['username'] , nickname=request.form['nickname'] ,email='null',password=psw)
                        db.session.add(user)
                        db.session.commit()
                        return render_template("welcome.html",nickname=session['username'])
                return render_template("error.html")
        return render_template("welcome.html")
@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
        #Username = request.cookies.get('username')
        ret = models.User.query.filter_by(username=session['username']).first()
        #return render_template("profile.html",nickname=request.form['nickname'])
        return render_template("profile.html",nickname=ret.nickname)
@app.route('/settings/account')
def account():
        ret = models.User.query.filter_by(username=session['username']).first() 
        return render_template("account.html",nickname=ret.nickname)
@app.route('/settings/following')
def following():
        ret = models.User.query.filter_by(username=session['username']).first()
        return render_template("following.html",nickname=ret.nickname)
@app.route('/settings/donate')
def donate():
        return render_template("donate.html")
@app.route('/update1',methods=['POST','GET'])
def update1():
        if request.method == 'POST':
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                ret.nickname = request.form['nickname']
                ret.email = request.form['email']
                db.session.commit()
                return render_template("update.html")
        return render_template("error.html")
@app.route('/update2',methods=['POST','GET'])
def update2():
        if request.method == 'POST':
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                psw1 = convertmd5(request.form['oldpassword'])
                if ret.password == psw1:
                        psw2 = convertmd5(request.form['newpassword'])
                        ret.password = psw2
                        db.session.commit()
                        return render_template("update.html")
                return render_template("error.html")
        return render_template("error.html")
@app.route('/home',methods=['POST','GET'])
def home():
        if request.method == 'POST':
                session['username'] = request.form['username2']
                psw = convertmd5(request.form['password2'])
                miss = models.User.query.filter_by(username=request.form['username2']).first()
                if psw == miss.password:
                        return render_template("home.html",nickname=miss.nickname)
                return render_template("error.html")
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("home.html",nickname=ret.nickname)

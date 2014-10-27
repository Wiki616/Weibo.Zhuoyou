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
@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
        #cookie = request.cookies.get('username')
        #if (cookie == resp.
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
                        return render_template("profile.html",nickname=request.form['nickname'])
                return render_template("error.html")
                #return render_template("profile.html",nickname=request.form['nickname'])
        return render_template("profile.html",nickname='null')
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
        return render_template("profile.html")
@app.route('/talk',methods=['POST','GET'])
def talk():
        return render_template("talk.html")

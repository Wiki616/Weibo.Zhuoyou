from flask import render_template, flash, redirect,request,make_response
from app import app
import httplib
import urllib , urllib2
import json
import uuid

@app.route('/')
@app.route('/index')
def index():
        return render_template("index.html")
@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
        if request.method == 'POST':
                resp = make_response(render_template('index.html'))
                resp.set_cookie('username',request.form['username'])
                resp.set_cookie('nickname',request.form['nickname'])
                return render_template("profile.html",nickname=request.form['nickname'])
        return render_template("profile.html",nickname='null')
@app.route('/settings/account')
def account():
        return render_template("account.html")
@app.route('/settings/friend')
def friend():
        return render_template("friend.html")

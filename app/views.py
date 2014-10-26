from flask import render_template, flash, redirect,request
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
        return render_template("profile.html")
@app.route('/settings/account')
def account():
        return render_template("account.html")
@app.route('/settings/friend')
def friend():
        return render_template("friend.html")

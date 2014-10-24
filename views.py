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

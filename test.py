from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random

posts2 = models.Weibo.query.filter_by(content = 'AAA').all()
for post in posts2:
    print post.content


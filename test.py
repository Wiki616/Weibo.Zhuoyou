from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random

username = 'Wiki_ki'
url = "/static/pic/head" + str(ord(username[0]) % 9) + ".jpg"
print url

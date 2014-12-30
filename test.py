from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random

pall = models.Weibo.query.filter_by().all()
posts = random.sample(pall,9)
posts1 = post[0:3]
posts2 = post[3:6]
posts3 = post[6:9]

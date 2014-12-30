from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random

ans = [session['username']]
ans = ans + ['xq']
for ele in friend:
    ans = ans + ele.followname
posts = []
for ele in ans:
    posts = posts + models.Weibo.query.filter_by(username = ele,wtype="o").all()
posts = sorted(posts, key = lambda d: d.potime, reverse = True)
print posts

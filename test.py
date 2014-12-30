from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random
friend = models.Follow.query.filter_by().all()
ans = ['a']
for ele in friend:
    ans = ans + ele.followname
print ans

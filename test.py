from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random

username = "Wiki_ki"
friend = models.Follow.query.filter_by(username='cdfgsv').all()
print friend
for ele in friend:
    if ele.followname == username:
        print ele.followname

from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random

point = 50
models.User.query.filter_by(username = 'Wiki_ki').update({point : point})
db.session.commit()

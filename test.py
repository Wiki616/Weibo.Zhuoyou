# -*- coding:utf-8 -*-
from flask import render_template, flash, session , redirect,request,make_response
from app import app , db , models
import httplib
import urllib , urllib2
import json
import uuid
import hashlib
import time
import random
import HTMLParser

susername = 'dddd'
rusername = 'Wiki_ki'
content = 'dsggsgdsghshsshsh'
potime = time.strftime(ISOTIMEFORMAT, time.localtime())
idweibo = ssername + potime + str(len(content))
wtype = "l"
fatherid = "null"
number = 0
url = ret.url
weibo = models.Weibo(url = url , username = susername , potime = potime ,content = content , idweibo = idweibo, wtype = wtype , fatherid = fatherid ,number = number)
db.session.add(weibo)
db.session.commit()
imessage = idweibo+susername
message = models.Message(susername = susername , rusername = rusername , idweibo = idweibo , imessage = imessage)
db.session.add(message)
db.session.commit()

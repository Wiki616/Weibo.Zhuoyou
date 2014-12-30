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

ISOTIMEFORMAT='%Y/%m/%d-%X'

def convertmd5(origin):
        m = hashlib.md5()
        m.update(origin)
        psw = m.hexdigest()
        return psw

@app.route('/')
@app.route('/index')
def index():
        return render_template("index.html")

@app.route('/logout')
def logout():
        session.pop('username',None)
        return render_template("index.html")

@app.route('/result',methods=['POST','GET'])
def result():
        if request.method == 'POST':
                query = request.form['query']
                posts = models.User.query.filter_by(username = query).all()
                posts2 = models.Weibo.query.filter_by(content = query).all()
                return render_template("result.html" , posts = posts , posts2 = posts2)
        return render_template("result.html")

@app.route('/settings/follows')
def follows():
        return render_template("follows.html")

@app.route('/welcome',methods=['POST','GET'])
def welcome():
        if request.method == 'POST':
                resp = make_response(render_template('index.html'))
                session['username'] = request.form['username']
                miss = models.User.query.filter_by(username=request.form['username']).first()
                if miss == None:
                        psw = convertmd5(request.form['password'])
                        user = models.User(username=request.form['username'] , nickname=request.form['nickname'] ,email='null',password=psw)
                        db.session.add(user)
                        db.session.commit()
                        return render_template("welcome.html",nickname=session['username'])
                return render_template("error.html")
        return render_template("welcome.html")

@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
        #Username = request.cookies.get('username')
        ret = models.User.query.filter_by(username=session['username']).first()
        #return render_template("profile.html",nickname=request.form['nickname'])
        return render_template("profile.html",nickname=ret.nickname)

@app.route('/settings/account')
def account():
        ret = models.User.query.filter_by(username=session['username']).first() 
        return render_template("account.html",nickname=ret.nickname)

@app.route('/settings/following')
def following():
        ret = models.User.query.filter_by(username=session['username']).first()
        return render_template("following.html",nickname=ret.nickname)

@app.route('/settings/donate')
def donate():
        return render_template("donate.html")

@app.route('/update1',methods=['POST','GET'])
def update1():
        if request.method == 'POST':
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                ret.nickname = request.form['nickname']
                ret.email = request.form['email']
                db.session.commit()
                return render_template("update.html")
        return render_template("error.html")

@app.route('/update2',methods=['POST','GET'])
def update2():
        if request.method == 'POST':
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                psw1 = convertmd5(request.form['oldpassword'])
                if ret.password == psw1:
                        psw2 = convertmd5(request.form['newpassword'])
                        ret.password = psw2
                        db.session.commit()
                        return render_template("update.html")
                return render_template("error.html")
        return render_template("error.html")

@app.route('/home',methods=['POST','GET'])
def home():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                friend = models.Follow.query.filter_by(username=session['username']).all()
                ans = [session['username']]
                ans = ans + ['Admin']
                for ele in friend:
                        ans = ans + ele.followname
                posts = []
                for ele in ans:
                        posts = posts + models.Weibo.query.filter_by(username = ele,wtype="o").all()
                posts = sorted(posts, key = lambda d: d.potime, reverse = True)
                follows = len(models.Follow.query.filter_by(followname = Username).all())
                topic = len(models.Weibo.query.filter_by(username = Username).all())
                following = len(models.Follow.query.filter_by(username = Username).all())

                if request.method == 'POST':
                        username = Username
                        potime = time.strftime(ISOTIMEFORMAT, time.localtime())
                        content = request.form['content']
                        idweibo = Username + potime + str(len(content))
                        wtype = "o"
                        fatherid = "null"
                        number = 0
                        weibo = models.Weibo(username = username , potime = potime , content = content , idweibo = idweibo ,wtype = wtype ,fatherid=fatherid , number=number)
                        db.session.add(weibo)
                        db.session.commit()
                        return render_template("home.html",posts=posts,ret=ret,nickname=ret.nickname,topic=topic,follows=follows,following=following) 
                return render_template("home.html",posts=posts,ret=ret,nickname=ret.nickname,topic=topic,follows=follows,following=following)
        
        if request.method == 'POST':
                session['username'] = request.form['username2']
                psw = convertmd5(request.form['password2'])
                miss = models.User.query.filter_by(username=request.form['username2']).first()
                if psw == miss.password:
                        friend = models.Follow.query.filter_by(username=session['username']).all()
                        ans = [session['username']]
                        ans = ans + ['Admin']
                        for ele in friend:
                                ans = ans + ele.followname
                        posts = []
                        for ele in ans:
                                posts = posts + models.Weibo.query.filter_by(username = ele,wtype="o").all()
                        posts = sorted(posts, key = lambda d: d.potime, reverse = True)
                        follows = len(models.Follow.query.filter_by(followname = session['username']).all())
                        topic = len(models.Weibo.query.filter_by(username = session['username']).all())
                        following = len(models.Follow.query.filter_by(username = session['username']).all())
                        return render_template("home.html",posts=posts,ret=miss,nickname=miss.nickname,topic=topic,follows=follows,following=following)
                return render_template("error.html")
        return render_template("error.html")

@app.route('/homepage')
def homepage():
        if request.args.get('uid') == 'self':
                if 'username' in session:
                        username = session['username']
                else:
                        return render_template("error.html")
                posts = models.Weibo.query.filter_by(username=username,wtype="o").all()
                posts.reverse()
                ret = models.User.query.filter_by(username=username).first()
                return render_template("homepage.html",posts=posts,ret = ret , nickname=ret.nickname)
        else:
                username = request.args.get('uid')
                posts = models.Weibo.query.filter_by(username=username,wtype="o").all()
                posts.reverse()
                ret = models.User.query.filter_by(username=username).first()
                return render_template("homepage.html",posts=posts,ret = ret, nickname=ret.nickname)
        return render_template("error.html")

@app.route('/message/letter')
def message():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("letter.html",nickname=ret.nickname)
        return render_template("error.html")

@app.route('/message/atme')
def atme():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("atme.html",nickname=ret.nickname)
        return render_template("error.html")

@app.route('/message/commit')
def commit():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("commit.html",nickname=ret.nickname)

@app.route('/system')
def system():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                if ret.role == 1:
                        return render_template("system.html",nickname=ret.nickname)
                else:
                        return render_template("error.html")
        return render_template("error.html")

@app.route('/square')
def square():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                pall = models.Weibo.query.filter_by().all()
                #length = len(pall)
                posts = random.sample(pall,9)
                posts1 = posts[0:3]
                posts2 = posts[3:6]
                posts3 = posts[6:9]
                return render_template("square.html",posts1=posts1,posts2=posts2,posts3=posts3,nickname=ret.nickname)
        return render_template("square.html")

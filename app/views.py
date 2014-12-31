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

ISOTIMEFORMAT='%Y/%m/%d-%X'

def decodeHtml(input):
    h = HTMLParser.HTMLParser()
    s = h.unescape(input)
    return s

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
                if 'username' in session:
                        Username = session['username']
                        ret = models.User.query.filter_by(username=Username).first()
                        return render_template("result.html" , ret = ret , nickname = ret.nickname , posts = posts , posts2 = posts2)
                return render_template("result.html" , ret = ret , nickname = ret.nickname , posts = posts , posts2 = posts2)
        return render_template("error.html")

@app.route('/settings/follows')
def follows():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                friend = models.Follow.query.filter_by(followname=Username).all()
                posts = []
                for ele in friend:
                        posts = posts + [models.User.query.filter_by(username=ele.username).first()]
                return render_template("follows.html",posts=posts,ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/welcome',methods=['POST','GET'])
def welcome():
        if request.method == 'POST':
                resp = make_response(render_template('index.html'))
                session['username'] = request.form['username']
                miss = models.User.query.filter_by(username=request.form['username']).first()
                if miss == None:
                        psw = convertmd5(request.form['password'])
                        username = request.form['username']
                        url = "/static/pic/head" + str(ord(username[0]) % 9) + ".jpg"
                        user = models.User(role = 1 ,url = url , username=username , nickname=request.form['nickname'] ,email='null',password=psw)
                        db.session.add(user)
                        db.session.commit()
                        return render_template("welcome.html",ret=miss,nickname=session['username'])
                return render_template("error.html")
        return render_template("welcome.html")

@app.route('/settings',methods=['POST','GET'])
@app.route('/settings/profile',methods=['POST','GET'])
def profile():
        error = None
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
        #Username = request.cookies.get('username')
        #return render_template("profile.html",nickname=request.form['nickname'])
                return render_template("profile.html",ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/settings/account')
def account():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("account.html",ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/settings/following')
def following():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                friend = models.Follow.query.filter_by(username=Username).all()
                posts = []
                for ele in friend:
                        posts = posts + [models.User.query.filter_by(username=ele.followname).first()]
                l = len(posts)
                posts1 = posts[:l/2]
                n = l/2
                m = l - n
                posts2 = posts[l/2:]
                return render_template("following.html",n = n , m = m ,posts1=posts1,posts2=posts2,ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/settings/donate')
def donate():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("donate.html",ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/update1',methods=['POST','GET'])
def update1():
        if request.method == 'POST':
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                ret.nickname = request.form['nickname']
                ret.email = request.form['email']
                db.session.commit()
                return render_template("update.html",ret=ret)
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
                        return render_template("update.html",ret=ret)
                return render_template("error.html")
        return render_template("error.html")

@app.route('/home',methods=['POST','GET'])
def home():
        """

        :rtype : object
        """
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                if request.method == 'POST':
                        username = Username
                        potime = time.strftime(ISOTIMEFORMAT, time.localtime())
                        content = request.form['content']
                        idweibo = Username + potime + str(len(content))
                        wtype = "o"
                        fatherid = "null"
                        number = 0
                        url = ret.url
                        if content[0] == '@':
                                res = content[1:]
                                me = models.User.query.filter_by(username = res).first()
                                if me != None:
                                        wtype = "a"
                                        #content = "<a href='/homepage?uid=" + me.username + "'>" + content + "</a>"
                                        #content = decodeHtml(content)
                                        imessage = idweibo+me.username
                                        susername = username
                                        rusername = me.username
                                        message = models.Message(imessage=imessage,idweibo=idweibo,susername=susername,url=url,rusername=rusername)
                                        db.session.add(message)
                                        db.session.commit()
                        weibo = models.Weibo(url = url , username = username , potime = potime , content = content , idweibo = idweibo ,wtype = wtype ,fatherid=fatherid , number=number)
                        db.session.add(weibo)
                        db.session.commit()
                friend = models.Follow.query.filter_by(username=session['username']).all()
                ans = [session['username']]
                #ans = ans + ['Admin']
                for ele in friend:
                        tt = models.User.query.filter_by(username=ele.followname).first()
                        if tt.state == 1:
                                ans = ans + [ele.followname]
                posts = []
                for ele in ans:
                        posts = posts + models.Weibo.query.filter_by(username = ele,wtype="o").all()
                        posts = posts + models.Weibo.query.filter_by(username = ele,wtype="a").all()
                posts = sorted(posts, key = lambda d: d.potime, reverse = True)
                follows = len(models.Follow.query.filter_by(followname = Username).all())
                topic = len(models.Weibo.query.filter_by(username = Username).all())
                following = len(models.Follow.query.filter_by(username = Username).all())
                point = follows*3 + topic*2 + following*1
                ret.point = point
                if ret.point>10000:
                        ret.lvip = 1
                db.session.commit()
                return render_template("home.html" , posts=posts,ret=ret,nickname=ret.nickname,topic=topic,follows=follows,following=following) 
                
        if request.method == 'POST':
                session['username'] = request.form['username2']
                psw = convertmd5(request.form['password2'])
                miss = models.User.query.filter_by(username=request.form['username2']).first()
                if psw == miss.password and miss.state == 1:
                        friend = models.Follow.query.filter_by(username=session['username']).all()
                        ans = [session['username']]
                        ans = ans + ['Admin']
                        for ele in friend:
                                tt = models.User.query.filter_by(username=ele.followname).first()
                                if tt.state == 1:
                                        ans = ans + [ele.followname]
                        posts = []
                        for ele in ans:
                                posts = posts + models.Weibo.query.filter_by(username = ele,wtype="o").all()
                                posts = posts + models.Weibo.query.filter_by(username = ele,wtype="a").all()
                        posts = sorted(posts, key = lambda d: d.potime, reverse = True)
                        follows = len(models.Follow.query.filter_by(followname = session['username']).all())
                        topic = len(models.Weibo.query.filter_by(username = session['username']).all())
                        following = len(models.Follow.query.filter_by(username = session['username']).all())
                        return render_template("home.html",posts=posts,ret=miss,nickname=miss.nickname,topic=topic,follows=follows,following=following)
                return render_template("error.html")
        return render_template("error.html")

@app.route('/homepage')
def homepage():
        if 'username' not in session:
                return render_template("error.html")
        username = session['username']
        miss=models.User.query.filter_by(username=username).first()
        if request.args.get('uid') == 'self':
                username = session['username']
        else:
                username = request.args.get('uid')
        posts = models.Weibo.query.filter_by(username=username,wtype="o").all()
        posts.reverse()
        follows = len(models.Follow.query.filter_by(followname = username).all())
        topic = len(models.Weibo.query.filter_by(username = username).all())
        following = len(models.Follow.query.filter_by(username = username).all())
        ret = models.User.query.filter_by(username=username).first()
        if request.args.get('uid') == 'self' or request.args.get('uid') == session['username']:
                return render_template("homepage.html",display="none",posts=posts,ret = ret , nickname=miss.nickname, follows=follows , topic=topic , following = following)
        else:
                friend = models.Follow.query.filter_by(username=session['username']).all()
                for ele in friend:
                        if ele.followname == username:
                                return render_template("homepage.html" , display="block" , typed="close" , color="success" , relation = "unfollow", posts=posts , ret = ret , nickname=miss.nickname, follows=follows , topic=topic , following = following)
                return render_template("homepage.html" , display="block" , typed="open" , color="primary" , relation = "follow", posts=posts , ret = ret , nickname=miss.nickname, follows=follows , topic=topic , following = following)
                
@app.route('/message/letter')
def message():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                ans = models.Message.query.filter_by(rusername=Username).all()
                posts = []
                for ele in ans:
                    Id = ele.idweibo
                    c = models.Weibo.query.filter_by(idweibo = Id).first()
                    if c.wtype == "l":
                        posts = posts + [c]
                return render_template("letter.html",posts = posts , ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/message/atme')
def atme():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                ans = models.Message.query.filter_by(rusername=Username).all()
                posts = []
                for ele in ans:
                    Id = ele.idweibo
                    c = models.Weibo.query.filter_by(idweibo = Id).first()
                    if c.wtype == "a":
                        posts = posts + [ele]
                return render_template("atme.html",posts = posts , ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/message/commit')
def commit():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                ans = models.Message.query.filter_by(rusername=Username).all()
                posts = []
                for ele in ans:
                    Id = ele.idweibo
                    c = models.Weibo.query.filter_by(idweibo = Id).first()
                    if c.wtype == "r":
                        posts = posts + [c]
                return render_template("commit.html",posts = posts , ret=ret,nickname=ret.nickname)
        return render_template("error.html")

@app.route('/system')
def system():
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                posts = models.User.query.filter_by().all()
                if ret.role == 1:
                        return render_template("system.html",posts=posts,ret=ret,nickname=ret.nickname)
                else:
                        return render_template("error.html")
        return render_template("error.html")

@app.route('/square')
def square():
        pall = models.Weibo.query.filter_by().all()
        #length = len(pall)
        if len(pall) >= 9:
                posts = random.sample(pall,9)
                posts1 = posts[0:3]
                posts2 = posts[3:6]
                posts3 = posts[6:9]
        else:
                return render_template("error.html")
        if 'username' in session:
                Username = session['username']
                ret = models.User.query.filter_by(username=Username).first()
                return render_template("square.html",posts1=posts1,posts2=posts2,posts3=posts3,ret=ret,nickname=ret.nickname)
        return render_template("square.html",posts1=posts1,posts2=posts2,posts3=posts3)

@app.route('/addfriend',methods=["POST","GET"])
def addfriend():
        if 'username' in session:
                Username = session['username']
                followname = request.form['followname']
                friend = models.Follow.query.filter_by(username = Username).all()
                for ele in friend:
                        if ele.followname == followname:
                                models.Follow.query.filter_by(username = Username , followname=followname).delete()
                                db.session.commit()
                                return render_template("temp.html")
                idname = Username + '%' + followname
                follow = models.Follow(username = Username , followname = followname , idname = idname)
                db.session.add(follow)
                db.session.commit()
                return render_template("temp.html")
        return render_template("error.html")

@app.route('/forward')
def forward():
        Username = session['username']
        miss = models.User.query.filter_by(username = Username).first()
        idweibo = request.args.get('id')
        ret = models.Weibo.query.filter_by(idweibo = idweibo).first()
        username = ret.username
        potime = time.strftime(ISOTIMEFORMAT, time.localtime())
        content = "FW : "+ ret.username + " " + ret.content
        idweibo = Username + potime + str(len(content))
        wtype = "o"
        fatherid = "null"
        number = 0
        url = miss.url
        weibo = models.Weibo(url = url , username = username , potime = potime , content = content , idweibo = idweibo ,wtype = wtype ,fatherid=fatherid , number=number)
        db.session.add(weibo)
        db.session.commit()
        username = session['username']
        ret = models.User.query.filter_by(username=Username).first()
        if request.method == 'POST':
            username = Username
            potime = time.strftime(ISOTIMEFORMAT, time.localtime())
            content = request.form['content']
            idweibo = Username + potime + str(len(content))
            wtype = "o"
            fatherid = "null"
            number = 0
            url = ret.url
            if content[0] == '@':
                res = content[1:]
                me = models.User.query.filter_by(username = res).first()
                if me != None:
                    wtype = "a"
                    #content = "<a href='/homepage?uid=" + me.username + "'>" + content + "</a>"
                    #content = decodeHtml(content)
                    imessage = idweibo+me.username
                    susername = username
                    rusername = me.username
                    message = models.Message(imessage=imessage,idweibo=idweibo,susername=susername,url=url,rusername=rusername)
                    db.session.add(message)
                    db.session.commit()
            weibo = models.Weibo(url = url , username = username , potime = potime , content = content , idweibo = idweibo ,wtype = wtype ,fatherid=fatherid , number=number)
            db.session.add(weibo)
            db.session.commit()
        friend = models.Follow.query.filter_by(username=session['username']).all()
        ans = [session['username']]
        #ans = ans + ['Admin']
        for ele in friend:
            tt = models.User.query.filter_by(username=ele.followname).first()
            if tt.state == 1:
                ans = ans + [ele.followname]
        posts = []
        for ele in ans:
            posts = posts + models.Weibo.query.filter_by(username = ele,wtype="o").all()
            posts = posts + models.Weibo.query.filter_by(username = ele,wtype="a").all()
        posts = sorted(posts, key = lambda d: d.potime, reverse = True)
        follows = len(models.Follow.query.filter_by(followname = Username).all())
        topic = len(models.Weibo.query.filter_by(username = Username).all())
        following = len(models.Follow.query.filter_by(username = Username).all())
        point = follows*3 + topic*2 + following*1
        ret.point = point
        if ret.point>10000:
            ret.lvip = 1
        db.session.commit()
        return render_template("home.html" , posts=posts,ret=ret,nickname=ret.nickname,topic=topic,follows=follows,following=following)
        # return "forward ok"
        # return render_template("error.html")


















                
                

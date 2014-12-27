# -*- coding:utf-8 -*-
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

STATE_NO = 0
STATE_OK = 1

TYPE_DEFAULT = 'default'

class User(db.Model):
    username = db.Column(db.String(128) , primary_key = True)
    nickname = db.Column(db.String(128) , index = True)
    email = db.Column(db.String(128) , index = True)
    password = db.Column(db.String(256) , index = True)
    state = db.Column(db.SmallInteger , default = STATE_OK)#激活和非激活状态
    #state = db.Column(db.SmallInteger , default = STATE_OK)#激活和非激活状态
    role = db.Column(db.SmallInteger ,default = ROLE_USER)#用户和管理员两种权限
    lvip = db.Column(db.SmallInteger , default = 0)#活跃度等级
    
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Follow(db.Model):
    idname = db.Column(db.String(256) , primary_key = True)#username%followname
    username = db.Column(db.String(128))
    followname = db.Column(db.String(128))#关注人username
    ftype = db.Column(db.String(128) , default = TYPE_DEFAULT)#关注人分类

    def __repr__(self):
        return '<IDname %r>' % (self.idname)

class Weibo(db.Model):
    idweibo = db.Column(db.String(256) , primary_key = True)#username+potime+content做md5加密
    username = db.Column(db.String(128))#发微博人
    wtype = db.Column(db.String(128))#微博类型，原微博，原微博下回复，私信
    fatherid = db.Column(db.String(256),default = 'null')#所在楼id
    number = db.Column(db.Integer)#楼数
    content = db.Column(db.String(1024))#内容
    
    
    
    


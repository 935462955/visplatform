from visplatform import db
from mongoengine import *
from flask_login import UserMixin#flask-login的UserMixin表
from werkzeug.security import generate_password_hash, check_password_hash#flask的两个依赖之一werkzeug（密码加密和密码验证）

class CourseModel(db.Document):
    _id = db.ObjectIdField()
    course_id = db.IntField()
    title = db.StringField()
    text = db.StringField()
    goal = db.StringField()
    frame_head = db.StringField()
    frame_foot = db.StringField()
    code = db.StringField()
    tag = db.StringField()
    meta = {
        "collection": "course",
        "strict": "False"
           }
class ProjectModel(db.Document):
    _id = db.ObjectIdField()
    project_id = db.IntField()
    title = db.StringField()
    text = db.StringField()
    test = db.StringField()
    meta = {
        "collection": "project",
        "strict": "False"
           }

class SubModule(db.EmbeddedDocument):
    sub_id = db.ObjectIdField()
    sub_order  = db.IntField()
    type =  db.StringField()


class ModuleModel(db.Document):
    _id = db.ObjectIdField()
    module_name = db.StringField()
    order = db.IntField(unique_with = 'module_name')
    sub_modules = db.SortedListField(db.EmbeddedDocumentField(SubModule),ordering="sub_order",reverse=False)
    meta = {
        "collection":"module",
        "strict":"False",
         'ordering': ['-order']
    }

class Unit(db.EmbeddedDocument):
    unit_id = db.ObjectIdField()
    unit_title = db.StringField()
    unit_order = db.IntField()
    unit_type = db.StringField()


class EmbeddedModuleModal(db.EmbeddedDocument):
    _id = db.ObjectIdField()
    module_name = db.StringField()
    order = db.IntField(unique_with='module_name')
    sub_modules = db.SortedListField(db.EmbeddedDocumentField(SubModule), ordering="sub_order", reverse=False)

class CategoryModel(db.Document):
    modules = db.SortedListField(db.EmbeddedDocumentField(EmbeddedModuleModal),ordering ='order',reverse=False)
    units = db.SortedListField(db.EmbeddedDocumentField(Unit),ordering='unit_order',reverse=False)
    meta = {
        "collection": "category",
        "strict": "False",
    }

#用户表
class User(db.Document, UserMixin):
    meta = {
        "collection": "user",#表名
        "ordering": ["-id"],#id
        "strict": True#自动修改表内容
    }
    username = db.StringField()#帐号
    password_hash = db.StringField()#密码
    nickname = db.StringField()#用户名
    superuser = db.BooleanField(default=False)#是否为管理员，后续可以用来进入后台（未实现）

    #密码加密
    def hash_password(self, password):
    	self.password_hash = generate_password_hash(password)
    	self.save()

    #密码验证
    def verify_password(self, password):
    	return check_password_hash(self.password_hash, password)
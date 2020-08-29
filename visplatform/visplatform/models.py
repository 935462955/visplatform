from visplatform import db
from mongoengine import *

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

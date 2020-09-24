import os

from bson import ObjectId

from visplatform.models import ModuleModel, CourseModel, ProjectModel, Concept


def listdir(path):
    return os.listdir(path)


# 建立id和子模块名称的映射
def get_sub_module_details(subs):
    dics = {}
    for sub in subs:
        if sub.type == 'code_page':
            item = CourseModel.objects.get(_id=sub.sub_id)
            dics[sub.sub_id] = item.title
        if sub.type == 'project_page':
            item = ProjectModel.objects.get(_id=sub.sub_id)
            dics[sub.sub_id] = item.title
    return dics


# 按id和类型查找子模块
def get_submodule_by_idAndType(id, type):
    if type == 'code_page':
        return CourseModel.objects.get_or_404(_id=id)
    if type == 'project_page':
        return ProjectModel.objects.get_or_404(_id=id)


# 关系类
class Relationship:
    def __init__(self, id, name, parent_id, parent_name, type):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.type = type


# 创建主界面各种关系
def create_relationship():
    relationship_list = []
    first = Relationship(id='1', name='数据可视化', parent_id='-1', parent_name='null', type='course')
    second = Relationship(id='2', name='项目挑战', parent_id='-1', parent_name='null', type='project')
    relationship_list.append(first.__dict__)
    relationship_list.append(second.__dict__)

    modules = ModuleModel.objects
    for module in modules:
        sub_modules = module.sub_modules
        for sub_module in sub_modules:
            if sub_module.type == 'code_page':
                course_temp = CourseModel.objects.get(_id=sub_module.sub_id)
                sub_moudule_temp = Relationship(id=str(sub_module.sub_id), name=course_temp.title,
                                                parent_id=str(module._id), parent_name=module.module_name,
                                                type='course')
                relationship_list.append(sub_moudule_temp.__dict__)
        moudule_temp = Relationship(id=str(module._id), name=module.module_name, parent_id='1',
                                    parent_name='数据可视化', type='course')
        relationship_list.append(moudule_temp.__dict__)

    courses = CourseModel.objects
    for course in courses:
        concepts = course.concept
        for concept in concepts:
            if concept.id:
                concept_in = Concept.objects.get(name=concept.id)
                concept_temp = Relationship(id=str(concept_in._id), name=concept_in.name,
                                            parent_id=str(course._id), parent_name=course.title, type='course')
                relationship_list.append(concept_temp.__dict__)

    projects = ProjectModel.objects
    for project in projects:
        porject_temp = Relationship(id=str(project._id), name=project.title, parent_id='2',
                                    parent_name='项目挑战', type='project')
        relationship_list.append(porject_temp.__dict__)

    return relationship_list

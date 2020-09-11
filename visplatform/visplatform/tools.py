import os
from visplatform.models import ModuleModel,CourseModel,ProjectModel
def listdir(path):
    return os.listdir(path)

#建立id和子模块名称的映射
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
#按id和类型查找子模块
def get_submodule_by_idAndType(id,type):
    if type == 'code_page':
        return CourseModel.objects.get_or_404(_id = id)
    if type == 'project_page':
        return ProjectModel.objects.get_or_404(_id = id)
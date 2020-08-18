import os
from visplatform.models import ModuleModel,CourseModel
def listdir(path):
    return os.listdir(path)

def get_sub_module_details(subs):
    dics = {}
    for sub in subs:
        if sub.type == 'code_page':
            item = CourseModel.objects.get(_id=sub.sub_id)
            dics[sub.sub_id] = item.title
    return dics

def get_submodule_by_idAndType(id,type):
    if type == 'code_page':
        return CourseModel.objects.get_or_404(_id = id)
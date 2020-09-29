import os
import math
import json
from visplatform import app
from visplatform.models import ModuleModel, CourseModel, ProjectModel, Concept, CategoryModel


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
    def __init__(self, id, name, parent_id, parent, type):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.parent = parent
        self.type = type


# 创建主界面各种关系
def create_relationship():
    relationship_list = []
    first = Relationship(id='1', name='数据可视化', parent_id='-1', parent='', type='code_page')
    second = Relationship(id='2', name='项目挑战', parent_id='-1', parent='', type='project_page')
    relationship_list.append(first.__dict__)
    relationship_list.append(second.__dict__)

    category = CategoryModel.objects.first()
    modules = category.modules

    for module in modules:
        sub_modules = module.sub_modules
        if module.module_name == '项目挑战':
            for sub_module in sub_modules:
                project_temp = ProjectModel.objects.get(_id=sub_module.sub_id)
                sub_module_temp = Relationship(id=str(sub_module.sub_id), name=project_temp.title,
                                               parent_id='2', parent='项目挑战',
                                               type='project_page')
                relationship_list.append(sub_module_temp.__dict__)
        else:
            for sub_module in sub_modules:
                if sub_module.type == 'code_page':
                    course_temp = CourseModel.objects.get(_id=sub_module.sub_id)
                    concepts = course_temp.concept
                    for concept in concepts:
                        if concept.id:
                            concept_in = Concept.objects.get(name=concept.id)
                            concept_temp = Relationship(id=str(concept_in._id), name=concept_in.name,
                                                        parent_id=str(course_temp._id), parent=course_temp.title,
                                                        type='code_page')
                            relationship_list.append(concept_temp.__dict__)
                    sub_moudule_temp = Relationship(id=str(sub_module.sub_id), name=course_temp.title,
                                                    parent_id=str(module._id), parent=module.module_name,
                                                    type='code_page')
                    relationship_list.append(sub_moudule_temp.__dict__)
            moudule_temp = Relationship(id=str(module._id), name=module.module_name, parent_id='1',
                                        parent='数据可视化', type='code_page')
            relationship_list.append(moudule_temp.__dict__)

    return relationship_list


## 生成课程概念图
class tree:  # 树节点
    def __init__(self, name, id, type):
        self.name = name
        self.id = id
        self.type = type
        self.deepth = None
        self.children = []
        self.parent = None
        self.cx = 0
        self.cy = 0
        self.r = 0
        self.tx = 0
        self.ty = 0


def pre_order(node):  # 先序遍历树
    print(node.name, len(node.children), node.parent)
    for i in node.children:
        pre_order(i)


def generate_drawable_data(relationship_list):
    df_tree = []  # 课程
    df_xm_tree = []  # 项目

    for i in relationship_list:
        if i['type'] == 'code_page':
            df_tree.append(i)
        else:
            df_xm_tree.append(i)
    # print(df_xm_tree)

    #types = {'name': str, 'parent': str, '知识点类型': str}

    # dic字典 通过节点名查找到节点
    dic = {}

    # 前一个节点的父亲节点
    #pre_parent = 0
    # t用于记录上一个节点的父亲节点的儿子数
    # 如果当前节点的父亲与上一个节点的父亲相同则t+1,否则更新当前节点所在层的最大儿子数
    #t = 0
    # 每一层最大的儿子数
    max_children_per_layer = {}
    # 初始化树

    for row in df_tree:
        node = tree(row['name'], row['id'], row['type'])
        dic[node.name] = node
    for row in df_tree:
        node = dic[row['name']]
        if row['parent'] == '':
            root = node
        else:
            parent = dic[row['parent']]
            node.parent = parent
            parent.children.append(node)
            # 这个if-else 用于计算每层的最大儿子数

    # print(pre_order(root))

    assin_deep(root, max_children_per_layer)

    # print(max_children_per_layer)

    # 计算圆的半径
    # R[0]为最大圆半径,R[1]为第二层圆半径
    R = [2000, 0, 0, 0]
    # 内圆离外圆的距离为内圆半径r的tr倍数
    tr = 0.2
    for i in range(1, 3):
        cal_R_in(i, R, tr, max_children_per_layer)
    cal_R_on(3, R, max_children_per_layer)
    # print(R)
    cal_pos(root, R[0], R[0], 0, 0, R, root, tr)

    # print(root.r)
    # pre_order1(root)

    # 存入问文件
    L = []
    built_li(root, L)
    # 计算项目挑战相关
    # xmn为总项目数
    xm_n = len(df_xm_tree) - 1

    Rx = [(R[0] - (2 + tr) * R[1]) / 1.2, 0]
    tem = 1 / math.sin(math.pi / (xm_n * 1.5)) + 1 + tr
    Rx[1] = Rx[0] / tem
    #print(Rx)
    for row in df_xm_tree:
        node = tree(row['name'], row['id'], row['type'])
        dic[node.name] = node
    for row in df_xm_tree:
        node = dic[row['name']]
        if row['parent'] == '':
            xm_root = node
            node.cx = root.cx
            node.cy = root.cy
            node.r = Rx[0]
        else:
            parent = dic[row['parent']]
            node.parent = parent
            node.r = Rx[1]
            parent.children.append(node)

    for index, node in enumerate(xm_root.children):
        angle = (1 + 1 / xm_n) * index * (2 * math.pi) / (xm_n + 1)
        tem = node.parent.r - (1 + tr) * node.r
        node.cx = xm_root.cx + tem * math.sin(angle)
        node.cy = xm_root.cy - tem * math.cos(angle)
    max_children_per_layer2 = {}
    assin_deep(xm_root, max_children_per_layer2)
    built_li(xm_root, L)

    # print(L)

    filename = os.path.join(app.config['VISUALIZATION_FOLDER'], 'data.json')
    # 能够写入中文
    with open(filename, 'w', encoding='utf-8') as f_obj:
        json.dump(L, f_obj, ensure_ascii=False)


# 计算在大圆内圆的半径,index为深度
# ny_k越大内圆越小
def cal_R_in(index, R, tr, max_children_per_layer, ny_k=1.3):
    pre_r = R[index - 1]
    tem = 1 / math.sin(math.pi / (max_children_per_layer[index - 1] * ny_k)) + 1 + tr
    R[index] = pre_r / tem


# 计算在大圆上圆的半径
# sy_k越大上圆越小
def cal_R_on(index, R, max_children_per_layer, sy_k=2.8):
    R[index] = R[index - 1] * math.sin(math.pi / (max_children_per_layer[index - 1] * sy_k))


# 计算圆的坐标
# node为节点,x,y为父节点的圆心坐标，n为父节点的孩子个数，k为当前节点是第k个孩子
def cal_pos(node, x, y, n, k, R, root, tr):
    # 当前节点的半径由深度决定
    node.r = R[node.deepth]
    if node == root:
        # 根节点的坐标为传入的x，y
        node.cx = x
        node.cy = y
    elif node.deepth == 3:
        # 计算在圆上的圆的坐标
        angle = (1 + 1 / n) * k * (2 * math.pi) / (n + 1)
        tem = node.parent.r
        node.cx = x + tem * math.sin(angle)
        node.cy = y - tem * math.cos(angle)
    else:
        # 计算在圆内圆的坐标
        angle = (1 + 1 / n) * k * (2 * math.pi) / (n + 1)
        tem = node.parent.r - (1 + tr) * node.r
        node.cx = x + tem * math.sin(angle)
        node.cy = y - tem * math.cos(angle)
        temx = node.cx - node.parent.cx
        temy = node.cy - node.parent.cy
        temr = (node.r + node.parent.r) * 0.95  # 最后一个参数是小圆的文本与大圆的圆心距的比例
        temk = temr / math.sqrt(temx * temx + temy * temy)
        node.tx = temk * temx - temx
        node.ty = temk * temy - temy
    # 先序遍历计算孩子的坐标
    len_c = len(node.children)
    for index, i in enumerate(node.children):
        # 先序遍历计算之后的节点
        cal_pos(i, node.cx, node.cy, len_c, index, R, root, tr)


# L.append(['name','deepth','cx','cy','r'])
def built_li(node, L):
    if node.parent:
        parentName = node.parent.name
    else:
        parentName = "根节点"
    Lj = {"name": node.name, "deepth": node.deepth, "cx": node.cx, "cy": node.cy, "r": node.r, "parent": parentName,
          "tx": node.tx, "ty": node.ty, "id": node.id, "type": node.type}
    L.append(Lj)
    # Li = []
    for i in node.children:
        # Li.append(i.name)
        built_li(i, L)
    # Lj["children"]=Li


def assin_deep(node, max_children_per_layer):  # 先序给树的节点深度赋值

    if node.parent == None:
        node.deepth = 0
    else:
        node.deepth = node.parent.deepth + 1
    if node.deepth not in max_children_per_layer or max_children_per_layer[node.deepth] < len(node.children):
        max_children_per_layer[node.deepth] = len(node.children)
    for i in node.children:
        assin_deep(i, max_children_per_layer)

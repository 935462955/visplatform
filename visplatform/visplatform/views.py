from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from visplatform import app
from visplatform.models import CourseModel,ModuleModel,SubModule,CategoryModel,Unit,EmbeddedModuleModal
from flask_mongoengine.wtf import model_form
from visplatform import tools
import json,os

@app.route('/')
def index():
    anchor = request.cookies.get('anchor', '')  # 锚点
    return redirect(url_for('show_category',_anchor=anchor))

@app.route('/upgrade_id')
def upgrade_id():
    start = request.args.get('start_num')
    end = request.args.get('end_num')
    try:
        op = int(request.args.get('op'))
    except:
        flash('必须填写数字','danger')
        return redirect(url_for('Admin'))
    if start > end:
        flash('起点序号不能大于终点序号','danger')
    else:
        for item in CourseModel.objects.filter(course_id__gte=start, course_id__lte=end):
                item.course_id += op
                item.save()

        flash('序号已更新','success')
    return redirect(url_for('Admin'))

@app.route('/course/<string:_id>',methods=['POST','GET'])
def show_course(_id):
    type = request.args.get('type')
    order = request.args.get('order',1,int)
    units = CategoryModel.objects.first_or_404().units

    print(_id)
    try : #获取id为_id的课程
        if type == 'code_page':
            course = CourseModel.objects.get_or_404(_id=_id)
            try:  # 处理非法goal
                goal = json.loads(course.goal)
            except:
                goal = json.loads('[]')
        else:
            return redirect(url_for('show_category'))
    except:
        return redirect(url_for('show_category'))


    try:
        next_id = units[order].unit_id
        next_type = units[order].unit_type
        next_order = order+1
    except:
        next_id = ' '
        next_type = ' '
        # 获取下一个课程的链接
        next_order = 1
    response = make_response(render_template('course.html',course=course,goal=goal,next_id = next_id,next_type = next_type,next_order=next_order))
    response.set_cookie('anchor', 'id_' + _id, max_age=7 * 24 * 3600)
    return response

@app.route('/category_set_cookie',methods=['POST'])
def category_set_cookie():
    data = json.loads(request.data)
    resp = make_response("success")  # 设置响应体
    resp.set_cookie(data['id'], data['state'], max_age=7*24*3600)
    return resp

@app.route('/category')
def show_category():
    category = CategoryModel.objects.first_or_404()
    modules = category.modules
    dics = {}
    order = 1
    collapse_state = {}
    for module in modules:
        collapse_state[str(module._id)] = request.cookies.get(str(module._id),'fold') #折叠状态
        dics.update(tools.get_sub_module_details(module.sub_modules))
        for sub in module.sub_modules:
            sub.order = order
            order +=1

    return render_template('category.html',modules=modules,dics=dics,collapse_state = collapse_state)

@app.route('/Admin')
def Admin():
   '''page = request.args.get('page', 1, type=int)
    per_page = 10
    paginate = CourseModel.objects.order_by('course_id').paginate(page=page, per_page=per_page)
    return render_template('CourseList1.html', paginate=paginate)'''
   return redirect(url_for('show_codepages'))

@app.route('/new',methods=['POST','GET'])
def add_course():
    course = CourseModel.objects.get_or_404(course_id=0)
    CourseForm = model_form(CourseModel)
    form = CourseForm(request.form)
    all_id = CourseModel.objects.order_by('course_id').fields(course_id=1)
    max_id = all_id[len(all_id)-1].course_id + 1
    if request.method == 'POST':
        title = form.title.data
        text = form.text.data
        frame_head = form.frame_head.data
        frame_foot = form.frame_foot.data
        code = form.code.data
        goal = form.goal.data
        course_id = form.course_id.data
        tag = form.tag.data
        new_course = CourseModel(title=title,text=text,frame_head = frame_head, frame_foot = frame_foot,goal=goal,code=code,course_id=course_id,tag=tag)
        new_course.save(force_insert=True)
        return redirect(url_for('Admin'))
    course.course_id = max_id
    files = tools.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('editcourse.html', course=course, form=form,files = files)

@app.route('/editcourse/<string:_id>', methods=['POST', 'GET'])
def edit_course(_id):
    #print(request.method)
    course = CourseModel.objects.get_or_404(_id=_id)
    CourseForm = model_form(CourseModel)
    form = CourseForm(request.form)
    #print(form.validate())
    if request.method == 'POST':
        course.title = form.title.data
        course.text = form.text.data
        course.frame_head = form.frame_head.data
        course.frame_foot = form.frame_foot.data
        course.code = form.code.data
        course.course_id = form.course_id.data
        course.goal = form.goal.data
        course.tag = form.tag.data
        course.save()
        # flash('Course updated.','success')
        return redirect(url_for('edit_course',_id = _id))
    files = tools.listdir(app.config['UPLOAD_FOLDER'])
    #print(files)
    return render_template('editcourse.html', course=course, form=form,files=files)

@app.route('/editcourse/upload',methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['upload_file']
        filename = request.form['file_name']
        file_path =  os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(file_path)
        files = tools.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify({'html':render_template('file_list.html',files = files)})

@app.route('/editcourse/delete',methods=['POST'])
def delete_file():
    if request.method == 'POST':
        filename = str(request.data,'utf-8')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)
        files = tools.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('file_list.html',files =files)

@app.route('/modules')
def show_modules():
    modules = ModuleModel.objects.order_by('order').all()
    dics  = {}
    order = 1
    for module in modules:
        dics.update(tools.get_sub_module_details(module.sub_modules))
        for sub in module.sub_modules:
            sub.order = order
            order +=1
    return render_template('modules.html', modules=modules, dics=dics)


@app.route('/modules/update',methods=['POST'])
def update_modules():
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)

        if data['type'] == 'sub_module': # 子模块位置更新
            old_module = ModuleModel.objects.get_or_404(_id = data['sub_source_container'])
            old_sub_modules = old_module.sub_modules
            item = old_sub_modules.pop(data['sub_source'])
            for i in old_sub_modules[data['sub_source']:]:
                i.sub_order -= 1
                print(i.sub_order)
            old_module.save()
            new_module = ModuleModel.objects.get_or_404(_id = data['sub_target_container'])
            new_sub_modules = new_module.sub_modules
            item.sub_order = data['sub_target'] + 1
            for i in new_sub_modules[data['sub_target']:]:
                i.sub_order += 1
            new_sub_modules.insert(data['sub_target'],item)
            new_module.save()
        elif data['type'] == 'module': # 模块更新
            modules_base = ModuleModel.objects.order_by('order').all()
            modules = []
            for i in modules_base:
                modules.append(i)
            old_index = data['module_source']
            new_index = data['module_target']
            module = modules[old_index]
            module.order = new_index + 1
            module.save()

            if old_index > new_index:
                for i in modules[new_index:old_index]:
                    i.order += 1
                    i.save()
            elif old_index < new_index:
                for i in modules[old_index+1:new_index+1]:
                    i.order -= 1
                    i.save()
        elif data['type'] == 'add_sub_module':#给单元增加子模块
            module = ModuleModel.objects.get_or_404(_id=data['module_as_container'])
            subs = module.sub_modules
            if len(subs) != 0:
                max_order = subs[-1].sub_order + 1
            else:
                max_order = 1
            for i in data['sub_modules']:
                subs.append(SubModule(sub_id = i['id'],sub_order = max_order,type = data['sub_module_type']))
                max_order += 1
            module.save()
            dics = tools.get_sub_module_details(subs)
            return render_template('fragment_modules_sub_li.html',sub_modules = subs, dics= dics)
        elif data['type'] == 'delete_module':#删除给定单元 后面的依次前移
            module = ModuleModel.objects.get_or_404(_id = data['target_id'])
            for i in ModuleModel.objects.filter(order__gt=module.order):
                i.order -= 1
                i.save()
            ModuleModel.objects(_id = data['target_id']).delete()
        elif data['type'] == 'delete_sub_module':#删除给定单元中的给定子模块 后面的依次前移
            module = ModuleModel.objects.get_or_404(_id = data['container_id'])
           # print(module.sub_modules.)

            for i in module.sub_modules:
                if str(i.sub_id) == data['sub_module_id']:
                    sub = i
            for i in module.sub_modules:
                if i.sub_order > sub.sub_order:
                    i.sub_order -= 1
            module.sub_modules.remove(sub)
            module.save()
        elif data['type'] == 'add_module':
            num = ModuleModel.objects.count()
            module = ModuleModel(module_name = data['module_title'],order = num+1)
            module.save()
            module = ModuleModel.objects.get_or_404(order = num + 1)
            return render_template('fragment_modules_module_li.html',modules=[module],dics={})
        elif data['type'] == 'publish': #发布出版模型
            modules = ModuleModel.objects.order_by('order').all()
            if CategoryModel.objects.count() == 0:
                category = CategoryModel()
                category.save(force_insert=True)
            else:
                category = CategoryModel.objects.first_or_404()
            module_list = []
            unit_list = []
            order = 1
            for module in modules:
                module_list.append(module)
                for i in module.sub_modules:
                    sub = tools.get_submodule_by_idAndType(i.sub_id,i.type)
                    unit_list.append(Unit(unit_id = i.sub_id,unit_order = order, unit_title = sub.title,unit_type=i.type))
                    order +=1
            category.modules = []
            for i in modules:
                subs = []
                for j in i.sub_modules:
                   subs.append(SubModule(sub_id = j.sub_id,sub_order=j.sub_order,type=j.type))
                category.modules.append(EmbeddedModuleModal(_id=i._id,module_name=i.module_name,order=i.order,sub_modules=subs))
       #     for i in modules:
        #        print(i.module_name)
        #        i.save()
         #       category.modules.append(i.to_dbref())
          #      print(i.to_dbref)
            category.units = unit_list
            category.save()

    return 'success'

@app.route('/modules/fetch',methods=['POST'])
def get_sub_module():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data['type'] == 'code_page':
            courses = CourseModel.objects.order_by('course_id').fields(_id=1,title=1)
            return render_template('fragment_modules_modal_li.html', sub_modules = courses)

    return '1'

@app.route('/codepage')
def show_codepages():
    courses = CourseModel.objects.order_by('course_id').fields(title=1, course_id=1, tag=1,_id=1)[1:]
    for course in courses:
        try:
            if course.tag:
                course.tag = course.tag.split(',')
        except:
            # print(course.tag)
            course.tag = [' ']
    return render_template('codepagelist.html', courses=courses)

@app.route('/test')
def test():
    return render_template('test_jasmine.html')
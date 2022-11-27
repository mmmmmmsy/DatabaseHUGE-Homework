from winreg import QueryInfoKey
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
app = Flask(__name__)
#设置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://msy:123456@127.0.0.1:3308/medic'
db = SQLAlchemy(app)

username=''

@app.route('/')
def welcome():
    s = 'ER图如下：'
    return render_template('welcome.html',a = s)

#定义模型(为了看得方便，我把它搬上来这里了
class User(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    content = db.Column(db.String(255))
    passwd = db.Column(db.String(255))

@app.route('/index')
def dex():
    return render_template('login.html',msg = '请登录')

@app.route('/login',methods=['post'])
def login():
    global username
    username = request.form.get('username')
    password = request.form.get('password')
    pw = db.session.query(User.passwd).filter(User.name == username).all()
    #hhh这里逻辑有点怪，但还算可以实现（主要是基础知识不足+懒
    if (password in str(pw)):
        return render_template('login_success.html')
    else:
        return render_template('login.html',msg = '用户名或密码错误！')

@app.route('/choose_function')
def choose_function():
    choice_function = request.args.get("choice_function")
    if choice_function == '1':
        return table_list()
    elif choice_function == '2':
        return query_list()
'''
从此往下的一大堆杂玩意就全是数据库部分的内容了，可在url后面加上/table_list进去查看
'''

#表名页
@app.route('/table_list')
def table_list():
    return render_template('table_list.html')

#选择展示某个表
@app.route('/choose')
def choose_table():
    choice_table = request.args.get("choice")
    if choice_table == "1":
        return select_disease_list()
    elif choice_table == "2":
        return select_disease_suffered()
    elif choice_table == "3":
        return select_edit_record()
    elif choice_table == "4":
        return select_people()
    else:
        return select_user()

#定义模型
class DiseaseList(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    ifImg = db.Column(db.Integer)
    ifText = db.Column(db.Integer)
    lastEditTime = db.Column(db.Date)
    hid = db.Column(db.Integer)

#查询所有数据
@app.route("/select_disease_list")
def select_disease_list():
    Disease_List = DiseaseList.query.order_by(DiseaseList.id.desc()).all()
    return render_template("disease_list.html",disease_list = Disease_List)

#添加数据
@app.route('/insert_disease_list',methods=['GET','POST'])
def insert():
    #进行添加操作
    name = request.form['name']
    ifImg = request.form['ifImg']
    ifText = request.form['ifText']
    lastEditTime = request.form['lastEditTime']
    hid = request.form['hid']
    diseaseList = DiseaseList(name=name,ifImg=ifImg,ifText=ifText,lastEditTime=lastEditTime,hid=hid)
    db.session.add(diseaseList)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_disease_list")
def insert_page():
    #跳转至添加信息页面
    return render_template("disease_list_insert.html")


#删除数据
@app.route("/delete_disease_list",methods=['GET'])
def delete():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    diseaseList = DiseaseList.query.filter_by(id=id).first()
    db.session.delete(diseaseList)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_disease_list",methods=['GET','POST'])
def alter():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        name = request.args.get('name')
        ifImg = request.args.get("ifImg")
        ifText = request.args.get("ifText")
        lastEditTime = request.args.get("lastEditTime")
        hid = request.args.get("hid")
        diseaseList = DiseaseList(id=id,name=name,ifImg=ifImg,ifText=ifText,lastEditTime=lastEditTime,hid=hid)
        return render_template("disease_list_alter.html",diseaseList = diseaseList)
    else:
        #接收参数，修改数据
        id = request.form["id"]
        name = request.form['name']
        ifImg = request.form['ifImg']
        ifText = request.form['ifText']
        lastEditTime = request.form['lastEditTime']
        hid = request.form['hid']
        diseaseList = DiseaseList.query.filter_by(id=id).first()
        diseaseList.name = name
        diseaseList.ifImg = ifImg
        diseaseList.ifText = ifText
        diseaseList.lastEditTime = lastEditTime
        diseaseList.hid = hid
        db.session.commit()
        return redirect('/table_list')

#定义模型
class DiseaseSuffered(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    hid = db.Column(db.Integer)
    diseaseGet = db.Column(db.String(255))
    time = db.Column(db.Date)

#查询所有数据
@app.route("/select_disease_suffered")
def select_disease_suffered():
    Disease_Suffered = DiseaseSuffered.query.order_by(DiseaseSuffered.id.desc()).all()
    return render_template("disease_suffered.html",disease_suffered = Disease_Suffered)

#添加数据
@app.route('/insert_disease_suffered',methods=['GET','POST'])
def insert_disease_suffered():
    #进行添加操作
    hid = request.form['hid']
    diseaseGet = request.form['diseaseGet']
    time = request.form['time']
    diseaseSuffered = DiseaseSuffered(hid=hid,diseaseGet=diseaseGet,time=time)
    db.session.add(diseaseSuffered)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_disease_suffered")
def insert_page_disease_suffered():
    #跳转至添加信息页面
    return render_template("disease_suffered_insert.html")


#删除数据
@app.route("/delete_disease_suffered",methods=['GET'])
def delete_disease_suffered():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    diseaseSuffered = DiseaseSuffered.query.filter_by(id=id).first()
    db.session.delete(diseaseSuffered)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_disease_suffered",methods=['GET','POST'])
def alter_disease_suffered():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        hid = request.args.get("hid")
        diseaseGet= request.args.get("diseaseGet")
        time = request.args.get("time")
        diseaseSuffered = DiseaseSuffered(id=id,hid=hid,diseaseGet=diseaseGet,time=time)
        return render_template("disease_suffered_alter.html",diseaseSuffered = diseaseSuffered)
    else:
        #接收参数，修改数据
        id = request.form["id"]
        hid = request.form['hid']
        diseaseGet = request.form['diseaseGet']
        time = request.form['time']
        diseaseSuffered = DiseaseSuffered.query.filter_by(id=id).first()
        diseaseSuffered.hid = hid
        diseaseSuffered.diseaseGet = diseaseGet
        diseaseSuffered.time = time
        db.session.commit()
        return redirect('/table_list')

#定义模型
class EditRecord(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(255))
    editor = db.Column(db.String(255))
    time = db.Column(db.Date)

#查询所有数据
@app.route("/select_edit_record")
def select_edit_record():
    Edit_Record = EditRecord.query.order_by(EditRecord.id.desc()).all()
    return render_template("edit_record.html",edit_record = Edit_Record)

#添加数据
@app.route('/insert_edit_record',methods=['GET','POST'])
def insert_edit_record():
    #进行添加操作
    content = request.form['content']
    editor = request.form['editor']
    time = request.form['time']
    editRecord = EditRecord(content=content,editor=editor,time=time)
    db.session.add(editRecord)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_edit_record")
def insert_page_edit_record():
    #跳转至添加信息页面
    return render_template("edit_record_insert.html")


#删除数据
@app.route("/delete_edit_record",methods=['GET'])
def delete_edit_record():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    editRecord = EditRecord.query.filter_by(id=id).first()
    db.session.delete(editRecord)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_edit_record",methods=['GET','POST'])
def alter_edit_record():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        content = request.args.get("content")
        editor= request.args.get("editor")
        time = request.args.get("time")
        editRecord = EditRecord(id=id,content=content,editor=editor,time=time)
        return render_template("edit_record_alter.html",editRecord = editRecord)
    else:
        #接收参数，修改数据
        id = request.form["id"]
        content = request.form['content']
        editor = request.form['editor']
        time = request.form['time']
        editRecord = EditRecord.query.filter_by(id=id).first()
        editRecord.content = content
        editRecord.editor = editor
        editRecord.time = time
        db.session.commit()
        return redirect('/table_list')

#定义模型
class People(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    hid = db.Column(db.Integer)
    age = db.Column(db.Integer)
    address = db.Column(db.String(255))
    disease_history = db.Column(db.String(255))
    work = db.Column(db.String(255))

#查询所有数据
@app.route("/select_people")
def select_people():
    ppeople = People.query.order_by(People.id.desc()).all()
    return render_template("people.html",people = ppeople)

#添加数据
@app.route('/insert_people',methods=['GET','POST'])
def insert_people():
    #进行添加操作
    hid = request.form['hid']
    address = request.form['address']
    age = request.form['age']
    disease_history = request.form['disease_history']
    work = request.form['work']

    ppeople = People(hid=hid,address=address,age=age,disease_history=disease_history,work=work)
    db.session.add(ppeople)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_people")
def insert_page_people():
    #跳转至添加信息页面
    return render_template("people_insert.html")


#删除数据
@app.route("/delete_people",methods=['GET'])
def delete_people():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    ppeople = People.query.filter_by(id=id).first()
    db.session.delete(ppeople)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_people",methods=['GET','POST'])
def alter_people():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        hid = request.args.get("hid")
        address= request.args.get("address")
        age = request.args.get("age")
        disease_history = request.args.get("disease_history")
        work = request.args.get("work")
        ppeople = People(id = id,hid=hid,address=address,age=age,disease_history=disease_history,work=work)
        return render_template("people_alter.html",people = ppeople)
    else:
        #接收参数，修改数据
        id = request.form['id']
        hid = request.form['hid']
        address = request.form['address']
        age = request.form['age']
        disease_history = request.form['disease_history']
        work = request.form['work']
        ppeople = People.query.filter_by(id=id).first()
        ppeople.hid = hid
        ppeople.address = address
        ppeople.age = age
        ppeople.disease_history = disease_history
        ppeople.work = work
        db.session.commit()
        return redirect('/table_list')


  
#查询所有数据
@app.route("/select_user")
def select_user():
    user = User.query.order_by(User.id.desc()).all()
    return render_template("user.html",user = user)

#添加数据
@app.route('/insert_user',methods=['GET','POST'])
def insert_user():
    #进行添加操作
    name = request.form['name']
    content = request.form['content']
    passwd = request.form['passwd']

    user = User(name=name,content=content,passwd=passwd)
    db.session.add(user)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_user")
def insert_page_user():
    #跳转至添加信息页面
    return render_template("user_insert.html")


#删除数据
@app.route("/delete_user",methods=['GET'])
def delete_user():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_user",methods=['GET','POST'])
def alter_user():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        name = request.args.get("name")
        content= request.args.get("content")
        passwd = request.args.get("passwd")
        user = User(id=id,name=name,content=content,passwd=passwd)
        return render_template("user_alter.html",user = user)
    else:
        #接收参数，修改数据
        id = request.form['id']
        name = request.form['name']
        content = request.form['content']
        passwd = request.form['passwd']
        user = User.query.filter_by(id=id).first()
        user.name=name
        user.content=content
        user.passwd = passwd
        db.session.commit()
        return redirect('/table_list')

'''
各表展示部分到此结束
以下是查询部分代码,可以在url后面加入query_list进去查看
'''

#查询列表页
@app.route('/query_list')
def query_list():
    return render_template('querylist.html')

#选择展示某个表
@app.route('/querychoose')
def querychoose():
    choice = request.args.get("choice")
    if choice == "1":
        return query1()
    elif choice == "2":
        return query2()
    elif choice == "3":
        return query3()
    elif choice == "4":
        return query4()
    elif choice == "5":
        return query5()
    elif choice == "6":
        return query6()
    elif choice == "7":
        return query7()
    elif choice == "8":
        return query8()

@app.route('/query1')
def query1():
    return render_template("query1input.html")

@app.route('/query1exe',methods=['POST'])
def query1exe():
    '''
        给定疾病名称，查询病人的职业
    '''
    dise = request.form["dise"]
    sql = '''
    Select P.work
    From people P, disease_suffered D
    Where P.hid = D.hid and D.hid in(
    Select F.hid
    From disease_suffered F 
    Where F.diseaseGet='{}')
    Group By P.work
    '''.format(dise)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query1result.html",result = re)

@app.route('/query2')
def query2():
    return render_template("query2input.html")

@app.route('/query2exe',methods=['POST'])
def query2exe():
    '''
    给定疾病名称，查询疾病数据贡献来源的人所患有的所有疾病
    db:连接的数据库
    '''
    dise = request.form["dise"]
    sql = '''
    select P.hid,D.diseaseGet
    from people P, disease_suffered D
    where P.hid = D.hid and P.hid in
    (select B.hid
    from disease_list B
    where B.name = '{}'
    )
    '''.format(dise)
    ret = db.session.execute(sql)
    re = list(ret)
    print(re)
    return render_template("query2result.html",result = re)

@app.route('/query3')
def query3():
    return render_template("query3input.html")

@app.route('/query3exe',methods=['POST'])
def query3exe():
    '''
    给定疾病名称，查询疾病来源地
    db:连接的数据库
    '''
    dise = request.form["dise"]
    sql = '''
    select P.address
    from people P
    where exists
    (select *
    from disease_list B
    where B.name = '{}' and B.hid = P.hid
    )
    '''.format(dise)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query3result.html",result = re)

@app.route('/query4')
def query4():
    return render_template("query4input.html")

@app.route('/query4exe',methods=['POST'])
def query4exe():
    '''
    给定疾病，查询该疾病的患病人数
    db:连接的数据库
    '''
    dise = request.form["dise"]
    sql = '''
    select COUNT(*) AS scount
    from disease_suffered D, people P
    where D.diseaseGet = '{}' and D.hid = P.hid
    '''.format(dise)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query4result.html",result = re)

@app.route('/query5')
def query5():
    return render_template("query5input.html")

@app.route('/query5exe',methods=['POST'])
def query5exe():
    '''
    给定疾病，查询患有该病的患者的平均年龄
    db:连接的数据库
    '''
    dise = request.form["dise"]
    sql = '''
    select AVG(P.age)
    from people P
    where exists
    (select *
    from disease_list DL
    where DL.name = '{}' and DL.hid = P.hid
    )
    '''.format(dise)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query5result.html",result = re)
    
@app.route('/query6')
def query6():
    return render_template("query6input.html")

@app.route('/query6exe',methods=['POST'])
def query6exe():
    '''
    给定年龄和职业 查找患者患有的疾病有哪些
    db:连接的数据库
    '''
    data_work = request.form["data_work"]
    data_age = request.form["data_age"]
    sql = '''
    select DS.diseaseGet 
    from disease_suffered DS 
    where DS.hid in (select P.hid 
        from people P 
        where P.age={} or P.work='{}')
    '''.format(data_age , data_work)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query6result.html",result = re)

@app.route('/query7')
def query7():
    return render_template("query7input.html")

@app.route('/query7exe',methods=['POST'])
def query7exe():
    '''
        给定修改人查询修改时间和修改内容
        db:连接的数据库
    '''
    data_editor = request.form["data_editor"]
    sql = '''select content , time  from edit_Record eR where eR.editor = '{}' '''.format(data_editor)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query7result.html",result = re)

@app.route('/query8')
def query8():
    return render_template("query8input.html")

@app.route('/query8exe',methods=['POST'])
def query8exe():
    '''
        给定疾病名称，查询提供疾病资料的人的病史
        db:连接的数据库
    '''
    dise = request.form["dise"]
    sql = '''
    Select P.disease_history
    From people P,disease_suffered D
    Where D.hid=P.hid and D.hid in(
    Select F.hid
    From disease_suffered F 
    Where F.diseaseGet='{}')
    Group By P.work
    '''.format(dise)
    ret = db.session.execute(sql)
    re = list(ret)
    return render_template("query8result.html",result = re)

if __name__ == '__main__':
    app.run(debug = True,port=5000)

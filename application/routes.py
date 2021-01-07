from application import app
from flask import render_template,request,Response,json, redirect, flash,session,url_for
#from application.models import User,Course,Enrollment
from application.forms import LoginForm, RegisterForm,PayForm
import sqlite3 as sql
import datetime as dt


#memberData = [
#            {"memberID":"1111","name":"Raman","address":"A-102,Mumbai","total":"10000","remaining":"10000"}, 
#            {"memberID":"2222","name":"Dinesh","address":"A-103,Mumbai","total":"15000","remaining":"5000"}, 
#            {"memberID":"3333","name":"Dilip","address":"A-104,Mumbai","total":"10000","remaining":"10000"}, 
#            {"memberID":"4444","name":"Raja","address":"A-105,Mumbai","total":"4000","remaining":"16000"}, 
#            {"memberID":"5555","name":"Amit","address":"A-106,Mumbai","total":"1000","remaining":"19000"}]

courseData = [
            {"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"},
            {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"},
            {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, 
            {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, 
            
            {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]
  
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",index=True)

@app.route("/login", methods=['GET','POST'])
def login():
     
    return render_template("login.html",login=True )

@app.route("/courses")
def courses():
    
      return render_template("courses.html", courseData=courseData, courses = True )
   
@app.route("/register")
def register():
    return render_template("register.html",register=True)

@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form['title']
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, data={"id":id,"title":title,"term":term})    


@app.route("/index1")
def index1():
    if session['memid']:
        return render_template("index1.html", index1=True)  
    else:
        return render_template("index1.html", index1=False)

@app.route("/home")
def home():
        return render_template("index1.html", index1=False)   

@app.route("/member1")
def member1():
    if not session.get('memid'):
        return redirect(url_for('index1'))
    else:  
        conn = sql.connect('database.db')
        membid = session.get('memid')
        qry_member="select memberid, name, address,AMOUNT, (AMOUNT-PAID) remaining from MEMBER_VIEW where memberid = " + str(membid)
        memberData=conn.execute(qry_member)
        conn.close
        return render_template("member1.html", memberData=memberData, member1 = True)

@app.route("/detail1",methods=["GET","POST"])
def detail1():
    if not session.get('memid'):
        return redirect(url_for('index1'))
    else:  
        conn = sql.connect('database.db')
        membid = session.get('memid')
        qry_payment="select memberid, amount, paydate,reference from payment where memberid = " + str(membid)
        payData=conn.execute(qry_payment)
        conn.close
        return render_template("detail1.html", payData=payData, detail1 = True)     

@app.route("/register1",methods=["GET","POST"])
def register1():
    if session.get('memname'):
        return redirect(url_for('index1'))
    form = RegisterForm()
    if form.validate_on_submit():
        email=request.form.get("email")
        conn = sql.connect('database.db')
        qry_email_check="select count(1) from member where email = '" + email + "'"
        emailcheckData=conn.execute(qry_email_check)
        for rs in emailcheckData:
            l_email_count = rs[0]
       
        if l_email_count==0:
            qry_max_count="select max(memberid) cnt from member"
            maxCountData=conn.execute(qry_max_count)
            for rs1 in maxCountData:
                l_max_count = rs1[0]
                print(l_max_count)
            l_max_count =l_max_count+1  
            email       = form.email.data
            password    = form.password.data
            name        = form.name.data
            address     = form.address.data
            amt         = form.amount.data
            startdate   =  str(dt.date.today())
            qry_insert ="insert into member(memberid,name,address,email,password,startdate,amount) values ("
            qry_insert +="'"+str(l_max_count) + "',"
            qry_insert +="'"+ name + "',"
            qry_insert +="'"+ address + "',"
            qry_insert +="'"+ email + "',"  
            qry_insert +="'"+ password + "',"  
            qry_insert += "'"+ str(startdate)+ "'," 
            qry_insert +="'"+ str(amt) + "')" 
            print (qry_insert)
            conn.execute(qry_insert)
            conn.commit()
            flash(email + " Successfully Registered", "success")
            return redirect(url_for('index1'))
        else:
            flash(email + " Already in use!, please pick another one", "danger")
             
                
        conn.close
        return redirect(url_for('index1'))
    return render_template("register1.html", title="Register", form=form, register1=True)

     

@app.route("/logout1")
def logout1():
    session['memid']=False
    session['memname']=False
    return redirect(url_for('index1'))  

@app.route("/login1", methods=['GET','POST'])
def login1():
    form = LoginForm()
    
    if form.validate_on_submit():
        email=request.form.get("email")
        conn = sql.connect('database.db')
        qry_login="select count(1),name,memberid from member where email = '" + email + "'"
        loginData=conn.execute(qry_login)
        for rs in loginData:
            l_email_count = rs[0]
            l_email_name  = rs[1]
            l_email_id    = rs[2]
        if l_email_count==0:
            flash("Sorry, something went wrong.","danger") 
        else:
            #flash("You are successfully logged in!" +l_email_name, "success")
            session['memid']   = l_email_id
            session['memname'] = l_email_name
            return redirect(url_for('index1'))
                
        conn.close    
    return render_template("login1.html", title="Login", form=form, login1=True )

@app.route("/payment1", methods=['GET','POST'])
def payment1():
    form = PayForm()
    if not session.get('paymemid'):
       session['paymemid'] =request.form.get('memberID')
       session['paymemname'] = request.form.get('name1')
       session['paymemadd'] = request.form.get('address')
       form.memberid.data=session.get('paymemid')    
       form.memberName.data = session.get('paymemname')
       form.memberAddress =session.get('paymemadd')
    if form.validate_on_submit():
        if session.get('paymemid'):
            payMemberid = session.get('paymemid') 
            print("after"+session['paymemid'])
            paydate = form.paydate.data
            payamount = form.payAmount.data
            payreference = form.payReference.data
            print(paydate+paydate+payamount) 
            conn = sql.connect('database.db')
            qry_max_count="select max(paymentid) cnt from payment"
            maxCountData=conn.execute(qry_max_count)
            for rs1 in maxCountData:
                l_max_count = rs1[0]
                print(l_max_count)
            l_max_count =l_max_count+1  
            qry_insert ="insert into payment(paymentid,memberid,amount,paydate,reference) values ("
            qry_insert +="'"+str(l_max_count) + "',"
            qry_insert +="'"+ str(payMemberid) + "',"
            qry_insert +="'"+ payamount + "',"
            qry_insert +="'"+ paydate + "',"  
            qry_insert +="'"+ payreference + "')"  
            print (qry_insert)
            conn.execute(qry_insert)
            conn.commit()
            conn.close

        session['paymemid'] =False
        session['paymemname'] = False
        session['paymemadd'] = False
        flash(payamount + " Payment Added against Member Id:" + payMemberid , "success")
        return redirect(url_for('member1')) 
    #data={"id":id,"name1":name1,"address":address}
    return render_template("payment1.html", payment1=True, form=form)  

   

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    
    return Response(json.dumps(jdata), mimetype="application/json")



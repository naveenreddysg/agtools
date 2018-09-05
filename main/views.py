"""Purpose is to server general requests of the app"""
# -*- coding: utf-8 -*-
from flask import render_template, jsonify, make_response, request, redirect, flash, url_for
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
from flask import Blueprint
from flask import session as flask_sess
from flask_bcrypt import Bcrypt
from forms import LoginForm, RegistrationForm
import constants as cts
from extensions import db
from sqlalchemy import func
from models import User, client_raw, AuditLogs, UserPack,client_etl_db
import bcrypt

flask_bcrypt = Bcrypt()

__author__ = 'hughson.simon@gmail.com'


blueprint = Blueprint('views', __name__)

@blueprint.route("/",methods=['GET','POST'])
@login_required
def index():
    import datetime
    total_users = User.query.count()
    total_visit = AuditLogs.query.count()
    latest_users = User.query.order_by("created_time desc")
    total_fruits = client_raw.fruits.find({}).count()
    total_vegetables = client_raw.vegetables.find({}).count()
    total_herbs = client_raw.herbs_raw.distinct("Commodity")
    total_nuts = client_raw.nuts_raw.distinct("Commodity")
    total_ornamentals = client_raw.ornamentals_raw.distinct("Commodity")
    #latest_visits = AuditLogs.query.filter_by(activityType='login').order_by('auditlog."loggedTime" desc').limit(100)
    total_subscriptions = UserPack.query.count()
    total_locations = client_raw.locations.find({}).count()

    # result = AuditLogs.query.filter_by(activityType='login').order_by('auditlog."loggedTime" desc').limit(200)
    N = 0
    try:
        N = int(request.form.get("submit"))
        date_N_days_ago = datetime.date.today() - datetime.timedelta(days=N)
        Cdate = datetime.date.today()
        Bdate = date_N_days_ago
        val = db.engine.execute("select * from auditlog where \"loggedTime\" between '{}' and '{}' and"
                                " \"activityType\"='login' order by \"loggedTime\" desc".format(Bdate,
                                                                                                Cdate)).fetchall()
    except Exception as e:
        # print e
        val = AuditLogs.query.filter_by(activityType='login').order_by('auditlog."loggedTime" desc').all()

    from collections import defaultdict
    groups = defaultdict(list)
    try:
        for obj in val:
            obj = obj.__dict__
            date = obj.get('loggedTime').strftime("%b-%d-%Y %H:%M:%S")
            obj['loggedTime'] = date
            try:
                del obj['_sa_instance_state']
            except:
                pass
            groups[obj['email']].append(obj)
        new_list = groups.values()
        new_list = sorted(new_list,
                          key=lambda x: datetime.datetime.strptime(x[0].get('loggedTime'), '%b-%d-%Y %H:%M:%S'),
                          reverse=True)
    except:
        for obj in val:
            obj = dict(obj)
            date = obj.get('loggedTime').strftime("%b-%d-%Y %H:%M:%S")
            obj['loggedTime'] = date
            try:
                del obj['_sa_instance_state']
            except:
                pass
            groups[obj['email']].append(obj)
        new_list = groups.values()
        new_list = sorted(new_list,
                          key=lambda x: datetime.datetime.strptime(x[0].get('loggedTime'), '%b-%d-%Y %H:%M:%S'),
                          reverse=True)

    def list_filter(l):
        l = l[0:10]
        return l

    # def list_filter(l):
    #     for i in range(20, len(l) + 1):
    #         try:
    #             l.pop(20)
    #         except:
    #             break
    #     return l

    sessions = [len(i) for i in new_list]
    # print sessions
    new_list = map(list_filter, new_list)
    return render_template('index.html',
                           result_items=latest_users,
                           total_users=total_users,
                           #latest_visits=latest_visits,
                           total_visit=total_visit,
                           total_fruits=total_fruits,
                           total_vegetables=total_vegetables,
                           total_subscriptions=total_subscriptions,
                           total_locations=total_locations,
                           total_herbs=len(total_herbs),
                           total_nuts=len(total_nuts),
                           total_ornamentals=len(total_ornamentals),
                           new_list=new_list,
                           total_visits=len(val),N=N,sessions=sessions)

#To deactivate a user in Registered Users
@blueprint.route("/deactivate")
def users_deactivate():
    val = request.args.get("id")
    print val
    db.engine.execute("update userdetails set confirmed ='false' where {} = {}".format('"userId"', val))
    return redirect('/')

#To activate a user in Registered Users
@blueprint.route("/activate")
def users_activate():
    val = request.args.get("id")
    print val
    db.engine.execute("update userdetails set confirmed ='true' where {} = {}".format('"userId"', val))
    return redirect('/')

@blueprint.route('/login', methods=['GET', 'POST'])
def adminLogin():
    error = None
    login_form = LoginForm(csrf_enabled=True)
    if request.method == 'POST':
        print request.form['email']
        emailid, password = request.form['email'].lower(), request.form['password']
        #emailid = emailid.encode('ascii', 'ignore')
        #password = password.encode('ascii', 'ignore')

        try:
            user = User.query.filter_by(username=emailid, isAdmin=1).first()
            # print user.userId

        except Exception, e:
            raise
            error = "Incorrect email address."
        else:
            if user:
                remember_me = False
                if 'remember_me' in request.form:
                    remember_me = True
                if user.password:
                    if flask_bcrypt.check_password_hash(str(user.password), str(password)):
                        flask_sess['user_id'] = user.userId
                        login_user(user, remember=remember_me)
                        return redirect("/")
                    error = "Incorrect password."
                else:
                    error = "Incorrect password."
            else:
                error = "Incorrect email"
    else:
        user = current_user
        logout_user()
        flask_sess.clear()
        logout_user()
    return render_template('login.html', error=error, login_form=login_form)

@blueprint.route('/admin_register', methods=['GET', 'POST'])
def adminRegister():
    form=RegistrationForm(request.form)

    if request.method == "POST":
        res = request.form.to_dict()
        print res['email1'],res['name1'], res['pwd1'], res['userType'], res['city'].encode('utf-8'), res['state'].encode('utf-8'), res['country']
        salt = bcrypt.gensalt(10, prefix=b'2a')
        pwd = bcrypt.hashpw(res['pwd1'].encode('utf-8'), salt)
        print(pwd)
        state = str(res['state'].encode('utf-8'))
        print(state)
        city = str(res['city'].encode('utf-8'))
        print(city)
        print pwd, state, city
        if res['userType'] == "GROWER":
            userId = 1
        elif res['userType'] == "BUYER":
            userId = 2
        elif res['userType'] == "TRUCKER":
            userId = 3
        else:
            userId = 4
        print userId

        r = db.engine.execute("SELECT * FROM USERDETAILS WHERE USERNAME='{}'".format(res['email1'])).fetchall()
        # d = db.engine.execute("select ud.state from userdetails as ud where username='naveenreddy.sg@gmail.com'").fetchall()
        # print(d[0][0])
        print len(r)
        if len(r) > 0:
            flash('Email already in use.', 'error')
            return redirect('/admin_register')
        else:
            # db.engine.execute(
                # "INSERT INTO USERDETAILS(username,name,password,\"isAdmin\",usertype,usertype_id,city,state,country,zipcode,confirmed)VALUES('{}','{}','{}',0,'{}','{}','{}','{}','{}',0,'{}')".format(
                #     res['email1'], res['name1'], pwd, res['userType'], userId, city, state, res['country'], 'true'))
            flash('User Registration Successful.','info')
            return redirect('/admin_register')

    return render_template('admin_register.html',form=form)

@blueprint.route('/get_states', methods=['GET', 'POST'])
def get_states():
    option = request.form['country']
    print(option)
    db = client_etl_db['dbagtools']
    states = db.cities.distinct("state", {"country": option})
    states = list(states)
    return render_template("states.html", states=states)


@blueprint.route('/get_cities', methods=['GET', 'POST'])
def get_cities():
    option = request.form['state'].encode('utf-8')
    print(option)
    db = client_etl_db['dbagtools']
    cities = db.cities.distinct("city", {"state": option})
    cities = list(cities)
    return render_template("cities.html", cities=cities)

@blueprint.route('/logout')
def logout():
    """Logout the current user."""
    try:
        user = current_user
        user.authenticated = False
        logout_user()
        flask_sess.clear()
        logout_user()
    except Exception as e:
        print(e)
        # return e
    return redirect("/login")
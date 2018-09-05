"""Purpose is to serve requests related to User Create Delete and update

"""
from flask import abort, Blueprint, session, redirect, render_template, request, Flask, url_for
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
import constants as cts
from utils import validate_json, validate_registration_input
from flask import jsonify
import datetime as dttim
from models import User, SubscriptionPackages, UserPack, AuditLogs
from extensions import db
from datetime import datetime
import uuid
from emails import user_register_email
import datetime

__author__ = 'hughson.simon@gmail.com'

blueprint = Blueprint('users', __name__)

@blueprint.route("/admin_users/", methods=['GET','POST'])
# @blueprint.route("/admin_users/<int:page_num>", methods=['GET', 'POST'])
@login_required
def users_list():

    """list all available users and respective permission.
    :return: dict: users dict items with available permissions
    """
    FromDate="FromDate"
    ToDate="ToDate"
    response_dict = {}
    res = {}
    try:

        if request.method == "POST":
            res = request.form.to_dict()
            FromDate = res['fdate']
            ToDate = res['tdate']
        # val = db.engine.execute(
        #     "select * from userdetails where created_time between '{}' and '{}'".format(res['fdate'],res['tdate'])).fetchall()

        val = db.engine.execute(
            "SELECT userdetails.*, max(auditlog.\"loggedTime\") AS log FROM userdetails left outer join auditlog on "
            "userdetails.\"userId\" = auditlog.\"userId\" where created_time between '{}' and '{}' GROUP BY userdetails.\"userId\" ".format(res['fdate'],res['tdate'])).fetchall()

    except Exception as e:
        # raise
        db.session.rollback()

        val = db.engine.execute(
            "SELECT userdetails.*, max(auditlog.\"loggedTime\") AS log FROM userdetails left outer join auditlog on "
            "userdetails.\"userId\" = auditlog.\"userId\" GROUP BY userdetails.\"userId\" ").fetchall()

        #latest_users = User.query.order_by("created_time desc").all()

        #user_packs = db.engine.execute("SELECT userdetails.* , count(user_packages.subscriptionid) AS totalsubscription FROM userdetails "
                               #"left outer join user_packages on \"userId\" = userid GROUP BY \"userId\"").fetchall()

        # val = db.engine.execute("SELECT userdetails.*, max(auditlog.\"loggedTime\") AS log FROM userdetails left outer join auditlog on "
        #                              "userdetails.\"userId\" = auditlog.\"userId\" GROUP BY userdetails.\"userId\" ").fetchall()

    return render_template('admin_users.html',
                           result_items=val,
                           total_users=len(val),FromDate=FromDate,ToDate=ToDate) #user_packs_view=len(user_packs)

#To deactivate a user in Registered Users
@blueprint.route("/admin_users/deactivate")
def users_deactivate():
    val = request.args.get("id")
    print val
    db.engine.execute("update userdetails set confirmed ='false' where {} = {}".format('"userId"', val))
    return redirect('/admin_users/')

#To activate a user in Registered Users
@blueprint.route("/admin_users/activate")
def users_activate():
    val = request.args.get("id")
    print val
    db.engine.execute("update userdetails set confirmed ='true' where {} = {}".format('"userId"', val))
    return redirect('/admin_users/')

#To filter users using Joined Date in Registered Users
@blueprint.route("/admin_users/filters/", methods=['GET','POST'])
def users_filters():
    if request.method == "POST":
        res=request.form.to_dict()
        # print res['fdate']
        # print res['tdate']
    val = db.engine.execute("select * from userdetails where created_time between '{}' and '{}'".format(res['fdate'],res['tdate'])).fetchall()
    return render_template('admin_users_filters.html',
                           result=val,
                           total_users=len(val))

#To display users log details in Registered Users
@blueprint.route("/admin_userlog", methods=['GET','POST'])
def users_logs():
    import datetime
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
        new_list = sorted(new_list, key=lambda x: datetime.datetime.strptime(x[0].get('loggedTime'), '%b-%d-%Y %H:%M:%S'), reverse=True)

    except:
        for obj in val:
            obj = dict(obj)
            date = obj.get('loggedTime').strftime("%d-%m-%Y %H:%M:%S")
            obj['loggedTime'] = date
            try:
                del obj['_sa_instance_state']
            except:
                pass
            groups[obj['email']].append(obj)
        new_list = groups.values()
        new_list = sorted(new_list,
                          key=lambda x: datetime.datetime.strptime(x[0].get('loggedTime'), '%d-%m-%Y %H:%M:%S'),
                          reverse=True)

    def list_filter(l):
        l = l[0:10]
        return l

    sessions = [len(i) for i in new_list]
    new_list = map(list_filter, new_list)

    return render_template('admin_userlog.html',#result=val,
                           total_visits=len(val),N=N,new_list=new_list,sessions=sessions)



# To display users log details using days filter in Registered Users
@blueprint.route("/admin_userlog_range", methods=['GET', 'POST'])
def users_logs_range():
    import datetime
    N = int(request.form.get("daysrange"))
    #print N
    date_N_days_ago = datetime.date.today() - datetime.timedelta(days=N)

    Cdate = datetime.date.today()
    Bdate = date_N_days_ago
    #print Cdate, Bdate
    result = db.engine.execute("select * from auditlog where \"loggedTime\" between '{}' and '{}' and \"activityType\"='login' order by \"loggedTime\" desc".format(Bdate,Cdate)).fetchall()

    return render_template('admin_userlog_range.html', #result=result,
            total_visits=len(result),result=result,N=N)

#To get the user profile details in Registered Users
@blueprint.route("/admin_users/user_info")
def user_info():
    val = request.args.get("id")
    print val
    curr = db.engine.execute('select * from userdetails where "userId" ='+val).fetchone()
    curr1 = db.engine.execute('select * from user_packages where userid='+val).fetchone()
    curr2 = db.engine.execute('select count(subscriptionid) as tot  from user_packages where userid='+val).fetchone()
    user_packs = db.engine.execute(
        "SELECT userdetails.* , count(user_packages.subscriptionid) AS totalsubscription FROM userdetails "
        "left outer join user_packages on \"userId\" = userid GROUP BY \"userId\"").fetchall()
    curr3 = db.engine.execute('select * from auditlog where "userId" ='+val)
    # Query for Commodity Names which User Subscribed
    curr4 = db.engine.execute('select * from user_pkg_commodity where "userpkgId" in (select "userpkgId" from user_packages where userid={val})'.format(val=val)).fetchall()
    commodities=""
    for i in curr4:
        if i[0]==curr4[-1][0]:
            commodities+=i[0]
        else:
            commodities+=(i[0]+", ")
    return render_template('admin_users_info.html', total_users=len(user_packs),entries=curr, entry=curr1,curr2=curr2,curr3=curr3,commodities=commodities)

@blueprint.route("/user/view", methods=['POST'])
@validate_json
def user_view():
    """View user details
    sample request
    {
        "user_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34"
    }

    sample response:
    {
      "response_status": "SUCCESS",
      "response_message":{
                    "email": "hughson.simon@gmail.com",
                    "id": "18fcbb87-d56a-48ed-b589-47a26166eb8c",
                    "last_login": "Wed, 09 Aug 2017 19:06:24 GMT",
                    "name": "hughsonsees1sad2e3 hughsonsees1sad2e3",
                    "auth_user_groups": [1,2],
                    "status": true
                }
    }
    :return: response dict with status and users dict items with available groups
    """
    request_dict = request.get_json()
    response_dict = {}

    if "user_id" in request_dict:
        try:
            user_exists = User.query.filter_by(user_uuid=request_dict['user_id']).first()
            # print(request_dict['user_id'])
            if user_exists:
                # View user auth groups
                users_dict = {}
                group_list = []
                users_dict['id'] = user_exists.user_uuid
                users_dict['name'] = user_exists.full_name
                users_dict['email'] = user_exists.email
                users_dict['status'] = user_exists.is_active()
                users_dict['last_login'] = user_exists.last_login
                for group in user_exists.auth_user_groups.all():
                    group_list.append(group.group_id)
                users_dict['auth_user_groups'] = group_list
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
                response_dict[cts.RESPONSE_MESSAGE] = users_dict

            else:
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
                response_dict[cts.RESPONSE_MESSAGE] = cts.RECORD_NOTFOUND
        except:
            db.session.rollback()
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
            response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST
    else:
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST

    return jsonify(response_dict), 200

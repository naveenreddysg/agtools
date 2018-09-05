"""Purpose is to serve requests related to User Create Delete and update

"""
from flask import abort, Blueprint, session, redirect, render_template, request, url_for
from flask_login import current_user
from flask_login import login_required
import constants as cts
from utils import validate_json, validate_registration_input
from flask import jsonify
import datetime as dttim
from models import client_raw, client_etl_db
import uuid
from emails import user_register_email
from flask_paginate import Pagination, get_page_parameter


__author__ = 'hughson.simon@gmail.com'

blueprint = Blueprint('weather', __name__)

@blueprint.route("/admin_weather_alert")
@login_required
def alert_list():

    alert = client_raw.weather.find({}).sort([("date",-1)]).limit(1000)
    alert_count = client_raw.weather.find({}).count()
    return render_template('admin_weather_alert.html',
                           result_items = alert,total_weather = alert_count)

@blueprint.route("/admin_weather_color_alert",methods=['GET','POST'])
@login_required
def alert_color_list():
    subuser_type = {
        'GROWER':{'PLANTING':1, 'HARVESTING':2},
        'BUYER':{'PLANNING':3, 'PURCHASING':4},
        'TRUCKER': {'LOGISTICAL PLANNING':5, 'LOGISTICAL DAILY':6},
        'GOVERNAMENTAGENT':{'PLANNING':7, 'PURCHASING':8}
    }
    if request.method == "POST":
        res = request.form.to_dict()
        res['subuserType']=subuser_type[res['userType']][res['subuserType']]
        print res['subuserType']
        try:
            db = client_etl_db['dbagtools']
            posts = db.weatherRange
            posts.insert(res)
            # for post in posts.find():
            #     print(post)
        except Exception as e:
            print e

    fruits = client_raw.fruits.find({}).sort([("fruit_name",1)])
    vegetables = client_raw.vegetables.find({}).sort([("vegetable_name",1)])
    herbs = client_raw.herbs_raw.distinct("Commodity")
    herbs.sort()
    nuts = client_raw.nuts_raw.distinct("Commodity")
    nuts.sort()
    ornamentals = client_raw.ornamentals_raw.distinct("Commodity")
    ornamentals.sort()
    return render_template('admin_weather_color_alert.html',
                           fruits=fruits,vegetables=vegetables,
                           herbs=herbs,nuts=nuts,ornamentals=ornamentals)

@blueprint.route('/weather_table', methods=['POST'])
def weatherTable():
    option = request.form['commodity']
    print option
    db = client_etl_db['dbagtools']
    result_items = db.weatherRange.find({"commodity": "{}".format(option)})
    result = [item for item in result_items]
    return render_template('admin_weathertable.html', result_items=result)


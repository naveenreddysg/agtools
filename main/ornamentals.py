"""Purpose is to serve requests related to User Create Delete and update

"""
from flask import abort, Blueprint, session, redirect, render_template, request, url_for
from flask_login import current_user
from flask_login import login_required
import constants as cts
from utils import validate_json, validate_registration_input
from flask import jsonify
import datetime as dttim
from models import client_raw, client_etl


__author__ = 'hughson.simon@gmail.com'


blueprint = Blueprint('ornamentals', __name__)

@blueprint.route("/admin_ornamentals_meta")
@login_required
def ornamentals_list():
    """list all available ornamentals and respective permission.
    :return:
    """
    ornamentals_meta = client_raw.ornamentals_raw.distinct("Commodity")

    pipe = [{'$group': {'_id': "$Commodity", "Terminal_Market": {
        '$sum': {'$cond': {'if': {'$eq': ["$report_type", "Terminal Market"]}, 'then': 1, 'else': 0}}},
                        "Shipping_Point": {'$sum': {
                            '$cond': {'if': {'$eq': ["$report_type", "Shipping Point"]}, 'then': 1, 'else': 0}}},
                        "Movement": {
                            '$sum': {'$cond': {'if': {'$eq': ["$report_type", "Movement"]}, 'then': 1, 'else': 0}}}}}]

    ornamentals_count = client_raw.ornamentals_raw.aggregate(pipeline=pipe)

    return render_template('admin_ornamentals_meta.html', result_items=ornamentals_meta, total_ornamentals=len(ornamentals_meta),ornamentals_count=ornamentals_count)

@blueprint.route("/admin_ornamentals_shipping", methods = ['GET','POST'])
@login_required
def ornamentals_shipping_point():
    """list latest 500 shipping point ornamentals
    :return:
    """
    FromDate = "FromDate"
    ToDate = "ToDate"
    FromDate1, ToDate1 = 0, 0
    try:
        if request.method == "POST":
            res = request.form.to_dict()
            FromDate = res['fdate']
            ToDate = res['tdate']
            FromDate1, ToDate1 = FromDate.split('/'), ToDate.split('/')
            # print(FromDate1, ToDate1)
        d = dttim.datetime(int(FromDate1[2]), int(FromDate1[0]), int(FromDate1[1]))
        f = dttim.datetime(int(ToDate1[2]), int(ToDate1[0]), int(ToDate1[1]))
        total_shipping = client_raw.ornamentals_raw.find({"report_type": "Shipping Point", "report_date": {'$gte': d, '$lt': f}})
        total_ornamentals = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.ornamentals_raw.find({"report_type": "Shipping Point"}).sort("report_date",-1).limit(500)

        total_ornamentals = client_raw.ornamentals_raw.find({"report_type": "Shipping Point"}).count()
    return render_template('admin_ornamentals_shipping.html',
                           result_items=total_shipping,
                           total_ornamentals=total_ornamentals, FromDate=FromDate, ToDate=ToDate)

@blueprint.route("/admin_ornamentals_terminal", methods = ['GET','POST'])
@login_required
def ornamentals_terminal_market():
    """list latest 500 Terminal Market ornamentals
    :return:
    """
    FromDate = "FromDate"
    ToDate = "ToDate"
    FromDate1, ToDate1 = 0, 0
    try:
        if request.method == "POST":
            res = request.form.to_dict()
            FromDate = res['fdate']
            ToDate = res['tdate']
            FromDate1, ToDate1 = FromDate.split('/'), ToDate.split('/')
            # print(FromDate1, ToDate1)
        d = dttim.datetime(int(FromDate1[2]), int(FromDate1[0]), int(FromDate1[1]))
        f = dttim.datetime(int(ToDate1[2]), int(ToDate1[0]), int(ToDate1[1]))
        total_shipping = client_raw.ornamentals_raw.find({"report_type": "Terminal Market", "report_date": {'$gte': d, '$lt': f}})
        total_ornamentals = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.ornamentals_raw.find({"report_type": "Terminal Market"}).sort("report_date", -1).limit(500)

        total_ornamentals = client_raw.ornamentals_raw.find({"report_type": "Terminal Market"}).count()
    return render_template('admin_ornamentals_terminal.html',
                           result_items=total_shipping,
                           total_ornamentals=total_ornamentals, FromDate=FromDate, ToDate=ToDate)

@blueprint.route("/admin_ornamentals_volume", methods = ['GET','POST'])
@login_required
def ornamentals_volume():
    """list latest 500 Volume/Movement ornamentals
    :return:
    """
    FromDate = "FromDate"
    ToDate = "ToDate"
    FromDate1, ToDate1 = 0, 0
    try:
        if request.method == "POST":
            res = request.form.to_dict()
            FromDate = res['fdate']
            ToDate = res['tdate']
            FromDate1, ToDate1 = FromDate.split('/'), ToDate.split('/')
            # print(FromDate1, ToDate1)
        d = dttim.datetime(int(FromDate1[2]), int(FromDate1[0]), int(FromDate1[1]))
        f = dttim.datetime(int(ToDate1[2]), int(ToDate1[0]), int(ToDate1[1]))
        total_shipping = client_raw.ornamentals_raw.find({"report_type": "Movement", "report_date": {'$gte': d, '$lt': f}})
        total_ornamentals = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.ornamentals_raw.find({"report_type": "Movement"}).sort("report_date", -1).limit(500)

        total_ornamentals = client_raw.ornamentals_raw.find({"report_type": "Movement"}).count()
    return render_template('admin_ornamentals_volume.html',
                           result_items=total_shipping,
                           total_ornamentals=total_ornamentals, FromDate=FromDate, ToDate=ToDate)


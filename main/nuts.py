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


blueprint = Blueprint('nuts', __name__)

@blueprint.route("/admin_nuts_meta")
@login_required
def nuts_list():
    """list all available nuts and respective permission.
    :return:
    """
    nuts_meta = client_raw.nuts_raw.distinct("Commodity")

    pipe = [{'$group': {'_id': "$Commodity", "Terminal_Market": {
        '$sum': {'$cond': {'if': {'$eq': ["$report_type", "Terminal Market"]}, 'then': 1, 'else': 0}}},
                        "Shipping_Point": {'$sum': {
                            '$cond': {'if': {'$eq': ["$report_type", "Shipping Point"]}, 'then': 1, 'else': 0}}},
                        "Movement": {
                            '$sum': {'$cond': {'if': {'$eq': ["$report_type", "Movement"]}, 'then': 1, 'else': 0}}}}}]

    nuts_count = client_raw.nuts_raw.aggregate(pipeline=pipe)

    return render_template('admin_nuts_meta.html', result_items=nuts_meta, total_nuts=len(nuts_meta),nuts_count=nuts_count)

@blueprint.route("/admin_nuts_shipping", methods = ['GET','POST'])
@login_required
def nuts_shipping_point():
    """list latest 500 shipping point nuts
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
        total_shipping = client_raw.nuts_raw.find({"report_type": "Shipping Point", "report_date": {'$gte': d, '$lt': f}})
        total_nuts = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.nuts_raw.find({"report_type": "Shipping Point"}).sort("report_date", -1).limit(500)

        total_nuts = client_raw.nuts_raw.find({"report_type": "Shipping Point"}).count()
    return render_template('admin_nuts_shipping.html',
                           result_items=total_shipping,
                           total_nuts=total_nuts, FromDate=FromDate, ToDate=ToDate)

@blueprint.route("/admin_nuts_terminal", methods = ['GET','POST'])
@login_required
def nuts_terminal_market():
    """list latest 500 Terminal Market nuts
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
        total_shipping = client_raw.nuts_raw.find({"report_type": "Terminal Market", "report_date": {'$gte': d, '$lt': f}})
        total_nuts = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.nuts_raw.find({"report_type": "Terminal Market"}).sort("report_date", -1).limit(500)

        total_nuts = client_raw.nuts_raw.find({"report_type": "Terminal Market"}).count()
    return render_template('admin_nuts_terminal.html',
                           result_items=total_shipping,
                           total_nuts=total_nuts, FromDate=FromDate, ToDate=ToDate)

@blueprint.route("/admin_nuts_volume", methods = ['GET','POST'])
@login_required
def nuts_volume():
    """list latest 500 Volume/Movement nuts
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
        total_shipping = client_raw.nuts_raw.find({"report_type": "Movement", "report_date": {'$gte': d, '$lt': f}})
        total_nuts = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.nuts_raw.find({"report_type": "Movement"}).sort("report_date", -1).limit(500)

        total_nuts = client_raw.nuts_raw.find({"report_type": "Movement"}).count()
    return render_template('admin_nuts_volume.html',
                           result_items=total_shipping,
                           total_nuts=total_nuts, FromDate=FromDate, ToDate=ToDate)




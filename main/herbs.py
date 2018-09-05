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

blueprint = Blueprint('herbs', __name__)

@blueprint.route("/admin_herbs_meta")
@login_required
def herbs_list():
    """list all available herbs and respective permission.
    :return:
    """
    herbs_meta = client_raw.herbs_raw.distinct("Commodity")

    pipe = [{'$group': {'_id': "$Commodity", "Terminal_Market": {
        '$sum': {'$cond': {'if': {'$eq': ["$report_type", "Terminal Market"]}, 'then': 1, 'else': 0}}},
                        "Shipping_Point": {'$sum': {
                            '$cond': {'if': {'$eq': ["$report_type", "Shipping Point"]}, 'then': 1, 'else': 0}}},
                        "Movement": {
                            '$sum': {'$cond': {'if': {'$eq': ["$report_type", "Movement"]}, 'then': 1, 'else': 0}}}}}]

    herbs_count = client_raw.herbs_raw.aggregate(pipeline=pipe)

    return render_template('admin_herbs_meta.html', result_items=herbs_meta, total_herbs=len(herbs_meta),herbs_count=herbs_count)

@blueprint.route("/admin_herbs_shipping", methods=['GET','POST'])
@login_required
def herbs_shipping_point():
    """list latest 500 shipping point herbs
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
        total_shipping = client_raw.herbs_raw.find({"report_type": "Shipping Point", "report_date": {'$gte': d, '$lt': f}})
        total_herbs = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.herbs_raw.find({"report_type":"Shipping Point"}).sort("report_date", -1).limit(500)

        total_herbs = client_raw.herbs_raw.find({"report_type":"Shipping Point"}).count()
    return render_template('admin_herbs_shipping.html',
                           result_items=total_shipping,
                           total_herbs=total_herbs,FromDate=FromDate,ToDate=ToDate)

@blueprint.route("/admin_herbs_terminal", methods=['GET','POST'])
@login_required
def herbs_terminal_market():
    """list latest 500 Terminal Market herbs
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
        total_shipping = client_raw.herbs_raw.find(
            {"report_type": "Terminal Market", "report_date": {'$gte': d, '$lt': f}})
        total_herbs = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.herbs_raw.find({"report_type": "Terminal Market"}).sort("report_date", -1).limit(500)

        total_herbs = client_raw.herbs_raw.find({"report_type": "Terminal Market"}).count()
    return render_template('admin_herbs_terminal.html',
                           result_items=total_shipping,
                           total_herbs=total_herbs, FromDate=FromDate, ToDate=ToDate)

@blueprint.route("/admin_herbs_volume", methods=['GET','POST'])
@login_required
def herbs_volume():
    """list latest 500 Volume/Movement herbs
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
        total_shipping = client_raw.herbs_raw.find(
            {"report_type": "Movement", "report_date": {'$gte': d, '$lt': f}})
        total_herbs = total_shipping.count()
    except Exception as e:

        total_shipping = client_raw.herbs_raw.find({"report_type": "Movement"}).sort("report_date", -1).limit(500)

        total_herbs = client_raw.herbs_raw.find({"report_type": "Movement"}).count()
    return render_template('admin_herbs_volume.html',
                           result_items=total_shipping,
                           total_herbs=total_herbs, FromDate=FromDate, ToDate=ToDate)


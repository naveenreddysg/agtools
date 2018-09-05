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


blueprint = Blueprint('fruits', __name__)

@blueprint.route("/admin_fruits_meta")
@login_required
def fruits_list():
    """list all available fruits and respective permission.
    :return:
    """
    #fruits_meta = client_raw.fruits.find({})
    fruits_meta = client_raw.counts_commodity_each.find({})
    return render_template('admin_fruits_meta.html', result_items=fruits_meta, total_fruits=fruits_meta.count())


@blueprint.route("/admin_fruits_shipping", methods = ['GET','POST'])
@login_required
def fruits_shipping_point():
    """list latest 500 shipping point fruits
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
            print(FromDate1, ToDate1)
        d = dttim.datetime(int(FromDate1[2]), int(FromDate1[0]), int(FromDate1[1]))
        f = dttim.datetime(int(ToDate1[2]), int(ToDate1[0]), int(ToDate1[1]))
        fruits_shipping = client_raw.marketnews.find({"report_type": "Shipping Point", "commodity_type":"fruits","report_date": {'$gte': d, '$lt': f}})
        total_shipping = fruits_shipping.count()
        fallback = ""
        records = [{'commodity': str(terminal['Commodity']),
                    'location': str(terminal['location']),
                    'report_date': dttim.date.strftime(terminal['report_date'], "%Y-%m-%d"),
                    'report_type': str(terminal['report_type']),
                    'type': str(terminal['Type']),
                    'size': str(terminal.get('Item Size', fallback)),
                    'low_high_mostly_price': str(terminal.get('Mostly Low-High Price', fallback)),
                    'low_high_price': str(terminal.get('Low-High Price', fallback)),
                    'package': str(terminal.get('Package', fallback)),
                    'grade': str(terminal.get('Grade', fallback)),
                    'variety': str(terminal.get('Variety', fallback)),
                    'market': str(terminal['Market']),
                    'color': str(terminal.get('Color', fallback)),
                    'comment': str(terminal.get('Comment', fallback)),
                    'comments': str(terminal.get('Comments', fallback)),
                    'sub_variety': str(terminal.get('Sub Variety', fallback)),
                    'crawl_date': str(terminal.get('crawl_date', fallback)),
                    'unit_of_sale': str(terminal.get('Unit of Sale', fallback)),
                    'storage': str(terminal.get('Storage', fallback)),
                    'appearance': str(terminal.get('Appearance', fallback)),
                    'season': str(terminal.get('Season', fallback)),
                    'quality': str(terminal.get('Quality', fallback))
                    } for terminal in fruits_shipping]
    except Exception as e:
        fruits_shipping = client_raw.marketnews.find({'commodity_type': cts.COMMODITY_CLASS[0].lower(),
                                                  'report_type': cts.COMMODITY_REPORT_TYPE[0]}).sort("report_date", -1).limit(500)
    # total_shipping = client_raw.counts_commodity_class.find_one({'count_type': 'commodity_class',
    #                                                          'report_type': cts.COMMODITY_REPORT_TYPE[0],
    #                                                          'commodity_class': cts.COMMODITY_CLASS[0]})

        total_shipping = client_raw.marketnews.find({"report_type":"Shipping Point","commodity_type":"fruits"}).count()
        fallback = ""
        records = [{'commodity': str(terminal['Commodity']),
                              'location': str(terminal['location']),
                              'report_date': dttim.date.strftime(terminal['report_date'], "%Y-%m-%d"),
                              'report_type': str(terminal['report_type']),
                              'type': str(terminal['Type']),
                              'size': str(terminal.get('Item Size', fallback)),
                              'low_high_mostly_price': str(terminal.get('Mostly Low-High Price', fallback)),
                              'low_high_price': str(terminal.get('Low-High Price', fallback)),
                              'package': str(terminal.get('Package',fallback)),
                              'grade': str(terminal.get('Grade',fallback)),
                              'variety': str(terminal.get('Variety',fallback)),
                              'market': str(terminal['Market']),
                              'color': str(terminal.get('Color',fallback)),
                              'comment': str(terminal.get('Comment', fallback)),
                              'comments': str(terminal.get('Comments', fallback)),
                              'sub_variety': str(terminal.get('Sub Variety',fallback)),
                              'crawl_date':str(terminal.get('crawl_date',fallback)),
                              'unit_of_sale': str(terminal.get('Unit of Sale', fallback)),
                              'storage': str(terminal.get('Storage',fallback)),
                              'appearance': str(terminal.get('Appearance', fallback)),
                              'season': str(terminal.get('Season', fallback)),
                              'quality': str(terminal.get('Quality', fallback))
                } for terminal in fruits_shipping]
    return render_template('admin_fruits_shipping.html',
                           result_items=records,total_fruits=total_shipping,FromDate=FromDate,ToDate=ToDate)
                           # total_fruits=total_shipping['total_count']


@blueprint.route("/admin_fruits_terminal", methods = ['GET','POST'])
@login_required
def fruits_terminal_market():
    """list latest 500 terminal Market fruits
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
            print(FromDate1, ToDate1)
        d = dttim.datetime(int(FromDate1[2]), int(FromDate1[0]), int(FromDate1[1]))
        f = dttim.datetime(int(ToDate1[2]), int(ToDate1[0]), int(ToDate1[1]))
        fruits_terminal = client_raw.marketnews.find({"report_type": "Terminal Market", "commodity_type": "fruits", "report_date": {'$gte': d, '$lt': f}})
        total_count = fruits_terminal.count()
        fallback = ""
        records = [{'commodity': str(terminal['Commodity']),
                    'location': str(terminal.get('location', fallback)),
                    'origin': str(terminal.get('Origin', fallback)),
                    'report_date': dttim.date.strftime(terminal['report_date'], "%Y-%m-%d"),
                    'report_type': str(terminal['report_type']),
                    'district': str(terminal.get('Origin District', fallback)),
                    'type': str(terminal.get('Type', fallback)),
                    'size': str(terminal.get('Item Size', fallback)),
                    'low_high_mostly_price': str(terminal.get('Mostly Low-High Price', fallback)),
                    'low_high_price': str(terminal.get('Low-High Price', fallback)),
                    'package': str(terminal.get('Package', fallback)),
                    'grade': str(terminal.get('Grade', fallback)),
                    'variety': str(terminal.get('Variety', fallback)),
                    'repacked': str(terminal.get('Repacked', fallback)),
                    'market': str(terminal.get('Market', fallback)),
                    'color': str(terminal.get('Color', fallback)),
                    'comment': str(terminal.get('Comment', fallback)),
                    'comments': str(terminal.get('Comments', fallback)),
                    'sub_variety': str(terminal.get('Sub Variety', fallback)),
                    'crawl_date': str(terminal.get('crawl_date', fallback)),
                    'trans_mode': str(terminal.get('Trans Mode', fallback)),
                    'unit_of_sale': str(terminal.get('Unit of Sale', fallback)),
                    'storage': str(terminal.get('Storage', fallback)),
                    'appearance': str(terminal.get('Appearance', fallback))
                    } for terminal in fruits_terminal]
    except Exception as e:
        fruits_terminal = client_raw.marketnews.find({'commodity_type': cts.COMMODITY_CLASS[0].lower(),
                                                  'report_type': cts.COMMODITY_REPORT_TYPE[1]}).sort("report_date", -1).limit(500)
    # total_count = client_raw.counts_commodity_class.find_one({'count_type': 'commodity_class',
    #                                                          'report_type': cts.COMMODITY_REPORT_TYPE[1],
    #                                                          'commodity_class': cts.COMMODITY_CLASS[0]})

        total_count = client_raw.marketnews.find({"report_type":"Terminal Market","commodity_type":"fruits"}).count()
        fallback = ""
        records = [{'commodity': str(terminal['Commodity']),
                    'location': str(terminal.get('location', fallback)),
                    'origin': str(terminal.get('Origin', fallback)),
                    'report_date': dttim.date.strftime(terminal['report_date'], "%Y-%m-%d"),
                    'report_type': str(terminal['report_type']),
                    'district': str(terminal.get('Origin District', fallback)),
                    'type': str(terminal.get('Type', fallback)),
                    'size':  str(terminal.get('Item Size', fallback)),
                    'low_high_mostly_price': str(terminal.get('Mostly Low-High Price',fallback)),
                    'low_high_price': str(terminal.get('Low-High Price',fallback)),
                    'package': str(terminal.get('Package',fallback)),
                    'grade': str(terminal.get('Grade',fallback)),
                    'variety': str(terminal.get('Variety',fallback)),
                    'repacked': str(terminal.get('Repacked', fallback)),
                    'market': str(terminal.get('Market', fallback)),
                    'color': str(terminal.get('Color', fallback)),
                    'comment': str(terminal.get('Comment', fallback)),
                    'comments': str(terminal.get('Comments', fallback)),
                    'sub_variety': str(terminal.get('Sub Variety',fallback)),
                    'crawl_date':str(terminal.get('crawl_date',fallback)),
                    'trans_mode':str(terminal.get('Trans Mode', fallback)),
                    'unit_of_sale': str(terminal.get('Unit of Sale', fallback)),
                    'storage': str(terminal.get('Storage',fallback)),
                    'appearance': str(terminal.get('Appearance', fallback))
                } for terminal in fruits_terminal]
    return render_template('admin_fruits_terminal.html',
                           result_items=records,total_fruits=total_count,FromDate=FromDate,ToDate=ToDate)
                           # total_fruits=total_count['total_count']


def check_package_count(package_count):
    if package_count is None or package_count=="":
        package_count = 0
    else:
        package_count = package_count
    return package_count


def shippment_date(shippment_date):
    d = dttim.datetime.strptime(shippment_date, '%m/%d/%Y')
    new_date = dttim.date.strftime(d, "%Y-%m-%d")
    return new_date


def carvan_count(package_count):
    if package_count is None or package_count=="":
        package_count = 0
    else:
        package_count = package_count
    return package_count


@blueprint.route("/admin_fruits_volume", methods = ['GET','POST'])
@login_required
def fruits_volume():
    """list latest 500 volume fruits
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
            print(FromDate1, ToDate1)
        d = dttim.datetime(int(FromDate1[2]), int(FromDate1[0]), int(FromDate1[1]))
        f = dttim.datetime(int(ToDate1[2]), int(ToDate1[0]), int(ToDate1[1]))
        fruits_records = client_raw.marketnews.find({"report_type": "Movement", "commodity_type": "fruits", "report_date": {'$gte': d, '$lt': f}})
        total_count = fruits_records.count()
        fallback = ""
        fallbackint = 0
        package_count = 0
        records = [{'commodity': str(terminal['Commodity']),
                    'location': str(terminal.get('Location', fallback)),
                    'report_date': dttim.date.strftime(terminal['report_date'], "%Y-%m-%d"),
                    'shipment_date': shippment_date(terminal['Shipment Date']),
                    'report_type': str(terminal['report_type']),
                    'district': str(terminal.get('District', fallback)),
                    'import_export': str(terminal.get('Import/Export', fallback)),
                    'type': str(terminal.get('Type', fallback).lower()),
                    # 'size':  str(terminal.get('Item Size', fallback)),
                    'lb_units': int(terminal.get('10000 lb units', fallbackint)),
                    'package': str(terminal.get('Package', fallback)),
                    'grade': str(terminal.get('Grade', fallback)),
                    'variety': str(terminal.get('Variety', fallback)),
                    'season': int(terminal.get('Season', fallbackint)),
                    'package_count': int(check_package_count(terminal['Package Count'])),
                    'state': str(terminal.get('state', fallback)),
                    'market': str(terminal.get('Market', fallback)),
                    'comments': str(terminal.get('Comments', fallback)),
                    'adjustments': str(terminal.get('Adjustments', fallback)),
                    'offerings': str(terminal.get('Offerings', fallback)),
                    'sub_variety': str(terminal.get('Sub Variety', fallback)),
                    'crawl_date': str(terminal.get('crawl_date', fallback)),
                    'trans_mode': str(terminal.get('Trans Mode', fallback)),
                    'car_van_count': int(carvan_count(terminal['Car/Van Count']))
                    } for terminal in fruits_records]
    except Exception as e:
        fruits_records = client_raw.marketnews.find({'commodity_type': cts.COMMODITY_CLASS[0].lower(),
                                                  'report_type': cts.COMMODITY_REPORT_TYPE[2]}).sort("report_date", -1).limit(500)
    # total_count = client_raw.counts_commodity_class.find_one({'count_type': 'commodity_class',
    #                                                          'report_type': cts.COMMODITY_REPORT_TYPE[2],
    #                                                          'commodity_class': cts.COMMODITY_CLASS[0]})

        total_count = client_raw.marketnews.find({"report_type":"Movement","commodity_type":"fruits"}).count()
        fallback = ""
        fallbackint = 0
        package_count = 0
        records = [{'commodity': str(terminal['Commodity']),
                    'location': str(terminal.get('Location', fallback)),
                    'report_date': dttim.date.strftime(terminal['report_date'], "%Y-%m-%d"),
                    'shipment_date': shippment_date(terminal['Shipment Date']),
                    'report_type': str(terminal['report_type']),
                    'district': str(terminal.get('District', fallback)),
                    'import_export': str(terminal.get('Import/Export',fallback)),
                    'type': str(terminal.get('Type', fallback).lower()),
                    #'size':  str(terminal.get('Item Size', fallback)),
                    'lb_units': int(terminal.get('10000 lb units',fallbackint)),
                    'package': str(terminal.get('Package',fallback)),
                    'grade': str(terminal.get('Grade',fallback)),
                    'variety': str(terminal.get('Variety',fallback)),
                    'season': int(terminal.get('Season',fallbackint)),
                    'package_count': int(check_package_count(terminal['Package Count'])),
                    'state': str(terminal.get('state', fallback)),
                    'market': str(terminal.get('Market', fallback)),
                    'comments': str(terminal.get('Comments', fallback)),
                    'adjustments': str(terminal.get('Adjustments', fallback)),
                    'offerings': str(terminal.get('Offerings', fallback)),
                    'sub_variety': str(terminal.get('Sub Variety',fallback)),
                    'crawl_date':str(terminal.get('crawl_date',fallback)),
                    'trans_mode':str(terminal.get('Trans Mode', fallback)),
                    'car_van_count': int(carvan_count(terminal['Car/Van Count']))
                } for terminal in fruits_records ]
    return render_template('admin_fruits_volume.html',
                           result_items=records,total_fruits=total_count,FromDate=FromDate,ToDate=ToDate)
                           # total_fruits=total_count['total_count']
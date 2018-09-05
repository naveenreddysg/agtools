"""Purpose is to serve requests related to User Create Delete and update

"""
from flask import abort, Blueprint, session, redirect, render_template, request, url_for
from flask_login import current_user
from flask_login import login_required
import constants as cts
from utils import validate_json, validate_registration_input
from flask import jsonify
import datetime as dttim
from models import client_raw
import uuid
from emails import user_register_email


__author__ = 'hughson.simon@gmail.com'


blueprint = Blueprint('exchangerates', __name__)

@blueprint.route("/admin_exchangerates_canada")
@login_required
def canada_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    canada_rates = client_raw.exchange_rates_live_raw.find({"class":"Canada"}).sort([("report_date",-1)])
    return render_template('admin_exchangerates_canada.html',
                           result_items=canada_rates,
                           total_canada_rates=canada_rates.count())

@blueprint.route("/admin_exchangerates_mexico")
@login_required
def mexico_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    mexico_rates = client_raw.exchange_rates_live_raw.find({"class":"Mexico"}).sort([("report_date",-1)])
    return render_template('admin_exchangerates_mexico.html',
                           result_items=mexico_rates,
                           total_mexico_rates=mexico_rates.count())
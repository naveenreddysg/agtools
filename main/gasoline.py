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
from flask_bootstrap import Bootstrap


__author__ = 'hughson.simon@gmail.com'


blueprint = Blueprint('gasoline', __name__)

@blueprint.route("/admin_gasoline_gasprices")
@login_required
def gasprices_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    gasprices = client_raw.gas_raw.find({}).sort([("report_date",-1)])
    return render_template('admin_gasoline_gasprices.html',
                           result_items=gasprices,
                           total_gasprices=gasprices.count())

@blueprint.route("/admin_gasoline_fuelprices")
@login_required
def fuelprices_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    fuelprices = client_raw.diesel_raw.find({}).sort([("report_date",-1)])
    return render_template('admin_gasoline_fuelprices.html',
                           result_items=fuelprices,
                           total_fuelprices=fuelprices.count())
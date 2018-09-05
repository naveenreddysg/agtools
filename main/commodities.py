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


blueprint = Blueprint('commodities', __name__)

@blueprint.route("/admin_commodities_meta")
@login_required
def fruits_list():
    """list all available fruits and respective permission.
    :return:
    """

    fruits_meta = client_raw.commodities_meta.find({"Commodity_Type":"fruits"})
    vegetables_meta = client_raw.commodities_meta.find({"Commodity_Type":"vegetables"})
    herbs_meta = client_raw.commodities_meta.find({"Commodity_Type":"herbs"})
    ornamentals_meta = client_raw.commodities_meta.find({"Commodity_Type":"ornamentals"})
    nuts_meta = client_raw.commodities_meta.find({"Commodity_Type":"nuts"})
    return render_template('admin_commodities_meta.html', result_items=fruits_meta,total_fruits=fruits_meta.count(),
                                                          result_items1=vegetables_meta,total_vegetables=vegetables_meta.count(),
                                                          result_items2=herbs_meta,total_herbs=herbs_meta.count(),
                                                          result_items3=ornamentals_meta,total_ornamentals=ornamentals_meta.count(),
                                                          result_items4=nuts_meta, total_nuts=nuts_meta.count())



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


blueprint = Blueprint('consumer', __name__)

@blueprint.route("/admin_consumerprice_cities")
@login_required
def cities_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    cities = client_raw.cpi_raw.find({"class":"all_cities"})
    return render_template('admin_consumerprice_cities.html',
                           result_items=cities,
                           total_cities=cities.count())

@blueprint.route("/admin_consumerprice_fruits")
@login_required
def fruits_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    fruits = client_raw.cpi_raw.find({"class":"fresh_fruits"})
    return render_template('admin_consumerprice_fruits.html',
                           result_items=fruits,
                           total_fruits=fruits.count())

@blueprint.route("/admin_consumerprice_food")
@login_required
def fruitsvegetables_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    fruitsvegetables = client_raw.cpi_raw.find({"class":"fruits_vegetables"})
    return render_template('admin_consumerprice_fruitsvegetables.html',
                           result_items=fruitsvegetables,
                           total_fruitsvegetables=fruitsvegetables.count())

@blueprint.route("/admin_consumerprice_vegetables")
@login_required
def vegetables_list():
    """list all available vegetables and respective permission.
    :return: dict: users dict items with available permissions
    """
    vegetables = client_raw.cpi_raw.find({"class":"fresh_vegetables"})
    return render_template('admin_consumerprice_vegetables.html',
                           result_items=vegetables,
                           total_vegetables=vegetables.count())
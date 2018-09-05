from extensions import db
from extensions import login_manager

from pymongo import MongoClient

def connect_to_server(raw, etl):
    prod = True
    if raw:
        if prod:
            client = MongoClient("mongodb://agroot:Sunshine$2017@10.6.52.71:27111/?authSource=agtools_celery")
        else:
            mongo_server="13.82.27.233"
            monport = 27017
            client = MongoClient("mongodb://agroot:Sunshine$2017@vserver.amicuswa.com:27017/?authSource=agtools_celery&authMechanism=SCRAM-SHA-1")
        client = client.agtools_celery
    else:
        if prod:
            mongo_server="localhost"
            monport = 27111
            client = MongoClient("mongodb://agroot:Sunshine$2017@192.168.10.22:27111/?authSource=dbagtools&authMechanism=SCRAM-SHA-1")
        else:
            mongo_server="13.82.27.233"
            monport = 27111
            client = MongoClient("mongodb://agroot:Sunshine$2017@vserver.amicuswa.com:27111/?authSource=dbagtools&authMechanism=SCRAM-SHA-1")
        client = client.dbagtools
    return client

client_etl = connect_to_server(False, True)
client_raw = connect_to_server(True, False)

client_etl_db = MongoClient("mongodb://agroot:Sunshine$2017@10.6.52.71:27111/?authSource=dbagtools")
# client_etl_db = MongoClient("mongodb://agroot:Sunshine$2017@vserver.amicuswa.com:27017/?authSource=dbagtools&authMechanism=SCRAM-SHA-1")
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    __tablename__ = 'userdetails'
    __bind_key__ = 'db1'

    userId = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(154))
    username = db.Column(db.String(154))
    name = db.Column(db.String(154))
    usertype = db.Column(db.String(54))
    #is_staff = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=True)
    created_time = db.Column(db.String(154))
    usertype_id = db.Column(db.Integer())
    city = db.Column(db.String(154))
    state = db.Column(db.String(154))
    country = db.Column(db.String(154))
    zipcode = db.Column(db.String(154))
    trailexpired = db.Column(db.Integer())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userId)  # python 2
        except NameError:
            return str(self.userId)  # python 3

class Commodity(db.Model):
    __tablename__ = "commodities"
    commodityId = db.Column(db.Integer, primary_key=True)
    commodityName = db.Column(db.String(50))

class Feat(db.Model):
    __tablename__ = "features"
    featureId = db.Column(db.Integer, primary_key=True)
    featureCode = db.Column(db.String(50))
    featureName = db.Column(db.String(50))
    description = db.Column(db.String(100))

class Package(db.Model):
    __tablename__ = "package_details"
    commodityCount = db.Column(db.Integer)
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    packageId = db.Column(db.Integer)
    createdAt = db.Column(db.String(50))
    updatedAt = db.Column(db.String(50))
    finalPrice = db.Column(db.Integer)
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    active = db.Column(db.String(50))

class Subscription(db.Model):
    __tablename__ = "subscription"
    subscriptionid = db.Column(db.Integer,primary_key=True, autoincrement=True)
    subdetails = db.Column(db.String(200))
    price = db.Column(db.Integer)

class SubscriptionPackages(db.Model):
    __tablename__ = "subscription_packages"
    packageId = db.Column(db.Integer,primary_key=True, autoincrement=True)
    packageName = db.Column(db.String(200))
    subscriptionId = db.Column(db.Integer)
    months = db.Column(db.Integer)
    sortOrder = db.Column(db.Integer)
    active = db.Column(db.String(20))

class SubuserType(db.Model):
    __tablename__ = "subusertype"
    subusertypeid = db.Column(db.Integer,primary_key=True, autoincrement=True)
    usertypeid = db.Column(db.Integer)
    subusername = db.Column(db.String(100))

class UserCommodity(db.Model):
    __tablename__ = "user_commodity"
    id = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    subusertypeid = db.Column(db.Integer)
    subscriptionid = db.Column(db.Integer)
    commodityid = db.Column(db.Integer,primary_key=True, autoincrement=True)
    commodityName = db.Column(db.String(50))
    subscriptionStatus = db.Column(db.String(50))
    enddate = db.Column(db.String(50))
    packageDetailId = db.Column(db.Integer)
    payerId = db.Column(db.Integer)
    paypalId = db.Column(db.Integer)
    createdAt = db.Column(db.String(50))

class UserPack(db.Model):
    __tablename__ = "user_packages"
    userid = db.Column(db.Integer,primary_key=True, autoincrement=True)
    subusertypeid = db.Column(db.Integer)
    subscriptionid = db.Column(db.Integer)
    subscriptionStatus = db.Column(db.String(50))
    enddate = db.Column(db.String(100))
    packageDetailId = db.Column(db.Integer)
    createdAt = db.Column(db.String(100))
    packageId = db.Column(db.Integer)
    userpkgId = db.Column(db.Integer)
    paypalId = db.Column(db.Integer)
    payerId = db.Column(db.Integer)
    token = db.Column(db.String(50))
    isNew = db.Column(db.String(50))

class UserPkgCommodity(db.Model):
    __tablename__ = "user_pkg_commodity"
    commodityName = db.Column(db.String(100))
    commodityId = db.Column(db.Integer,primary_key=True, autoincrement=True)
    userpkgId = db.Column(db.Integer)
    commodityType = db.Column(db.String(50))

class UserType(db.Model):
    __tablename__ = "usertype"
    usertypeId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    usertype = db.Column(db.String(50))

class UserFeature(db.Model):
    __tablename__ = "usertype_feature_mapping"
    usertypeId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    fcode = db.Column(db.String(50))
    subusertypeId = db.Column(db.Integer)
    subscriptiontype = db.Column(db.String(50))

class AuditLogs(db.Model):
    __tablename__ = "auditlog"
    logId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True)
    firstname = db.Column(db.String(140), unique=True)
    lastname = db.Column(db.String(140), unique=True)
    activityType = db.Column(db.String(140), unique=True)
    loggedTime = db.Column(db.String(240), unique=True)
    commodity = db.Column(db.String(140), unique=True)
    userId = db.Column(db.Integer)

    def get_id(self):
        try:
            return unicode(self.logId)  # python 2
        except NameError:
            return str(self.logId)  # python 3


class AuthUserGroups(db.Model):
    __tablename__="auth_user_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('auth_group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    created_on = db.Column(db.String(100))


class Emails(db.Model):
    __tablename__ = 'content_emails'
    id = db.Column(db.Integer, primary_key=True)
    email_message = db.Column(db.Text)
    email_subject = db.Column(db.Text)
    email_name = db.Column(db.Text)
    email_status = db.Column(db.String(26))
    email_slug = db.Column(db.String(26))

class AuthGroups(db.Model):
    __tablename__="auth_group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    created_on = db.Column(db.String(100))
    auth_group_permissions=db.relationship('AuthGroupPermissions', backref='authgroupperm', lazy='dynamic')

    @property
    def list(self):
        return {
            "id": self.id,
            "name": self.name
        }


class AuthGroupPermissions(db.Model):
    __tablename__="auth_group_permissions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('auth_group.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('auth_permission.id'))
    created_on = db.Column(db.String(100))
    #auth_permissions=db.relationship('AuthPermissions', backref='authpermits', lazy='dynamic')

    @property
    def list(self):
        return {
            "id": self.id,
            "group_id": self.group_id
        }

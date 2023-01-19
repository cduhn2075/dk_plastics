# import os
#
import itsdangerous

from pe_reports.manage_login.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from time import sleep
from pe_reports import db, app
# from flask_login import UserMixin
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# import re
# from importlib_resources import files
#
# from pe_reports.data import config
#
#
# import glob
#
# s = Serializer('secret', 5)
#
# token = s.dumps({'user_id': 1}).decode('utf-8')
# sleep(10)
# theload = s.loads(token)
# def get_reset_token(self, expires_sec=1800):
try:
    user = User.query.filter_by(username='cduhn75').first()
    s = Serializer(app.config['SECRET_KEY'], 5)

    thetoken = s.dumps({"user_id": user.username}).decode('utf-8')

    print(thetoken)
    sleep(10)
    print(s.loads(thetoken)['user_id'])
except itsdangerous.SignatureExpired as e:
    print(f'The token is expired {e.payload}.')

# print(f'The token is {token}')




# def isValidSSN(str):
#     # Regex to check valid
#     # SSN (Social Security Number).
#     regex = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"
#
#     # Compile the ReGex
#     p = re.compile(regex)
#
#     # If the string is empty
#     # return false
#     if (str == None):
#         return False
#
#     # Return if the string
#     # matched the ReGex
#     if (re.search(p, str)):
#         return True
#     else:
#         return False

# print(isValidSSN('645-22-5889'))

# REPORT_DB_CONFIG = files("pe_reports").joinpath("data/dbconfig.config")
#
# BASEDIR = os.path.abspath(os.path.dirname(REPORT_DB_CONFIG))


#
# myfile = glob.glob(f'{BASEDIR}/*.config')
# # print(BASEDIR)
# print(myfile)
# # print(config)

# Local packages
# from pe_reports.manage_login.models import User
# from pe_reports import db, app
#
# #PE-Reports import forms
# from pe_reports.manage_login.forms import LoginForm, RegistrationForm
#
# #Third party packages
# from flask import render_template, flash, redirect, url_for, Blueprint, request
# from flask_login import login_user, login_required, logout_user
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#
#
# def get_reset_token(self, expires_sec=1800):
#     user = User.query.filter_by(username='cduhn75').first()
#     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#
#     return s.dumps({"user_id": user.id}).decode('utf-8')
#
#
# print(get_reset_token())





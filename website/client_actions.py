from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename


# from datetime import datetime
from datetime import datetime, timedelta
import base64
import random
import imghdr
import datetime as dt

from . import DateToolKit as dtk
from . import function_pool
from . import ScreenGoRoute
from . import id_generator

from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
from .SarahDBClient import encrypt

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserFBET"), None




client_actions = Blueprint('client_actions', __name__)
ca = client_actions


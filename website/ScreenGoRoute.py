from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import DateToolKit as dtk
import base64
import json
import imghdr
from .SarahDBClient.db import dbORM
from .SarahDBClient import encrypt
import random
from . import function_pool
import datetime as dt
from . import id_generator
from datetime import datetime, timedelta

@login_required
def go_to(screen_id, _redirect=False, **kwargs):
	"""
	Handles the redirection to different screens within the application dashboard.

	Parameters:
	- screen_id (str): ID of the screen to navigate to.
	- _redirect (bool): Whether to redirect to the main dashboard or not (default is False).
	- kwargs (dict): Additional keyword arguments to customize the context passed to the template.

	Returns:
	- A rendered template for the respective dashboard screen or a redirection to the dashboard/login screen.
	"""

	if _redirect:
		return redirect(url_for("views.dashboard"))

	# Fetch the current user's information from the database
	u = dbORM.get_all("UserFBET").get(str(current_user.id))
	print(">>>>>>>>>>>>>>>>>", current_user.id)

	if not u:
		flash("User not found", category=['EOC', 'Oops! Seems you will have to login again'])
		return redirect(url_for("login"))

	def tryGetKwargs(keyword, exception_text):
		"""
		Attempts to retrieve a value from kwargs; returns a fallback text if the key is not found.

		Parameters:
		- keyword (str): The key to look for in kwargs.
		- exception_text (str): Fallback value if the key is missing.

		Returns:
		- The value associated with the keyword in kwargs or the fallback text.
		"""
		try:
			return kwargs[keyword]
		except:
			return exception_text

	# Context setup with user and system-specific data
	context = {
		'CUser': u,
		'ScreenID': screen_id,
		'DashboardTabs': ['All', 'Your Level', f'Today'],
		'ActiveDSH_Tab': tryGetKwargs('main_tab', 'All'),
		'DTK': dtk,
		'GetOppositeVisibility': function_pool.GetOppositeVisibility,
		'ToJoin': function_pool.toJoin,
		'DeviceType': function_pool.detectDeviceType(kwargs['request']),
		'WhichDevice': function_pool.which_device,
		'GetDBItem': function_pool.getDBItem,
		'DBORM': function_pool.dbORMJinja,
		'ShortenText': function_pool.shorten_text,
		'CurrentDate': function_pool.getDateTime()[0],
		'DecryptTYPE13': encrypt.decrypter,
		'ToInt': int,
		'LengthFunc': len,
		'ToStr': str,
		'ToFloat': float,
		'RandomID': id_generator.generateTID,
		'NoneType': None,
		'RoundFloat': round,
		'EnumerateFunc': enumerate,
		'ZipFunc': zip,
		'ToFloatToInt': function_pool.floatToInt,
		'PythonEval': function_pool.python_eval,
		'HideSensitive': function_pool.change_to_dots,
		'Thousandify': function_pool.thousandify,
		'GetIMG': dbORM.GetBase64Media,
		'getMIME': function_pool.get_mime_type,
		'TimeDifference': function_pool.calcTimeDifference,
		'CurrentTime': function_pool.getDateTime()[1],
		'HTMLBreak_': function_pool.HTMLBreak,
		'CONTRACT_CODE': function_pool.getContractCode(),
		'API_KEY': function_pool.getAPIKey(),
		'IsADPost': function_pool.IsADPost,
		'SECRET_KEY': function_pool.getSecretKey()
	}

	# Fetch user notifications
	notifications = dbORM.get_all("NotificationIEEE")
	context['UserNotifications'] = [n for n in notifications.values() if n['recipient_id'] == u['id']]
	context['NotificationCount'] = sum(1 for n in context['UserNotifications'] if n['status'] == 'delivered')
	context['NotificationCount'] = int(context['NotificationCount']) if int(context['NotificationCount']) >= 10 else int(context['NotificationCount'])
	context['TheNotification'] = tryGetKwargs("the_notification", '')

	# Fetch the list of users excluding admins
	users = dbORM.get_all("UserFBET")
	context['UserList'] = [u for u in users.values() if u['role'] != 'admin' or u['id'] != context['CUser']['id']]

	# Fetch the list of drives
	drivers = dbORM.get_all("UserFBET")
	context['AllDrivers'] = [d for d in drivers.values() if d['role'] == 'driver']

	

	# ... (existing code)

	data = dbORM.get_all("MatchFBET")
	matches = list(data.values())

	# Sort matches by start_date and start_time
	matches.sort(key=lambda x: (x['start_date'], x['start_time']))

	# Separate matches into "live/recent" and "upcoming"
	current_date = datetime.now().date()
	live_recent_matches = []
	upcoming_matches = {}

	for match in matches:
		match_date = datetime.strptime(match['start_date'], '%Y-%m-%d').date()
		if match_date <= current_date:
			live_recent_matches.append(match)
		else:
			if match_date not in upcoming_matches:
				upcoming_matches[match_date] = []
			upcoming_matches[match_date].append(match)

	context['live_recent_matches'] = live_recent_matches
	context['upcoming_matches'] = upcoming_matches



	# Inject dynamic data into context from kwargs
	for x, y in kwargs.items():
		context[f'{x}'] = y

	# Determine which template to render
	template = "admin-dashboard.html" if tryGetKwargs('admin_screen', None) else "dashboard.html"
	return render_template(template, **context)

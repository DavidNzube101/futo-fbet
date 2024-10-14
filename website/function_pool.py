# from .db import dbORM
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import base64
import magic
import imghdr
import datetime as dt
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from . import DateToolKit as dtk
import math as Math
import random
from . import id_generator
# from . import encrypt

from .SarahDBClient.db import db
from .SarahDBClient.db import dbORM
from .SarahDBClient import encrypt


def encode_image(file_storage):
    image_data = file_storage.read()
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    return encoded_string

def calcTimeDifference(dpt, ct):
	return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]

def getDBItem(model, column, value, f=False):
	
	try:
		if f == True:
			i = dbORM.find_one(model, column, value)
		else:
			i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
	except Exception as e:
		i = {}

	return i

def isFound(model, column, value):
	if dbORM.find_one(model, column, value)['status'][0] == "not found":
		result = None
	else:
		# print(dbORM.find_one(model, column, value))
		result = dbORM.find_one(model, column, value)['status'][1]

	# print(">>>>>>><><><><><>>>>>>>>>>>>> ", result, " ", dbORM.find_one(model, column, value))
	return result

def returnJSONData(title, content):
	return jsonify({
		"message": {title: content}
	})

def isFoundAll(model, column, value):
	if dbORM.find_all(model, column, value)['status'][0] == "not found":
		result = []
	else:
		# print(dbORM.find_one(model, column, value))
		result = dbORM.find_all(model, column, value)['status'][1]

	# print(">>>>>>><><><><><>>>>>>>>>>>>> ", result, " ", dbORM.find_one(model, column, value))
	return result

def dbORMJinja(what, table, column, value):

	try:
		if what == "get_all":
			return dbORM.get_all(table)[f'{isFound(table, column, value)}']

		elif what == "find_all":
			return isFoundAll(table, column, value)

		else:
			return {}
	except KeyError as e:
		return None

def getComponent(html_file):
	with open(f"website/templates/{html_file}.html", "r") as HTMLFILE:
		html_data = HTMLFILE.read()

	return html_data

def disbandAPROC(aproc_key):

	if "CONKEY" in aproc_key:
		signed_key = aproc_key.replace("CONKEY::", "")
	else:
		return {
			'auth1': None,
			'auth2': None,
			'message': 'Invalid APROC Key.\nDisband unsuccessful.'
		}
	
	auth1, auth2 = map(str, signed_key.split("::"))
	
	return {
		'auth1': encrypt.decrypter(auth1),
		'auth2': encrypt.decrypter(auth2),
		'message': 'APROC Key Signed.\nDisband successful.'
	}

def removeAdmins(d):
	new_list = []
	for _d in d:
		if _d['tier'] != 'god':
			new_list.append(_d)
			
	return new_list
	if dbORM.get_all("UserAPRO")[user_id]['tier'] == 'god':
		return True
	else:
		return False

	the_solution = dbORM.get_all("SolutionAPRO")[f'{isFound("SolutionAPRO", "id", solution_id)}']
	review_data = eval(the_solution['review'])
	bad_count = 0
	good_count = 0
	if str(type(review_data)) == "<class 'list'>":
		for data in review_data:
			for x, y in data.items():

				if y[0] == 1:
					good_count = good_count + 1
				if y[1] == 1:
					bad_count = bad_count + 1

	return [good_count, bad_count]

def shorten_text(text, max_length):

	try:
		words = text.split()
		if len(words) > max_length:
			return " ".join(words[:max_length]) + "..."
		else:
			return text
	except:
		return text

def RandomSearchText():
	texts = ['today assignment', '100 level', 'gst103']
	def returnText():
		return random.choice(texts)

	text1 = returnText()
	text2 = returnText()

	return [text1, text2 if text1 != text2 else returnText()]

def python_eval(exp):

	try:
		return eval(exp)
	except:
		return []

def eddie():
	return "ds"

def loopAppendAndReverse(a, b):
	try:
		for k, v in a.items():
			b.append(v)
		return b[::-1]
	except Exception as e:
		return f"Error occured\nError: {e}"

def toJoin(i, j):
	return f"{i}{j}"

def thousandify(amount):
	amount = "{:,}".format(float(amount))
	return f"{amount}"

def is_test():
	return "True"

def floatToInt(n):
	return f"{Math.ceil(float(n))}"

def getDateTime():
	# Getting Date-Time Info
	current_date = dt.date.today()
	current_time = datetime.now().strftime("%H:%M:%S")

	# Date Format: "YYYY-MM-DD"
	formatted_date = current_date.strftime("%Y-%m-%d")
	date = formatted_date
	time = current_time

	return [date, time]

def getNextBillingDate(billing_format):
	if billing_format == 'month':
		return f"{dt.date.today() + timedelta(days=30)}"
	else:
		return f"{dt.date.today() + timedelta(days=90)}"
	
def getContractCode():
	return "7208450356"

def getAPIKey():
	return "MK_TEST_DBQQF0A5P5"

def getSecretKey():
	return "Z16JHXZY89TXQS8QFF4YJ44HLCS0YHEG"

def change_to_dots(text):
	new_text = []
	for letter in text:
		new_text.append("•")

	return "".join(new_text)

def HTMLBreak(n):
	breaks = ""

	for x in range(int(n)):
		breaks = breaks + "\n<br>"	

	return breaks

def getOppositeTheme(theme):
	if theme == 'light':
		return 'dark'
	else:
		return 'light'

def oppositeCurrency(currency):
	return "NGN" if currency == "$" else "NGN"

def CurrencyExchange():
	v1 = float(f"0.{dtk.split_date(getDateTime()[0])['Day']}") # initial float
	v2 = float(f"0.{dtk.split_date(getDateTime()[0])['Month']}") # error margin

	return round(v1 * v2, 2)

def get_mime_type(data):
	try:
		decoded_data = base64.b64decode(data)
		mime_type = magic.from_buffer(decoded_data, mime=True)
		return mime_type if mime_type else ""
	except:
		decoded_data = base64.b64decode(data)
		image_type = imghdr.what(None, h=decoded_data)
		return f'image/{image_type}' if image_type else ''
    

def checkImagePassError(image_raw):
	try:
		rr = f"data:{getMIME(image_raw)};base64,{image_raw}"
		return "false"
	except:
		return "true"
	
	

def return_approved_subjects():
	subject_codes = []
	subjects = {
		"MTH101": "Mathematics 100 Level",
		"GST103": "Philosophy 100 Level",
		"IFT203": "Information Technology 200 Level"
	}
	for x, y in subjects.items():
		subject_codes.append(x)

	return subject_codes

def GetOppositeVisibility(visibility):
	if visibility == "Private":
		return "Public"
	else:
		return "Private"

def return_faculty(faculty_code):

	faculty_def = {
		"Select a Faculty": "None",
		"SAAT": "School of Agriculture and Agricultural Technology (SAAT)",
		"SBMS": "School of Basic Medical Science (SBMS)",
		"SOBS": "School of Biological Science (SOBS)",
		"SEET": "School of Engineering and Engineering Technology (SEET)",
		"SESET": "School of Electrical Systems and Engineering Technology (SESET)",
		"SOHT": "School of Health Technology (SOHT)",
		"SICT": "School of Information and Communication Technology (SICT)",
		"SLIT": "School of Logistics and Innovation Technology (SLIT)",
		"SOPS": "School of Physical Science (SOPS)",
		"SOES": "School of Environmental Sciences (SOES)",
		"CMHS": "College of Medicine and Health Sciences (CMHS)",
		"SMAT": "School of Management Technology (SMAT)"
	}

	return faculty_def[faculty_code]

def insertAds(**kwargs):
	new_list = []
	new_list.append(kwargs['_list'])
	for i in range(kwargs['interval'], len(new_list) + len(new_list) // kwargs['interval'], kwargs['interval'] + 1):
		new_list.insert(i, kwargs['ad_item'])

	return new_list[::-1]


	# import random

	# # Generate the list from 1 to 10
	# generated_list = list(range(1, 11))

	# # Define the new item and number of random insertions
	# new_item = "new_item"
	# num_insertions = 4  # Number of times to insert the new item

	# # Randomly select positions while avoiding consecutive placements
	# possible_positions = [i for i in range(1, len(generated_list))]  # Possible positions to insert
	# insert_positions = random.sample(possible_positions, num_insertions)  # Pick random positions

	# # Sort the positions so we insert without altering indices
	# insert_positions.sort()

	# # Insert new items at the selected positions
	# for i, pos in enumerate(insert_positions):
	#     generated_list.insert(pos + i, new_item)

	# print(generated_list)


def IsADPost(item):
	print(">>>>>>>>>>>wqwqwq>>>>>sas>>>>>>", type(item))
	if item is None:
		return "false"
	else:
		try:
			if item['visibility'] == 'Public Ad' :
				return "true"
			else:
				return "false"
		except Exception as e:
			return "false"
		



def detectDeviceType(theRequest):
	user_agent = theRequest.user_agent.string.lower()

	if 'android' in user_agent:
		device_type = 'Android'

	elif "iphone" in user_agent:
		device_type = 'iPhone'

	else:
		device_type = 'Desktop'

	return device_type

def which_device(dev_code):
	try:
		if dev_code == "ADR":
			return "Android"
		elif dev_code == "IOS":
			return "iPhone"
		elif dev_code == "DEK":
			return "Desktop"
		else:
			return "JustShow"
	except:
		return "error"

def calculate_net_value(_list):
	single_value = []
	single = []
	for j in _list:
		single.append(j)

	try:
		single.remove({})
	except:
		pass


	for k in single:
		single_value.append(float(k['wallet_balance']))

	# print(single_value)

	return sum(single_value)










# def encode_image(file_storage):
#     """
#     Encodes an image file into a base64 string.

#     Args:
#         file_storage: The image file to be encoded.

#     Returns:
#         A base64 encoded string representation of the image.
#     """
#     image_data = file_storage.read()
#     encoded_string = base64.b64encode(image_data).decode("utf-8")

#     return encoded_string


# def calcTimeDifference(dpt, ct):
#     """
#     Calculates the time difference between two time strings.

#     Args:
#         dpt (str): The departure time in "HH:MM" format.
#         ct (str): The current time in "HH:MM:SS" format.

#     Returns:
#         List[int]: A list of two integers representing hours and minutes of the difference.
#     """
#     return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]


# def getDBItem(model, column, value, f=False):
#     """
#     Retrieves an item from the database by column and value.

#     Args:
#         model: The database model to query.
#         column: The column to match.
#         value: The value to search for.
#         f (bool): A flag indicating whether to find one or return all items.

#     Returns:
#         dict: The database item found, or an empty dictionary on failure.
#     """
#     try:
#         if f == True:
#             i = dbORM.find_one(model, column, value)
#         else:
#             i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
#     except Exception as e:
#         i = {}

#     return i


# def isFound(model, column, value):
#     """
#     Checks if an item exists in the database by column and value.

#     Args:
#         model: The database model to query.
#         column: The column to match.
#         value: The value to search for.

#     Returns:
#         The result of the query if found, or None if not found.
#     """
#     if dbORM.find_one(model, column, value)['status'][0] == "not found":
#         result = None
#     else:
#         result = dbORM.find_one(model, column, value)['status'][1]

#     return result


# def returnJSONData(title, content):
#     """
#     Returns JSON formatted data.

#     Args:
#         title: The title of the message.
#         content: The content of the message.

#     Returns:
#         JSON object containing the title and content.
#     """
#     return jsonify({
#         "message": {title: content}
#     })


# def isFoundAll(model, column, value):
#     """
#     Checks if multiple items exist in the database by column and value.

#     Args:
#         model: The database model to query.
#         column: The column to match.
#         value: The value to search for.

#     Returns:
#         A list of all matching items or an empty list if none found.
#     """
#     if dbORM.find_all(model, column, value)['status'][0] == "not found":
#         result = []
#     else:
#         result = dbORM.find_all(model, column, value)['status'][1]

#     return result


# def dbORMJinja(what, table, column, value):
#     """
#     Executes database operations for Jinja templates.

#     Args:
#         what: The operation to perform (e.g., 'get_all', 'find_all').
#         table: The table to query.
#         column: The column to match.
#         value: The value to search for.

#     Returns:
#         The result of the operation or None on failure.
#     """
#     try:
#         if what == "get_all":
#             return dbORM.get_all(table)[f'{isFound(table, column, value)}']
#         elif what == "find_all":
#             return isFoundAll(table, column, value)
#         else:
#             return {}
#     except KeyError as e:
#         return None


# def getComponent(html_file):
#     """
#     Retrieves HTML content from a specified file.

#     Args:
#         html_file (str): The name of the HTML file (without extension).

#     Returns:
#         str: The content of the HTML file.
#     """
#     with open(f"website/templates/{html_file}.html", "r") as HTMLFILE:
#         html_data = HTMLFILE.read()

#     return html_data


# def disbandAPROC(aproc_key):
#     """
#     Decrypts an APROC key and returns authentication details.

#     Args:
#         aproc_key (str): The APROC key to decrypt.

#     Returns:
#         dict: A dictionary containing the decrypted auth keys and a message.
#     """
#     if "CONKEY" in aproc_key:
#         signed_key = aproc_key.replace("CONKEY::", "")
#     else:
#         return {
#             'auth1': None,
#             'auth2': None,
#             'message': 'Invalid APROC Key.\nDisband unsuccessful.'
#         }
    
#     auth1, auth2 = map(str, signed_key.split("::"))
    
#     return {
#         'auth1': encrypt.decrypter(auth1),
#         'auth2': encrypt.decrypter(auth2),
#         'message': 'APROC Key Signed.\nDisband successful.'
#     }


# def removeAdmins(d):
#     """
#     Removes users with the 'god' tier from a list of users.

#     Args:
#         d (list): The list of users.

#     Returns:
#         list: The list without 'god' tier users.
#     """
#     new_list = []
#     for _d in d:
#         if _d['tier'] != 'god':
#             new_list.append(_d)
            
#     return new_list



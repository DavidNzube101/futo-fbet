from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin

import json
import os
import random

from .SarahDBClient.db import db
from . import function_pool
from flask_mail import Mail, Message

from .SarahDBClient.db import dbORM
from .SarahDBClient.encrypt import encrypter, decrypter
from .DateToolKit import split_date
from . import id_generator

from . import ScreenGoRoute

if dbORM == None:
    User, Record = None, None


def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'FBETFBETFBET'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__).replace('\\', '/'), 'static/_UM_')
    print(f"UF: ({UPLOAD_FOLDER})")

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = f'{decrypter("&012;&009;&022;&005;&st;&006;&002;&005;&020;&020;&009;&014;&007;&at;&007;&013;&001;&009;&012;&st;&003;&015;&013;")}'
    app.config['MAIL_PASSWORD'] = f'{decrypter("&019;&015;&010;&014;&026;&013;&025;&018;&003;&009;&026;&003;&012;&013;&009;&005;")}'
    app.config['MAIL_DEBUG'] = True

    mail = Mail(app)


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .admin_actions import admin_actions
    from .client_actions import client_actions
    from .payment_handler import payment_handler_actions

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin_actions, url_prefix='/')
    app.register_blueprint(payment_handler_actions, url_prefix='/')
    app.register_blueprint(client_actions, url_prefix='/')

    @app.errorhandler(500)
    def internal_server_error(e, err_code=500):
        app.logger.error(f"Internal Server Error: {e}")
        return render_template('broken-page.html', error=e, code=err_code), 500

    @app.errorhandler(404)
    def internal_server_error(e, err_code=404):
        app.logger.error(f"Route Not Found: {e}")
        return render_template('broken-page.html', error=e, code=err_code), 404

    # @app.errorhandler(500)
    # def internal_server_error(e, err_code=500):
    #     app.logger.error(f"Internal Server Error: {e}")
    #     return render_template('broken-page.html', error=e, code=err_code), 500

    from flask_login import UserMixin, LoginManager

    FL_Login = LoginManager(app)
    FL_Login.login_view = 'login'

    class UserClass:
        def __init__(self, id):
            self.id = id

        @staticmethod
        def is_authenticated():
            return True

        @staticmethod
        def is_active():
            return True

        @staticmethod
        def is_anonymous():
            return False

        def get_id(self):
            return self.id


        @FL_Login.user_loader
        def load_user(id):
            try:
                u = function_pool.isFound("UserFBET", "id", id)
                if not u:
                    return None
                return UserClass(id=dbORM.get_all("UserFBET")[f'{u}']['id'])
            except:#Skipp
                anonymous = {
                    "0": {
                        "id": "0", 
                        "email": "NULL"
                    }
                }
                return UserClass(id=anonymous['0']['id'])


    @app.route("/login", methods=['GET', 'POST']) 
    def login():
        User = dbORM.get_all("UserFBET")

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = function_pool.isFound("UserFBET", "username", username)

            if user and check_password_hash(dbORM.get_all("UserFBET")[f'{user}']['password'], password):
                t_user = UserClass(id=f'{user}')
                login_user(t_user, remember=True)

                return redirect(url_for('views.dashboard'))
                
            else:
                return render_template("login.html", status=("Incorrect password or username.", "Error occurred"))

        return render_template('login.html', status=("", "None"))

    @app.route("/verify-otp", methods=['GET', 'POST'])
    def verifyOTP():
        if request.method == "POST":
            otp = request.form['otp']
            email = request.form['email']
            try:
                User = dbORM.get_all("UserFBET")[f'{function_pool.isFound("UserFBET", "email", email)}']
                OTP = User['temp_data1']
                if otp == OTP:
                    dbORM.update_entry(
                        "UserFBET", 
                        f"{function_pool.isFound('UserFBET', 'email', email)}", 
                        encrypter(str(
                            {
                                "temp_data1": f""
                            }
                        )), 
                        dnd=False
                    )

                    # return function_pool.returnJSONData("success", "otp verification success")
                    return redirect(url_for('views.dashboard'))
                    
                else:
                    return render_template("verifyOTP.html", status=("", "OTP is wrong", "1"), CUser=dbORM.get_all("UserFBET")[f'{function_pool.isFound("UserFBET", "id", current_user.id)}'])
                
                # return render_template("verifyOTP.html", status=("", "None", "1"))

                
                
                
            except KeyError as e:
                return function_pool.returnJSONData("failed", f"error: {e}\nimplication: user with email '{email}' not found.")
        return render_template("verifyOTP.html", status=("", "None", "1"), CUser=dbORM.get_all("UserFBET")[f'{function_pool.isFound("UserFBET", "id", current_user.id)}'])


    @app.route("/signup", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':

            username = request.form.get('username')
            email = request.form.get('email')
            email_address = email

            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            user = function_pool.isFound("UserFBET", 'email', email)

            if user:
                return render_template("signup.html", status=("Email is already taken.", "Sign Up Error", "2", email, username))
            elif len(email) < 4:
                return render_template("signup.html", status=("Email must be at least 4 characters long.", "Sign Up Error", "3", email, username))
            elif len(username) < 6:
                
                return render_template("signup.html", status=("Email must be at least 4 characters long.", "Sign Up Error", "3", email, username))
            
            elif function_pool.isFound("UserFBET", 'username', username) != None:
                return render_template("signup.html", status=("Username Taken.", "Sign Up Error", "3", email, username))

            elif password1 != password2:
                return render_template("signup.html", status=("Passwords do not match. Please re-enter your password.", "Sign Up Error", "1", email, username))
            elif len(password1) < 8:
                return render_template("signup.html", status=("Password is too short. It must be at least 8 characters long.", "Sign Up Error", "1", email, username))
            else:
                numbers = []
                for x in range(10):
                    numbers.append(x)

                otp = f"{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}"
                new_user = {
                    'email': dbORM.sanitize_string(email),
                    'wallet_balance': '0.0',
                    'unique_id': id_generator.generate_id(10),
                    'username': dbORM.sanitize_string(username).replace(' ', ''),
                    'password': generate_password_hash(password1),
                    'temp_data1': otp
                }

                dbORM.add_entry("UserFBET", f"{encrypter(str(new_user))}")

                t_user = UserClass(id=f'{function_pool.isFound("UserFBET", "email", email)}')
                login_user(t_user, remember=True)

                User = dbORM.get_all("UserFBET")[f'{function_pool.isFound("UserFBET", "email", email)}']

                # try:
                msg = Message("Welcome to FBet! Here's your OTP!", sender=decrypter("&012;&009;&022;&005;&st;&006;&002;&005;&020;&020;&009;&014;&007;&at;&007;&013;&001;&009;&012;&st;&003;&015;&013;"), recipients=[User['email']])
                msg.body = f"""
Welcome to the FBet! We're excited to have you join our community.

To verify your email address and complete your registration, please enter the following One-Time Password (OTP) within 60 minutes:

Your OTP is: {otp}

Click the link below or paste the OTP into the registration form to proceed:

https://futo-fbet.vercel.app/client/verify-account/{User['email']}
"""
                mail.send(msg)
                return redirect(url_for('verifyOTP'))
                # except:
                #     return redirect(url_for("views.dashboard"))
                #     return render_template("signup.html", status=("You've registered. You can now login", "Sign Up Error", "1", email, username))



                

        return render_template("signup.html", status=("", "None", "1", "", ""), ref_codee="NULL")
    
    @app.route("/client/verify-account/<string:email>")
    def verifyEmail(email):
        try:
            User = dbORM.get_all("UserFBET")[f'{function_pool.isFound("UserFBET", "email", email)}']
            dbORM.update_entry(
                "UserFBET", 
                f"{function_pool.isFound('UserFBET', 'id', User['id'])}", 
                encrypter(str(
                    {
                        "temp_data1": f""
                    }
                )), 
                dnd=False
            )
            
        except KeyError as e:
            return function_pool.returnJSONData("failed", f"error: {e}\nimplication: user with email '{email}' not found.")

        return render_template("AccountVerified.html", CUser=User)
        

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.", category='Success') 
        return redirect(url_for('views.login'))
    

    return app
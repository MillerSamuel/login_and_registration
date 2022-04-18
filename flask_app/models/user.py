from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


email_regex=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]


    @classmethod
    def add_new(cls,data):
        query="INSERT INTO users (first_name, last_name,email,password,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW())"
        return connectToMySQL("login_and_registration").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_and_registration").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL("login_and_registration").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])



    @staticmethod
    def validate_new(data):
        is_valid=True
        if len(data["first_name"])<2:
            is_valid=False
            flash("*First name must be atleast 2 characters*")
        if len(data["last_name"])<2:
            is_valid=False
            flash("*Last name must be atleast 2 characters*")
        if len(data["email"])<2:
            is_valid=False
            flash("*Email must be atleast 2 characters*")
        elif not email_regex.match(data["email"]):
            is_valid=False
            flash("*Please enter a valid email*")
        if User.get_by_email(data):
            is_valid=False
            flash("*Email already in use*")
        
        if len(data["password"])<7:
            is_valid=False
            flash("*Password must be atleast 8 characters*")
        if data["password"]!=data["confirm"]:
            is_valid=False
            flash("*Password did not match confirmation*")
        return is_valid

    @staticmethod
    def validate_login(data):
        user_in_db = User.get_by_email(data)
        is_valid=True
    # user is not registered in the db
        if not user_in_db:
            flash("Invalid Email/Password")
            is_valid=False
        elif not bcrypt.check_password_hash(user_in_db.password, data['password']):
        # if we get False after checking the password
            flash("Invalid Email/Password")
            is_valid=False
        return is_valid
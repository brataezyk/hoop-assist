from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import court
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'Hoop_Assist'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.profile_picture = db_data['profile_picture']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.courts = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW())"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    # Not Sure if get_one_user classmethod is required if get_one_with_courts classmethod exists?
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        user = cls(results[0])
        return user
    
    @classmethod
    def edit_one_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s , last_name = %(last_name)s , email = %(email)s, password = %(password)s WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod 
    def update_profile_pic(cls, data):
        query = "UPDATE users SET profile_picture = %(new_picture)s WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results
    
    # NOT SURE IF get_info_email CLASS METHOD NEEDED haven't needed to use that I can see!
    @classmethod
    def get_info_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])

    @classmethod 
    def add_fav_court(cls, data):
        query ="INSERT INTO favorites (user_id, court_id) VALUES (%(user_id)s, %(court_id)s);"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result

# THIS SHOULD BE USED ON THE DASHBOARD PAGE TO VIEW THE USERS FAVORITE COURTS
    @classmethod
    def get_one_with_courts(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.user_id LEFT JOIN courts ON courts.id = favorites.court_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        
        user = cls(results[0])

        for row in results:
            if row['courts.id'] == None:
                break
            c = {
                'id': row['courts.id'],
                'state': row['state'],
                'city': row['city'],
                'num_of_hoops': row['num_of_hoops'],
                'num_of_courts': row['num_of_courts'],
                'created_at': row['courts.created_at'],
                'updated_at': row['courts.updated_at']
            }
            user.courts.append(court.Court(c))
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('Hoop_Assist').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name min 3 characters.", "register")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last name min 3 characters.", "register")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.", "register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password min 8 characters.", "register")
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Passwords do not match!", "register")

        return is_valid
    
    @staticmethod
    def validate_edit(user, current_email):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(new_email)s;"
        results = connectToMySQL('Hoop_Assist').query_db(query, user)
        if len(results) >= 1:
            if user['new_email'] != current_email:
                flash("Email already taken.","register")
                is_valid=False
        if len(user['new_first_name']) < 3:
            is_valid = False
            flash("First Name min 3 characters.", "edit_user")
        if len(user['new_last_name']) < 3:
            is_valid = False
            flash("Last Name min 3 characters.", "edit_user")
        if not EMAIL_REGEX.match(user['new_email']):
            is_valid = False
            flash("Invalid Email Address.", "edit_user")
        if  len(user['new_password']) < 8:
            is_valid = False
            flash("Password min 8 characters.", "edit_user")
        if user['new_password'] != user['comfirm_password']:
            is_valid = False
            flash("Passwords do not match!", "edit_user")

        return is_valid
# Look at this Static method, because not doing what we want.
    @staticmethod
    def validate_fav(user, data):
        is_valid = True 
        # print(any(str(court.id) != data['court_id'] for court in user.courts))
        for court in user.courts:
            # print("COURT ===>", type(court.id))
            # print("DATA COURT ===>", type(data['court_id']))
            if str(court.id) == data['court_id']:
                # print("I'm HERE ===>")
                is_valid = False
                flash("You Have Already Favorited This Court!", "plus_favs")
            
        
        return is_valid


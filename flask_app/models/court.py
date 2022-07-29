from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash
from flask_app.models import user
import math

class Court:
    db_name = 'Hoop_Assist'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.state = db_data['state']
        self.city = db_data['city']
        self.num_of_hoops = db_data['num_of_hoops']
        self.num_of_courts = db_data['num_of_courts']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users_name = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO courts (state, city, num_of_hoops, num_of_courts, created_at, updated_at) VALUES(%(state)s,%(city)s,%(num_hoops)s,%(num_courts)s,NOW(),NOW())"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def view_court_id(cls, data):
        query = "SELECT * FROM courts WHERE id = %(court_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM courts;"
        results = connectToMySQL(cls.db_name).query_db(query)
        courts = []
        for court in results:
            courts.append(cls(court))
        return courts

    @classmethod
    def edit_one_court(cls, data):
        query = "UPDATE users SET first_name = %(new_first_name)s , last_name = %(new_last_name)s , email = %(new_email)s, password = %(new_password)s WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def delete_court(cls, data):
        query = "DELETE FROM courts WHERE id = %(court_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @staticmethod
    # Check if None is what is given back in the form, because if not then need to change None functions.
    def validate_court(court):
        is_valid = True
        if court['state'] == None:
            is_valid = False
            flash("Must select a State!", "add_court")
        if len(court['city']) < 3:
            is_valid = False
            flash("City min 3 characters.", "add_court")
        if court['num_hoops'] == None:
            is_valid = False
            flash("Must select number of hoops!", "add_court")
        if court['num_hoops'] == None:
            is_valid = False
            flash("Must select number of hoops!", "add_court")

        return is_valid



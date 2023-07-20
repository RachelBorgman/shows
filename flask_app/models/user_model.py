from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt      
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

db = 'black_belt'

class User: #class - predefined structure of data
    def __init__( self , user_data: dict | None ): #can only pass a dictionary in to create User class
        self.id = user_data['id'] #left is class attribute name, right side is database column names
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.email = user_data['email']
        self.password = user_data['password']
        self.created_at = user_data['created_at']
        self.updated_at = user_data['updated_at']
    
    @staticmethod
    def validate(raw_user_data: dict):
        is_valid = True
        if len(raw_user_data['first_name']) < 2:
            flash("First Name must be at least 3 characters.", 'register')
            is_valid = False
        if len(raw_user_data['last_name']) < 2:
            flash("Last Name must be at least 3 characters.", 'register')
            is_valid = False
        # if len(raw_user_data['email']) < 3:
        #     flash("Email must be at least 3 characters.", 'register')
        #     is_valid = False
        # if len(raw_user_data['password']) < 8:
        #     flash("Password must be at least 8 characters.", 'register')
        #     is_valid = False
        # if len(raw_user_data['password']) < 8:
        #     flash("Password must be at least 8 characters.", 'register')
        #     is_valid = False
        # if not any(char.isdigit() for char in raw_user_data['password']):
        #     flash('Password should have at least one number', 'register')
        #     is_valid = False
        # if not any(char.isupper() for char in raw_user_data['password']):
        #     flash('Password should have at least one uppercase letter', 'register')
        #     is_valid = False
        if raw_user_data['password'] != raw_user_data['c_pw']:
            flash("Passwords do not match.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(raw_user_data['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(password: str, user):
        is_valid = True
        if len(password) < 3:
            flash("Login Password must be at least 3 characters.", 'login')
            is_valid = False
        if not bcrypt.check_password_hash(user.password, password):
            flash("Passwords Don't Match", 'login')
            is_valid = False
        return is_valid
    
    @classmethod
    def new_email(cls, data):
        print(data)
        query = "SELECT email FROM user WHERE email = %(email)s"
        result = connectToMySQL(db).query_db(query, data)
        print(result)
        if len(result) == 0:
            return True
        # print(f"Email is: {cls(result[0])}")
        # flash('Already Registered. Please Log in.')
        return False

    @classmethod
    def save(cls,data: dict): #data is dictionary being passed in from controller when it's called
        query = """INSERT INTO user (first_name, last_name, email, password) VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """ #%() matches key from created dictionary being passed in
        return connectToMySQL(db).query_db(query, data)  #data always needs to be a dictionary
    
    @classmethod
    def get_by_email(cls, email: str):
        print(email)
        data = {
            "email": email
        }
        query = "SELECT * FROM user WHERE email = %(email)s"
        result = connectToMySQL(db).query_db(query, data) #data always needs to be a dictionary
        print(result)
        if result is None or result == False or len(result) == 0:
            # print("invalid login")
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, id: int | str):
        data = { # because query_db requiers a dict, we're creating one to pass in
            "user_id": id #"user_id" is created key that needs to match %() in the query, the blue is passed in with the funtion
        }
        query = "SELECT * FROM user WHERE id = %(user_id)s"
        result = connectToMySQL(db).query_db(query, data) #data always needs to be a dictionary
        print(result)
        if result is None or result == False or len(result) == 0:
            # print("invalid login")
            # flash('Please Register First', 'login')
            return False
        return cls(result[0])


#     @classmethod
#     def get_all(cls):
#         query = "SELECT * FROM users;"
#         results = connectToMySQL('users_schema').query_db(query)
#         users = []
#         for u in results:
#             users.append(cls(u))
#         return users
    
#     @classmethod
#     def get_one(cls, data):
#         query = """
#                 SELECT * FROM users
#                 WHERE id = %(id)s;
#         """
#         result = connectToMySQL('users_schema').query_db(query, data)
#         return cls(result[0])
    
#     @classmethod
#     def update(cls,data):
#         query = """
#             UPDATE users
#             SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at=NOW()
#             WHERE id = %(id)s;
#         """
#         results = connectToMySQL('users_schema').query_db(query, data)
#         return results
    
#     @classmethod
#     def delete(cls, data):
#         query = "DELETE FROM users WHERE id = %(id)s;"
#         results = connectToMySQL('users_schema').query_db(query, data)
#         return results

#     @classmethod
#     def save(cls, data):
#         query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
#         # data is a dictionary that will be passed into the save method from server.py
#         return connectToMySQL('users_schema').query_db(query, data)

#    @classmethod
#    def get_all(cls):
#       query = """
#      SELECT * FROM posts
#     JOIN users ON posts.users_id = users.id;
#    """
#   results = connectToMySQL(cls.db).query_db(query)
#    all_posts = []
#    for row in results:
#       posting_user = User({
#               "id": row["user_id"],
#              "first_name": row["first_name"],
#             "last_name": row["last_name"],
#           "created_at": row["created_at"],
#          "updated_at": row["updated_at"],
#         "password": row["password"]
#    })
#          new_post = Post({
#             "id": row["id"],
#            "content": row["content"],
#           "created_at": row["created_at"],
#          "updated_at": row["updated_at"],
#         "user": posting_user
#    })
#   all_posts.append(new_post)
#       return all_posts

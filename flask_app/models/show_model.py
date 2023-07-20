from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user_model
from flask_app.controllers import show_controller 
import re
import pprint

db = 'black_belt'

class Show: #class - predefined structure of data
    def __init__( self , show_data: dict | None ): #can only pass a dictionary in to create User class
        self.id = show_data['id'] #left is class attribute name, right side is database column names
        self.title = show_data['title']
        self.network = show_data['network']
        self.release_date = show_data['release_date']
        self.description = show_data['description']
        self.posted_by = show_data['posted_by']
        self.created_at = show_data['created_at']
        self.updated_at = show_data['updated_at']
        self.users_who_liked = []

    @staticmethod
    def validate_show(raw_show_data: dict):
        is_valid = True
        if len(raw_show_data['title']) < 3:
            flash("Title must be at least 3 characters.", 'show')
            is_valid = False
        if len(raw_show_data['network']) < 3:
            flash("Network must be at least 3 characters.", 'show')
            is_valid = False
        if len(raw_show_data['description']) < 3:
            flash("Description must be at least 3 characters.", 'show')
            is_valid = False
        if raw_show_data['release_date'] is None:
            flash("Release Date is a required field", 'show')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_show_update(raw_show_data: dict):
        is_valid = True
        if len(raw_show_data['title']) < 3:
            flash("Title must be at least 3 characters.", 'show')
            is_valid = False
        if len(raw_show_data['network']) < 3:
            flash("Network must be at least 3 characters.", 'show')
            is_valid = False
        if len(raw_show_data['description']) < 3:
            flash("Description must be at least 3 characters.", 'show')
            is_valid = False
        if raw_show_data['release_date'] is None:
            flash("Release Date is a required field", 'show')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_id(cls, show_data):
        query = """
        SELECT * FROM black_belt.show
        WHERE id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, show_data)
        if results:
            show = results[0]
            return show
        return False
    
    @classmethod
    def save(cls,data: dict): #data is dictionary being passed in from controller when it's called
        query = """INSERT INTO black_belt.show (title, network, release_date, description, posted_by) 
        VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(posted_by)s);
        """ #%() matches key from created dictionary being passed in
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, show_data):
        query = """
        SELECT * FROM black_belt.show JOIN black_belt.user ON black_belt.show.posted_by = black_belt.user.id
        WHERE black_belt.show.id = %(show_id)s;
        """
        results = connectToMySQL(db).query_db(query, show_data)
        if not results:
            return False
        for row in results:
            posted_by = user_model.User({
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "created_at": row["user.created_at"],
                "updated_at": row["user.updated_at"],
                "password": ""
            })
            show = Show({
                "id": row["id"],
                "title": row['title'],
                'network': row['network'],
                'release_date': row['release_date'],
                'description': row['description'],
                'liked_by': row["liked_by"],
                'posted_by': posted_by,
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
            results = results[0]
        print('these are the get_one results:', results)
        return show

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM black_belt.show 
        LEFT JOIN black_belt.like ON black_belt.show.id = black_belt.like.show_id 
        LEFT JOIN user ON user.id = black_belt.like.liked_by;
        """
        results = connectToMySQL(db).query_db(query)
        print("This is the get_all query results=", results)
        all_shows = []
        # print(results[0]['description'])
        for row in results:
            posted_by = user_model.User({
                "id": row["posted_by"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "password": ""
            })
            # liked_by = None
            # if row['liked_by'] is not None:
            #     # driver = user_model.User.get_by_id(row['driver'])
            #     liked_by = user_model.User({
            #         "id": row["liked_by.id"],
            #         "first_name": row["liked_by.first_name"],
            #         "last_name": row["liked_by.last_name"],
            #         "email": row["liked_by.email"],
            #         "created_at": row["liked_by.created_at"],
            #         "updated_at": row["liked_by.updated_at"],
            #         "password": ""
            #     })
                
            show = Show({
                    "id": row["id"],
                    "title": row['title'],
                    'network': row['network'],
                    'release_date': row['release_date'],
                    'description': row['description'],
                    'posted_by': posted_by,
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                })
            all_shows.append(show)
        print("THESE ARE ALL_SHOWS:", all_shows)
        return all_shows
    
    @classmethod
    def get_show_with_likes(cls, show_data):
        query = """
                SELECT * FROM black_belt.show LEFT JOIN black_belt.like ON black_belt.show.id = black_belt.like.show_id LEFT JOIN user ON user.id = black_belt.like.liked_by
		WHERE black_belt.show.id = %(show_id)s;
        """
        results = connectToMySQL(db).query_db(query, show_data)
        print("THESE ARE GET SHOW WITH LIKES RESULTS:", results)
        show = cls(results[0])
        for row in results:
            if row['user.id'] == None:
                break
            data = {
                    "id": row["id"],
                    "title": row['title'],
                    'network': row['network'],
                    'release_date': row['release_date'],
                    'description': row['description'],
                    'posted_by': row['posted_by'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    "liked_by": row["liked_by"],
                    "first_name": row["first_name"],
            }
            show.users_who_liked.append(user_model.User(data))
            print("!!!!!!!!!!!!!!!", show)
        return show

    @classmethod
    def get_like_count(cls, show_data):
        query = """
        SELECT count(*) FROM black_belt.like LEFT JOIN black_belt.show ON black_belt.show.id = black_belt.like.show_id LEFT JOIN user ON user.id = black_belt.like.liked_by
        WHERE black_belt.show.id = %(show_id)s;
        """
        results = connectToMySQL(db).query_db(query, show_data)
        count = results[0]['count(*)']
        print("###########", count)
        return count


    @classmethod
    def update(cls,valid_show_data):
        query = """
            UPDATE black_belt.show
            SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s
            WHERE id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, valid_show_data)
        return results

    @classmethod
    def delete(cls, show_id: int):
        query = "DELETE FROM black_belt.show WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {"id":show_id})
        return results
    
    @classmethod
    def assign_like(cls, show_data: int):
        query = """
            INSERT INTO black_belt.like (liked_by, show_id)
            VALUES (%(show_id)s, %(liked_by)s);
        """
        results = connectToMySQL(db).query_db(query, show_data)
        return results
    
    @classmethod
    def cancel_like(cls, show_data: int):
        query = """
            DELETE from black_belt.like
            WHERE show_id = %(show_id)s AND liked_by = %(liked_by)s;
            """
        results = connectToMySQL(db).query_db(query, show_data)
        return results
    
    # @classmethod
    # def get_driver_by_id(cls, ride_data):
    #     query = """
    #     SELECT user.first_name FROM user
    #     JOIN ride ON user.id = ride.driver
    #     WHERE ride.id = %(id)s;
    #     """
    #     results = connectToMySQL(db).query_db(query, ride_data)
    #     if results:
    #         driver = results[0]
    #         print("This is the driver:", driver)
    #         return driver
    #     return False
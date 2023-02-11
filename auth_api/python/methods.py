import database
import jwt
import mysql.connector
import os
import re


# Class for generating token
class Token:
    def __init__(self):

        # Database connection
        self.conn = database.Database()
        self.conn.connect()

        # Secret key for encoding/decoding JWT
        self.secret = os.environ["SECRET_KEY"]

    # Apply validations
    def validate_username(self, username):
        # Validate the username
        if re.match("^[a-zA-Z0-9_]+$", username) is None:
            return False
        return True

    def validate_password(self, password):
        # Validate the password
        if len(password) < 8:
            return False
        return True

    def generate_token(self, username, password):
        try:
            if not self.validate_username(username) or not self.validate_password(password):
                return None

            # Connecting to the database
            cursor = self.conn.get_cursor()
            # Fetching user data from the database based on the username and password
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            cursor.close()
        except mysql.connector.Error as error:
            print("Failed to fetch data from database: {}".format(error))
            return "An error occurred while connecting to the database"

        if result is not None:
            # Getting the role from the user data
            role = result[3]
            # Defining the payload for the token
            payload = {"role": role}
            # Encoding the JWT with the payload and secret key
            token = jwt.encode(payload, self.secret, algorithm="HS256")
            return token
        else:
            return None


# Class for accessing protected data
class Restricted:
    def __init__(self):
        # Secret key for encoding/decoding JWT
        self.secret = os.environ["SECRET_KEY"]

    def access_data(self, token):
        try:
            # Decoding the JWT using the secret key
            decoded = jwt.decode(token, self.secret, algorithms=["HS256"])
            # Checking if the role exists in the decoded JWT and is "admin"
            if "role" in decoded and decoded["role"] == "admin":
                # Data to be returned if the role is "admin"
                data = "You are under protected data"
                return data
            else:
                # Error message to be returned if the role is not "admin"
                return None
        except jwt.exceptions.DecodeError:
            # Error message to be returned if the JWT is invalid
            return {"error": "Bad Request: The token provided is invalid"}  


# Class to validate the login
class Login:
    def __init__(self):
        self.user_pass = {
            "admin": os.getenv("ADMIN_PASSWORD"),
            "noadmin": os.getenv("NOADMIN_PASSWORD"),
            "bob": os.getenv("BOB_PASSWORD")
        }

    def is_valid(self, username, password):
        if username in self.user_pass and self.user_pass[username] == password:
            return True
        return False


# Retrieve the environment variable
admin_token = os.environ.get('ADMIN_TOKEN')


class Access:
    def __init__(self):
        self.auth_tokens = [admin_token]

    def is_valid(self, auth_token):
        if not auth_token:
            return False
        return auth_token in self.auth_tokens

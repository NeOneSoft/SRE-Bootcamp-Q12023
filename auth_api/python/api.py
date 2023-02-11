from flask import Flask
from flask import jsonify
from flask import request
from methods import Token, Restricted, Login, Access

app = Flask(__name__)
login = Token()
protected = Restricted()


# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# Login API endpoint, accepts a POST request with `username` and `password` as form data
# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({"error": "username and password is required"}), 400

    username = request.form['username']
    password = request.form['password']

    # Create an instance of the Login and Token class
    login = Login()
    gen_token = Token()

    # Add check for valid username and password
    if not login.is_valid(username, password):
        # Return 401 Unauthorized if not valid
        return jsonify({"error": "Unauthorized"}), 401

    res = {
        "data": gen_token.generate_token(username, password)
    }
    return jsonify(res)


# Protected API endpoint, accepts a GET request with an `Authorization` header
# e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    # Get the `Authorization` header
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return jsonify({
            "error": "Authorization header is required"
        }), 400

    # Create an instance of the Access class
    access = Access()
    try:
        # Validate the provided token
        is_valid = access.is_valid(auth_token)
        if not is_valid:
            # Return 400 Bad Request if the token is not valid
            return jsonify({"error": "Invalid token"}), 400
        res = {
            "data": protected.access_data(auth_token)
        }
        return jsonify(res)
    except Exception as e:
        # Return the error message if any exception occurs
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

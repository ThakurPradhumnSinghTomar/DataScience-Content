from flask import Flask, request, jsonify , render_template,redirect, url_for, flash,session
from flask_session import Session  # Import session extension
import mysql.connector

app = Flask(__name__)



# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",   # Your MySQL username
    password="9993350128",  # Your MySQL password
    database="flask_db"
)

cursor = db.cursor()


@app.route('/welcome')
def welcome():
    email = request.args.get("email")  # Get email from URL
    username = request.args.get("username")  # Get username from URL

    if not email:
        return redirect(url_for("signin_page"))  # Redirect if no email

    return render_template('welcome.html', user_email=email, username=username)


@app.route('/',methods=["GET", "POST"])
def home_page() :
    return render_template("index.html")


@app.route('/signup_page',methods=["GET", "POST"])
def signup_page() :
    return render_template("signup.html")


@app.route('/signin_page',methods=["GET", "POST"])
def signin_page() :
    return render_template("signin.html")




@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    try:
        data = request.json  # Fetch JSON data from frontend
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        insert_query = "INSERT INTO users(username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, email, password))
        db.commit()


        return jsonify({"success": True, "message": "User added successfully! Now you can Sign In."})

    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({"success": False, "message": "User with this email or username already exists. Try a different email or username."})
        else:
            return jsonify({"success": False, "message": "An error occurred. Please try again later."})



@app.route('/sign_in', methods=['POST'])
def sign_in():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        query = "SELECT username FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            return jsonify({"success": True, "message": "Login Successful!", "username": user[0], "email": email})
        else:
            return jsonify({"success": False, "message": "Invalid email or password."})

    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred. Please try again."})



@app.route('/add_contact', methods=["POST"])
def add_contact():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        mobile_no = data.get('mobile_no')

        # Check if email exists in users table
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if not existing_user:
            return jsonify({"success": False, "message": "User does not exist. Please register first."})

        # Insert contact data
        insert_query = "INSERT INTO user_data (email, name, mobile_no) VALUES (%s, %s, %s)"

        cursor.execute(insert_query, (email, name, mobile_no))
        db.commit()

        return jsonify({"success": True, "message": "Contact added successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"})


@app.route('/delete_contact', methods=["POST"])
def delete_contact():
    try:
        data = request.json
        email = data.get('email')  # User's email to ensure they delete their own contacts
        name = data.get('name')

        if not email or not name:
            return jsonify({"success": False, "message": "Both email and name are required!"})

        cursor = db.cursor()  # Create a new cursor to avoid unread results

        # Check if the contact exists for the user
        cursor.execute("SELECT * FROM user_data WHERE email = %s AND name = %s", (email, name))
        contact = cursor.fetchone()

        if not contact:
            cursor.close()  # Close cursor before returning
            return jsonify({"success": False, "message": "Contact not found!"})

        cursor.fetchall()  # Ensure no unread results remain

        # Delete the contact
        delete_query = "DELETE FROM user_data WHERE email = %s AND name = %s"
        cursor.execute(delete_query, (email, name))
        db.commit()

        cursor.close()  # Close cursor after execution
        return jsonify({"success": True, "message": f"Contact '{name}' deleted successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"})


@app.route('/get_all_contacts', methods=["POST"])
def get_all_contacts():
    try:
        data = request.json
        email = data.get('email')

        cursor.execute("SELECT name, mobile_no FROM user_data WHERE email = %s", (email,))
        contacts = cursor.fetchall()

        if contacts:
            contacts_list = [{"name": row[0], "mobile_no": row[1]} for row in contacts]
            return jsonify({"success": True, "contacts": contacts_list})
        else:
            return jsonify({"success": False, "message": "No contacts found."})

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"})

@app.route('/logout')
def logout():
    return redirect(url_for('signin_page'))





if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, request, jsonify, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

from src.constant.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)
from .forms import UserForm
from .models import Users, db
from .config.config import Config

mail = Mail()

# Create a blueprint for the register module
views = Blueprint("views", __name__, url_prefix="/api/v1/users")

secret_key_variable = Config()
secret_key = secret_key_variable.SECRET_KEY
serialiser = URLSafeTimedSerializer(secret_key)

# Route to signup a user
@views.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        
        # Process the form data and register the user
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)  # Store the hash copy of the password
        user_type = form.select_user_type.data
        
        # Create a new user instance
        new_user = Users(username=username, email=email, password=password, user_type=user_type)
        
        # Commit the data to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Create a unique token for email verification
        token = serialiser.dumps(form.email.data, salt='R0FjIsi65Y#ZQy*t$@n%t4$P6X5v(B(s')

        # Send email with verification link
        subject = 'Email Verification'
        body = f'Click the link below to verify your email:\n{url_for("verify_email", token=token, _external=True)}'
        msg = Message(subject=subject, recipients=[form.email.data], body=body)
        mail.send(msg)
        
        # Send verification email
        flash('A verification link has been sent to your email. Please check your inbox.', 'success')
        return redirect(url_for('login'))
        
    
    return jsonify({'message':'successful'}), HTTP_201_CREATED


# login as a user
@views.route("/login")
def login():
    email = request.json["email"]
    username = request.json["username"]
    password = request.json["password"]

    if email or username:
        return jsonify({"message": "please enter your username or email"})

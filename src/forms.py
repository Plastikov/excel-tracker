from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    Regexp,
)


# create a signup class for user, requiring username, email and password
class UserForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or " "underscores",
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$", message="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."),
            Regexp(r"^-?\d+$", message="Requires an integer."),
            Regexp(r"^.*$", message="Requires at least one character."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", "Passwords must match")],
    )
    select_user_type = RadioField(
        "I am a:",
        choices=[(1, "Teacher"), (2, "Guardian"), (3, "Student")],
        coerce=int,
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        
        pass

    def validate_username(self, field):
        
        pass

    def validate_password(self, field):
        
        pass

# send an email link to redirect to a complete registration page
# create a complete profile
# create a a child profile
# a child profile can be created by a parent and a teacher
# a child profile created by a parent must not be editable by a teacher and vice versa
# only a teacher should be able to create a subject based assessment for a child

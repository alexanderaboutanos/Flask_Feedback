from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """ Redirect to /register."""
    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register():
    """ 

    IF GET REQUEST --> Shows a form that when submitted will register/create a user. This form accepts a username, password, email, first_name, and last_name. Uses WTForms and password input hides the characters that the user is typing.

    IF POST REQUEST --> Process the registration form by adding a new user. Then redirect to /secret

    """
    form = UserForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password,
                                 email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username

        return redirect('/secret')
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
    GET --> Shows a form that when submitted will login a user. This form acepts a username and a password.

    POST --> Process the login form, ensuring the user is authenticated and going to /secret if so.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.first_name}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_secret(username):
    """Return the user info"""
    if 'username' not in session:
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)


@app.route('/logout')
def logout():
    """Clear any information from the session and redirect """
    session.clear()
    # session.pop('username')
    return redirect('/')

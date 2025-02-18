from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_mail import Message
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app.models.database import db
from app.forms.auth_forms import EmailForm, CompleteRegistrationForm, LoginForm
from app import mail, serializer

auth_bp = Blueprint('auth', __name__)

def send_email(subject, recipient, template, **kwargs):
    msg = Message(subject, recipients=[recipient])
    msg.html = render_template(f'emails/{template}.html', **kwargs)
    msg.body = render_template(f'emails/{template}.txt', **kwargs)
    mail.send(msg)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.login'))
        
        token = serializer.dumps(form.email.data, salt='email-confirm')
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        
        send_email('Confirm Your Email', form.email.data, 'confirm_email', confirm_url=confirm_url)

        flash('A confirmation email has been sent. Please check your inbox.', 'info')
        return redirect(url_for('home.home'))

    return render_template('register.html', form=form)


@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=600)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.register'))

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already confirmed. Please log in.', 'info')
        return redirect(url_for('auth.login'))

    new_user = User(email=email, is_verified=True)
    db.session.add(new_user)
    db.session.commit()
    flash('Email confirmed! Complete your registration.', 'success')
    return redirect(url_for('auth.complete_registration', email=email))

@auth_bp.route('/complete_registration', methods=['GET', 'POST'])
def complete_registration():
    email = request.args.get('email')
    form = CompleteRegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.name = form.name.data
            user.city = form.city.data
            db.session.commit()
            login_user(user)
            flash('Registration completed successfully!', 'success')
            return redirect(url_for('home.dashboard'))
        flash('Error completing registration.', 'danger')
    return render_template('complete_registration.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home.home'))
        flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

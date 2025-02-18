from flask import Blueprint, render_template
from flask import Flask, request, session, redirect, url_for
from flask_login import login_required, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html')

@home_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@home_bp.route('/set_language', methods=['POST'])
def set_language():
    """ Guarda el idioma seleccionado en la sesión y redirige a la página de inicio. """
    session['lang'] = request.form['language']
    return redirect(url_for('home.home'))  # Redirige a la home después de cambiar el idioma
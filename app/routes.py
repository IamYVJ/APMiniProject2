from app import app , db, bcrypt
from flask import render_template, flash, redirect , url_for , request, session , g
import sqlite3
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

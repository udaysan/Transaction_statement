from flask import Blueprint,render_template, request, flash, redirect, url_for
import re
from .models import db, Customer
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime



auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password = request.form.get('password')

        customer=Customer.query.filter_by(email=email).first()
        if customer:
            if check_password_hash(customer.password,password):
                flash('Logged in successfully',category='success')
                login_user(customer, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again',category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",customer=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        govName = request.form.get('govName')
        phoneNumber = request.form.get('phoneNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address')
        social_security_number = request.form.get('social_security_number')

        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

        pattern = re.compile(r'^\(?(\d{3})\)?[-.]?(\d{3})[-.]?(\d{4})$')
        match = pattern.match(phoneNumber)

        customer=Customer.query.filter_by(email=email).first()

        if customer:
            flash('Email already exists.', category='error')
        elif len(email)<4:
            flash('Email must be greater than 3 characters.',category='error')
        elif len(firstName)<2:
            flash('First name must be greater than 1 characters.',category='error')
        elif password1!=password2:
            flash('Passwords don\'t  match',category='error')
        elif len(password1)<7:
            flash('Passwords must be at least 7 characters',category='error')
        elif match is None:
            flash('Please check entered phone number',category='error')
        elif firstName not in govName or lastName not in govName:
            flash('First name or last name is not present in official name',category='error')
        elif len(social_security_number)!=12 or (social_security_number.isdigit())==False:
            flash('Please check your Aadhar number')           
        else:
            new_user = Customer(email=email, firstname=firstName,lastname=lastName,govname=govName,phonenumber=phoneNumber, password=generate_password_hash(password1, method='scrypt'),date_of_birth=date_of_birth,address=address,social_security_number=social_security_number)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            #add user to database

    return render_template("sign_up.html",customer=current_user)




 

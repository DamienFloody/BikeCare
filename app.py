import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, make_response, send_from_directory
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required, allowed_file
from base import Session, Base, engine
from models import User, Bike
from datetime import datetime, date

app = Flask(__name__)

app.secret_key = 'somesecretkeyhere'

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['UPLOAD_PATH'] = 'uploads'

bikeTypes = {"BMX", "City", "Mountain", "Road", "Racer", "Electric", "Cyclocross", "Touring", "Fitness", "Cruiser"}

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route("/")
def index():
    
    return render_template('index.html',session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    
    # clear user session
    session.clear()

    if request.method == "POST":

        userName = request.form.get("username")
        passWord = request.form.get("password")

        # Ensure username was submitted
        if not userName:
        
            flash('UserName not submitted')
            return render_template("login.html")

        # Ensure password was submitted
        elif not passWord:

            flash('Password not submitted')
            return render_template("login.html")

        DbSession = Session()

        users = DbSession.query(User) \
        .filter(User.userName == userName ) \
        .first()

        # PWCheck = check_password_hash(users.hash, passWord)

        # Ensure username exists and password is correct
        if users:

            if check_password_hash(users.hash, passWord):

                session["user_id"] = users.id
                session["user_firstname"] = users.firstName
                session["user_lastname"] = users.lastName
     
                return redirect("/")

            else:

                flash('invalid username or password')
                return render_template("login.html")
            
        else:

            flash('invalid username or password')
            return render_template("login.html")


    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/bikes", methods=["GET"])
@login_required
def bikes():
  
    DbSession = Session()

    print(session["user_id"])

    bikes = DbSession.query(Bike) \
    .filter(Bike.userID == session["user_id"]) \
    .all()

    return render_template('bikes.html',session=session, bikeData = bikes)

@app.route("/register", methods=["GET", "POST"])
def register():
    
    DbSession = Session()

    if request.method == "POST":

        userName = request.form.get("username")
        firstName = request.form.get("firstname")
        lastName = request.form.get("lastname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        # Ensure username was submitted
        if not userName:

            flash("must provide username")
            return render_template("register.html")
        
        # Ensure password was submitted
        elif not password:
           flash("must provide password")
           return render_template("register.html")
        

        # Ensure passwords match
        elif password != confirmPassword:
            flash("passwords must match")
            return render_template("register.html")
        

        users = DbSession.query(User) \
        .filter(User.userName == userName ) \
        .all()

        # Ensure username does not already exist
        if len(users) != 1:

            #Hash the password
            hash = generate_password_hash(request.form.get("password"))

            new_user = User(userName, firstName,lastName, email, phone, hash)

            DbSession.add(new_user)

            DbSession.commit()

            DbSession.close()

        else:

            flash ('Username alread exists')
            return render_template("register.html")


        return redirect("/")

    else:

        return render_template("register.html")

@app.route("/registerBike", methods=["GET", "POST"])
def registerBike():
    
    DbSession = Session()

    if request.method == "POST":

        userID = session["user_id"]
        name = request.form.get("name")
        description = request.form.get("description")
        brand = request.form.get("brand")
        model = request.form.get("model")
        type = request.form.get("type")
        colour = request.form.get("colour")
        size = request.form.get("size")
        serialNumber = request.form.get("serialNumber")
        year = request.form.get("year")
        date = request.form.get("date")
        price = request.form.get("price")

        date_object = datetime.strptime(date, '%d-%m-%Y')

        images = request.files.getlist('image')

        imageUpload = ""

        for i in images:

            if i and allowed_file(i.filename):
                filename = secure_filename(i.filename)
                imageUpload = filename
                i.save(os.path.join(app.config['UPLOAD_PATH'], filename))


        new_bike = Bike(userID, name, description, brand, model, type, colour, size, serialNumber, year, date_object, price, imageUpload)

        DbSession.add(new_bike)

        DbSession.commit()

        DbSession.close()

        flash("Registered sucessfully")

        return redirect("/bikes")

    else:

        return render_template("registerBike.html", bikeTypes = bikeTypes)

@app.route("/editBike/<bikeId>", methods=["GET", "POST"])
@login_required
def editBike(bikeId):
    
    DbSession = Session()

    if request.method == "POST":

        userID = session["user_id"]
        name = request.form.get("name")
        description = request.form.get("description")
        brand = request.form.get("brand")
        model = request.form.get("model")
        type = request.form.get("type")
        colour = request.form.get("colour")
        size = request.form.get("size")
        serialNumber = request.form.get("serialNumber")
        year = request.form.get("year")
        ddate = request.form.get("date")
        price = request.form.get("price")
        image = request.form.get("image")

        date_object = datetime.strptime(ddate, '%d-%m-%Y')

        update_bike = DbSession.query(Bike).filter_by(id=bikeId).one()

        update_bike.name = name
        update_bike.description = description
        update_bike.brand = brand
        update_bike.type = type
        update_bike.colour = colour
        update_bike.serialNumber = serialNumber
        update_bike.year = year
        update_bike.date = date_object
        update_bike.price = price
        update_bike.image = image

        DbSession.commit()

        DbSession.close()

        # return render_template("bikes.html")

        return redirect(url_for('bikes'))

    else:

        bikeData = DbSession.query(Bike) \
        .filter(Bike.id == int(bikeId)) \
        .one()

        dateObj = bikeData.date

        cr_date = dateObj.strftime("%d-%m-%Y")

        print(cr_date)
        return render_template("editBike.html", bikeData = bikeData, date = cr_date,  bikeTypes = bikeTypes)

@app.route("/viewBike/<bikeId>", methods=["GET"])
@login_required
def viewBike(bikeId):
    
    DbSession = Session()

    bikeData = DbSession.query(Bike) \
    .filter(Bike.id == int(bikeId)) \
    .one()

    dateObj = bikeData.date

    cr_date = dateObj.strftime("%d-%m-%Y")

    print(cr_date)
    return render_template("viewBike.html", bikeData = bikeData, date = cr_date)

@app.route("/deleteBike/<bikeId>", methods=["GET", "POST"])
@login_required
def deleteBike(bikeId):

    DbSession = Session()

    if request.method == "POST":

        bikesData = DbSession.query(Bike) \
        .filter(Bike.id == int(bikeId)) \
        .all()

        if bikesData:
            
            for i in bikesData:

                if i.image:

                    filename = i.image
                    
                    path = os.path.join(app.config['UPLOAD_PATH'], filename) 

                    os.remove(path) 

        delete_bike = DbSession.query(Bike).filter_by(id=bikeId).delete()

        DbSession.commit()

        DbSession.close()

        flash("Sucessfully deleted")

        return redirect(url_for('bikes'))

    else:
        
        bikeData = DbSession.query(Bike) \
        .filter(Bike.id == int(bikeId)) \
        .all()

        return render_template("deleteBike.html", id = bikeId, bikeData = bikeData)

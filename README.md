## Title

CS50 2020 Final Project - Web Track

## Introduction

For my final submission for the CS50 2020 Final Project Web Track, I developed a small web application which allows users to keep a catalogue of their bicyles (bikes).

The application is called "MyBike", where users can register and then login to the MyBike site.

Once sucessfully logged into the site, users can register their bikes with some of the common bike specifications e.g. Brand, Make, Model, Image etc.

The application allows users to perform CRUD (Create, Read, Update, Delete) actions on their bike information.

I choose to use Flask as the web development framework for this application as it allows for simple and scalable applications.

All the applcation data is stored in a SQLite database, and I used SQLAlchemy for working with the database, as it gives the flexabilty of using ORM (Object Relational Mapper) and easier database queries.

The website has a simple yet responsive design which is managed by Bootstrap and works on mobile and desktop browsers.


## Technologies
This web application has been developed using the following technologies:

* Python version: 3.8.5
* Flask version: 1.1.2
* SQLAlachemy version: 1.3.22
* SQLite version: 3.34.0
* Bootstrap version: 4.0.0
* Bootstrap date picker: (https://github.com/uxsolutions/bootstrap-datepicker)
* jQuery version: 3.3.1


## Features
MyBike web application has the following core features:

* Register user
* Login user
* Logout user
* Create bike information
* Read bike information
* Edit bike information
* Delete bike information
	
## Setup
To run this project, install it locally using npm:

```
$ cd ../lorem
$ npm install
$ npm start
```

URL : http://calm-plains-2686.herokuapp.com/

# Book Reservation App

A Python app used for temporary book lending by various users.
It has the folowing functionalities:
- Multiple user Registration
- Book Addition by present user
- Book information editing by owner in Book view page
- Adding reservations for books lent by other users
- Book Tagging functionality on the view book page 
- Cross referencing books with its respective tags
- An RSS link to dump all the reservations for a particular book into XML format
- time validation. Takes care of the functionality when the book is unavailable, or if there is an existing reservation
- Reservation Deletion Functionality

## Running Locally
After installing Heroku and starting your python virtual environment

```sh
$ git clone https://github.com/mkunaparaju/student-commerce.git
$ cd student-commerce
$ pip install -r requirements.txt
$ createdb ost
$ heroku local:run python manage.py migrate
$ python manage.py collectstatic
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku open
```

## Developer's Guide

- This application has been developed using python with Django framework. It is being hosted by Heroku server with the database being postgresql.
- It has been built with a basic MVC framework which is located inside the 'Hello' folder. Model.py is the model, veiws.py is the controller and templates are the views.
- The templates are written in html and CSS for the UI.
- Model.py contains the database structure which can be synced remotely to Postgresql server
- views.py contains the business logic
- Django has a ModelForm utility which can be used to render the html input for forms. This functionality has been provided in forms.py
- settings.py located in getting started contains provides us with the base dir root, database settings home page dir etc..
- urls.py takes care of routing the html to its respective view



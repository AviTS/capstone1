# capstone1

FinTrackr
https://fintrackrcapstone.herokuapp.com/


First, the user will have to signup. From there, the user can create a watchlist with whatever name they want. Then, the user can add whatever stock they want to that watchlist. Once a user creates a watchlist, they will be able to add stocks to it by entering the stock symbol. Once added to a watchlist, they can click on the stock to display information pertaining to that stock. A user can also remove a stock from a watchlist. 

I used Flask as the application's web framework. Flask uses Jinja as its templating engine. Additionally, I used Flask-Bcrypt, which allowed for the user's password to be hashed and stored securely in the database. I used WTForms for all forms (signup, login, watchlist creation, and stock creation). By using WTForms, it allowed for a significantly easier implementation of form validation.

For the database, I used SQLAlchemy. SQLAlchemy is an ORM based on SQL. Since I was already familiar with SQL, it was easy to use SQLAlchemy for my application's querying of the database.

For the styling of my web application, I used Bootstrap.

Lastly, for deploying my web application, I used GitHub paired with Heroku. 

API I used for gathering all stock-related information:
https://rapidapi.com/alphavantage/api/alpha-vantage

In this project, I utilized the following technologies and languages:
1. Python - Flask, WTForms, Bcrypt
2. Database - SQLAlchemy
3. HTML - Jinja
4. CSS - Bootstrap
5. Deployment - GitHub and Heroku
6. Other - dotenv

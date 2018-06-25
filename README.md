# REST APIs


This repository contains FLASK REST APIs project which perform CRUD operations. The DataBase used in this project is MYSQL, which is running on AWS. You can run this project on your local machine by setting EndPoint, user_name and password for your database. 


### Run on your local machine
```sh
$ git clone https://github.com/jasmeet17/bcdevtest.git
$ cd bcdevtest
$ FLASK_APP=run.py flask run
```

I have deployed my Database on AWS and Flask app on Heroku. I choose Heroku for deploying my application becuase of its simplicity and its free. I have set configuration variables in my heroku applicartion to connect it with MySql on AWS. If you are running locally make sure you provide the enviornment variables mentioned in the config.py

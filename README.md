# Project hotel

our projet follow this shema 
![Alt text](/images/model_db.png "follow this model")



## installation local API back 

create a database mysql.

clone this project

in root of project

create venv with this command :
```
python3 -m venv .venv
```

enter in venv with 
```
Set-ExecutionPolicy Unrestricted -Scope Proces
.\.venv\Scripts\activate
```

then create .env in folder back-hotel and edit with your credentials of mysql and create your super key 
```
FLASK_APP = "bookhotel.py"
FLASK_ENV = "development"
FLASK_RUN_PORT = "5000"
APP_SUPER_KEY="YourSuperKey"
DEV_DATABASE_URL="mysql+pymysql://root:root@localhost:3306/bookhotel"
TEST_DATABASE_URL="mysql+pymysql://root:root@localhost:3306/bookhotel"
```

in folder back-hotel install the dependance with
```
pip install -r .\requirements.txt
```

Create tables of database with 
```
flask db upgrade
```

Launch project with 
```
flask run
```

Api is available on http://localhost:5000/ 

Api docs is available on http://localhost:5000/api/docs


## installation local API front (requirement back)

Split the terminal and paste this following command :

```
Set-ExecutionPolicy Unrestricted -Scope Proces
.\.venv\Scripts\activate
```

Next go to the front-hotel folder 

create a .env in the folder and paste this variables : 

```
FLASK_APP = "app.py"
FLASK_ENV = "development"
FLASK_RUN_PORT = "5001"
```

Next install dependency with : 

```
pip install -r requirements.txt
```

And for finish juste do a :

```
flask run
```

Front is available on http://localhost:5001/


## Lauch test on API hotel in local 

Enter in venv then go to folder back-hotel
then create .env in folder back-hotel and edit with your credentials of mysql and create your super key 

```
FLASK_APP = "bookhotel.py"
FLASK_ENV = "development"
FLASK_RUN_PORT = "5000"
APP_SUPER_KEY="YourSuperKey"
DEV_DATABASE_URL="mysql+pymysql://root:root@localhost:3306/bookhotel"
```

for lauch the test 
```
python -m unittest test.<Name of wish test>
```

it exists this list of unit test
    * test_unitaire_booking
    * test_unitaire_hotel
    * test_unitaire_chambres
    * test_unitaire_user
    * test_unitaire_image
each model test GET, POST, PUT and DELETE

For test of integration 
    * test_integration
there are tests of scenario using different object user, hotel, chambres, image and booking
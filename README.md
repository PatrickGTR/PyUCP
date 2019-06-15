## Information
This website is build using **Bootstrap** framework, **Python** and **MySQL**.

## Installation
#### Importrant!
Make sure you create environment variables for secret_key and MySQL credentials for the **login** and **content management system** to work properly.

#### How to install environment variables
#### Windows
[Take me there!](https://www.computerhope.com/issues/ch000549.htm)

#### Linux
Creating Environment Variable
```bash
VARIABLE_NAME = variable_value
```
Check if Environment Variable has been created
```bash
echo $VARIABLE_NAME
```
Deleting environment variable
```bash
unset VARIABLE_NAME
```

#### Required Environment Variables
```py
SECRET_KEY      = os.environ.get('SECRET_KEY')
MYSQL_USERNAME  = os.environ.get('MYSQL_USERNAME')
MYSQL_PASSWORD  = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE  = os.environ.get('MYSQL_DATABASE')
MYSQL_HOST      = os.environ.get('MYSQL_HOST')
```

##### Python Version
3.7.3

##### Install dependencies in one line!
```bash
pip install -r requirements.txt
```

## Live Demo

**Login: demo
Password: demo**


#### [Take me there now!](https://ucpdemo.herokuapp.com)

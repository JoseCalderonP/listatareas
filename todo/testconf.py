import mysql.connector
from decouple import config
from flask import current_app, g

host = config('DATABASE_HOST')
user = config('DATABASE_USER')
password = config('DATABASE_PASSWORD')
database = config('DATABASE')

print(host)
print(user)
print(password)
print(database)
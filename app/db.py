import psycopg2
from flask import flash
import user as u
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import logging

def getData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606', dbname='TO', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except (Exception, psycopg2.DatabaseError) as ex:
        logging.ERROR(ex)
        print(ex)
    finally:
        connection.close()


def setData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606', dbname='TO', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as ex:
        logging.ERROR(ex)
        print(ex)
    finally:
        connection.close()
        

def getUserById(id):
    try:
        user = getData(f"SELECT u.id, u.email, u.password, u.lastname, u.firstname, u.phone, r.role from users u join roles r on u.role = r.id and u.id = {id}")
        if user != []:
            person = u.User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5], user[0][6])
            return {'id': person.id, 'email': person.email, 'password': person.password, 'lastname': person.lastname, 'firstname': person.firstname, 'phone': person.phone,'role': person.role}
        else:
            return False
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getUserByEmail(email):
    try:
        user = getData(f"SELECT u.id, u.lastname, u.firstname, u.email, u.password, r.role from users u join roles r on u.role = r.id and u.email = '{email}'")
        if user != []:
            person = u.User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5])
            return  {'id': person.id, 'email': person.email, 'password': person.password, 'lastname': person.lastname, 'firstname': person.firstname, 'phone': person.phone,'role': person.role}
        else: 
            return False
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def createUser(login, password, firstname, lastname, phone ):
    password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    try:
        setData(f'INSERT INTO users ( email, password, lastname, firstname, phone, role) VALUES { login, password_hash, lastname, firstname, phone, 3}')
        flash('Пользователь успешно добавлен!')
    except Exception as error:
        logging.error(error)
        flash('Пользователь с таким email существует!')
        print(error)
        
        
def checkUser(password_hash, password):
    try:
        return check_password_hash(password_hash, password)
    except Exception as ex:
        logging.error(ex)
        print(ex)
    
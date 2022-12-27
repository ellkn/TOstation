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
        user = getData(f"SELECT u.id, u.email, u.password, u.lastname, u.firstname, u.phone, r.role from users u join roles r on u.role = r.id and  u.email = '{email}'")
        if user != []:
            person = u.User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5],  user[0][6])
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
        
        
def createOrder(user_id, goods_id):
    date = datetime.datetime.now()
    try:
        for good in goods_id:
            setData(f"INSERT INTO shop (user_id, good_id, datetime) VALUES {user_id, good, date}")
    except Exception as ex:
        print(ex)
        logging.error(ex)


def createServiceOrder(employee_id, user_id, services_id):
    date = datetime.datetime.now()
    date_out = (date + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        for service in services_id:
            #group by ???
            setData(f"INSERT INTO serviceshop (employees_id, user_id, good_id, service_id, datein, dateout, status) VALUES {employee_id, user_id, service, date, date_out, 1}")
    except Exception as ex:
        print(ex)
        logging.error(ex)


def addGood(name, price, type_id):
    try:
        setData(f"INSERT INTO goods (name, price, type) VALUES {name, price, type_id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)



def addService(name, price, type_id):
    try:
        setData(f"INSERT INTO services (name, price, type) VALUES {name, price, type_id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)


def addTypeGood(type):
    try:
        setData(f"INSERT INTO types (type) VALUES {type}")
    except Exception as ex:
        print(ex)
        logging.error(ex)


def addTypeService(type):
    try:
        setData(f"INSERT INTO servicetypes (type) VALUES {type}")
    except Exception as ex:
        print(ex)
        logging.error(ex)


def editUser(email, lastname, firstname, phone, role, id):
    try:
        setData(f"UPDATE users SET email = '{email}',  lastname = '{lastname}', firstname = '{firstname}', phone = '{phone}', role = {role} WHERE id = {id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)


def getUsers():
    try:
        return getData("select u.id, u.email, u.lastname, u.firstname, u.phone, r.role from users u join roles r on r.id = u.role")
    except Exception as ex:
        logging.error(ex)
        print(ex)
    

def getRoles():
    try:
        return getData(f'SELECT * FROM roles')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getAdminsCount():
    try:
        return getData(f'SELECT count(*) FROM users WHERE role = 1')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def getOrders():
    try:
        return getData("select s.id, u.email, u.lastname, u.firstname, u.phone, g.name, g.price, t.type, s.datetime from shop s join users u on u.id = s.user_id join goods g on s.good_id = g.id join types t on g.type = t.id")
    except Exception as ex:
        logging.error(ex)
        print(ex)


def getUserOrders(user_id):
    try:
        return getData(f"select s.id, u.email, u.lastname, u.firstname, u.phone, g.name, g.price, t.type, s.datetime from shop s join users u on u.id = s.user_id join goods g on s.good_id = g.id join types t on g.type = t.id WHERE s.user_id = {user_id}")
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def getTransactions():
    try:
        return getData("select s.id, e.email, e.lastname, e.firstname, e.phone, u.email, u.lastname, u.firstname, u.phone, ser.name, ser.price, st.type, s.datein, s.dateout, ss.status from serviceshop s join users u on u.id = s.user_id join users e on u.id = s.employees_id  join status ss on ss.id = s.status join services ser on ser.id = s.service_id join servicetypes st on st.id = ser.type")
    except Exception as ex:
        logging.error(ex)
        print(ex)


def getGoods():
    try:
        return getData("select g.id, g.name, g.price, t.type, g.type from goods g join types t on t.id = g.type")
    except Exception as ex:
        logging.error(ex)
        print(ex)


def getGoodTypes():
    try:
        return getData("select * from types")
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        

def getService():
    try:
        return getData("select s.id, s.name, s.price, st.type, s.type from services s join servicetypes st on st.id = s.type")
    except Exception as ex:
        logging.error(ex)
        print(ex)


def getServiceTypes():
    try:
        return getData("select * from servicetypes")
    except Exception as ex:
        logging.error(ex)
        print(ex)
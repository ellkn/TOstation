from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import db as db
import user as u
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY'
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(filename="logs/info.log", filemode='a', level=logging.INFO, format='%(asctime)s | %(message)s')
logging.basicConfig(filename="logs/error.log", filemode='a', level=logging.ERROR)

@login_manager.user_loader
def load_user(user_id):
    return u.UserLogin().dbi(user_id)


@app.route('/', methods = ["GET", "POST"])
def index():
    try:
        return render_template('index.html')
    except:
        return render_template('error.html')
    

@app.route('/login', methods = ["GET", "POST"])
def login():
    try:
        if not current_user.get_id():
            if request.method == 'POST':
                user = db.getUserByEmail(request.form.get("email"))
                if user:
                    if db.checkUser(user['password'], request.form.get("password")):
                        login_user(u.UserLogin().create(user))
                        flash("Успешный вход")
                        return redirect("/")
                    else:
                        flash("Неверный логин или пароль")
                        return render_template('login.html')
                return render_template('login.html')
            
            return render_template('login.html')
        else:
            return redirect("/")
    except:
        return render_template('error.html')
    
    
@app.route('/logout')
@login_required
def logout():
    if current_user.get_id():
        logout_user()
        return redirect("/login")
    else:
        return redirect("/")  
    

@app.route('/registration', methods = ["GET", "POST"])
def registration():
    try:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            if request.method == 'POST':
                if request.form.get("select") == "-1":
                    flash("Вы ввели некорректные данные, повторите попытку")
                    return render_template('registration.html')
                else:
                    db.createUser(request.form.get('email'), request.form.get('password'), request.form.get('lastname'), request.form.get('name'), request.form.get('phone'))
                    return redirect('/login')
            return render_template('registration.html')
    except:
        return render_template('error.html')
    
    
#страница для вывода деталей(всем)
@app.route('/shop')
def shop():
    try:        
        goods = db.getGoods()
        type = db.getGoodTypes()
        return render_template('shop.html', goods = goods, type = type)
    except:
        return render_template('error.html')
    

#страница для вывода услуг пользователя (админу)
@app.route('/services')
def services():
    try:        
        services = db.getService()
        type = db.getServiceTypes()
        print(services)
        print(type)
        return render_template('services.html', services = services, type = type)
    except:
        return render_template('error.html')
    
    
    
#страница для вывода покупок пользователя (пользователю)
@app.route('/orders')
def orders():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            orders = db.getOrders()
            return render_template('orders.html', orders = orders)
        elif current_user.is_authenticated and current_user.get_role() == 'USER':
            orders = db.getUserOrders(current_user.get_id())
            return render_template('orders.html', orders = orders)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')
    except:
        return render_template('error.html')    
    
    
@app.route('/createOrder',  methods = ["GET", "POST"])
def createOrder():
    try:
        if current_user.is_authenticated:
            users = db.getUsers() 
            goods = db.getGoods()
            goddtypes = db.getGoodTypes()
            if request.method == 'POST':
                if current_user.get_role() == 'ADMIN':
                    if request.form.get("good") == "-1" or request.form.get("user") == "-1":
                        flash("Введите корректные данные")
                    else:
                        db.createOrder(request.form.get("user"), request.form.get("good"))
                        flash('Заказ создан')
                        return redirect('/orders')
                elif current_user.get_role() == 'USER':
                    if request.form.get("good") == "-1":
                        flash("Введите корректные данные")
                    else:
                        print(request.form.get("good"))
                        db.createOrder(current_user.get_id(), request.form.get("good"))
                        flash('Заказ создан')
                        return redirect('/orders')
            return render_template('createOrder.html', users = users, good = goods, goddtypes = goddtypes)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return render_template('error.html')
    
    
#страница для вывода покупок услуг (админу)
@app.route('/transactions')
def transactions():
    try:
        return render_template('transactions.html')
    except:
        return render_template('error.html')
    

#страница для добавления товара (админу)
@app.route('/addGood', methods = ["GET", "POST"])
def addGood():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' :
            goodtypes = db.getGoodTypes()
            if request.method == 'POST':
                if request.form.get("type") == "-1" :
                    flash("Введите корректные данные")
                else:
                    db.addGood(request.form.get("name"), request.form.get("price"), request.form.get("type"))
                    flash('Товар добавлен')
                    return redirect('/shop')
            return render_template("addGood.html", type = goodtypes)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return render_template('error.html')
    
 
#страница для добавления категории товара (админу)   
@app.route('/addTypeGood', methods = ["GET", "POST"])
def addTypeGood():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' :
            if request.method == 'POST':
                if request.form.get("type") == "-1" :
                    flash("Введите корректные данные")
                else:
                    db.addTypeService(request.form.get("name"))
                    flash('Товар добавлен')
                    return redirect('/shop')
            return render_template("addTypeGood.html")
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return render_template('error.html')
    
    
#страница для добавления категории услуги (админу)     
@app.route('/addTypeService', methods = ["GET", "POST"])
def addTypeService():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' :
            if request.method == 'POST':
                if request.form.get("type") == "-1" :
                    flash("Введите корректные данные")
                else:
                    db.addTypeService(request.form.get("name"))
                    flash('Товар добавлен')
                    return redirect('/services')
            return render_template("addTypeService.html")
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return render_template('error.html')
    
    
#страница для добавления услуги (админу)     
@app.route('/addService', methods = ["GET", "POST"])
def addService():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' :
            goodtypes = db.getServiceTypes()
            if request.method == 'POST':
                if request.form.get("type") == "-1" :
                    flash("Введите корректные данные")
                else:
                    db.addService(request.form.get("name"), request.form.get("price"), request.form.get("type"))
                    flash('Услуга добавлена')
                    return redirect('/services')
            return render_template("addService.html", type = goodtypes)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return render_template('error.html')


#страница для управления пользователями (админу)  
@app.route('/users')
def users():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            users = db.getUsers()
            return render_template('users.html', users = users)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')
    except:
        return render_template('error.html')
    
    
#страница для изменения пользователями (админу) 
@app.route('/edit/<id>', methods = ["GET", "POST"])
def edit(id):
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            user = db.getUserById(id)
            role = db.getRoles()
            if request.method == "POST":
                if request.form.get("role") == "-1":
                    flash("Введите корректные данные")
                else:
                    if db.getAdminsCount()[0][0] == 1 and current_user.get_role() == 'ADMIN' and request.form.get("role") != 2:
                        flash("Вы не можете изменить роль у единственного пользователя с ролью ADMIN")
                    else:
                        db.editUser(request.form.get("email"), request.form.get("lastname"), request.form.get("firstname"), request.form.get("phone"), request.form.get("role"), id)
                    return render_template('edit.html', user = user, role = role)  
                
            return render_template('edit.html', user = user, role = role)   
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return render_template('error.html')
    

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('error.html', title="Страница не найдена")
    

if __name__ == '__main__':
   app.run(debug = True)

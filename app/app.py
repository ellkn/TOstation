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
    
    
#страница для вывода покупок пользователя (админу)
@app.route('/shop')
def shop():
    try:
        return render_template('shop.html')
    except:
        return render_template('error.html')
    
    
#страница для вывода покупок пользователя (пользователю)
@app.route('/orders')
def orders():
    try:
        return render_template('orders.html')
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
        return render_template('addGood.html')
    except:
        return render_template('error.html')
    
 
#страница для добавления категории товара (админу)   
@app.route('/addTypeGood', methods = ["GET", "POST"])
def addTypeGood():
    try:
        return render_template('addTypeGood.html')
    except:
        return render_template('error.html')
    
    
#страница для добавления категории услуги (админу)     
@app.route('/addTypeService', methods = ["GET", "POST"])
def addTypeService():
    try:
        return render_template('addTypeService.html')
    except:
        return render_template('error.html')
    
    
#страница для добавления услуги (админу)     
@app.route('/addService', methods = ["GET", "POST"])
def addService():
    try:
        return render_template('addService.html')
    except:
        return render_template('error.html')


#страница для управления пользователями (админу)  
@app.route('/users')
def users():
    try:
        return render_template('users.html')
    except:
        return render_template('error.html')
    
    
#страница для изменения пользователями (админу) 
@app.route('/edit/<id>', methods = ["GET", "POST"])
def edit(id):
    try:
        return render_template('edit.html')
    except:
        return render_template('error.html')
    
    
@app.route('/error')
def error():
    return render_template('error.html')
    
    
app.run(debug=True)
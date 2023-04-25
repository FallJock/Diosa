from flask import Flask, render_template, url_for, request, redirect
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import csv
from random import choice
import speech_recognition as sr
from flask_mail import Mail, Message
import os

db_session.global_init("db/blogs.db")
class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class HelpForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    subject = StringField("Тема сообщения", validators=[DataRequired()])
    problem = TextAreaField("Сообщение", validators=[DataRequired()])
    submit = SubmitField('Отправить')

app = Flask(__name__, template_folder="")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rozavaaponi@gmail.com'
app.config['MAIL_PASSWORD'] = 'fhmesrdqwicplkfr' # https://myaccount.google.com/apppasswords
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)
test = {
    "file": "",
    "test": [],
    "count": 0,
    "right": []
}
login_manager = LoginManager()
login_manager.init_app(app)
# user = User()
# user.name = "Пользователь 1"
# user.about = "биография пользователя 1"
# user.email = "email@email.ru"
# db_sess = db_session.create_session()
# db_sess.add(user)
# db_sess.commit()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    param['number'] = 6
    return render_template('test02.html', **param)



@app.route('/modules')
def modules():
    param = {}
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    if not current_user.is_authenticated:
        param["img"] = url_for('static', filename="img/account_where.gif")
        return render_template('acc.html', **param)
    
    # param['number'] = 10
    return render_template('project_course_example.html', **param)

@app.route('/modules/<int:n>')
def module(n):
    param = {}
    test['file'] = ""
    test['count'] = 0
    test['test'] = []
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    if not current_user.is_authenticated:
        param["img"] = url_for('static', filename="img/account_where.gif")
        return render_template('acc.html', **param)
    return render_template(f'module{n}.html', **param)


@app.route('/modules/<int:n>/<task>', methods=["POST", "GET"])
def module_task(n, task):
    global test
    param = {}
    # param["audio_text"] = []
    param["audio_text"] = True
    param["quest"] = "Нету вопроса"
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    if not current_user.is_authenticated:
        param["img"] = url_for('static', filename="img/account_where.gif")
        return render_template('acc.html', **param)
    link = f"module{n}-{task}"
    if test['file'] != link:
        test['file'] = link
        test['test'] = []
        test['count'] = 0
        test['right'] = []
        if "exercises" in link:
            
            sil = f"static/csv/{link}.csv"
            with open(sil, encoding="utf8") as cv:
                reader = list(csv.reader(cv, delimiter=';', quotechar='"'))
                n = range(len(reader))
                for i in range(5):
                    test['test'] += [reader[choice(n)]]
                print(test)
                param["quest"] = test['test'][0][0]
                return render_template(f'{link}.html', request="POST", **param)
    else:
        if len(test['test']) == 0:
            test['file'] = ""
            test['test'] = []
            test['count'] = 0
            test['right'] = []
            return render_template(f'{link}.html', request="POST", **param)
        param["quest"] = test['test'][0][0]
    if request.method == "POST":
        f = request.files["audio_data"]
        r = sr.Recognizer()
        with sr.WavFile(f) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="es-ES", show_all=True)
            print(text)
        if text == []:
            param["audio_text"] = False
            print("НЕРАСПОЗНАЛ")
            return render_template(f'{link}.html', request="POST", **param)
        else:
            tx = []
            test['count'] += 1
            check = test['test'][0][1]
            for i in text["alternative"]:
                n = i["transcript"].lower()
                tx += [n]
            param["audio_text"] = True
            check_is = check.lower() in tx
            test['right'] += [check_is]
            print("принял. ответил на:", check_is)
            if len(test['test']) == 1:
                test['file'] = ""
                test['test'] = []
                test['count'] = 0
                param['right'] = test['right']
                imgs = "love.jpg cool.jpg ud.gif two.jpg hacker.gif oh_no.gif".split()
                imgs.reverse()
                param['img'] = url_for('static', filename=imgs[test['right'].count(True)])
                return render_template('results.html', **param)
            else:
                test['test'] = test['test'][1:]
            
            param["quest"] = test['test'][0][0]
            
        return render_template(f'{link}.html', request="POST", **param)

    return render_template(f'{link}.html', **param)

@app.route('/help', methods=['GET', 'POST'])
def help():
    param = {}
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    form2 = HelpForm()
    print(form2.data)
    if form2.validate_on_submit():
        # print(form2.data['name'])
        msg = Message(f'Нужна поддержка: {form2.data["subject"]}', sender = 'rozavaaponi@gmail.com', recipients = ['rozavaaponi@gmail.com'])
        msg.body = f"{form2.data['name']} {form2.data['surname']} почта - {form2.data['email']} говорит: {form2.data['problem']}"
        msg.html = ""
        mail.send(msg)
        return "Отправлено"

    return render_template('help.html', form2=form2, **param)
    # return "поддержки пока нет, но вы держитесь" - этот шедевр нужно оставить :)


@app.route('/login', methods=['GET', 'POST'])
def login():
    param = {}
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **param)
    return render_template('login.html', title='Авторизация', form=form, **param)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    param = {}
    param['bos'] = url_for('static', filename="css/bootstrap_min.css")
    param['style'] = url_for('static', filename='css/style.css')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", **param)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", **param)
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, **param)

if __name__ == '__main__':
    # app.run(port=8080, host='127.0.0.1')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

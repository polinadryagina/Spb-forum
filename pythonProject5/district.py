from flask import Flask, render_template, redirect, request, make_response, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm, LoginForm
from data.news import News, NewsForm
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
district_name = 'Неопределенный район'
district_code = 'None'


def main(district_nm, district_cd):
    global district_name, district_code
    district_name = district_nm
    district_code = district_cd
    db_session.global_init("db/blogs.db")
    app.run(host='0.0.0.0', port=5000)


@app.route("/")
def index():
    posts = 'Добро пожаловать в {}!'.format(district_name)
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        posts = 'Записи в блоге "{}"'.format(district_name)
        news = db_sess.query(News).filter(
            ((News.user == current_user) | (News.is_private != True)) & (News.district == district_code))
    else:
        news = db_sess.query(News).filter(
            (News.is_private != True) & (News.district == district_code))
    return render_template("index.html", news=news, posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    global district_code
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.district = district_code
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    global district_code
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user,
                                          News.district == district_code
                                          ).first()
        if news:
            form.title.data = news.title
            form.address.data = news.address
            form.latitude.data = news.latitude
            form.longitude.data = news.longitude
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user,
                                          News.district == district_code
                                          ).first()
        if news:
            news.title = form.title.data
            news.address = form.address.data
            news.latitude = form.latitude.data
            news.longitude = form.longitude.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            news.district = district_code
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user,
                                      News.district == district_code
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/post/<int:id>/')
def publish(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(
        (News.id == id)).first()
    news.is_private = (news.is_private + 1) % 2
    db_sess.commit()
    return redirect("/")


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    # main('центральный район Санкт-Петербурга','central')
    main('невский район Санкт-Петербурга', 'neva')
    main('кронштадтский район Санкт-Петербурга', 'kronshtadt')

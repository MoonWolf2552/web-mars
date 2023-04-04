from flask import Flask, url_for, request, render_template, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api

from data import db_session, jobs_api, users_resource
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.department import DepartmentForm, EdDepartmentForm
from forms.job import JobForm, EdJobForm
from forms.login_form import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

api.add_resource(users_resource.UsersListResource, '/api/v2/users')

api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:news_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs, title='Журнал работ')


@app.route('/departments')
def departments():
    session = db_session.create_session()
    departments = session.query(Department).all()
    return render_template('departments.html', departments=departments, title='Журнал департаментов')


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.team_leader.choices = [(i.id, i.name) for i in users]
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            is_finished=form.is_finished.data
        )
        if form.collaborators.data:
            job.collaborators = form.collaborators.data
        if form.start_date.data:
            job.start_date = form.start_date.data
        if form.end_date.data:
            job.end_date = form.end_date.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Добавление работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = EdJobForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.team_leader.choices = [(i.id, i.name) for i in users]
    if request.method == "GET":
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            if job.user == current_user or current_user.id == 1:
                form.team_leader.data = job.team_leader
                form.job.data = job.job
                form.work_size.data = job.work_size
                form.collaborators.data = job.collaborators
                form.start_date.data = job.start_date
                form.end_date.data = job.end_date
                form.is_finished.data = job.is_finished
            else:
                abort(404)
        else:
            abort(404)
    if form.validate_on_submit():
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Редактирование работы', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job and (Jobs.user == current_user or current_user.id == 1):
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/adddepartment', methods=['GET', 'POST'])
@login_required
def adddepartment():
    form = DepartmentForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.chief.choices = [(i.id, i.name) for i in users]
    if form.validate_on_submit():
        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Добавление департамента', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = EdDepartmentForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.chief.choices = [(i.id, i.name) for i in users]
    if request.method == "GET":
        department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            if department.user == current_user or current_user.id == 1:
                form.title.data = department.title
                form.chief.data = department.chief
                form.members.data = department.members
                form.email.data = department.email
            else:
                abort(404)
        else:
            abort(404)
    if form.validate_on_submit():
        department = db_sess.query(Department).filter(Jobs.id == id).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html', title='Редактирование департамента', form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id).first()
    if department and (Department.user == current_user or current_user.id == 1):
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/training/<prof>')
def traning(prof):
    return render_template('training.html', prof=prof, title="Тренировки в полёте")


@app.route('/list_prof')
@app.route('/list_prof/<list>')
def list_prof(list='ol'):
    professions = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                   'инженер по терраформированию', 'климатолог', 'специалист по радиационной защите',
                   'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения', 'метеоролог',
                   'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов']
    return render_template('list_prof.html', prof=list, professions=professions,
                           title="Список профессий")


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    param = {
        'title': 'Автоматический ответ',
        'surname': 'Twen',
        'name': 'Mark',
        'education': 'middle',
        'profession': 'doctor',
        'sex': 'male',
        'motivation': 'popularity',
        'ready': 'True',
    }
    return render_template('auto_answer.html', **param)


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect('/')
#     return render_template('login.html', title='Авторизация', form=form)


@app.route('/promotion')
def promotion():
    a = ["Человечество вырастает из детства.</p>",
         "Человечеству мала одна планета.</p>",
         "Мы сделаем обитаемыми безжизненные пока планеты.</p>",
         "И начнем с Марса!</p>",
         "Присоединяйся!</p>"]
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Рекламная кампания</title>
                  </head>
                  <body>
                    <h2>{'<p>'.join(a)}</h2>
                  </body>
                </html>"""


@app.route('/image_mars')
def image_mars():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/mars.png')}" 
                            alt="здесь должна была быть картинка, но не нашлась">
                        <p>Вот она какая, красная планета.</p>
                      </body>
                    </html>"""


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    photoes = ['static/img/mars2.jpg',
               'static/img/mars3.jpg']
    active = 'static/img/mars1.jpg'
    if request.method == 'GET':
        return render_template('galery.html', title='Галерея', active=active, photoes=photoes)
    if request.method == 'POST':
        photoes.append(f'static/img/{request.form["img"]}')
        return render_template('galery.html', title='Галерея', active=active, photoes=photoes)


@app.route('/carousel', methods=['POST', 'GET'])
def carousel():
    return f"""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
                            integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
                            crossorigin="anonymous">
                            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" 
                            integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" 
                            crossorigin="anonymous"></script>
                            <title>Пейзажи Марса</title>
                          </head>
                          <body>
                            <h1 align="center">Пейзажи Марса</h1>
                            <div id="carouselExampleControls" class="carousel slide" data-bs-ride="true">
                             <div class="carousel-inner">
                                <div class="carousel-item active">
                                  <img src="static/img/mars1.jpg" class="d-block w-100"
                                  height = "1000"
                                  alt="здесь должна была быть картинка, но не нашлась">
                                </div>
                                <div class="carousel-item">
                                  <img src="static/img/mars2.jpg" class="d-block w-100" 
                                  height = "1000"
                                  alt="здесь должна была быть картинка, но не нашлась">
                                </div>
                                <div class="carousel-item">
                                  <img src="static/img/mars3.jpg" class="d-block w-100"
                                  height = "1000"
                                  alt="здесь должна была быть картинка, но не нашлась">
                                </div>
                              </div>
                              <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">Previous</span>
                              </button>
                              <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">Next</span>
                              </button>
                            </div>
                          </body>
                        </html>"""


@app.route('/load_photo', methods=['POST', 'GET'])
def load_image():
    if request.method == 'GET':
        return f"""<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
                                    <link rel="stylesheet" type="text/css" href="static/css/style.css" />
                                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
                                    <title>Загрузка фотографии</title>
                                  </head>
                                  <body>
                                    <h1 align="center">Загрузка фотографии</h1>
                                    <h2 align="center">для участи в миссии</h2>
                                    <div>
                                        <form class="img_form" form method="post" enctype="multipart/form-data">
                                            <div class="form-group">
                                                <label for="photo">Загрузите фотографию</label>
                                                <input type="file" class="form-control-file" id="photo" name="img">
                                            </div>
                                            <br>
                                            <button type="submit" class="btn btn-primary">Отправить</button>
                                         </form>
                                    </div>
                                  </body>
                                </html>"""
    if request.method == 'POST':
        from io import BytesIO
        a = BytesIO(request.files['img'].read())
        from base64 import b64encode

        # Получаем байты из объекта BytesIO и кодируем их в base64
        img_data = a.getvalue()
        img_base64 = b64encode(img_data).decode('utf-8')
        # Выводим изображение на HTML страницу
        html = f'<img src="data:image/jpeg;base64,{img_base64}"/>'
        return f"""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="static/css/style.css" />
                            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
                            <title>Загрузка фотографии</title>
                          </head>
                          <body>
                            <h1 align="center">Загрузка фотографии</h1>
                            <h2 align="center">для участи в миссии</h2>
                            <div>
                                <form class="img_form" method="post">
                                    <div class="form-group">
                                        <label for="photo">Загрузите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="img">
                                    </div>
                                    <br>
                                    {html}
                                    <br>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                 </form>
                            </div>
                          </body>
                        </html>"""


@app.route('/promotion_image')
def promotion_image():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <link rel="stylesheet"
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                        crossorigin="anonymous">
                        <title>Реклама с картинкой</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/mars.png')}" 
                            width="300" height="300" 
                            alt="здесь должна была быть картинка, но не нашлась">
                        <div class="alert alert-secondary" role="alert">Человечество вырастает из детства.</div>
                        <div class="alert alert-success" role="alert">Человечеству мала одна планета.</div>
                        <div class="alert alert-secondary" role="alert">Мы сделаем обитаемыми безжизненные пока планеты.</div>
                        <div class="alert alert-warning" role="alert">И начнем с Марса!</div>
                        <div class="alert alert-danger" role="alert">Присоединяйся!</div>
                      </body>
                    </html>"""


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1 align="center">Анкета претендента</h1>
                            <h2 align="center">на участие в миссии</h2>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите фамилию" name="surname">
                                    <input type="text" class="form-control" id="password" placeholder="Введите имя" name="name">
                                    <p></p>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="educationSelect">Какое у Вас образование</label>
                                        <select class="form-control" id="educationSelect" name="education">
                                          <option>Начальное</option>
                                          <option>Основное</option>
                                          <option>Среднее</option>
                                          <option>Среднее профессиональное</option>
                                          <option>Высшее</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label for="professionSelect">Какие у Вас профессии</label>
                                        <div>
                                            <input type="checkbox" id="in-is" name="in-is" checked>
                                            <label for="in-is">Инженер-исследователь</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="pilot" name="pilot">
                                          <label for="pilot">Пилот</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="climat" name="climat">
                                          <label for="climat">Климатолог</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="doctor" name="doctor">
                                          <label for="doctor">Врач</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="builder" name="builder">
                                          <label for="builder">Строитель</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="exobio" name="exobio">
                                          <label for="exobio">Экзобиолог</label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="quest">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="quest" rows="3" name="quest"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>

                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы ли остаться на Марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form.get('surname'))
        print(request.form.get('name'))
        print(request.form.get('email'))
        print(request.form.get('education'))
        print(request.form.get('in-is', 'off'))
        print(request.form.get('pilot', 'off'))
        print(request.form.get('climat', 'off'))
        print(request.form.get('doctor', 'off'))
        print(request.form.get('builder', 'off'))
        print(request.form.get('exobio', 'off'))
        print(request.form.get('sex'))
        print(request.form.get('quest'))
        print(request.form.get('file'))
        print(request.form.get('accept'))
        return "<h1>Форма отправлена<h1>"


def user_create():
    session = db_session.create_session()

    user = User(surname='Scott',
                name='Ridley',
                age=21,
                position='captain',
                speciality='research engineer',
                address='module_1',
                email='scott_chief@mars.org')
    session.add(user)
    session.commit()

    user = User(surname='Harry',
                name='Potter',
                age=14,
                position='magl',
                speciality='engineer',
                address='module_1',
                email='harry@mars.org')
    session.add(user)

    user = User(surname='Joe',
                name='Biden',
                age=60,
                position='prezident',
                speciality='biolog',
                address='module_2',
                email='biden@mars.org')
    session.add(user)

    user = User(surname='Mark',
                name='Twen',
                age=45,
                position='writer',
                speciality='coocker',
                address='module_3',
                email='twen@mars.org')
    session.add(user)


def jobs_create():
    session = db_session.create_session()

    job = Jobs(team_leader=1,
               job='deployment of residential modules 1 and 2',
               work_size=15,
               collaborators='2, 3',
               is_finished=False,
               )
    session.add(job)

    job = Jobs(team_leader=1,
               job='cleaning of modules 1 and 2',
               work_size=20,
               collaborators='1, 4',
               is_finished=False,
               )
    session.add(job)

    session.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # user_create()
    # jobs_create()
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1')

from flask import Flask, url_for, request, render_template, redirect

from forms.login_form import LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index')
@app.route('/index/<title>')
def index(title='Миссия на Марс'):
    return render_template('index.html', title=title)


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


@app.route('/distribution')
def distribution():
    cosm = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', cosm=cosm, title="По каютам!")


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


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


@app.route('/carousel')
def carousel():
    return f"""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
                            integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
                            crossorigin="anonymous">
                            <title>Пейзажи Марса</title>
                          </head>
                          <body>
                            <h1 align="center">Пейзажи Марса</h1>
                            <div id="carouselExampleControls" class="carousel slide" data-bs-ride="true">
                             <div class="carousel-inner">
                                <div class="carousel-item active">
                                  <img src="static/img/mars1.jpg" class="d-block w-100"
                                  alt="здесь должна была быть картинка, но не нашлась">
                                </div>
                                <div class="carousel-item">
                                  <img src="static/img/mars2.jpg" class="d-block w-100" 
                                  alt="здесь должна была быть картинка, но не нашлась">
                                </div>
                                <div class="carousel-item">
                                  <img src="static/img/mars3.jpg" class="d-block w-100"
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

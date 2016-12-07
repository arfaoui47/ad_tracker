from flask import Flask, render_template, request, flash, session, url_for, redirect
from flaskext.mysql import MySQL
from forms import *
from models import db, User


app = Flask(__name__)
mysql = MySQL()
app.config.from_object('config')
db.init_app(app)
mysql.init_app(app)


@app.route('/')
def home():
    if 'email' not in session:
        return render_template('pages/placeholder.notsignin.html')
    else:
        cur = mysql.connect().cursor()
        cur.execute('''SELECT * FROM images''')
        rv = cur.fetchall()
        col_key_mapper = {'date': 2,
                          'site': 4}
        sort = request.args.get('sort', 'date')
        reverse = (request.args.get('direction', 'asc') == 'desc')

        direction = 'asc' if reverse else 'desc'

        sort_by_date = url_for('home', sort='date', direction=direction)
        sort_by_website = url_for('home', sort='site', direction=direction)

        result = sorted(rv, key=lambda x: x[col_key_mapper[sort]],
                        reverse=reverse)

        return render_template('pages/placeholder.home.html', result=result,
                               sort_by_date=sort_by_date,
                               sort_by_website=sort_by_website)


@app.route('/manage')
def about():
    return render_template('pages/placeholder.manage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            # print 'ssssssssssss'
            return render_template('forms/register.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data,
                           form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            session['name'] = form.firstname
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('forms/register.html', form=form)


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    else:
        return render_template('pages/placeholder.home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('forms/login.html', form=form)
        else:
            session['email'] = form.email.data
            session['name'] = form.firstname
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('forms/login.html', form=form)


@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/test')
def test():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM images''')
    rv = cur.fetchall()
    return render_template('pages/placeholder.home.html.html', result=rv)


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


# Default port:
if __name__ == '__main__':
    app.run()

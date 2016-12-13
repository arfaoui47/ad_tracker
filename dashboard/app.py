from flask import Flask, render_template, request, flash, session, url_for, redirect
from flaskext.mysql import MySQL
from forms import *
from models import db, User, Advert, Adtracking, Website


app = Flask(__name__)
mysql = MySQL()
app.config.from_object('config')
db.init_app(app)
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():   
    if 'email' not in session:
        return render_template('pages/placeholder.notsignin.html')
    else:
        conn = mysql.connect() 
        cur = conn.cursor()
        cur.execute('''SELECT * FROM images WHERE authorized="NULL"''')
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

        if request.method == 'POST':
            options = request.form['options']
            track_value = str(options).split()[0]
            checksum = str(options).split()[1]

            cur.execute(''' UPDATE images SET authorized={} WHERE 
                        checksum={}'''.format(
                            repr(track_value), repr(checksum)))
            conn.commit()

            if track_value == 'True':
                return redirect(url_for('manage_advert', checksum=checksum))
            else:
                return redirect(url_for('home'))

        return render_template('pages/placeholder.home.html', result=result,
                               sort_by_date=sort_by_date,
                               sort_by_website=sort_by_website)


@app.route('/websites', methods=['GET', 'POST'])
def manage_websites():
    form = WebsiteForm()
    websites = Website.query.filter_by()
    delete = request.args.get('delete', 'false')
    edit = request.args.get('edit', 'false')

    if 'email' not in session:
        return render_template('pages/placeholder.notsignin.html')
    else:
        if request.method == 'POST':
            if edit != 'false':
                website = Website.query.filter_by(domain_name=edit).first()
                website.cost = form.cost.data if form.cost.data else 0
                print website.domain_name
                print form.cost.data
                db.session.commit()
                return redirect(url_for('manage_websites'))

            if not form.validate():
                return render_template('pages/placeholder.websites.html',
                            websites=websites, form=form)
            else:
                cost = form.cost.data if form.cost.data else 0
                new_website = Website(form.domain_name.data, cost)
                db.session.add(new_website)
                db.session.commit()
            return redirect(url_for('manage_websites', edit=edit))
        
        elif request.method == 'GET':
            if delete != 'false':
                Website.query.filter_by(domain_name=delete).delete()
                db.session.commit()
            return render_template('pages/placeholder.websites.html',
                                websites=websites, form=form, edit=edit)


@app.route('/advert/<string:checksum>', methods=['GET', 'POST'])
def manage_advert(checksum):
    form = AdvertForm()

    advert = Advert.query.filter_by(checksum=checksum).first()
    adtracking = Adtracking.query.filter_by(checksum=checksum)

    edit = request.args.get('edit', 'false')
    delete = request.args.get('delete', 'false')
    website_selected = request.args.get('website', advert.website)

    website_list = [ad.location for ad in adtracking]

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('pages/advert.html', form=form, advert=advert)
        else:
            advert.description = form.description.data if form.description.data else advert.description
            if not form.rate.data:
                if not advert.rate:
                    advert.rate = 0
            else:
                advert.rate = form.rate.data

            if not form.value.data:
                if not advert.rate:
                    advert.rate = 0
            else:
                advert.value = form.value.data

            advert.product = form.product.data if form.product.data else advert.product
            advert.class_customer = form.class_customer.data if form.class_customer.data else advert.class_customer
            advert.category = form.category.data if form.category.data else advert.category
            advert.sector = form.sector.data if form.sector.data else advert.sector
            advert.image_id = form.image_id.data
            db.session.commit()
            return redirect(url_for('manage_advert', checksum=checksum))

    elif request.method == 'GET':
        
        
        if delete == 'true':
            Advert.query.filter_by(checksum=checksum).delete()
            db.session.commit()
            return redirect(url_for('home'))
        
        return render_template('pages/advert.html', form=form, advert=advert,
                                edit=edit, website_list=website_list,
                                website_selected=website_selected)


    return checksum

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
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

'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()'''

# Default port:
if __name__ == '__main__':
    app.run()

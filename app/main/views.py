from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from .forms import NameForm
from ..email import send_email
from .. import db
from ..models import User


@main.route('/',methods=['GET','POST'])
def home():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        return redirect(url_for('main.home'))
    return render_template('home.html', 
                            form=form, 
                            name=session.get('name'),
                            known=session.get('known', False))

@main.route('/about')
def about():
    return render_template('about.html')
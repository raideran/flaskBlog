from flask import render_template, redirect, session, flash, url_for, current_app
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email



@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
            flash(f'User {user.username} has been created successfully' )
        else:
            session['known'] = True
        session['name'] = form.name.data               
        return redirect(url_for('.index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known', False))

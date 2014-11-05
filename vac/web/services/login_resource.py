from werkzeug.utils import redirect
from vac.web.html.login_form import LoginForm
from flask import Blueprint, render_template

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/test', methods=['GET'])
def test():
    return "VacPi's alive!\n"


@login_blueprint.route('/', methods=['GET'])
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        return redirect('/test')
    return render_template('login.html',
                           title='Sign In',
                           form=form)

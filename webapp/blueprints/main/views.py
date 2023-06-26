from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates',
                 static_folder='static',
                 static_url_path='/main/static')


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/terms')
def terms():
    return render_template('main/terms.html')


@main.route('/privacy')
def privacy():
    return render_template('main/privacy.html')

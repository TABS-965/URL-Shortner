from flask import Blueprint, request, redirect, render_template, url_for, flash
from .models import URL
from .utils import generate_short_code
from . import db

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not original_url:
            flash('URL is required!')
            return redirect(url_for('main.index'))
        
        
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            return render_template('index.html', short_url=request.host_url + existing_url.short_code)
        

        short_code = generate_short_code()
        if not short_code:
            flash('Could not generate a unique short code. Please try again.')
            return redirect(url_for('main.index'))
        

        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        
        return render_template('index.html', short_url=request.host_url + short_code)
    
    return render_template('index.html')

@bp.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.original_url)
    else:
        return render_template('redirect.html', error="Short URL not found"), 404
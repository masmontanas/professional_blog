from flask import render_template, flash
from app import app, db, cache

@app.errorhandler(404)
@cache.cached(timeout=50, key_prefix='404_error')
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
@cache.cached(timeout=50, key_prefix='500_error')
def internal_error(error):
    flash(u'The administrator has been notified of the error.','error')
    return render_template('500.html'), 500
from flask import render_template, flash, redirect, url_for, session, g, request, jsonify, make_response, send_from_directory, send_file, current_app

from sqlalchemy import and_

from werkzeug.utils import secure_filename

import pandas as pd

from sqlalchemy_json_querybuilder.querybuilder.search import Search

import locale

# locale.setlocale(locale.LC_ALL, 'de_DE')
digitformat = locale.format

from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .models import *
from .forms import *
from datetime import datetime, timedelta
from sqlalchemy import func, or_


from calendar import monthrange

import os, time
os.environ['TZ'] = "Africa/Kampala"
time.tzset() 


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'])




@app.route('/')
@login_required
def home():
	# flash("this is the flash", category='success')
    return redirect(url_for('equipment_management.complaint_view'))




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/upload_file', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(app.config['UPLOAD_FOLDER']+"/"+str(filename))
            
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


# Exporting file to user

@app.route('/file_download/<file_name>')
def file_download(file_name):
    
    path = app.config['DOWNLOAD_FILES_PATH']   
    
    send_file = send_from_directory(
									directory=path,
									filename='{}.xlsx'.format(file_name), 
									as_attachment=True,
									attachment_filename='{}.xlsx'.format(file_name)
									)
    
    send = make_response(send_file)
    
    send.headers["x-suggested-filename"] ='{}.xlsx'.format(file_name)
    send.headers['Cache-Control'] = "max-age=0, no-cache, no-store, must-revalidate"
    send.headers['Pragma'] = "no-cache"
    send.headers['Expires'] = "Wed, 11 Jan 1984 05:00:00 GMT"
    send.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    send.headers["Content-Disposition"] =  "attachment; filename='{}.xlsx'".format(file_name)
    
    return send





@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def page_not_found(e):
	
	return "page not found",404

@app.errorhandler(500)
def server_error(e):
	return "server_error", 500

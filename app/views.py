import sqlite3
from app import app
from forms import IndicatorForm
from flask import render_template, flash, redirect, _app_ctx_stack, request, jsonify, url_for, json, send_from_directory
import os
from werkzeug.utils import secure_filename
import xls2csv
import uuid

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'db', 'indicators.sqlite')

def get_db():
    top = _app_ctx_stack.top
    db = getattr(top, '_database', None)
    if db is None:
        db = top._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/indicators", methods = ['GET'])
def indicators():
    project = request.args.get('project')
    country = request.args.get('country')

    if not(project and country):
        result = json.dumps({
                'success': False,
                'error': app.config['MSG_MISSING_PARAM']
        }, encoding="utf-8")
        return render_template('indicators.html',result=result)

    indicatorlist = []
    for indic in query_db("select * from indicators where post = ? and project = ?",[country, project]):
        indicatorlist.append({'post': indic[0], 'project': indic[2], 'goal': indic[3], 'objective': indic[4], 'indicator': indic[5]})

    if len(indicatorlist) == 0:
        result = json.dumps({
                'success': False,
                'error': app.config['MSG_INVALID_COUNTRY_PROJECT_COMBINATION']
        }, encoding="utf-8")
    else:
        result = json.dumps({
                'success': True,
                'indicatorlist': indicatorlist
        }, encoding="utf-8")

    return render_template('indicators.html',country=country,project=project,result=result)

@app.route("/")
@app.route("/index", methods = ['GET','POST'])
def index():
    return render_template("index.html", title='Home')

@app.route("/apidemo", methods = ['GET','POST'])
def apidemo():
    form = IndicatorForm(request.form)
    countrylist = []
    for country in query_db("select distinct post from indicators order by post"):
        countrylist.append((country[0],country[0]))
    form.country.choices = countrylist

    projectlist = []
    for project in query_db("select distinct project from indicators where post = ? order by project",[countrylist[0][0]]):
        projectlist.append((project[0],project[0]))
    form.project.choices = projectlist

    if request.method == 'POST':
        return redirect(url_for('indicators', country=form.country.data, project=form.project.data))

    return render_template('apidemo.html',title='REST API demo',form=form)

# callback for Javascript
@app.route("/updateprojects", methods = ['POST'])
def updateprojects():
    country = request.form['country']
    projectlist = []
    for project in query_db("select distinct project from indicators where post = ? order by project",[country]):
        projectlist.append(project[0])
    return jsonify({'options': projectlist})

@app.route("/upload", methods = ['GET'])
def upload():
    return render_template("upload.html", title='Upload spreadsheet')

@app.route("/uploadxls", methods = ['POST'])
def uploadXLS():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = os.path.splitext(secure_filename(file.filename))[0]
            random_uuid = uuid.uuid4()
            path = os.path.join(app.config['UPLOAD_FOLDER'], str(random_uuid))
            if not os.path.exists(path): os.makedirs(path)
            genfile = os.path.join(path, filename)
            file.save(genfile)

            convert_file(genfile)

            return redirect(url_for('servefiles', uuid=random_uuid, filename=filename))

    flash(u'Invalid filetype. Only XLS or XLSX allowed.','xlsuploaderror')
    return redirect('/upload')

# TODO: add radio to choose CSV vs SQLITE
# TODO: show some kind of progress bar

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def convert_file(filename):
    outcsvfilename = '%s.csv' % filename
    xls2csv.xls2csv(filename, outcsvfilename)
    outsqlitefilename = '%s.sqlite' % filename
    xls2csv.csv2sqlite(outcsvfilename, outsqlitefilename)

@app.route("/servefiles/<uuid>/<filename>", methods = ['GET','POST'])
def servefiles(uuid, filename):
    csvfilename = os.path.join(uuid, '%s.csv' % filename)
    sqlitefilename = os.path.join(uuid, '%s.sqlite' % filename)
    return render_template("servefiles.html", csvfilename=csvfilename, sqlitefilename=sqlitefilename)

@app.route("/download/<uuid>/<filename>")
def downloadfile(uuid, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], uuid)
    if not os.path.exists(directory):
        flash(u'Sorry, the requested file was not found. Please upload your spreadsheet again.','conversionerror')
        return redirect('/upload')

    filename = os.path.join(uuid, filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)

@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    db = getattr(top, '_database', None)
    if db is not None:
        db.close()

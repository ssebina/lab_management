import os

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:sundapostgres@178.128.65.113:5432/labmonitordb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

DOWNLOAD_FILES_PATH = os.path.join(basedir,"generated_files")

UPLOAD_FOLDER = os.path.join(basedir,"generated_files")


WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-cant-guess-what-this-is'

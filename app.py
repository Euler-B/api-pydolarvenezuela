import logging 
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from src.core import limiter
from src.consts import TIMEOUT, GETLOGS, DROPBOX_JOB, TELEGRAM_JOB
from src import cron
from src.routes import index, monitors, admin
from src.exceptions import (
    HTTPException,
    handle_http_exception,
    forbidden,
    method_not_allowed,
    page_not_found,
    internal_server_error,
    gateway_timeout
)

if GETLOGS:
    logging.basicConfig(filename='logs.log', level=logging.INFO)

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(cron.job, 'cron', minute=f'*/{TIMEOUT}', id='job')

if DROPBOX_JOB:
    scheduler.add_job(cron.upload_backup_dropbox, 'cron', day_of_week='sat', hour='6', minute='0', id='backup_dropbox')

if TELEGRAM_JOB:
    scheduler.add_job(cron.upload_backup_telegram, 'cron', day_of_week='sat', hour='6', minute='0', id='backup_telegram')

scheduler.start()

# app
app = Flask(__name__)
CORS(app)
limiter.init_app(app)
swagger = Swagger(app, template_file='src/swagger.yaml')

# error handling
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(403, forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(405, method_not_allowed)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(504, gateway_timeout)

# routes
app.register_blueprint(index.route)
app.register_blueprint(monitors.route, url_prefix='/api/v1')
app.register_blueprint(admin.route, url_prefix='/api/admin')

if __name__ == '__main__':
    # https://github.com/agronholm/apscheduler/issues/521
    # The instance will not have to perform the task twice
    # because the instance will be unique. use_reloader=False
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)
    scheduler.shutdown()
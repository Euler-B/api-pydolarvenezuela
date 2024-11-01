import os
import subprocess
from typing import Dict, Any
from .consts import SQL_USER, SQL_HOST, SQL_DB_NAME, SQL_PASSWORD

if os.getenv('PGPASSWORD') is None:
    os.environ['PGPASSWORD'] = SQL_PASSWORD

os.makedirs(os.path.join(os.path.dirname(__file__), 'tmp'), exist_ok=True)
_BACKUP_PATH = os.path.join(
    os.path.dirname(__file__), 'tmp', 'backup.sql'
)

def backup() -> Dict[str, Any]:
    try:
        subprocess.run(
            ['pg_dump', '-h', SQL_HOST, '-U', SQL_USER, SQL_DB_NAME, '-f', _BACKUP_PATH]
        )
        return {'message': 'Backup completed successfully.', 'success': True}
    except subprocess.CalledProcessError as e:
        return {'message': 'An error occurred during backup.', 'success': False}
    except Exception as e:
        return {'message': f'Error {e}', 'success': False}
import os
import subprocess
from datetime import datetime
from typing import Dict, Any
from .consts import SQL_USER, SQL_HOST, SQL_DB_NAME, SQL_PASSWORD

if os.getenv('PGPASSWORD') is None:
    os.environ['PGPASSWORD'] = SQL_PASSWORD

backup_dir = os.path.join(os.path.dirname(__file__), 'tmp')
os.makedirs(backup_dir, exist_ok=True)

def backup() -> Dict[str, Any]:
    if os.listdir(backup_dir):
        for file in os.listdir(backup_dir):
            if file.startswith('backup_'):
                os.remove(os.path.join(backup_dir, file))
        
    datetime_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_path = os.path.join(backup_dir, f'backup_{datetime_str}.sql')

    try:
        subprocess.run(
            ['pg_dump', '-h', SQL_HOST, '-U', SQL_USER, SQL_DB_NAME, '-f', backup_path]
        )
        return {'message': 'Backup completed successfully.', 'success': True, 'path': backup_path}
    except subprocess.CalledProcessError as e:
        return {'message': 'An error occurred during backup.', 'success': False}
    except Exception as e:
        return {'message': f'Error {e}', 'success': False}
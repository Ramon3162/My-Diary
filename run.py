from app.app import app
from instance.config import app_config



app.config.from_object(app_config['development'])

if __name__ == '__main__':
    app.run()
    
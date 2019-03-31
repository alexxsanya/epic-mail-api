from api import create_app
from os import environ

config_name = environ.get("APP_SETTING")

app = create_app(config_name)
    
if __name__ == "__main__":
    app.run()
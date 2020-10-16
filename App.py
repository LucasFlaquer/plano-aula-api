from src import app
import os
env_port = os.environ.get('FLASK_RUN_PORT', 3000)

if __name__ == '__main__':
    #app.
    app.run(port=env_port)
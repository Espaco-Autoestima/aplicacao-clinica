import os
from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret-key-ea'

from controllers import *

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
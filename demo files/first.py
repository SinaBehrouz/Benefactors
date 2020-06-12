"""
    Sets up a basic Flask application 
    
"""
# TO DO : Take out demo comments

# important to highlight how we can set up these this simple flask app with an api with just a couple lines of code
# super lightweight 
from flask import Flask  # when doing intro, can talk about how these two lines work
app = Flask(__name__)

# default is get, can specify other methods, shown in next file
# show different endpoint, i.e switch from '/' to 'hello'
# talk about how simple @app.route decorater associates the '/' endpoint with hello_world function
@app.route('/')
def hello_world():
    return 'Hello, World!'

# don't need this, but just lets you be in debug mode
# super helpful for debugging, and automatically restarting when changes are made in your file
if __name__ == '__main__':
    app.run(debug=True)
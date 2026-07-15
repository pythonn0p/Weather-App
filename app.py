#File is standard naming convention in importing flask
from flask import Flask,render_template, request
from weather import main as get_weather

#creates the flask application
app = Flask(__name__)

#Since it is a single page application, all of the behaviour will be rendered by a single route
@app.route('/', methods=['GET', 'POST']) #route it simply the home page
def index():
    data = None #ensures there is always a variable
    data = get_weather() #Need to give this data to the render template
    return render_template('index.html', data = data) 

#If deploying change this to production application
if __name__ == '__main__':
    app.run(debug=True)
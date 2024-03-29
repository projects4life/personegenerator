from flask import Flask, render_template, abort
from blueprints.login.login import login_page
from blueprints.persona.persona import persona_page


app = Flask(__name__)
app.secret_key = '6226bfbe64b9'  # Change this!!

# BluePrints
app.register_blueprint(login_page)
app.register_blueprint(persona_page)

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

# Index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8080)

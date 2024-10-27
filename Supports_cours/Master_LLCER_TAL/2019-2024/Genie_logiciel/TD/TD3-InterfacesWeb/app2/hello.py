from flask import Flask, redirect, url_for, render_template, request, flash
from werkzeug.utils import secure_filename
import os 
from forms import ContactForm

app = Flask(__name__, static_url_path='/static')

# ici on spécifie le nom du dossier
app.config["UPLOAD_FOLDER"] = 'files'
# ici on crée ce dossier
os.makedirs('files', exist_ok='True')


@app.route('/')
def hello_world():
   return "Hello World"

@app.route("/nicolas")
def hello_votre_nom():
   return "hello nicolas"

@app.route("/<name>")
def hello_X(name):
   return f"hello {name}"

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   # si nom est "admin", redirige vers la fonction hello_admin 
   if name =='admin':
      return redirect(url_for('hello_admin'))
   # sinon redirige vers la fonction hello_guest 
   else:
      return redirect(url_for('hello_guest',guest = name))

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)

@app.route('/hello/if/<int:score>')
def hello_if(score):
   return render_template('hello_if.html', marks = score)

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('hello_for.html', result = dict)

@app.route('/request')
def request_name():
    # ici, on accède à la variable name de l'URL.
    # si cette variable n'existe pas, cela retourne None
   name = request.args.get('name')
   return name

@app.route('/student')
def student():
   return render_template('student.html')

@app.route('/result_form',methods = ['POST', 'GET'])
def result_form():
   if request.method == 'POST':
        # ici on récupère la requête sous forme de dictionnaire
      result = request.form
      # on emploie les données de result pour afficher la page result.html
      return render_template("result_form.html",result = result)


@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   
   if request.method == 'POST':
    # erreur le username et password sont différents de admin
      if request.form['username'] != 'admin' or \
         request.form['password'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
        # on flash un message seulement si le login est réussi
         flash('You were successfully logged in')
         flash('OUIIIIIIIIIIIIIIIIIIIIIII')
         return redirect(url_for('index'))
    # que le login réussisse ou non, on retourne le template login.html
   return render_template('login.html', error = error)

@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return 'file uploaded successfully'

@app.route('/success')
def success():

    return "Success !"

@app.route('/contact', methods=["GET", "POST"])
def contact():
   form = ContactForm()
   if form.validate_on_submit():
      print(form.errors)

      return redirect(url_for('success'))

   return render_template('contact.html', form = form)

if __name__ == '__main__':
   
   app.secret_key = 'ddd'

   # app.run()
   # debug = True nous permet de modifier le code et de voir les modifications directement en 
   # rechargeant la page, sans avoir à redémarrer le serveur
   app.run(debug = True)
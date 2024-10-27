from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename
from forms import ContactForm
import json
import os
from getpass import getpass
from mysql.connector import connect, Error


app = Flask(__name__, static_url_path='/static')
app.config["UPLOAD_FOLDER"] = 'files'
os.makedirs('files', exist_ok='True')
# app.config["MAX_CONTENT_PATH"] = 500

# on peut également se connecter à la base en même temps que l'on se connecte au serveur
try:
    # on obtient une variable connection de type MySQLConnection avec laquelle on peut intéragir avec le serveur
    connection = connect(
        host="localhost",
        user = "root",
        password = "L4dy-15-BacK",
        database="mydatabase"
        # user=input("Enter username: "),
        # password=getpass("Enter password: ")
    )
    print(connection)
# gestion de toutes erreurs de connection
except Error as e:
    print(e)


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
         print(request)
        # on flash un message seulement si le login est réussi
         flash('You were successfully logged in')
         return redirect(url_for('index'))
      
    # si le login échoue, on revient à la page de login
   return render_template('login.html', error = error)


@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      # f.save(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
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

@app.route('/request')
def request_name():
   name = request.args.get('name')
   data = request.json

   return data

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


# notez ici le "/", qui indique la racine du chemin, c'est à dire
# la page de base
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# retourne tous les éléments de books
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    # notez l'emploi de jsonify ici au lieu de json.dumps
    # jsonify permet de générer une réponse JSON attendu par
    # le moteur de recherche. json.dump lui ne retourne qu'un
    # dictionnaire
    # ainsi, dans le cadre du dévelopement web, utilisez jsonfify
    # et non pas json.dump
   #  return json.dumps(books)
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Vérifie si le paramètre ID est donné dans l'URL
    # Si oui, l'assigne à une variable, si non retourne
    # une erreur

    # les arguments d'une requêtes commence par un ?
    # situé après le endpoint
    # ici, on verife que id est donné en argument
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Erreurr: Argument ID absent. Merci de donner un argument ID à l'URL"

    # Liste qui contiendra les résultats retournés
    results = []

    # parcours les données jusqu'à obtenir un livre qui a
    # l'id demandé
    for book in books:
        if book['id'] == id:
            results.append(book)
            break

    return jsonify(results)

@app.route('/api/v1/resources/movies/all', methods=['GET'])
def api_movies_all():
    query = 'SELECT * FROM movies'
   # l'argument dictionary=True permet de retourner
   # les résultats de la base de données sous forme
   # de dictionnaire, donc adapté au format JSON
   # il est possible d'utiliser jsonify sur les
   # resultats sous forme de tuples, mais il n'y
   # aura pas le nom des colonnes

   #  with connection.cursor() as cursor:
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/movie', methods=['GET'])
def api_movie():

   query = 'SELECT * FROM movies WHERE'
   to_filter = []

   query_parameters = request.args
   print(query_parameters)

   id = query_parameters.get('id')
   genre = query_parameters.get('genre')
   release_year = query_parameters.get('release_year')
   title = query_parameters.get('title')
   collection_in_mil = query_parameters.get('collection_in_mil')
    
   if id:
      query += ' id=%s AND '
      to_filter.append(id)

   if genre:
      query += ' genre=%s AND '
      to_filter.append(genre)

   if release_year:
      query += ' release_year=%s AND '
      to_filter.append(release_year)

   if title:
      query += ' title=%s AND '
      to_filter.append(title)

   if collection_in_mil:
      query += ' collection_in_mil=%s AND '
      to_filter.append(release_year)

   if not (id and genre and release_year and title and collection_in_mil) :
      return page_not_found(404)

   # l'argument dictionary=True permet de retourner
   # les résultats de la base de données sous forme
   # de dictionnaire, donc adapté au format JSON
   # il est possible d'utiliser jsonify sur les
   # resultats sous forme de tuples, mais il n'y
   # aura pas le nom des colonnes
   query = query[:-4]
   print(query, to_filter)
   #  with connection.cursor() as cursor:
   with connection.cursor(dictionary=True) as cursor:
      cursor.execute(query, to_filter)
      results = cursor.fetchall()

   return jsonify(results)

@app.route('/api/v1/resources/books/create_book', methods=['POST'])
def create_book():
    book = json.loads(request.data)

    books.append(book)

    return jsonify(books)

@app.route('/api/v1/resources/books/update_book', methods=['PUT'])
def update_record():
    updated_book = json.loads(request.data)

    update_index = 0
    for i, r in enumerate(books):

        if r['title'] == updated_book['title']:
            update_index = i 
    books[update_index].update(updated_book)

    return jsonify(books)

@app.route('/api/v1/resources/books/delete_book', methods=['GET'])
def delete_book():
   id = request.args.get('id')
   print('id', id)
   delete_index = 0
   for i, r in enumerate(books):
      if r['id'] == int(id):
         delete_index = i

   print(i)
   del books[delete_index]

   return jsonify(books)


if __name__ == '__main__':
   
    # app.run()
   # debug = True nous permet de modifier le code et de voir les modifications directement en 
   # rechargeant la page, sans avoir à redémarrer le serveur
   # app.config['SESSION_TYPE'] = 'filesystem'
   app.secret_key = 'ddd'

   app.run(debug = True)
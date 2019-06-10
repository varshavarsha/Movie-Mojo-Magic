from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_movies
import created_movie
import pickle 
from sklearn.preprocessing import StandardScaler 
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Create an instance of our Flask app.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# app.config["MONGO_URI"] = "mongodb://localhost:27017/movie_app"
# mongo = PyMongo(app)
# client = MongoClient(f"mongodb+srv://varsha:{os.environ.get('atlaspw')}@cluster0-0rjut.mongodb.net/test?retryWrites=true&w=majority")
client = MongoClient("mongodb+srv://varsha:varshapassword@cluster0-0rjut.mongodb.net/test?retryWrites=true&w=majority")
db = client.movie_app

loaded_model = pickle.load(open("finalized_model.pkl", "rb"))
loaded_model2 = pickle.load(open("finalized_model2.pkl", "rb"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set route
@app.route('/')
def index():
   movies_data = db.newmovies.find()
   # print(movies_data)
   return render_template('index.html', movies_data = movies_data)

@app.route('/create_movie')
def create_movie():
   directors = db.directors.find()
   actors = db.actors.find()
   return render_template('create_movie.html', directors = directors, actors = actors)

@app.route('/predict')
def scrape_mongo():
   movies_data = db.newmovies
   movies_scraped = scrape_movies.scrape()
   movies_scraped = movies_scraped.fillna("")
   features = movies_scraped[["Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western", "Title Compound Sentiment"]]
   features_scaler = StandardScaler().fit(features)
   features_scaled = features_scaler.transform(features)
   predictions = loaded_model.predict(features_scaled)
   movies_scraped["Predictions"] = predictions
   print(predictions)
   movies_dict = []
   for movie in movies_scraped.itertuples():
      movies_dict.append({
         "movieTitles" : movie[1],
         "runtimes" : movie[2],
         "genres" : movie[3],
         "ratings" : movie[4],
         "metascores" : movie[5],
         "plots" : movie[6],
         "actors" : movie[7],
         "directors" : movie[8],
         "posters" : movie[9],
         "predictions" : movie[-1]
         })
   movies_data.delete_many({})
   movies_data.insert_many(movies_dict)
   return redirect("/", code=302)
   
@app.route('/create_movie_prediction', methods = ['POST', 'GET'])
def create_movie_prediction():
    if request.method == 'POST':
        print('Incoming..')
        file = request.files['poster']
        title = request.form["title"]
        runtime = request.form["runtime"]
        genre = request.form.getlist("genre")
        director = request.form["director"]
        actor = request.form.getlist("actor")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        features2 = created_movie.process_movie(title, runtime, genre, director, actor, filename)
        features_scaler2 = StandardScaler().fit(features2)
        features_scaled2 = features_scaler2.transform(features2)
        prediction = loaded_model2.predict(features_scaled2)
        print(prediction)
        os.remove(f"uploads/{filename}")
        return jsonify({'Prediction':int(prediction[0])}) 

    # GET request
    else:
        message = {'Error':'Data Missing?'}
        return jsonify(message)  # serialize and use JSON headers
   
if __name__ == "__main__":
    app.run(debug=True)
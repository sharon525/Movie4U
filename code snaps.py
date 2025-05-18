    
    # part of the html code for giving a rating
    <tbody>
      {% for movie in movi %}
      <td> {{movie.movieId}} </td>
      <td> {{movie.title}} </td>
      <td> {{movie.overview}} </td>
      <td>
        <div>
          <form method="POST" action="{{url_for('rate_movie')}}">
            <ula class="rate-area">
              <input type="radio" id="{{movie}}5-star" name="rating" value="5" />
              <label for="{{movie}}5-star" title="Amazing">5 stars</label>
              <input type="radio" id="{{movie}}4-star" name="rating" value="4" />
              <label for="{{movie}}4-star" title="Good">4 stars</label>
              <input type="radio" id="{{movie}}3-star" name="rating" value="3" />
              <label for="{{movie}}3-star" title="Average">3 stars</label>
              <input type="radio" id="{{movie}}2-star" name="rating" value="2" />
              <label for="{{movie}}2-star" title="Not Good">2 stars</label>
              <input type="radio" id="{{movie}}1-star" name="rating" value="1" />
              <label for="{{movie}}1-star" title="Bad">1 star</label>
            </ula>
            <br><br>
            <br />
            <div class="form-group">
              <label for="movieId"></label>
              <input
              
              type="text"
              class="form-control"
              id="movieId"
              name="movieId"
              placeholder="enter movieId"
              
              />
              <br>
              <br><button type="submit" class="btn btn-primary">Submit</button>
            </div>
            <br>
            
          </td>
        </form>
      </div>
    </td>
  </tr>
  {% endfor %}
  </tbody>
-----------------

# the models of the database

from flask_login import UserMixin
from project import db , login_manager

@login_manager.user_loader
def load_user(userId):
    return Users.query.get(int(userId))

class Ratings(db.Model):
    movieId = db.Column(db.Integer,db.ForeignKey('movies.movieId'),primary_key=True)
    rating = db.Column(db.Float)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'),primary_key=True)
    userate = db.relationship('Users')
    movierate = db.relationship('Movies')

class Users(db.Model, UserMixin):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    rates = db.relationship('Ratings')
    def get_id(self):
        return (self.userId)


class Movies(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    genres = db.Column(db.Text)
    year = db.Column(db.Text)
    budget = db.Column(db.Integer())
    language = db.Column(db.String(10))
    overview = db.Column(db.Text)
    runtime = db.Column(db.Integer())
    tagline = db.Column(db.Text)



# the register route

@app.route('/register', methods=['GET', 'POST'])
def register():
    import sqlite3
    import pandas as pd
    con = sqlite3.connect("path/to/your/database.db")
    cur = con.cursor()
    users = pd.read_sql_query('select * from users', con)

    form = Register()
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if username == Users:
            flash('username already exist', category='error')
        elif len(username) < 4:
            flash('username must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords dont match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            newusers = Users(username=form.username.data,
                             first_name=form.first_name.data,
                             password=form.password1.data)

            db.session.add(newusers)
            db.session.commit()

            return redirect(url_for('home'))

    return render_template("register.html", form=form)

#the search result logic

@app.route('/resultspage' , methods = ['GET' , 'POST'])
@login_required
def results():
    movies = conn.execute('''select a.movieId  as movieId, a.title as title,a.overview as overview, b.rating as rating from(
                         SELECT m.movieId , m.title ,m.overview from Movies m  
                         where m.title like :moviename )as a
                         LEFT join (
                         select r.movieId , r.rating from Ratings r
                         where r.userId == :user )as b 
                         on a. movieId = b.movieId ''', dict (moviename = moviename , user = user))
    

    movies = pd.DataFrame(movies)
    movies.columns = ['movieId' , 'title','overview','rating']
    engine = create_engine('sqlite:///result.db', echo=True)
    movies = movies.to_sql('result', con=engine, if_exists='replace', index=False)
    movies = engine.execute('select * from result')
    return render_template('resultspage.html', movies = movies )


# User Similarity Calculation and Recommendation Generation:

con = sqlite3.connect("path/to/your/database.db")  # Placeholder for actual database path
cur = con.cursor()

# Fetch data from database (ensure data is generic)
ratings = pd.read_sql_query('SELECT * FROM ratings', con)  
movies = pd.read_sql_query('SELECT * FROM movies ', con)  

# Merge ratings with movies based on movieId
dataframes = pd.merge(ratings, movies, on='movieId', how='inner')
del dataframes['movieId']  # Drop 'movieId' column for simplicity

# Create the user-item matrix
matr = dataframes.pivot_table(index='userId', columns='title', values='rating')

# Calculate cosine similarity between users
cosim3 = cosine_similarity(matr.fillna(0))
sim = pd.DataFrame(cosim3, index=matr.index, columns=matr.index)


# Drop the selected user to avoid self-similarity
cleansort = simsort.drop(index=select_user, inplace=False)


# Retrieve the movies watched by the target user
userid_watched = matr[matr.index == select_user].dropna(axis=1, how='all')

# Get the movies watched by similar users
similar_movies = matr[matr.index.isin(a.index)].dropna(axis=1, how='all')
similar_movies.drop(userid_watched.columns, axis=1, inplace=True, errors='ignore')

# Calculate the average rating of similar movies
totalrate = similar_movies.mean(axis=0)
totalrate = pd.DataFrame(totalrate).set_axis(["score"], axis=1)

# Merge with movie details (overview, title, etc.)
totalrate = pd.merge(totalrate, movies, on='title', how='outer')
totalrate = totalrate.sort_values(by='score', ascending=False)

# Get the top 5 most recommended movies
mostrecommended = totalrate[['movieId', 'title', 'overview']].head(5)

# Save recommendations to a mock database ()
engine = create_engine('sqlite:///mock_similar.db', echo=True)
movi = mostrecommended
movi.to_sql('simillar', con=engine, if_exists='replace', index=False)

# Fetch recommendations and render template
movi = engine.execute('SELECT * FROM simillar')
return render_template('home.html', movi=movi)
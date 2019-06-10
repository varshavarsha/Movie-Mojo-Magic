# Movie-Mojo-Magic

# Initial Scraping
My project involved scraping data using Pandas from the site Box Office Mojo for information about what movies were released on a monthly basis since 1982. I also scraped data regarding the actors and directors from the same site. Afterwards, I used the OMDB API to acquire more information about all of the movies I scraped data for. 

Here are the sites that I scraped from:

https://www.boxofficemojo.com/monthly/?view=releasedate&chart=&month=3&yr=2019

https://www.boxofficemojo.com/people/

https://www.boxofficemojo.com/people/?view=Director&p=.htm

Here is the API that I used:

http://www.omdbapi.com/

Once the data was acquired, I started cleaning it by finding any mismatched movies from making the API requests and dropped their rows from the dataframe. At this point in the project, I had columns that listed the actors and director for each movie. I was able to calculate the average total gross, average number of movies, and average number one picture gross for all of the actors in a movie using the initial actors data that I scraped. I also made sure merge the total gross, number of movies, and number one picture gross information for all of the directors in each movie.

Additionally, I decided to do some image processing on the movie poster and text processing on the movie title. I was eventually able to find out what the most dominant colors of the movie posters were and assigned them to color categories and figured out how positive, negative, or neutral the movie titles were. 

These are the following sites where I learned how to conduct the image processing and sentiment analysis:

http://ahmedhosny.github.io/theGreenCanvas/

https://github.com/cjhutto/vaderSentiment

I did some final cleaning of the dataset by converting the datatypes of certain values and made sure that all of the categorical data I wanted to use for machine learning such as genre and movie poster color was flattened. I started out with a plethora of features, however, I ended up much fewer after controlling for multicollinearity and conducting backwards elimination. In my final model, I only used the columns 'Runtime in Min', 'Action', 'Animation', 'Biography', 'Documentary', 'Drama','History', 'Horror', 'Romance', 'Sci-Fi', 'Short','Director Best Picture Gross', 'Black', 'White', 'Gray', 'Red', 'Yellow','Green', 'Cyan', and 'Blue.' I decided to use logistic regression to predict whether a movie will have at least an 8/10 IMDB Rating, and I was able to predict it with around a 90% accuracy.

# Application

I then decided to start building an application that would be able to scrape data using splinter and beatiful soup from the site https://www.imdb.com/movies-coming-soon/ and predict using my machine learning model which of the movies will end up with IMDB ratings of at least 7.5. I also added a section where you can create your own movie to see if it will be predicted to have an IMDB rating of at least 7.5. Try it out at the website below!

# https://movie-mojo-magic.herokuapp.com/



from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from PIL import Image
import urllib.request
import colorsys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def scrape(): 
    browser = Browser('chrome', headless=True)

    movies_url = 'https://www.imdb.com/movies-coming-soon/'
    browser.visit(movies_url)
    # time.sleep(1)
    movies_html = browser.html
    soup = BeautifulSoup(movies_html, 'html.parser')

    posters = soup.find_all('img', class_ = 'poster shadowed')
    poster_url = [poster["src"] for poster in posters]

    movies_info = soup.find_all("td", class_ = "overview-top")

    movie_titles = []
    runtimes = []
    genres = []
    ratings = []
    metascores = []
    plots = []
    actors = []
    directors = []

    for movie in movies_info:
        movie_title = movie.find("a").text.split('(')[0].strip()
        if movie_title:
            movie_titles.append(movie_title)
        else:
            movie_titles.append(float('nan'))
            
        runtime = movie.find("p", class_ = "cert-runtime-genre").find("time")
        if runtime:
            runtimes.append(runtime.text.strip(" min"))
        else:
            runtimes.append(float('nan'))
        
        genre = movie.find("p", class_ = "cert-runtime-genre").find_all("span", class_=None)
        if genre: 
            genres.append([g.text for g in genre])
        else:
            genres.append(float('nan'))
        
        rating = movie.find("p", class_ = "cert-runtime-genre").find("img")
        if rating:
            ratings.append(rating["title"])
        else:
            ratings.append(float('nan'))
            
        metascore = movie.find("span", class_ = "metascore")
        if metascore:
            metascores.append(metascore.text)
        else:
            metascores.append(float('nan'))
            
        plot = movie.find("div", class_ = "outline").text
        if plot:
            plots.append(plot)
        else:
            plots.append(float('nan'))
            
        director = movie.find_all("div", class_ = "txt-block")[0].find("a").text
        if director:
            directors.append(director)
        else:
            directors.append(float('nan'))

        actor = movie.find_all("div", class_ = "txt-block")[1].find_all("a")
        if actor:
            actors.append([a.text for a in actor])
        else:
            actors.append(float('nan'))
    
    movie_dict = {'Movie Title': movie_titles, 'Runtime': runtimes, 'Genre': genres, 'Rated': ratings, "Metascore": metascores, 
              "Plot" : plots, "Actors" : actors, "Director" : directors, "Poster" : poster_url}  
    
    movie_df = pd.DataFrame(movie_dict)
    
#     actors_df = pd.read_csv("dbs/Actors_Data.csv")

#     for row in movie_df.itertuples():
#         counter_tg = 0
#         counter_nm = 0
#         counter_g = 0
#         counter_a = 0
        
#         try:
            
# #             print(actors_df.loc[actors_df["Person"] == row[18][0], "Total Gross"].item())
#             actor_one_tg = actors_df.loc[actors_df["Person"] == row[7][0], "Total Gross"].item()
#             actor_one_nm = actors_df.loc[actors_df["Person"] == row[7][0], "Number of Movies"].item()
#             actor_one_g = actors_df.loc[actors_df["Person"] == row[7][0], "Gross"].item()
            
#             counter_tg = counter_tg + actor_one_tg
#             counter_nm = counter_nm + actor_one_nm
#             counter_g = counter_g + actor_one_g
#             counter_a = counter_a + 1

#         except:
#             pass
        
#         try:
# #             print(actors_df.loc[actors_df["Person"] == row[18][1], "Total Gross"].item())
#             actor_two_tg = actors_df.loc[actors_df["Person"] == row[7][1], "Total Gross"].item()
#             actor_two_nm = actors_df.loc[actors_df["Person"] == row[7][1], "Number of Movies"].item()
#             actor_two_g = actors_df.loc[actors_df["Person"] == row[7][1], "Gross"].item()
            
#             counter_tg = counter_tg + actor_two_tg
#             counter_nm = counter_nm + actor_two_nm
#             counter_g = counter_g + actor_two_g
#             counter_a = counter_a + 1
            
#         except:
#             pass
        
#         try:
# #             print(actors_df.loc[actors_df["Person"] == row[18][2], "Total Gross"].item())
#             actor_three_tg = actors_df.loc[actors_df["Person"] == row[7][2], "Total Gross"].item()
#             actor_three_nm = actors_df.loc[actors_df["Person"] == row[7][2], "Number of Movies"].item()
#             actor_three_g = actors_df.loc[actors_df["Person"] == row[7][2], "Gross"].item()
            
#             counter_tg = counter_tg + actor_three_tg
#             counter_nm = counter_nm + actor_three_nm
#             counter_g = counter_g + actor_three_g
#             counter_a = counter_a + 1
            
#         except:
#             pass
        
#         try:
# #             print(actors_df.loc[actors_df["Person"] == row[18][3], "Total Gross"].item())
#             actor_four_tg = actors_df.loc[actors_df["Person"] == row[7][3], "Total Gross"].item()
#             actor_four_nm = actors_df.loc[actors_df["Person"] == row[7][3], "Number of Movies"].item()
#             actor_four_g = actors_df.loc[actors_df["Person"] == row[7][3], "Gross"].item()
            
#             counter_tg = counter_tg + actor_four_tg
#             counter_nm = counter_nm + actor_four_nm
#             counter_g = counter_g + actor_four_g
#             counter_a = counter_a + 1
           
#         except:
#             pass
       
#         if counter_tg != 0:
#             movie_df.at[row.Index, "Actors Avg Total Gross"] = counter_tg/ counter_a
#             movie_df.at[row.Index, "Actors Avg Number of Movies"] = counter_nm/ counter_a
#             movie_df.at[row.Index, "Actors Avg Best Picture Gross"] = counter_g/ counter_a

    # directors_df = pd.read_csv("dbs/directors.csv")

    # movie_df = movie_df.merge(directors_df[['Total_Gross','No_Of_Movies', 'BestPic_Gross','DirectorName']], left_on='Director', right_on='DirectorName', how='left')
    # movie_df = movie_df.rename(columns={"Total_Gross": "Director Total Gross", "No_Of_Movies": "Director Number of Movies", "BestPic_Gross" : "Director Best Picture Gross" }).drop(columns=['DirectorName'])
    
    genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western"]    
    
    for movie in movie_df.itertuples():
        try:
            for genre in genres:
                if genre in movie[3]:
                    movie_df.at[movie.Index, genre] = 1
                else: 
                    movie_df.at[movie.Index, genre] = 0
        except:
            pass
    
    # def most_frequent_colour(url):
    
    #     try:                                           
    #         resp = urllib.request.urlopen(url)
    #         image = Image.open(resp)
    #         w, h = image.size
    #         pixels = image.getcolors(w * h)

    #         most_frequent_pixel = pixels[0]

    #         for count, colour in pixels:
    #             if count > most_frequent_pixel[0]:
    #                 most_frequent_pixel = (count, colour)
    #         peak = most_frequent_pixel[1]

    #         HLS = colorsys.rgb_to_hls(peak[0]/255.0,peak[1]/255.0,peak[2]/255.0)

    #         hueAngle = HLS[0]*360

    #         # Lightness
    #         if (HLS[1] < 0.2):
    #             myDominantColor = "Black"
    #         elif (HLS[1] > 0.8):
    #             myDominantColor = "White"
    #         # saturation
    #         elif (HLS[2] < 0.25):
    #             myDominantColor = "Gray"
    #         # hue
    #         elif (hueAngle < 30):
    #             myDominantColor = "Red"
    #         elif (hueAngle < 90):
    #             myDominantColor = "Yellow"
    #         elif (hueAngle < 150):
    #             myDominantColor = "Green"
    #         elif (hueAngle < 210):
    #             myDominantColor = "Cyan"
    #         elif (hueAngle < 270):
    #             myDominantColor = "Blue"
    #         elif (hueAngle < 330):
    #             myDominantColor = "Magenta"
    #         else:
    #             myDominantColor = "Red"

    #         return myDominantColor
        
    #     except:
    #         return float('nan')

    # movie_df['Poster Color'] = movie_df["Poster"].apply(most_frequent_colour)
    
    # colors = ["Black", "White", "Gray", "Red", "Yellow", "Green", 
    #         "Cyan", "Blue", "Magenta"]    
    
    # for poster in movie_df.itertuples():
    #         if pd.notna(poster[40]):
    #             for color in colors:
    #                 if color == poster[40]:
    #                     movie_df.at[poster.Index, color] = 1
    #                 else: 
    #                     movie_df.at[poster.Index, color] = 0
        
    #         else:
    #             movie_df.at[poster.Index, color] = float("nan")
    movie_titles = movie_df["Movie Title"].tolist()
    movie_titles

    analyzer = SentimentIntensityAnalyzer()
    vs_list = [analyzer.polarity_scores(title) for title in movie_titles]

    movie_df["Title Negative Sentiment"] = [vs["neg"] for vs in vs_list]
    movie_df["Title Neutral Sentiment"] = [vs["neu"] for vs in vs_list]
    movie_df["Title Positive Sentiment"] = [vs["pos"] for vs in vs_list]
    movie_df["Title Compound Sentiment"] = [vs["compound"] for vs in vs_list]

    
    movie_df = movie_df.rename(columns={"Runtime":'Runtime in Min'})

    movie_df["Metascore"] = movie_df["Metascore"].astype(float)
    movie_df["Runtime in Min"] = movie_df["Runtime in Min"].astype(float)
    movie_df["Plot"] = movie_df["Plot"].str.strip("\n").str.strip()
    
    movie_df = movie_df.dropna(subset = ["Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western","Title Compound Sentiment"])
    
    movie_df = movie_df.reset_index(drop=True)
    
    # print(movie_df.columns)

    return movie_df



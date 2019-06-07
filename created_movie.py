import pandas as pd
import numpy as np
from PIL import Image
import urllib.request
import colorsys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def process_movie(title, runtime, genre, director, actor, filename): 

    print(title)
    print(runtime)
    print(genre)
    print(director)
    print(actor)
   
    
    create_movie_dict = {'Movie Title': title, 'Runtime': runtime, 'Genre': [genre], 
              "Actors" : [actor], "Director" : director}  
    
    create_movie_df = pd.DataFrame(create_movie_dict)
    
    actors_df = pd.read_csv("dbs/Actors_Data.csv")


    counter_tg = 0
    counter_nm = 0
    counter_g = 0
    counter_a = 0



    try:

    #     print(actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][0], "Total Gross"].item())
        actor_one_tg = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][0], "Total Gross"].item()
        actor_one_nm = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][0], "Number of Movies"].item()
        actor_one_g = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][0], "Gross"].item()

        counter_tg = counter_tg + actor_one_tg
        counter_nm = counter_nm + actor_one_nm
        counter_g = counter_g + actor_one_g
        counter_a = counter_a + 1

    except:
        pass

    try:
    #     print(actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][1], "Total Gross"].item())
        actor_two_tg = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][1], "Total Gross"].item()
        actor_two_nm = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][1], "Number of Movies"].item()
        actor_two_g = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][1], "Gross"].item()

        counter_tg = counter_tg + actor_two_tg
        counter_nm = counter_nm + actor_two_nm
        counter_g = counter_g + actor_two_g
        counter_a = counter_a + 1

    except:
        pass

    try:
    #     print(actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][2], "Total Gross"].item())
        actor_three_tg = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][2], "Total Gross"].item()
        actor_three_nm = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][2], "Number of Movies"].item()
        actor_three_g = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][2], "Gross"].item()

        counter_tg = counter_tg + actor_three_tg
        counter_nm = counter_nm + actor_three_nm
        counter_g = counter_g + actor_three_g
        counter_a = counter_a + 1

    except:
        pass

    try:
    #     print(actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][3], "Total Gross"].item())
        actor_four_tg = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][3], "Total Gross"].item()
        actor_four_nm = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][3], "Number of Movies"].item()
        actor_four_g = actors_df.loc[actors_df["Person"] == create_movie_df["Actors"][0][3], "Gross"].item()

        counter_tg = counter_tg + actor_four_tg
        counter_nm = counter_nm + actor_four_nm
        counter_g = counter_g + actor_four_g
        counter_a = counter_a + 1

    except:
        pass

    if counter_tg != 0:
        create_movie_df["Actors Avg Total Gross"] = counter_tg/ counter_a
        create_movie_df["Actors Avg Number of Movies"] = counter_nm/ counter_a
        create_movie_df["Actors Avg Best Picture Gross"] = counter_g/ counter_a
        

    directors_df = pd.read_csv("dbs/directors.csv")

    create_movie_df = create_movie_df.merge(directors_df[['Total_Gross','No_Of_Movies', 'BestPic_Gross','DirectorName']], left_on='Director', right_on='DirectorName', how='left')
    create_movie_df = create_movie_df.rename(columns={"Total_Gross": "Director Total Gross", "No_Of_Movies": "Director Number of Movies", "BestPic_Gross" : "Director Best Picture Gross" }).drop(columns=['DirectorName'])
    
    genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western"]    
    


    for genre in genres:
        if genre in create_movie_df["Genre"][0]:
            create_movie_df[genre] = 1
        else: 
            create_movie_df[genre] = 0

    print(create_movie_df)
    print(filename)

    def most_frequent_colour(filename):
                            
        image = Image.open(f"uploads/{filename}")
        w, h = image.size
        pixels = image.getcolors(w * h)

        most_frequent_pixel = pixels[0]

        for count, colour in pixels:
            if count > most_frequent_pixel[0]:
                most_frequent_pixel = (count, colour)
        peak = most_frequent_pixel[1]

        HLS = colorsys.rgb_to_hls(peak[0]/255.0,peak[1]/255.0,peak[2]/255.0)

        hueAngle = HLS[0]*360

        # Lightness
        if (HLS[1] < 0.2):
            myDominantColor = "Black"
        elif (HLS[1] > 0.8):
            myDominantColor = "White"
        # saturation
        elif (HLS[2] < 0.25):
            myDominantColor = "Gray"
        # hue
        elif (hueAngle < 30):
            myDominantColor = "Red"
        elif (hueAngle < 90):
            myDominantColor = "Yellow"
        elif (hueAngle < 150):
            myDominantColor = "Green"
        elif (hueAngle < 210):
            myDominantColor = "Cyan"
        elif (hueAngle < 270):
            myDominantColor = "Blue"
        elif (hueAngle < 330):
            myDominantColor = "Magenta"
        else:
            myDominantColor = "Red"

        return myDominantColor
        


    create_movie_df['Poster Color'] = most_frequent_colour(filename)
    print(create_movie_df['Poster Color'])
    
    colors = ["Black", "White", "Gray", "Red", "Yellow", "Green", 
            "Cyan", "Blue", "Magenta"]    
 
    for color in colors:
        if color == create_movie_df['Poster Color'][0]:
            create_movie_df[color] = 1
        else: 
            create_movie_df[color] = 0

    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(create_movie_df["Movie Title"][0]) 

    create_movie_df["Title Negative Sentiment"] = vs["neg"]
    create_movie_df["Title Neutral Sentiment"] = vs["neu"] 
    create_movie_df["Title Positive Sentiment"] = vs["pos"]
    create_movie_df["Title Compound Sentiment"] = vs["compound"] 

    
    create_movie_df = create_movie_df.rename(columns={"Runtime":'Runtime in Min'})
    create_movie_df["Runtime in Min"] = create_movie_df["Runtime in Min"].astype(float)

    create_movie_df = create_movie_df[["Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western", "Actors Avg Total Gross", "Actors Avg Number of Movies", 
            "Actors Avg Best Picture Gross", "Director Total Gross", "Director Number of Movies", 
            "Director Best Picture Gross","Title Compound Sentiment"]]
    
    # print(movie_df.columns)

    return create_movie_df




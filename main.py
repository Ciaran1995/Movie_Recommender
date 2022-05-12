import pandas as pd
import tkinter as tk
import numpy as np
import random as rand
from difflib import SequenceMatcher



def create_new_count_table(n):
    from os.path import exists

    if exists('movie_ratings_count_over_' + str(n) + '.csv'):
        print('File: movie_ratings_count_over_' + str(n) + '.csv already exists')
        return

    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')

    movie_ratings = pd.merge(ratings, movies)
    num_ratings = movie_ratings['title'].value_counts()

    movie_ratings['num_ratings'] = num_ratings[movie_ratings['title']].values

    new_movie_count = movie_ratings[movie_ratings['num_ratings'] >= n]
    new_movie_count.to_csv('movie_ratings_count_over_' + str(n) + '.csv', index=False)


min_rating_count = 1000
movie_ratings_data = pd.read_csv(f'movie_ratings_count_over_' + str(min_rating_count) + '.csv')
num_ratings_data = movie_ratings_data['title'].value_counts()

#movie_ratings_data = pd.read_csv('movies_100k.csv')
#num_ratings_data = movie_ratings_data['title'].value_counts()

ratings_matrix = movie_ratings_data.pivot_table(index='userId', columns='title', values='rating')


def most_like(st1, list1):
    likeness = [SequenceMatcher(None, st1, i).ratio() for i in list1]
    max_index = likeness.index(max(likeness))

    if likeness[max_index] >= 0.5:
        return list1[max_index]
    else:
        return "This Movie Doesn't Seem To Be In Our List :("

def recommend():
    warning_label.config(text='')
    if movie_entry.get() in movie_ratings_data['title'].values:
        my_movie_ratings = ratings_matrix[movie_entry.get()]
        corr_ratings = ratings_matrix.corrwith(my_movie_ratings).dropna().sort_values(ascending=False)

        s = [num_ratings_data.loc[i] for i in corr_ratings.keys()]
        alt_corr_ratings = (corr_ratings*s).sort_values(ascending=False)

        recommendations = alt_corr_ratings/alt_corr_ratings.max()

        # Below will recommend a random movie from the top 5 (or the top) recommendations
        # calculated for the entered movie
        recommend_label.config(text='Recommendation: '
                                    + rand.choice((recommendations.drop(index=movie_entry.get())).keys()[0:4]))
        # recommend_label.config(text='Recommendation: ' + recommendations.keys()[0])

        # Could add a check for if the movie entered only has a small number of ratings, in which case good
        # recommendations may be difficult. This isn't needed for the refined data sets.
        if num_ratings_data.loc[movie_entry.get()] < 30:
            warning_label.config(text='Warning: ' + movie_entry.get()
                                      + ' may not be enough ratings for a good recommendation')

    else:
        recommend_label.config(text='This entry does not match any movie in the database \n Did you mean: '
                                    + most_like(movie_entry.get(), movie_ratings_data['title'].unique()))

# ------------------ GUI ----------------------
win = tk.Tk()
win.title("Movie Recommender")
win.geometry("600x200")
win.config(padx=60, pady=10)


app_label2 = tk.Label(win, text="🎥 Please Enter a Movie You Like 🎥", font=("Ariel", 24))
app_label2.grid(row=0, column=1)


blank_label = tk.Label(win, text=" ")
blank_label.grid(row=1, column=1)

movie_entry = tk.Entry(win, text='e.g. Jumanji (1995)', justify='center')
movie_entry.grid(row=2, column=1)

blank_label = tk.Label(win, text=" ")
blank_label.grid(row=4, column=1)

recommend_label = tk.Label(win, text="")
recommend_label.grid(row=5, column=1)

warning_label = tk.Label(win, text="")
warning_label.grid(row=6, column=1)

start_button = tk.Button(text='Find Recommendation', command=recommend, highlightthickness=0, anchor='center')
start_button.grid(row=3, column=1)


win.mainloop()

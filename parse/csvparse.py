__author__ = 'zachbai'

import csv
import numpy as np
import re

DATA = "allmovies.csv"
OUTPUT = "movies.csv"

file = open(DATA)
movie_data = csv.reader(file)

matrix = np.array(["title", "budget", "genre", "mpaa", "runtimes", "rating",  "gross"])

b_count, g_count, gr_count, ra_count, ru_count, i_count = (0,)*6
old_movie = ""
movie = np.zeros([7], dtype="S100")
def update_mat(src, trg, cat, cat_ind, count=0, max_count=1):
    if src[2] in cat and count < max_count:
        trg[cat_ind] = src[3]
    return count + 1
#end update_mat

genre_map = dict(zip(["", "Documentary", "Horror", "Short", "Drama", "Comedy",
                             "Mystery", "Sport", "Sci-Fi","Romance", "Family", "Biography",
                             "Music", "Adventure", "Crime", "War", "Musical", "Fantasy",
                             "Thriller", "Animation", "Action", "History", "Western", "Adult",
                             "Film-Noir", "Experimental", "Erotica", "News",
                             "Reality-TV", "Game-Show", "Talk-Show", "Lifestyle","Commercial"], range(33)))
rating_map = dict(zip(["", "G", "PG", "PG-13", "R", "NC-17"], range(6)))
rating_map["PG-"] = 3

for row in movie_data:
    if old_movie != row[0]:
        if b_count == 1 and g_count == 1 and ra_count == 1 and ru_count == 1 and gr_count == 1:
            matrix = np.vstack((matrix,movie))
        old_movie = row[0]
        movie = np.zeros([7], dtype="S100")
        b_count, g_count, gr_count, ra_count, ru_count = (0,)*5
        movie[0] = row[1]
        movie[5] = row[4]
    if row[2] == "budget" and b_count < 1:
        movie[1] = re.sub('\D', "", row[3])
        b_count += 1
    if row[2] == "genres" and g_count < 1:
        movie[2] = genre_map[row[3]]
        g_count += 1
    if row[2] == "mpaa" and ra_count < 1:
        rating = re.match("Rated (.*) for (.*)", row[3])
        if rating != None:
            movie[3] = rating_map[rating.group(1).split()[0]]
        else:
            rating = re.match('rated (.*) for (.*)', row[3])
            if rating != None:
                movie[3] = rating_map[rating.group(1).split()[0]]
            else:
                rating = re.match('(.*) PG-13 for (.*)', row[3])
                if rating != None:
                    movie[3] = rating_map["PG-13"]
                else:
                    rating = re.match('ated (.*) for (.*)', row[3])
                    if rating != None:
                        movie[3] = rating_map["R"]
                    else:
                        rating = re.match('(.*) for (.*)', row[3])
                        if rating != None:
                            movie[3] = rating_map[rating.group(1)]
                        else:
                            movie[3] = rating_map[row[3].split()[1]]
        print movie[3]
        ra_count += 1
    if row[2] == "runtimes" and ru_count < 1:
        movie[4] = re.sub('\D', "", row[3])
        ru_count += 1
    if row[2] == "gross" and gr_count < 1:
        movie[6] = re.sub('\D', "", row[3])
        gr_count += 1




np.savetxt(OUTPUT,matrix, delimiter=",", fmt='"%s"' )

file.close()
__author__ = 'zachbai'

import csv
import numpy as np

CAST_DATA = "3movies.csv"
MOVIE_DATA= "3movies2.csv"
OUTPUT_DATA = "three_movies.csv"

cast_data = open(CAST_DATA)
cast_data_csv = csv.reader(cast_data)
movie_data = open(MOVIE_DATA)
movie_data_csv = csv.reader(movie_data)

matrix = np.array(["ti", "a1", "a2", "a3", "a4", "ci", "co",
                   "di", "ed", "p1", "p2", "p3", "p4", "p5",
                   "wr", "ru", "ds", "ra", "bu"])

a_count, ci_count, co_count, d_count, ed_count, p_count, wr_count = (0,)*7
old_movie = ""
double_prevent = False



def update_feat(src, trg, cat, cat_ind):
    if src[2] == cat: trg[cat_ind] = src[3]

for row1 in cast_data_csv:
    movie_id = row1[0]
    if row1[0] != old_movie:
        double_prevent = False
        a_count, d_count, ci_count, co_count, ed_count, p_count, wr_count = (0,)*7
        movie = np.zeros([19], dtype= "S25")
        old_movie = row1[0]
        movie[0] = row1[1]
    a_count = update_cast(row1, movie, ("actor","actress"), 1, a_count, 4)
    ci_count = update_cast(row1, movie, "cinematographer", 5, ci_count)
    co_count = update_cast(row1, movie, "composer", 6, co_count)
    d_count = update_cast(row1, movie, "director", 7, d_count, 1)
    ed_count = update_cast(row1, movie, "editor", 8, ed_count)
    p_count = update_cast(row1, movie, "producer", 9, p_count, 5)
    wr_count = update_cast(row1, movie, "writer", 14, wr_count)
    if wr_count == 1 and double_prevent == False:
        double_prevent = True
        for row2 in movie_data_csv:
            if movie_id == row2[0]:
                update_feat(row2, movie, "runtimes", 15)
                update_feat(row2, movie, "LD label", 16)
                update_feat(row2, movie, "mpaa", 17)
                update_feat(row2, movie, "budget", 18)
            movie_data = open("3movies2.csv")
            movie_data_csv = csv.reader(movie_data)
        matrix = np.vstack((matrix, movie))


np.savetxt(OUTPUT_DATA, matrix, delimiter= ",", fmt='"%s"')

cast_data.close()
movie_data.close()


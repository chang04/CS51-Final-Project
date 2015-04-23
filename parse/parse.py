__author__ = 'zachbai'

import csv
import numpy as np

cast_data = open("3movies1.csv")
cast_data_csv = csv.reader(cast_data)
movie_data = open("3movies2.csv")
movie_data_csv = csv.reader(movie_data)

matrix = np.array(["ti", "a1", "a2", "a3", "a4", "ci", "co",
                   "ed", "p1", "p2", "p3", "p4", "p5", "wr",
                   "ru", "ds", "ra", "bu"])

a_count, ci_count, co_count, ed_count, p_count, wr_count = (0,)*6
old_movie = ""
double_prevent = False

def update_cast(src, trg, role, role_ind, count, max_count=1):
    if src[2] in role and count < max_count:
        trg[role_ind + count] = src[3]
        return (count + 1)
    else: return count

def update_feat(src, trg, cat, cat_ind):
    if src[2] == cat: trg[cat_ind] = src[3]

for row1 in cast_data_csv:
    movie_id = row1[0]
    if row1[0] != old_movie:
        double_prevent = False
        a_count, ci_count, co_count, ed_count, p_count, wr_count = (0,)*6
        movie = np.zeros([18], dtype= "S25")
        old_movie = row1[0]
        movie[0] = row1[1]
    a_count = update_cast(row1, movie, ("actor","actress"), 1, a_count, 4)
    ci_count = update_cast(row1, movie, "cinematographer", 5, ci_count)
    co_count = update_cast(row1, movie, "composer", 6, co_count)
    ed_count = update_cast(row1, movie, "editor", 7, ed_count)
    p_count = update_cast(row1, movie, "producer", 8, p_count, 5)
    wr_count = update_cast(row1, movie, "writer", 13, wr_count)
    if wr_count == 1 and double_prevent == False:
        double_prevent = True
        for row2 in movie_data_csv:
            if movie_id == row2[0]:
                update_feat(row2, movie, "runtimes", 14)
                update_feat(row2, movie, "LD label", 15)
                update_feat(row2, movie, "mpaa", 16)
                update_feat(row2, movie, "budget", 17)
            movie_data = open("3movies2.csv")
            movie_data_csv = csv.reader(movie_data)
        matrix = np.vstack((matrix, movie))


np.savetxt("three_movies.csv", matrix, delimiter= ",", fmt='"%s"')

cast_data.close()
movie_data.close()


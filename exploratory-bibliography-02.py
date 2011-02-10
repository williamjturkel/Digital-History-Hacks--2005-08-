# exploratory-bibliography-02.py
#
# wjt
# 23-25 jan 2007
#
# http://digitalhistoryhacks.blogspot.com

import pickle

from_to = pickle.load(open("tempstorage"))

# get the list of original books
original_books = list(set([ row[0] for row in from_to ]))

# get the list of recommended books
recommended_books = [ row[1] for row in from_to ]

# remove any recommended books that are already in our biblio
new_recommended_books = [r for r in recommended_books if r not in original_books]

# count number of times each book is recommended and sort by inverse frequency
recommendation_freq = [new_recommended_books.count(n) for n in new_recommended_books]
recommendation_dictionary = dict(zip(new_recommended_books,recommendation_freq))
recommendations = [(recommendation_dictionary[key], key) for key in recommendation_dictionary]

# sort so most frequently recommended first
recommendations.sort()
recommendations.reverse()

# output suggestions
for r in recommendations:
    print r


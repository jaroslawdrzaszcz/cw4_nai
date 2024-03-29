###############################################################################################
# Movies recommendation - created by Jarosław Drząszcz(s16136) and Przemysław Białczak(s16121)#
###############################################################################################
import argparse
import json
import numpy as np


# Compute the Euclidean distance score between user1 and user2
def euclidean_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


# Compute the Pearson correlation score between user1 and user2
def pearson_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)

    # If there are no common movies between user1 and user2, then the score is 0
    if num_ratings == 0:
        return 0

    # Calculate the sum of ratings of all the common movies
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    # Calculate the sum of squares of ratings of all the common movies
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    # Calculate the sum of products of the ratings of the common movies
    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    # Calculate the Pearson correlation score
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Find users who are similar to the input user')
    parser.add_argument('--user', dest='user', required=True,
            help='Input user')
    return parser


# Finds users in the dataset that are similar to the input user
def find_similar_users(dataset, user, num_users, score_method):
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute Pearson score between input user
    # and all the users in the dataset
    if score_method == pearson_score:
        scores = np.array([[x, pearson_score(dataset, user, x)] for x in dataset if x != user])

    # Compute Euclidean score between input user
    # and all the users in the dataset
    elif score_method == euclidean_score:
        scores = np.array([[x, euclidean_score(dataset, user, x)] for x in dataset if x != user])
    # Sort the scores in decreasing order
    scores_sorted = np.argsort(scores[:, 1])[::-1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted[:num_users]

    return scores[top_users]


def prepare_recommendation(json_data, users):
    # creating list of users with the same movie taste
    users_with_the_same_movie_taste = []
    for item in users:
        users_with_the_same_movie_taste.append(item[0])

    # creating a list of movies rated by users with the same movies taste plus list of user movies
    movies_rated_by_most_similar_critics = []
    users_movies = []
    for key, value in json_data.items():
        if key in users_with_the_same_movie_taste:
            movies_rated_by_most_similar_critics.append(value)
        if key == user:
            users_movies.append(value)

    # converting data
    from collections import ChainMap
    movies_rated_by_most_similar_critics = dict(ChainMap(*movies_rated_by_most_similar_critics))
    users_movies = dict(ChainMap(*users_movies))

    # removing movies rated by USER from movies_rated_by_most_similar_critics
    for i, j in movies_rated_by_most_similar_critics.copy().items():
        for k, v in users_movies.items():
            if i == k:
                movies_rated_by_most_similar_critics.pop(i, j)

    # sorting dict with value
    sorted_movies_rated_by_most_similar_critics = sorted(movies_rated_by_most_similar_critics.items(), key=lambda kv: kv[1])

    print('Movies recommended for ' + user + ':\n')

    for i, j in sorted_movies_rated_by_most_similar_critics[-10:]:
        print(i, j)

    print('\nMovies NOT recommended for ' + user + ':\n')

    for i, j in sorted_movies_rated_by_most_similar_critics[:10]:
        print(i, j)


if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    user = args.user

    ratings_file = 'NAI_2019_2020_ratings.json'

    with open(ratings_file, 'r') as f:
        print(f)
        data = json.loads(f.read())

    print('\nUsers similar to ' + user + ' created using Pearson correlation score:\n')
    pearson_score_similar_users = find_similar_users(data, user, 5, pearson_score)
    print('User\t\t\tSimilarity score')
    print('-'*41)
    for item in pearson_score_similar_users:
        print(item[0], '\t\t', round(float(item[1]), 2))

    print('\n\nPreparing movie recommendation based on Pearson correlation score:\n')
    prepare_recommendation(data, pearson_score_similar_users)

    print('\nUsers similar to ' + user + ' created using Euclidean distance score:\n')
    euclidean_score_similar_users = find_similar_users(data, user, 5, euclidean_score)
    print('User\t\t\tSimilarity score')
    print('-' * 41)
    for item in euclidean_score_similar_users:
        print(item[0], '\t\t', round(float(item[1]), 2))

    print('\n\nPreparing movie recommendation based on Euclidean distance score:\n')
    prepare_recommendation(data, euclidean_score_similar_users)

###############################################################################################
# Movies recommendation - created by Jarosław Drząszcz(s16136) and Przemysław Białczak(s16121)#
###############################################################################################

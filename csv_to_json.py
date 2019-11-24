import csv
import json

if __name__ == '__main__':
    csv_file = open('NAI_2019_2020_ratings_non_pl.csv', 'r', encoding='UTF-8')
    json_file = open('NAI_2019_2020_ratings.json', 'w', encoding='UTF-8')
    data = []

    fieldnames = ("Name", "Group")
    csvReader = csv.DictReader(csv_file, fieldnames)
    for row in csvReader:
        for key in row:
            if key is "Name":
                data.append(row[key])
            if key is "Group":
                break
            else:
                movie = {}
                movies_data = row.__getitem__(None)
                data.append(movies_data)

    name_data = []
    movies_data = []
    for idx, i in enumerate(data):
        if idx % 2 == 0:
            name_data.append(i)
        else:
            movies_data.append(i)

    movies_dict_data = []
    for one_person_movies in movies_data:
        movies = []
        scores = []
        for idx, i in enumerate(one_person_movies):
            if idx % 2 == 0:
                movies.append(i)
            else:
                scores.append(int(i))
        zipped_person_movies = zip(movies, scores)
        one_person_movies_dict = dict(zipped_person_movies)
        movies_dict_data.append(one_person_movies_dict)

    zipped_data = zip(name_data, movies_dict_data)
    data_dict = dict(zipped_data)

    json.dump(data_dict, json_file, indent=4)

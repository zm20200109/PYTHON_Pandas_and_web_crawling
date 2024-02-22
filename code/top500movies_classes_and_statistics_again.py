from sys import stderr
class Movie:

    def __init__(self, title, released, IMDB_rating=None):
        self.title = title
        self.released = released
        self.genre = list()
        self.imdb_rating = IMDB_rating

    @property
    def released(self):
        return self.__released

    @released.setter
    def released(self, value):
        if isinstance(value,int):
            if value in range(1927,2025):
                self.__released = value
                return
            else:
                stderr.write("Not in range 1927-2024")
                return
        if isinstance(value,str):
            try:
                value_int = int(value)
            except ValueError as err:
                stderr.write(f"OS Error while parsing.\n{err}\n")
                return
            else:
                if value_int in range(1927,2025):
                    self.__released=value_int
                    return
                else:
                    stderr.write("Not in range 1927-2024")
                    return
        else:
            raise RuntimeError("End of released setter!\n")

    @property
    def imdb_rating(self):
        return self.__imdb_rating

    @imdb_rating.setter
    def imdb_rating(self,value):
        if isinstance(value,float):
            self.__imdb_rating = value
            return
        elif isinstance(value, str):
            try:
                value_flt = float(value)
            except ValueError as err:
                stderr.write(f"Error OS.\n{err}\n")
                return
            else:
                self.__imdb_rating=value_flt
                return
        else:
            raise RuntimeError("End of setter imdb_rating.")

    def __eq__(self,other):
        if not isinstance(other, Movie):
            return False
        elif self.released and other.released and self.title and other.title:
            return (self.released == other.released) and (other.title == self.title)
        else:
            raise RuntimeError("Nema svih potrebnih atributa za poredjenje.")

    def __str__(self):
        res_str=""
        res_str+=f"Title: {self.title}\n"
        res_str+=f"Released: {self.released}\n"
        res_str+= f"Genre:"
        res_str+=f"{', '.join([str(genre) for genre in self.genre])}\n"
        res_str+=f"IMDB rating:{self.imdb_rating}\n"
        return res_str

class MovieCollection:

    def __init__(self, genre):
        self.genre = genre
        self.movies = list()

    def add_movie(self, movie):
        if not isinstance(movie, Movie):
            raise TypeError("Movie must be instance of class Movie.\n")
        if movie in self.movies:
            stderr.write("Movie is already in movies list.\n")
            return
        if not any([gnr == self.genre for gnr in movie.genre]):
            stderr.write("Movie is not right genre.\n")
            return
        else:
            self.movies.append(movie)
            print("Successfully added movie.\n")
            return

    def load_movies_from_csv(self):
        from pathlib import Path
        import csv
        try:
            with open(Path.cwd()/'../data/movies/top500movies.csv','r') as fobj:
                movies = list(csv.DictReader(fobj)) # ne zaboraviti list konstruktor
        except OSError as err:
            stderr.write(f"OS error\n{err}\n")
        except csv.Error as err:
            stderr.write(f"CSV Error.\n{err}\n")
        for movie in movies:
            genres = movie['Genre '].split('|')
            if not any([gnr == self.genre for gnr in genres]):
                continue
            new_movie = Movie(movie['Title'], movie['Relased_Year'], movie['IMDB_Rating'])
            new_movie.genre = genres
            if new_movie not in self.movies:
                self.add_movie(new_movie)
        return self.movies
    # from_year, to_year, min_rating !!!

    def get_movies_upper_90_percentiles(self):
        movies = movie_collection.load_movies_from_csv()
        import pandas as pd
        for_df = []
        for movie in movies:
            for_df.append((movie.title, movie.released, movie.genre, movie.imdb_rating))
        df_movies = pd.DataFrame(for_df, columns=["Title","Relased_Year","Genre","IMDB_Rating"])
        #display(df_movies)
        min_rating_90_percent = df_movies["IMDB_Rating"].quantile(0.9)
        print(f"PERCENTILA {min_rating_90_percent}")
        df_movies['IMDB_Rating'] = pd.to_numeric(df_movies['IMDB_Rating'])
        print(df_movies)
        print(type(df_movies['IMDB_Rating'][0]))
        df_selected = df_movies.loc[df_movies['IMDB_Rating']>=min_rating_90_percent]
        #df_selected = df_selected.sort_values(by='IMDB_Rating', ascending=False)
        list_mv = df_selected.to_dict('records')
        return list_mv




    def generate_custom_movie_list(self, selection_dictionary):
        self.load_movies_from_csv()
        try:
            min_rating = selection_dictionary['min_rating']
            from_year = selection_dictionary['from_year']
            to_year = selection_dictionary['to_year']
            res_list = []

            for movie in self.movies:
                if float(movie.imdb_rating)<min_rating:
                    continue
                if from_year <= int(movie.released) <=to_year:
                    res_list.append(movie)
            if len(res_list)==0:
                get_top_90_percent = self.get_movies_upper_90_percentiles()
                for elem in get_top_90_percent:
                    yield elem
            for element in sorted(res_list, key=lambda element: element.imdb_rating, reverse=True):
                yield element
        except KeyError as Kerr:
            stderr.write(f"{Kerr}-Dobijeni su sledeci kljucevi: {','.join([ key for key in selection_dictionary.keys()])}")
            get_top_90_percent = self.get_movies_upper_90_percentiles()
            for elem in get_top_90_percent:
                yield elem

if __name__ == '__main__':
    movie1 = Movie('Movie 1',1999,9.8)
    movie2 = Movie('Movie 2','1999','8.8')
    movie3 = Movie('Movie 3',2009,6.8)
    print(movie1)
    print(movie2)
    print(movie3)
    print(movie1==movie1)
    print(movie1 == movie2)
    movie4 = movie1
    print(movie1 is movie4)

    movie_collection = MovieCollection('Drama')
    # movie1.genre = ['Drama']
    # movie_collection.add_movie(movie1)
    # movie_collection.load_movies_from_csv()
    #
    # for elem in movie_collection.movies:
    #     print(elem)
    # print(len(movie_collection.movies)) # 174 filma!!!
    #movie_collection.generate_custom_movie_list({'min_rating':8.0, 'from_year':1990, 'to_year':2010})
    # movies_upper_90 = movie_collection.get_movies_upper_90_percentiles()
    # for elem in movies_upper_90:
    #     print(elem)
    # movies = movie_collection.load_movies_from_csv()


    # for elem in list_mv:
    #     print(elem)
    # print(len(list_mv))

    # movies =  movie_collection.load_movies_from_csv()
    # print(len(movies))
    # for movie in sorted(movies, key=lambda el:el.imdb_rating, reverse=True)[:10]:
    #     print(movie)

    lst=movie_collection.generate_custom_movie_list({'min_ratin':8.0, 'from_year':1990, 'to_year':2010})
    for el in lst:
        print(el)
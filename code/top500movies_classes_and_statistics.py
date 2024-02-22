from sys import stderr
from pathlib import Path
import csv
from collections import defaultdict
class Movie:

    def __init__(self, title, released,imdb_rating=None):
        self.title=title
        self.released = released
        self.genre = list() #lista zanrova, to je lista stringova
        self.imdb_rating = imdb_rating

    @property
    def released(self):
        return self.__released

    @released.setter
    def released(self, value): #int, str, 1927-2024
        if isinstance(value,int):
            if value in range(1927,2025):
                self.__released=value
                return
        if isinstance(value,str):
            try:
                value_int = int(value)
            except ValueError as err:
                stderr.write("Error while parsing released.\n")
                return
            else:
                if value_int in range(1927,2025):
                    self.__released=value_int
                    return
        else:
            raise RuntimeError("Kraj metode!!!")

    @property
    def imdb_rating(self):
        return self.__imdb_rating

    @imdb_rating.setter
    def imdb_rating(self, value):
        if isinstance(value, float):
            self.__imdb_rating=value
            return
        if isinstance(value,str):
            try:
                value_flt = float(value)
            except ValueError as err:
                stderr.write(f"Value error occured while parsing imdb_rating.\n{err}")
                return
            else:
                self.__imdb_rating=value_flt
                return
        else:
            raise RuntimeError("Kraj metode imdb rating!\n\n")

    def __str__(self):
        res_str=""
        res_str+=f"Title:{self.title}\n"
        res_str+=f"Released:{self.released}\n"
        res_str+=f"Genres:"
        res_str+=f"{','.join([str(g) for g in self.genre])}\n"
        res_str+=f"IMDB rating: {self.imdb_rating}\n"
        return res_str

    def __eq__(self, other):
        if not isinstance(other,Movie):
            stderr.write("Not instance of Movie class.\n")
            return
        if self.title and other.title and self.released and other.released:
            return (self.released==other.released) & (self.title==other.title)
        else:
            return False

class MovieCollection:

    def __init__(self, genre):
        self.genre = genre
        self.movies = list()

    def add_movie(self, movie):
        if not isinstance(movie, Movie):
            stderr.write("Nije instance klase Movie.\n")
            return
        if movie in self.movies:
            stderr.write("Vec postoji u listi filmova\n")
            return
        if not any([gnr in self.genre for gnr in  movie.genre]):
            stderr.write("Nije pravog zanra\n")
            return
        else:
            self.movies.append(movie)
            #print("Successfully added movie")
            return

    def load_movies_from_csv(self):
        try:
            with open(Path.cwd()/'../data/movies/top500movies.csv') as fobject:
                list_of_movies = list(csv.DictReader(fobject))
                for movie in list_of_movies:
                    genres =movie['Genre '].split('|')
                    if self.genre in genres:
                        #print(f"Self genre:{self.genre}->genres of movie{genres}")
                        new_movie = Movie(movie['Title'], movie['Relased_Year'], movie['IMDB_Rating']) # PRVO STO KONSTRUKTOR NE PRIMA GENRE
                        new_movie.genre=['Drama','Romance'] # POTREBNO GA JE SETOVATI OVDE!!!
                        if new_movie not in self.movies: # TAJ MOVIE POKUSAVA DA STIGNE U METODU ADD MOVIE I TAMO MOZDA TAJ ISTI VEC POSTOJI.
                            self.add_movie(new_movie) # POTREBNO IH JE DODATI
        except OSError as err:
            stderr.write(f"OS ERROR- {err}")
        except csv.Error as err:
            stderr.write(f"CSV Error. \n{err}\n")


    def get_top10_percentages(self):
        self.load_movies_from_csv()
        import pandas as pd
        movies_tuple_list=list()
        for movie in self.movies:
            movies_tuple_list.append((movie.title,movie.released, movie.genre, movie.imdb_rating))
        movies_df = pd.DataFrame(movies_tuple_list, columns=["Title","Relased_Year","Genre","IMDB_Rating"])
        #display(movies_df)
        rating_90_percent=movies_df['IMDB_Rating'].quantile(0.9) # 8.370000000000003
        movies_90_precent = movies_df.loc[movies_df['IMDB_Rating']>rating_90_percent]
        #display(movies_90_precent)
        dict_movies_90_perc =movies_90_precent.to_dict('records')
        return dict_movies_90_perc


    #vraca filmove u kriterijumu, ako je lista prazna vraca genericku listu svih filmova koji imaju imdb rejting
    #veci od 90 posto filmova u tabeli. U svakom slucaju, liste su sortirane po imdb rejtingu.

    def generate_custom_movie_list(self, selection_criterium):
        self.load_movies_from_csv()

        try:
            resulting_list=[]
            for movie in self.movies:
                from_year = int(selection_criterium['from_year'])
                to_year = int(selection_criterium['to_year'])
                min_rating = int(selection_criterium['min_rating'])
                if movie.released in range(from_year, to_year+1) and movie.imdb_rating>=min_rating:
                    resulting_list.append(movie)

            if len(resulting_list)==0:
                list_result =self.get_top10_percentages()
                for movie in sorted(list_result, key=lambda elem_dct:elem_dct['IMDB_Rating'], reverse=True):
                    yield movie
            else:
                for res_movie in sorted(resulting_list, key=lambda mv:mv.imdb_rating, reverse=True):
                    yield res_movie
        except KeyError:
            stderr.write(f"Not right key values.{','.join([el for el in selection_criterium.keys()])}")
            list_result =self.get_top10_percentages()
            for movie in sorted(list_result, key=lambda elem_dct:elem_dct['IMDB_Rating'], reverse=True):
                yield movie








if __name__=='__main__':

    movie1 = Movie('Movie 1',1999,9.6)
    #print(movie1)
    movie2 = Movie('Movie2','2000','8.7')
    # print(movie2)
    # print(movie1==movie2)
    # print(movie1==movie1)

    movie1.genre = ['Historical','Drama']
    movie2.genre = ['Musical']
    movie_collection = MovieCollection('Drama')
    movie_collection.add_movie(movie1)
    #movie_collection.add_movie(movie1) # vraca da film vec postoji u listi
    #movie_collection.add_movie(movie2) # vraca nije pravog zanra

    # movies =read_from_csv(Path.cwd()/'../data/imdb_top_500_movies.csv')
    # for movie in movies:
    #     print(movie)
    movie_collection.load_movies_from_csv()
    # movies_drama = movie_collection.movies
    # print(len(movies_drama))

    # selected_movies = movie_collection.generate_custom_movie_list({'from_yea':2000,'to_year':2010,'min_rating':10.0})
    # while True:
    #     try:
    #         print(next(selected_movies))
    #     except StopIteration:
    #         break

    # import pandas as pd
    # data = [(movie.title,movie.released, movie.genre, movie.imdb_rating) for movie in selected_movies]
    # selected_movies_df = pd.DataFrame(data,columns=["Title","Relased_Year","Genre","IMDB_Rating"])
    # display(selected_movies_df) # OVAKO SE PRIKAZUJE DATA_FRAME

    # selected_movies2=movie_collection.generate_custom_movie_list({'from_yea':2000,'to_year':2010,'min_rating':8.0})
    # while True:
    #     try:
    #         print(next(selected_movies2))
    #     except StopIteration:
    #         break
    #movie_collection.get_best_movie_in_year()
    movies_list = movie_collection.generate_custom_movie_list({'from_yea':2000,'to_year':2010,'min_rating':8.0})
    while True:
        try:
            print(next(movies_list))
        except StopIteration:
            break
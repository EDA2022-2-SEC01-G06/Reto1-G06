"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
#actualizar limite de lectura de archivos
csv.field_size_limit(2147483647)

# Inicialización del Catálogo de libros

def newController(characteristics:dict):
    """
    Se crea una instancia del modelo
    -------------------------------------
    Recibe por parametro un diccionario que determina el tipo de TAD para cada lista dentro
     del catalogo
    """
    control={
        "model":None
    }
    control["model"]=model.NewCatalog(characteristics)
    return control

# Funciones para la carga de datos

def loadData(control, characteristics:dict):
    """
    Cargar los datos de las peliculas y las listas del catalog
    -----------------------------
    recibe por parametro un diccionario con las caracteristicas del catalogo
    """
    catalog=control["model"]
    data = loadMovies(catalog, characteristics)
    model.sortlist(catalog, characteristics["sort_algoritm"], "videos", model.cmpMoviesByReleaseYear)
    return catalog["videos"]

def loadMovies(catalog, characteristics:dict):
    """
    Cargar los datos de las peliculas del archivo csv.
    """
    sufijo= characteristics["data_size_sufijo"]
    #para la prueba se usan con el sufijo -small
    Amazon_data= cf.data_dir + "Streaming/amazon_prime_titles-utf8"+sufijo+".csv"
    Disney_data= cf.data_dir + "Streaming/disney_plus_titles-utf8"+sufijo+".csv"
    Hulu_data= cf.data_dir + "Streaming/hulu_titles-utf8"+sufijo+".csv"
    Netflix_data= cf.data_dir + "Streaming/netflix_titles-utf8"+sufijo+".csv"

    input_file_Amazon= csv.DictReader(open(Amazon_data, encoding= "utf-8"))
    input_file_Disney= csv.DictReader(open(Disney_data, encoding= "utf-8"))
    input_file_Hulu= csv.DictReader(open(Hulu_data, encoding= "utf-8"))
    input_file_Netflix= csv.DictReader(open(Netflix_data, encoding= "utf-8"))

    addMoviefromCSV_Input(catalog, input_file_Amazon, "amazon")
    addMoviefromCSV_Input(catalog, input_file_Disney, "disney")
    addMoviefromCSV_Input(catalog, input_file_Hulu, "hulu")
    addMoviefromCSV_Input(catalog, input_file_Netflix, "netflix")


def addMoviefromCSV_Input(catalog, input_file, stream_service:str):
    for video in input_file:
        ya_esta= model.already_exist(catalog["videos"], video)
        if ya_esta == True:
            video["show_id"]=video["show_id"]+"-"+stream_service
            video["stream_service"]= stream_service
        else:
            video["stream_service"]= stream_service
        model.addMovie(catalog, video)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def GetDataSpecifications(catalog):
    """
    Se obtienen los datos especificos del catalogo de videos. El numero de registros, numero de registros
    para cada servicio de stream, etc(lo demas que se pueda necesitar en el futuro)
    """
    cantidad_videos=model.Getlistsize(catalog, "videos")
    stream_service_count=catalog["stream_services"]

    return cantidad_videos, stream_service_count

def Get_Sample_Data(catalog, sample_size:int):
    return model.Get_sample_data(catalog, sample_size, "videos")

def Movies_by_year(catalog, year1:int, year2:int, characteristics:dict):
    """
    Se ejecuta la funcion Movies by year en el modelo
    """
    model.Search_movie_by_year(catalog,year1,year2)
    list_size=model.Getlistsize(catalog, "movies_by_year")
    if list_size > 0:
        model.sortlist(catalog, characteristics["sort_algoritm"], "movies_by_year", model.cmpMoviesByReleaseYear)
        return model.Get_sample_data(catalog, sample_size= 3,list_name="movies_by_year"), list_size
    else:
        return None, list_size

def TV_show_by_date_added(catalog, date1:str, date2:str, characteristics:dict):
    """
    Se ejecuta la funcion TV show by date en el modelo
    """
    model.Search_TV_show_by_date(catalog,date1,date2)
    list_size=model.Getlistsize(catalog, "tv_shows_by_date")
    if list_size > 0:
        model.sortlist(catalog, characteristics["sort_algoritm"], "tv_shows_by_date", model.cmpMoviesByReleaseYear)
        return model.Get_sample_data(catalog, sample_size= 3,list_name="tv_shows_by_date"), list_size
    else:
        return None, list_size

def Videos_by_country(catalog, country:str, characteristics:dict):
    """
    Se ejecuta la funcion Videos by country en el modelo
    """
    streaming_service_count=model.Search_videos_by_Country(catalog, country)
    list_size=model.Getlistsize(catalog, "videos_by_country")
    if list_size > 0:
        model.sortlist(catalog, characteristics["sort_algoritm"], "videos_by_country", model.cmpMoviesByReleaseYear)
        return model.Get_sample_data(catalog, sample_size= 3,list_name="videos_by_country"), list_size, streaming_service_count
    else:
        return (None, list_size, None)
    
def Content_by_gender(catalog,gender:str):
    """
    Se ejecuta la funcion contentgender en el modelo
    """
    contentg=model.Contentgender(catalog,gender:str)





def Videos_by_Director(catalog, director:str, characteristics:dict):
    """
    Se ejecuta la funcion Videos by director en el modelo
    """
    type_count, streaming_service_count=model.Search_videos_by_Director(catalog, director)
    list_size=model.Getlistsize(catalog, "director")
    if list_size > 0:
        model.sortlist(catalog, characteristics["sort_algoritm"], "director", model.cmpMoviesByReleaseYear)
        return model.Get_sample_data(catalog, sample_size= 3,list_name="director"), list_size,type_count, streaming_service_count
    else:
        return (None, list_size, None, None)

def Gender_ranking(catalog, Ntop:int, characteristics:dict):
    """
    Se ejecuta la funcion get gender count and specs en el modelo
    """
    model.Get_Genres_count_and_specs(catalog)
    model.sortlist(catalog, characteristics["sort_algoritm"], "genres_ranking", model.cmpRanking)
    top=model.Get_data_range(catalog, Ntop, "genres_ranking")
    for i in range(0,len(top)):
        top[i]["rank"]=i+1
    return top

#funciones de medicion de tiempo

def Get_time():
    return model.getTime()

def Delta_time(start, end):
    return model.deltaTime(start, end)

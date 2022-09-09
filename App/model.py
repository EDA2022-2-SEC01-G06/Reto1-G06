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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from gettext import Catalog
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import selectionsort as selection
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
import time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def NewCatalog(TADs:dict):
    """
    Crea el catalogo de peliculas. tiene 5 listas, una para los videos
    otra para las categorias, para los actores, directores y paises.
    ---------------------
    Recibe como parametro un diccionario con los tipos de TAD para cada lista dentro del catalogo
    el diccionario se encuentra en el view.py
    """
    catalog ={
         "videos":None,
         "stream_services": None
         #"categorias":None,
         #"actores":None,
         #"directores":None,
         #"paises":None,
         
            }

    # para el taller 3 solo se va a implementar la lista de videos
    catalog["videos"]=lt.newList(datastructure= TADs["videos"], cmpfunction= compare_videos)
    catalog["stream_services"]=lt.newList(TADs["stream_services"], cmpfunction=compare_streaming_services)

    return catalog

# Funciones para agregar informacion al catalogo


   
# Funciones para creacion de datos

def addMovie(catalog, movie):
    """
    Se añade un libro en la lista de videos del catalog
    """
    lt.addLast(catalog["videos"], movie)
    #añadir al conteo de videos para cada stream service
    streaming_service=movie["stream_service"]
    addStreaming_service(catalog, streaming_service.strip(), movie)
    #se obtienen los actores, el director y el pais (aun no implementado)

def addStreaming_service(catalog, streaming_service_name, video):
    """
    Añadir un servicio de streaming a la lista contenida en el catalogo
    """
    servicios_streaming=catalog["stream_services"]
    pos_streaming_s=lt.isPresent(servicios_streaming, streaming_service_name)
    if pos_streaming_s > 0:
        st_service = lt.getElement(servicios_streaming, pos_streaming_s)
    else:
        st_service = newStreaming_service(streaming_service_name)
        lt.addLast(servicios_streaming, st_service)
    lt.addLast(st_service["videos"], video)
    st_service["size"]+=1
    return catalog

def newStreaming_service(name:str):
    """
    Añade un nuevo servicio de streaming al catalogo, tiene referencia a los videos que tengan dicho servicio
    y el numero de elementos de la lista
    """
    streaming_service={"name":"", "videos":None, "size":0}
    streaming_service["name"]=name
    streaming_service["videos"]=lt.newList(datastructure="ARRAY_LIST")
    return streaming_service

# Funciones de consulta

def Getlistsize(catalog, list_name:str):
    return lt.size(catalog[list_name])

def already_exist(lista, elemento):
    presente=lt.isPresent(lista, elemento)
    if presente >0:
        return True
    else:
        return False

def Get_sample_data(catalog, sample_size:int, list_name:str):
    first_samples=[]
    last_samples=[]
    lista=catalog[list_name]
    list_size=Getlistsize(catalog, list_name)
    for i in range(1, sample_size+1):
        first_samples.append(lt.getElement(lista, i))
    for e in range(list_size, list_size-sample_size, -1):
        last_samples.append(lt.getElement(lista, e))
    return first_samples+last_samples

# Funciones utilizadas para comparar elementos dentro de una lista

def compare_streaming_services(streaming_s1, st_service):
    if streaming_s1.lower() == st_service['name'].lower():
        return 0
    elif streaming_s1.lower() > st_service['name'].lower():
        return 1
    return -1

def compare_videos(v1,video):
    if v1['show_id'].lower() == video['show_id'].lower():
        return 0
    elif v1['show_id'].lower() > video['show_id'].lower():
        return 1
    return -1
# Funciones de ordenamiento

def compare_by_year(video1, video2):
    return ((float(video1["release_year"])>float(video2["release_year"])) and ((video1["title"].lower()) > (video2["title"].lower())))

def cmpMoviesByReleaseYear(movie1, movie2): 
    """ Devuelve verdadero (True) si el release_year de movie1 son menores que los de movie2,
     en caso de que sean iguales tenga en cuenta el titulo y en caso de que ambos criterios
      sean iguales tenga en cuenta la duración, de lo contrario devuelva falso (False). 
      Args: movie1: informacion de la primera pelicula que incluye sus valores 'release_year',
       ‘title’ y ‘duration’ movie2: informacion de la segunda pelicula que incluye su valor
        'release_year', ‘title’ y ‘duration’ """
    if float(movie1["release_year"])<float(movie2["release_year"]):
        return True
    elif float(movie1["release_year"])==float(movie2["release_year"]):
        if movie1["title"].lower() < movie2['title'].lower():
            return True
        elif movie1["title"].lower() == movie2['title'].lower():
            if movie1["duration"] != "" and movie2["duration"] != "":
                if float(movie1["duration"].split(" ")[0])<float(movie2["duration"].split(" ")[0]):
                    return True
    
    return False



def sortVideos(catalog, sort_algoritm:str):
    if sort_algoritm == "shell":
        sa.sort(catalog["videos"], cmpfunction= cmpMoviesByReleaseYear)
    elif sort_algoritm == "insertion":
        insertion.sort(catalog["videos"], cmpfunction= cmpMoviesByReleaseYear)
    elif sort_algoritm == "selection":
        selection.sort(catalog["videos"], cmpfunction= cmpMoviesByReleaseYear)
    elif sort_algoritm == "merge":
        merge.sort(catalog["videos"], cmpfunction= cmpMoviesByReleaseYear)
    elif sort_algoritm == "quick":
        quick.sort(catalog["videos"], cmpfunction= cmpMoviesByReleaseYear)

#funciones para medir tiempo de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

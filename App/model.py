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
from datetime import datetime
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
         "stream_services": None,
         "movies_by_year":None,
         "tv_shows_by_date":None,
         "videos_by_country":None,
         "director":None,
         "genres_ranking":None
         #"actores":None,
         
            }

    # para el taller 3 solo se va a implementar la lista de videos
    catalog["videos"]=lt.newList(datastructure= TADs["videos"], cmpfunction= compare_videos)
    catalog["stream_services"]=lt.newList(TADs["stream_services"], cmpfunction=compare_streaming_services)

    return catalog

# Funciones para agregar informacion al catalogo

def New_list_to_catalog(catalog, List_name:str, TAD:str, cmpfunction):
    "añade o reescribe una nueva lista al catalogo// evita tener que recargar todo el catalogo de peliculas"
    catalog[List_name]=lt.newList(datastructure=TAD, cmpfunction=cmpfunction)

   
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
    #esta linea agrega el video al streaming service determinado, no obstante ya que ningun requerimiento lo pide
    #esta solo comentado
    #lt.addLast(st_service["videos"], video)
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

def Get_data_range(catalog, sample_size:int, list_name:str):
    samples=[]
    lista=catalog[list_name]
    list_size=Getlistsize(catalog, list_name)
    if list_size>=sample_size:
        for i in range(1, sample_size+1):
            samples.append(lt.getElement(lista, i))
    else:
        for i in range(1, list_size+1):
            samples.append(lt.getElement(lista, i))
    return samples

def Get_sample_data(catalog, sample_size:int, list_name:str):
    first_samples=[]
    last_samples=[]
    lista=catalog[list_name]
    list_size=Getlistsize(catalog, list_name)
    if list_size>=(sample_size*2):
        for i in range(1, sample_size+1):
            first_samples.append(lt.getElement(lista, i))
        for e in range(list_size, list_size-sample_size, -1):
            last_samples.append(lt.getElement(lista, e))
    else:
        for i in range(1, list_size+1):
            first_samples.append(lt.getElement(lista, i))

    return first_samples+ list(reversed(last_samples))

def Search_movie_by_year(catalog, year1:int, year2:int):
    """
    Se filtran los registros dentro del catalogo y se agregan a una lista los que se encuentren
    entre el rango de años
    """
    New_list_to_catalog(catalog, "movies_by_year", "ARRAY_LIST", compare_videos)
    #recorrer la lista de peliculas
    size_lista_peliculas=lt.size(catalog["videos"])
    for position in range(1,size_lista_peliculas+1):
        video=lt.getElement(catalog["videos"], position)
        #verificar si cumple los requisitos
        if (video["type"]=="Movie")and((int(video["release_year"])>=year1)and(int(video["release_year"])<=year2)):
            #contruir el registro que se va a agregar
            video2={
                "type":video["type"],
                "release_year":video["release_year"],
                "title":video["title"],
                "duration":video["duration"],
                "stream_service": video["stream_service"],
                "director": video["director"],
                "cast":video["cast"]
              }
            lt.addLast(catalog["movies_by_year"], video2)

def Search_TV_show_by_date(catalog, date1:str, date2:str):
    """
    Se recorre todo el catalogo de peliculas y se obtienen (y agregan a la lista tv_shows_by_date)
    los tv shows que se agregaron en las fechas especificadas.
    """
    #se crea la lista
    New_list_to_catalog(catalog, "tv_shows_by_date", "ARRAY_LIST", compare_videos)
    #se transforman los parametros a datetime
    initial_date=datetime.strptime(date1, "%B %d, %Y")
    final_date=datetime.strptime(date2, "%B %d, %Y")

    #se recorre el catalogo de peliculas
    size_lista_peliculas=lt.size(catalog["videos"])
    for position in range(1,size_lista_peliculas+1):
        tv_show=lt.getElement(catalog["videos"], position)
        if tv_show["date_added"] != "":
            tv_show_date=datetime.strptime(tv_show["date_added"], "%Y-%m-%d")
            #verificar si cumple los requisitos
            if (tv_show["type"]=="TV Show")and(initial_date<=tv_show_date<=final_date):
                show2={
                "type":tv_show["type"],
                "date_added": tv_show["date_added"],
                "title":tv_show["title"],
                "duration":tv_show["duration"],
                "release_year":tv_show["release_year"],
                "stream_service": tv_show["stream_service"],
                "director": tv_show["director"],
                "cast":tv_show["cast"]
              }
                lt.addLast(catalog["tv_shows_by_date"], show2)

def Search_videos_by_Country(catalog, country:str):
    New_list_to_catalog(catalog, "videos_by_country", "ARRAY_LIST", compare_videos)
    #recorrer la lista de peliculas
    size_lista_peliculas=lt.size(catalog["videos"])
    videos_by_streaming_service={}
    for position in range(1,size_lista_peliculas+1):
        video=lt.getElement(catalog["videos"], position)
        #verificar si cumple los requisitos
        if (video["country"]==country):
            #contruir el registro que se va a agregar
            video2={
                "type":video["type"],
                "release_year":video["release_year"],
                "title":video["title"],
                "duration":video["duration"],
                "stream_service": video["stream_service"],
                "director": video["director"],
                "cast":video["cast"]
              }
            #se agrega el video a la lista
            lt.addLast(catalog["videos_by_country"], video2)
            #agregar al conteo por streaming service
            videos_by_streaming_service[video["type"]]= videos_by_streaming_service.get(video["type"], 0)
            videos_by_streaming_service[video["type"]]+=1
    #se retorna el diccionario con el conteo por streaming service
    return {"type":videos_by_streaming_service.keys(), "count":videos_by_streaming_service.values()}

def Search_videos_by_Director(catalog, director:str):
    New_list_to_catalog(catalog, "director", "ARRAY_LIST", compare_videos)
    #recorrer la lista de peliculas
    size_lista_peliculas=lt.size(catalog["videos"])
    videos_by_streaming_service={}
    videos_by_type={}
    for position in range(1,size_lista_peliculas+1):
        video=lt.getElement(catalog["videos"], position)
        #verificar si cumple los requisitos
        if (video["director"].strip()==director):
            #contruir el registro que se va a agregar
            video2={
                
                "title":video["title"],
                "release_year":video["release_year"],
                "director": video["director"],
                "stream_service": video["stream_service"],
                "type":video["type"],
                "duration":video["duration"],
                "cast":video["cast"],
                "country":video["country"],
                "rating":video["rating"],
                "listed_in":video["listed_in"],
                "description":video["description"]
              }
            #se agrega el video a la lista
            lt.addLast(catalog["director"], video2)
            #agregar al conteo por streaming service
            videos_by_streaming_service[video["stream_service"]]= videos_by_streaming_service.get(video["stream_service"], 0)
            videos_by_streaming_service[video["stream_service"]]+=1
            #agregar conteo por tipo
            videos_by_type[video["type"]]= videos_by_type.get(video["type"], 0)
            videos_by_type[video["type"]]+=1
    #se retorna el diccionario con el conteo por streaming service
    return {"type":videos_by_type.keys(), "count":videos_by_type.values()}, {"stream_service":videos_by_streaming_service.keys(), "count":videos_by_streaming_service.values()}

def Get_Genres_count_and_specs(catalog):
    """
    Se recorre todo el catalogo de peliculas y se obtiene los datos de cada genero registrado
    (en cuantas peliculas esta listado el genero, el tipo de contenido: Movie/Tv show, el numero de veces que
    aparece en un streaming service)
    """
    #crear lista dentro del catalogo
    New_list_to_catalog(catalog, "genres_ranking", "ARRAY_LIST", cmpfunction=compare_ranking_pos)

    #lista de registros por genero, cada registro es un diccionario
    #{listed_in:str, count:int, type:str(dict{movie:int, tv_show:int}), stream_service:str(dict{stream:count...})}
    registros_list=[]
    #diccionario de claves valores, se usa para acceder y modificar algun registro en la lista de registros
    #sin tener que recorrerla toda cada vez
    claves_valores={}
    #recorrer el catalogo de peliculas
    size_lista_peliculas=lt.size(catalog["videos"])
    for position in range(1,size_lista_peliculas+1):
        video=lt.getElement(catalog["videos"], position)

        #obtener generos listados
        genres=video["listed_in"].split(",")
        n_genders=len(genres)
        for i in range(0, n_genders):
            genres[i] = genres[i].strip()
        
        #añadir generos al la lista de registros
        for gender in genres:
            #se verifica que este genero se encuentre ya en la lista
            #para ello se busca en el diccionario de claves_valores
            indice=claves_valores.get(gender, -1)
            if indice == -1:
                #si no se encuentra
                type_dict={}
                type_dict[video["type"]]=1
                stream_dict={}
                stream_dict[video["stream_service"]]=1
                new_gender={"listed_in":gender, "count":1, "type":type_dict, "stream_service":stream_dict}
                
                #añdir clave_valor para este genero en la lista
                claves_valores[gender]=len(registros_list)
                #añadir genero a la lista
                registros_list.append(new_gender)
            else:
                #si se encuentra
                # cambiar conteo
                registros_list[indice]["count"]+=1
                #cambiar count de type
                type_count=registros_list[indice]["type"].get(video["type"], 0)
                registros_list[indice]["type"][video["type"]]=type_count+1
                #cambiar count de stream service
                stream_count=registros_list[indice]["stream_service"].get(video["stream_service"], 0)
                registros_list[indice]["stream_service"][video["stream_service"]]=stream_count+1
    
    #añadir cada elemento de la lista de registros a la lista genres_ranking
    for rankin_element in registros_list:
        rankin_element["type"]=Dict_to_str(rankin_element["type"])
        rankin_element["stream_service"]=Dict_to_str(rankin_element["stream_service"])
        lt.addLast(catalog["genres_ranking"], rankin_element)

def Contentgender(catalog,gender:str):

    New_list_to_catalog(catalog, "generos", "SINGLE_LINKED", compare_videos)
    size_lista_peliculas=lt.size(catalog["videos"])
    for position in range(1,size_lista_peliculas+1):
        video=lt.getElement(catalog["videos"], position)
        if gender.lower() in video["listed_in"].lower():
            video2={
                
                "title":video["title"],
                "release_year":video["release_year"],
                "director": video["director"],
                "stream_service": video["stream_service"],
                "duration":video["duration"],
                "cast":video["cast"],
                "country":video["country"],
                "rating":video["rating"],
                "listed_in":video["listed_in"],
                "description":video["description"]
              }
            lt.addLast(catalog["generos"],video2)
    
   

def Dict_to_str(dictionary:dict):
    llaves=list(dictionary.keys())
    valores=list(dictionary.values())
    resultado=""
    for i in range(0,len(llaves)):
        resultado+=llaves[i]+"      "+str(valores[i])+"\n"
    return resultado

# Funciones utilizadas para comparar elementos dentro de una lista

def compare_streaming_services(streaming_s1, st_service):
    if streaming_s1.lower() == st_service['name'].lower():
        return 0
    elif streaming_s1.lower() > st_service['name'].lower():
        return 1
    return -1

def compare_ranking_pos(rankig_1, ranking):
    if rankig_1["count"] == ranking["count"]:
        return 0
    elif rankig_1["count"] > ranking["count"]:
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

def cmpRanking(gender1, gender2):
    """
    Esta funcion se usa para organizar el top de rankings
    """
    if gender1["count"] > gender2["count"]:
        return True
    else:
        if gender1["listed_in"] < gender2["listed_in"]:
            return True
    return False

def sortlist(catalog, sort_algoritm:str, list_name, cmpfunction):
    if sort_algoritm == "shell":
        sa.sort(catalog[list_name], cmpfunction= cmpfunction)
    elif sort_algoritm == "insertion":
        insertion.sort(catalog[list_name], cmpfunction= cmpfunction)
    elif sort_algoritm == "selection":
        selection.sort(catalog[list_name], cmpfunction= cmpfunction)
    elif sort_algoritm == "merge":
        merge.sort(catalog[list_name], cmpfunction= cmpfunction)
    elif sort_algoritm == "quick":
        quick.sort(catalog[list_name], cmpfunction= cmpfunction)

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

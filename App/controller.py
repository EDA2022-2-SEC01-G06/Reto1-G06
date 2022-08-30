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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
#actualizar limite de lectura de archivos
csv.field_size_limit(2147483647)

# Inicialización del Catálogo de libros

def newController():
    """
    Se crea una instancia del modelo
    """
    control={
        "model":None
    }
    control["model"]=model.NewCatalog()
    return control

# Funciones para la carga de datos

def loadData(control):
    """
    Cargar los datos de las peliculas y las listas del catalog
    """
    catalog=control["model"]
    data = loadMovies(catalog)
    model.sortVideos(catalog)
    return catalog["videos"]

def loadMovies(catalog):
    """
    Cargar los datos de las peliculas del archivo csv.
    """
    #para la prueba se usan con el sufijo -small
    Amazon_data= cf.data_dir + "Streaming/amazon_prime_titles-utf8-small.csv"
    Disney_data= cf.data_dir + "Streaming/disney_plus_titles-utf8-small.csv"
    Hulu_data= cf.data_dir + "Streaming/hulu_titles-utf8-small.csv"
    Netflix_data= cf.data_dir + "Streaming/netflix_titles-utf8-small.csv"

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
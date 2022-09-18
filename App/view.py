"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

from gettext import Catalog
import config as cf
import sys
import controller
import tabulate
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#Este comentario se puso para que el comentario del commit coincidiera con lo pedido en el pdf del laboratorio
#actualizar limites de recursion
default_limit = 1000 
sys.setrecursionlimit(default_limit*10)

controller_characteristics={
    #Este diccionario se usa como referencia para elegir el tipo de TAD al crear las listas que
    #componen al catalogo
    #tambien algunas otras caracteristicas que permiten modificar el controlador
    #estas caracteristicas se usan dentro del model.py para crear las listas, modificar los algoritmos sort, etc.
    "videos":"ARRAY_LIST",
    "stream_services":"ARRAY_LIST",
    "data_size_sufijo":"-small",
    "sort_algoritm":"shell"
}
def newController():
    control=controller.newController(controller_characteristics)
    return control

def printMenu():
    #muestra las opciones que el usuario puede elegir
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar peliculas estrenadas en un periodo")
    print("3- Listar shows de tv añadidos en un periodo")
    #requerimientos individuales 3, 4 y 5
    #requerimiento 3 --->opcion 4

    #requerimiento 4---->opcion 5

    #requerimiento 5---->opcion 6
    print("6- Listar contenido producido en un pais")

    print("7- Encontrar contenido con un director involucrado")
    print("8- Listar top N de generos con mas contenido")
    print("9- Cambiar el algoritmo para ordenamiento de los datos")
    print("10- Elegir TAD para el catalogo de peliculas")
    print("11- Elegir tamaño del catalogo de peliculas")
    #print("3- ")
    print("0- salir")

#funciones de los requerimientos

def loadData(control, controller_characteristics:dict):
    """
    Esta función solicita al controlador que cargue los datos en el modelo
    ------------------------
    Parametros:
        controller: el controlador que se va a asociar al view
    ------------------------
    Retorno:
        los datos de los videos
    """
    print("Información de los datos cargados:")
    
    controller.loadData(control, controller_characteristics)
    cantidad_videos, stream_s_count =controller.GetDataSpecifications(control["model"])
    print("Total de datos cargados:",cantidad_videos)

    specificaciones_list=[]
    for stream_s in stream_s_count["elements"]:
        specificaciones_list.append([stream_s["name"] , stream_s["size"]])
    print(tabulate.tabulate(specificaciones_list, headers=("servicio de streaming", "total") ,tablefmt="grid"))
    print("\n---------------------------------")

    #primeros y ultimos 3   
    show_data=controller.Get_Sample_Data(control["model"], 3)
    
    #mostrar tabla
    print(tabulate.tabulate(show_data, headers="keys", tablefmt="grid", maxcolwidths=[10,10,20,10,30,20,20,20,20,20,20,20,20]))
    print("La tabla puede mostrarse de manera incorrecta dependiendo del tamaño del terminal")
    
def Movies_by_year(control, year1,year2, characteristics:dict):
    sample_data, size_list=controller.Movies_by_year(control["model"], year1, year2,characteristics)
    #print(sample_data)
    print("==================Requerimiento 1==============")
    print(f"Hay un total de {size_list} peliculas estrenadas entre {year1} y {year2}")
    if size_list>0:
        print(tabulate.tabulate(sample_data, headers="keys", tablefmt="grid", maxcolwidths=[10,10,20,10,30,20,20,20,20,20,20,20,20]))
        print("La tabla puede mostrarse de manera incorrecta dependiendo del tamaño del terminal")

def Tv_shows_by_date(control, date1,date2, characteristics:dict):
    sample_data, size_list=controller.TV_show_by_date_added(control["model"], date1, date2,characteristics)
    #print(sample_data)
    print("==================Requerimiento 2==============")
    print(f"Hay un total de {size_list} Shows de tv estrenados entre {date1} y {date2}")
    if size_list>0:
        print(tabulate.tabulate(sample_data, headers="keys", tablefmt="grid", maxcolwidths=[10,10,20,10,30,20,20,20,20,20,20,20,20]))
        print("La tabla puede mostrarse de manera incorrecta dependiendo del tamaño del terminal")

def videos_by_country(control, country:str, characteristics:dict):
    sample_data, size_list, st_s_count=controller.Videos_by_country(control["model"], country,characteristics)
    #print(sample_data)
    print("==================Requerimiento 5==============")
    print(f"------------Conteo de producciones hechas en {country}----------")
    if size_list>0:
        print(f"Hay {size_list} producciones hechas en {country}")
        print(tabulate.tabulate(st_s_count,headers="keys",  tablefmt="grid"))
        print(tabulate.tabulate(sample_data, headers="keys", tablefmt="grid", maxcolwidths=[10,10,20,10,30,20,20,20,20,20,20,20,20]))
        print("La tabla puede mostrarse de manera incorrecta dependiendo del tamaño del terminal")
    else:
        print(f"No se ha encontrado contenido producido en {country}")

def videos_by_director(control, director:str, characteristics:dict):
    sample_data, size_list, type_count ,st_s_count=controller.Videos_by_Director(control["model"], director,characteristics)
    #print(sample_data)
    print("==================Requerimiento 6==============")
    print(f"------------Conteo de producciones hechas en {director}----------")
    if size_list>0:
        print(f"Hay {size_list} producciones dirigidas por {director}")
        print(tabulate.tabulate(type_count,headers="keys",  tablefmt="grid"))
        print(tabulate.tabulate(st_s_count,headers="keys",  tablefmt="grid"))
        print(tabulate.tabulate(sample_data, headers="keys", tablefmt="grid", maxcolwidths=[10,10,20,10,30,20,20,20,20,20,20,20,20]))
        print("La tabla puede mostrarse de manera incorrecta dependiendo del tamaño del terminal")
    else:
        print(f"No se ha encontrado contenido dirigido por {director}")

def Get_N_top(control, ntop, characteristics:dict):
    sample_data=controller.Gender_ranking(control["model"], ntop, characteristics)
    print("==================Requerimiento 7==============")
    print(f"Hay un total de {len(sample_data)} tags registradas")
    print(f"Los top {ntop} generos listados son: \n")
    print(tabulate.tabulate(sample_data, headers="keys", tablefmt="grid", stralign="right"))

def ChangeTAD_type(list_name:str):
    """
    Usando como referencia el diccionario controller_TADs, se cambia el tipo de TAD para alguna
    de las listas en el catalogo
    ------------------------------------------------
    Para que surta efecto, requiere que el catalogo sea cargado de nuevo en memoria
    """
    print("Al realizar esta acción se necesitara volver a cargar el catalogo de videos")
    print("Seleccione con que tipo de TAD quiere cargar los datos:")
    print("1- ARRAY_LIST (arreglo)")
    print("2- SINGLE_LINKED (lista encadenada)")
    
    user_inputs= input("\nSeleccione una opción para continuar\n")

    if int(user_inputs[0]) == 1:
        #cargar el catalogo con un arreglo
        controller_characteristics[list_name]="ARRAY_LIST"

    elif int(user_inputs[0]) == 2:
        controller_characteristics[list_name]="SINGLE_LINKED"
    else:
        print("Seleccione una opción valida")
        return None
    print("Se ha cambiado el tipo de TAD para la lista dentro del catalogo")
    print("-----------------------------------------------------------\n")
    Reload()
   
def Reload():
    print("desea recargar el catalogo en memoria? (necesario para que surgan efecto los cambios)\n")
    r=input("Y/N\n")
    print("---------------------------------------------------\n")
    if r.lower()[0] == "y":
        control = newController()
        print("Cargando información de los archivos ....")
        loadData(control, controller_characteristics)
    elif r.lower()[0] == "n":
        return None
    else:
        print("Selecione una opción correcta\n")
    
def Change_Data_size():
    """
    Se elige que archivos se van a usar para cargar los datos usando el sufijo
    pueden ser: -small, -large, -(5,10,20,30,50,80)pct
    """
    print("Al realizar esta acción se necesitara volver a cargar el catalogo de videos")
    print("Seleccione el tamaño de los datos a cargar:")
    print("1- small")
    print("2- large")
    print("3- 5pct")
    print("4- 10pct")
    print("5- 20pct")
    print("6- 30pct")
    print("7- 50pct")
    print("8- 80pct")
    
    user_inputs = input('Seleccione una opción para continuar\n')

    if int(user_inputs[0]) == 1:
        controller_characteristics["data_size_sufijo"]="-small"
    elif int(user_inputs[0]) == 2:
        controller_characteristics["data_size_sufijo"]="-large"
    elif int(user_inputs[0]) == 3:
        controller_characteristics["data_size_sufijo"]="-5pct"
    elif int(user_inputs[0]) == 4:
        controller_characteristics["data_size_sufijo"]="-10pct"
    elif int(user_inputs[0]) == 5:
        controller_characteristics["data_size_sufijo"]="-20pct"
    elif int(user_inputs[0]) == 6:
        controller_characteristics["data_size_sufijo"]="-30pct"
    elif int(user_inputs[0]) == 7:
        controller_characteristics["data_size_sufijo"]="-50pct"
    elif int(user_inputs[0]) == 8:
        controller_characteristics["data_size_sufijo"]="-80pct"
    
    Reload()

def Change_sort_algoritm():
    """
    Se elige el tipo de algoritmo sort que se usara para organizar la informacion del catalogo
    puede ser: shell, selection o insertion
    """
    print("Al realizar esta acción se necesitara volver a cargar el catalogo de videos")
    print("Seleccione el algoritmo a usar:")
    print("1- shell")
    print("2- selection")
    print("3- insertion")
    print("4- merge")
    print("5- quick")

    user_inputs = input('Seleccione una opción para continuar\n')

    if int(user_inputs[0]) == 1:
        controller_characteristics["sort_algoritm"]="shell"
    elif int(user_inputs[0]) == 2:
        controller_characteristics["sort_algoritm"]="selection"
    elif int(user_inputs[0]) == 3:
        controller_characteristics["sort_algoritm"]="insertion"
    elif int(user_inputs[0]) == 4:
        controller_characteristics["sort_algoritm"]="merge"
    elif int(user_inputs[0]) == 5:
        controller_characteristics["sort_algoritm"]="quick"

def show_configuration():
    print("-------------------------------------------")
    print(f"TAD actual: {controller_characteristics['videos']}")
    print(f"sufijo del archivo csv: {controller_characteristics['data_size_sufijo']}")
    print(f"algoritmo sort actual: {controller_characteristics['sort_algoritm']}")
    print("--------------------------------------------")
control=newController()
#catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        print("Cargando información de los archivos ....")
        start_time=controller.Get_time()
        control=newController()
        loadData(control, controller_characteristics)
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
        #acceso a datos del registro
        #print(((control["model"]["videos"])))

    elif int(inputs[0]) == 2:
        start_time=controller.Get_time()
        year1=int(input("Año inicial: "))
        year2=int(input("Año final: "))
        Movies_by_year(control, year1, year2, controller_characteristics)
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    
    elif int(inputs[0]) == 3:
        start_time=controller.Get_time()
        print("Introduce 2 fechas en el formato %B %d, %Y (ej: January 07, 2018)")
        date1=input("fecha inicial: ")
        date2=input("fecha final: ")
        Tv_shows_by_date(control, date1, date2, controller_characteristics)
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    
    elif int(inputs[0]) == 6:
        start_time=controller.Get_time()
        country=input("Pais (en ingles): ")
        videos_by_country(control, country, controller_characteristics)
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    
    elif int(inputs[0]) == 7:
        start_time=controller.Get_time()
        director=input("Director a buscar: ")
        videos_by_director(control, director, controller_characteristics)
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    
    elif int(inputs[0]) == 8:
        start_time=controller.Get_time()
        Ntop=int(input("N top: "))
        Get_N_top(control, Ntop, controller_characteristics)
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    #elif int(inputs[0]) == 2:
    #   pass
    elif int(inputs) == 9:   
        Change_sort_algoritm()
        show_configuration()
    elif int(inputs) == 10:
        start_time=controller.Get_time()
        ChangeTAD_type("videos")
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    elif int(inputs) == 11:
        start_time=controller.Get_time()
        Change_Data_size()
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución:{controller.Delta_time(start_time,end_time)} ms")
        show_configuration()
    else:
        sys.exit(0)
sys.exit(0)

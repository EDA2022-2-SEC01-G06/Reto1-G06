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
#actualizar limites de recursion
default_limit = 1000 
sys.setrecursionlimit(default_limit*10)

controller_characteristics={
    #Este diccionario se usa como referencia para elegir el tipo de TAD al crear las listas que
    #componen al catalogo
    #tambien algunas otras caracteristicas que permiten modificar el controlador
    "videos":"ARRAY_LIST",
    "stream_services":"ARRAY_LIST",
    "data_size_sufijo":"-small",
    "sort_algoritm":"shell"
}
def newController():
    control=controller.newController(controller_characteristics)
    return control

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("9- Cambiar el algoritmo para ordenamiento de los datos")
    print("10- Elegir TAD para el catalogo de peliculas")
    print("11- Elegir tamaño del catalogo de peliculas")
    #print("3- ")
    print("0- salir")

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
    
    data = controller.loadData(control, controller_characteristics)
    cantidad_videos, stream_s_count =controller.GetDataSpecifications(control["model"])
    print("Total de datos cargados:",cantidad_videos)

    specificaciones_list=[]
    for stream_s in stream_s_count["elements"]:
        specificaciones_list.append([stream_s["name"] , stream_s["size"]])
    print(tabulate.tabulate(specificaciones_list, headers=("servicio de streaming", "total") ,floatfmt="fancy_grid"))
    print("\n---------------------------------")

    #primeros y ultimos 3   
    show_data=controller.Get_Sample_Data(control["model"], 3)
    
    #mostrar tabla

    print(tabulate.tabulate(show_data, headers="keys"))
    print("La libreria tabulate mostrara la tabla de manera incorrecta dependiendo del tamaño de la terminal")

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

    user_inputs = input('Seleccione una opción para continuar\n')

    if int(user_inputs[0]) == 1:
        controller_characteristics["sort_algoritm"]="shell"
    elif int(user_inputs[0]) == 2:
        controller_characteristics["sort_algoritm"]="selection"
    elif int(user_inputs[0]) == 3:
        controller_characteristics["sort_algoritm"]="insertion"

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

    #elif int(inputs[0]) == 2:
     #   pass
    elif int(inputs) == 9:   
        Change_sort_algoritm()
    elif int(inputs) == 10:
        start_time=controller.Get_time()
        ChangeTAD_type("videos")
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
    elif int(inputs) == 11:
        start_time=controller.Get_time()
        Change_Data_size()
        end_time=controller.Get_time()
        print(f"Tiempo de ejecución: {controller.Delta_time(start_time,end_time)} ms")
    else:
        sys.exit(0)
sys.exit(0)

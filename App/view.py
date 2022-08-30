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

def newController():
    control=controller.newController()
    return control

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
   # print("2- ")
    print("0- salir")

def loadData(control):
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
    
    data = controller.loadData(control)
    cantidad_videos, stream_s_count =controller.GetDataSpecifications(control["model"])
    print("Total de datos cargados:",cantidad_videos)

    specificaciones_list=[]
    for stream_s in stream_s_count["elements"]:
        specificaciones_list.append([stream_s["name"] , stream_s["size"]])
    print(tabulate.tabulate(specificaciones_list, headers=("servicio de streaming", "total") ,floatfmt="fancy_grid"))
    print("\n---------------------------------")

    #primeros y ultimos 3   
    primeros3=data["elements"][0:3]
    ultimos3=data["elements"][-1:-4:-1]
    show_data=primeros3+ultimos3
    
    #mostrar tabla

    print(tabulate.tabulate(show_data, headers="keys"))
    print("La libreria tabulate mostrara la tabla 1de manera incorrecta dependiendo del tamaño de la terminal")

    #return data
control=newController()
catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        loadData(control)

    #elif int(inputs[0]) == 2:
     #   pass

    else:
        sys.exit(0)
sys.exit(0)

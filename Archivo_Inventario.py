import os
from tabulate import tabulate  # Libreria para crear tablas con diseños

# Clase para representar cada artículo en el inventario
class Mercaderia:
    def __init__(self, id_unico, nombre_articulo, cantidad, precio):
        self._id_unico = id_unico
        self._nombre_articulo = nombre_articulo
        self._cantidad = cantidad
        self._precio = precio

    # Getters: Métodos para acceder a atributos de objetos.
    def id_unico(self):
        return self._id_unico

    def descripcion_articulo(self):
        return self._nombre_articulo

    def cantidad_articulo(self):
        return self._cantidad

    def precio_articulo(self):
        return self._precio

    # Setters: Métodos para modificar atributos de objetos.
    def modificar_articulo(self, nombre_articulo):
        self._nombre_articulo = nombre_articulo

    def modificar_cantidad(self, cantidad):
        self._cantidad = cantidad

    def modificar_precio(self, precio):
        self._precio = precio

# Clase para manejar el inventario
class Inventario:
    def __init__(self):
        self.articulos = []
        self.cargar_inventario()  # Cargar inventario al iniciar

    # Método para verificar si un ID ya existe
    def id_existe(self, id_unico):
        return any(p.id_unico() == id_unico for p in self.articulos)    # Verifica si algún artículo tiene el ID único especificado

    # Método para añadir un nuevo articulo al inventario
    def agregar_articulo(self, articulo):
        if not self.id_existe(articulo.id_unico()):
            self.articulos.append(articulo)
            self.guardar_inventario()  # Guardar después de agregar
            return True
        return False

    def eliminar_articulo(self, id_unico):
        for articulo in self.articulos:
            if articulo.id_unico() == id_unico:
                self.articulos.remove(articulo)
                self.guardar_inventario()  # Guardar el Inventario actualizado después de eliminar un artículo
                self.guardar_articulo_eliminado(articulo)  # Guardar el artículo eliminado en el archivo de productos_fuera_de_stock.txt
                return True
        return False

    # Método para obtener un articulo por su ID
    def obtener_articulo(self, id_unico):
        for articulo in self.articulos:
            if articulo.id_unico() == id_unico:
                return articulo
        return None

    # Método para actualizar un articulo
    def actualizar_articulo(self, id_unico, nombre=None, cantidad=None, precio=None):
        articulo = self.obtener_articulo(id_unico)
        if articulo:
            if nombre is not None:
                articulo.modificar_articulo(nombre)
            if cantidad is not None:
                articulo.modificar_cantidad(cantidad)
            if precio is not None:
                articulo.modificar_precio(precio)
            self.guardar_inventario()  # Guarda la información actualizada en el archivo inventario.txt
            return True
        return False

    # Método para buscar articulos por nombre
    def buscar_articulos(self, nombre):
        return [p for p in self.articulos if nombre.lower() in p.descripcion_articulo().lower()]

    # Método para obtener todos los articulos del inventario
    def mostrar_articulos(self):
        return self.articulos

    # Método para guardar el inventario en un archivo
    def guardar_inventario(self):
        # Implementación y manejo de excepciones ante posibles errores durante la manipulación de archivos
        try:
            with open("inventario.txt", "w", encoding='utf-8') as file:
                for articulo in self.articulos:
                    file.write(f"{articulo.id_unico()},{articulo.descripcion_articulo()},{articulo.cantidad_articulo()},{articulo.precio_articulo():.2f}\n")
            print("Inventario guardado o actualizado exitosamente.")
        except IOError as error:
            print(f"Error al guardar el inventario: {error}")

    # Método para cargar el inventario desde un archivo
    def cargar_inventario(self):
        # Implementación y manejo de excepciones ante posibles errores durante la manipulación de archivos
        try:
            if os.path.exists("inventario.txt"):
                with open("inventario.txt", "r", encoding='utf-8') as file:
                    for line in file:
                        data = line.strip().split(',')
                        if len(data) == 4:
                            id_unico, nombre, cantidad, precio = data
                            self.articulos.append(Mercaderia(id_unico, nombre, int(cantidad), float(precio)))
                print("Inventario cargado exitosamente.")
            else:
                print("El archivo de inventario no existe. Se iniciará con un inventario vacío.")
        except IOError as error:
            print(f"Error al cargar el inventario: {error}")

    # Método para guardar artículos eliminados
    def guardar_articulo_eliminado(self, articulo):
        # Implementación y manejo de excepciones ante posibles errores durante la manipulación de archivos
        try:
            with open("productos_fuera_de_stock.txt", "a", encoding='utf-8') as file:
                file.write(f"{articulo.id_unico()},{articulo.descripcion_articulo()},{articulo.cantidad_articulo()},{articulo.precio_articulo():.2f}\n")
        except IOError as error:
            print(f"Error al guardar el artículo eliminado: {error}")

# Función para convertir una cadena a float, cuando el usuario digita coma (,) en vez de punto (.)
def convertir_a_float(valor):
    # Implementación y manejo de excepción de tipo ValueError durante el ingreso del valor del artículo
    try:
        return float(valor.replace(',', '.'))
    except ValueError:
        print("Error: Ingrese un número válido.")
        return None

# Función para mostrar articulos en una tabla con diseño
def mostrar_articulos_tabla(articulos):
    # Verifica si la lista de articulos no está vacía
    if articulos:
        headers = ["ID", "Nombre", "Cantidad", "Precio"]  # Define los encabezados de la tabla
        # Crea una lista de listas con la información de cada articulo
        tabla = [[p.id_unico(), p.descripcion_articulo(), p.cantidad_articulo(), f"${float(p.precio_articulo()):.2f}"] for p in articulos]
        # Imprime la tabla con formato y el estilo "fancy_grid"
        print(tabulate(tabla, headers, tablefmt="fancy_grid"))
    else:
        # Muestra un mensaje si no hay articulos
        print("No se encontraron articulos.")

# Función para mostrar artículos eliminados
def mostrar_articulos_eliminados():
    # Implementación y manejo de excepciones ante posibles errores durante la manipulación de archivos
    try:
        if os.path.exists("productos_fuera_de_stock.txt"):
            with open("productos_fuera_de_stock.txt", "r", encoding='utf-8') as file:
                articulos = []
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 4:
                        id_unico, nombre, cantidad, precio = data
                        articulos.append(Mercaderia(id_unico, nombre, int(cantidad), float(precio)))
                if articulos:
                    print("\nArtículos eliminados del inventario:")
                    mostrar_articulos_tabla(articulos)
                else:
                    print("No hay artículos eliminados registrados.")
        else:
            print("No se ha encontrado el archivo de artículos eliminados.")
    except IOError as error:
        print(f"Error al leer el archivo de artículos eliminados: {error}")

# Función principal del programa
def main():
    inventario = Inventario()

    while True:
        print("\n" + "=" * 50)
        print("║    Papelería Compu Click Tena - Inventario     ║")
        print("=" * 50)
        print("1. Añadir nuevo articulo")
        print("2. Eliminar articulo")
        print("3. Actualizar articulo")
        print("4. Buscar articulos")
        print("5. Mostrar todos los articulos")
        print("6. Mostrar artículos eliminados del inventario")
        print("7. Salir")
        print("=" * 50)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_unico = input("Ingrese ID único del articulo: ")
            if inventario.id_existe(id_unico):
                print("Error: ID ya existe en el inventario.")
            else:
                nombre = input("Ingrese nombre del articulo: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = None
                while precio is None:
                    precio = convertir_a_float(input("Ingrese precio: "))
                articulo = Mercaderia(id_unico, nombre, cantidad, precio)
                if inventario.agregar_articulo(articulo):
                    print("Artículo añadido con éxito y guardado en el archivo.")
                else:
                    print("Error: No se pudo añadir el artículo.")

        elif opcion == "2":
            id_unico = input("Ingrese ID único del articulo a eliminar: ")
            if inventario.eliminar_articulo(id_unico):
                print("Artículo eliminado con éxito y guardado en productos fuera de stock.")
            else:
                print("Error: El ID de artículo no existe en el inventario.")

        elif opcion == "3":
            id_unico = input("Ingrese ID único del articulo a actualizar: ")
            articulo = inventario.obtener_articulo(id_unico)
            if articulo:
                print(f"\nDatos actuales del articulo:")
                print(f"Nombre: {articulo.descripcion_articulo()}")
                print(f"Cantidad: {articulo.cantidad_articulo()}")
                print(f"Precio: ${articulo.precio_articulo():.2f}")

                nuevo_nombre = input(f"\nIngrese nuevo nombre: '{articulo.descripcion_articulo()}'): ")
                nueva_cantidad = input("Ingrese nueva cantidad: ")
                nuevo_precio = input("Ingrese nuevo precio: ")

                if nuevo_nombre:
                    articulo.modificar_articulo(nuevo_nombre)
                if nueva_cantidad:
                    articulo.modificar_cantidad(int(nueva_cantidad))
                if nuevo_precio:
                    precio = convertir_a_float(nuevo_precio)
                    if precio is not None:
                        articulo.modificar_precio(precio)

                if inventario.actualizar_articulo(id_unico, nuevo_nombre, nueva_cantidad, precio):
                    print("Artículo actualizado con éxito y guardado en el archivo.")
                else:
                    print("Error: No se pudo actualizar el artículo.")
            else:
                print("Error: Articulo no encontrado.")

        elif opcion == "4":
            nombre = input("Ingrese nombre o parte del nombre del articulo a buscar: ")
            articulos = inventario.buscar_articulos(nombre)
            print("\nArticulos encontrados:")
            mostrar_articulos_tabla(articulos)

        elif opcion == "5":
            articulos = inventario.mostrar_articulos()
            print("\nTodos los articulos en inventario:")
            mostrar_articulos_tabla(articulos)

        elif opcion == "6":
            mostrar_articulos_eliminados()

        elif opcion == "7":
            print("*********** Gracias por usar el sistema de inventario de Papelería Compu Click. ¡Hasta luego! ***********")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

        input("\nPresione Enter para continuar...")

main()
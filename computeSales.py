# pylint: disable=invalid-name
"""Toma dos archivos en formato JSON, buscando el precio de venta
  en uno y la cantidad vendida en otro, para así generar el costo
  total de la venta, al final suma todos los valores y genera un
  único costo total que es impreso en pantalla y en un archivo
  junto al detalle de cada historial de ventas, bajo el nombre
  "SalesResults.txt", adicionalmente controla y
  muestra en pantalla y en el archivo los errores detectados.
"""
import sys
import json
import time


def leer_archivo_json(ruta_archivo):
    """Recibe un archivo JSON.

    Parámetro(s):
        ruta_archivo (JSON): La ruta del archivo a leer.

    Salida(s):
        Devuelve el contenido del archivo JSON leído.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Archivo '{ruta_archivo}' no encontrado en la ruta indicada.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error en la decodificación con el archivo JSON: {e}")
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"No se pudo leer el contenido del archivo JSON: {e}")
        return None


def calcular_costo_total(catalogo, ventas, errores):
    """Recorre la información recibida realizando el cálculo de la venta y
       tomando la cantidad vendida (Quantity de las ventas) multiplicándolas
       por el precio (price del catálogo), realizando el cruce con el campo
       producto (title del catálogo) y producto (Product de las ventas).

    Parámetro(s):
        Recibe el contenido del catálogo de productos, el valor de las ventas
        y una lista para almacenar los errores que se generen en el proceso.

    Salida(s):
        Devuelve costo de venta calculado y llena la lista con los errores.
    """
    if catalogo is None or ventas is None:
        return None

    costo_total = 0

    for item in ventas:
        producto = item.get('Product')
        quantity = item.get('Quantity')

        if producto and quantity:
            cruce = [
                        product for product in catalogo
                        if product.get('title') == producto
                    ]
            if cruce:
                coincidente = cruce[0]
                price = coincidente.get('price')

                if price is not None:
                    subtotal = quantity * price
                    costo_total += subtotal
                else:
                    errores.append(f"No existe precio para '{producto}'")
            else:
                errores.append(f"No se encontró el producto '{producto}'")
        else:
            errores.append("No se encontró el campo 'product' o 'Quantity'.")

    return costo_total


def escribir_archivo(
                    costo_form, tiempo_transcurrido, ventas, catalogo, errores
                    ):
    """Crea un archivo llamado SalesResults.txt con el detalle, el costo en
        formato moneda, el tiempo transcurrido en la ejecución y los errores
        encontrados durante el cálculo (en caso de existir).

    Parámetro(s):
        Recibe el costo total formateado como moneda, el tiempo transcurrido y
        la lista con los posibles errores.

    Salida(s):
        Devuelve el archivo "SalesResults.txt" con los valores indicados.
    """
    with open("SalesResults.txt", 'w', encoding='utf-8') as file:
        if len(errores) > 0:
            file.write("Se presentaron errores:\n")
            for error in errores:
                file.write("* " + error + "\n")

        file.write("\nResultado de las ventas:")
        file.write(f"\n{'Producto':40} {'Cantidad':^10} "
                   f"{'Precio Unitario':^15} {'Subtotal':^15} \n")
        file.write("-" * 80 + "\n")
        for item in ventas:
            producto = item.get('Product')
            quantity = item.get('Quantity')
            cruce = [
                    product for product in catalogo
                    if product.get('title') == producto
                ]
            if cruce:
                coincidente = cruce[0]
                price = coincidente.get('price')
                subtotal = round(quantity * price, 2)
                file.write(f"{producto:<40} {quantity:^10}"
                           f"{price:^15} {subtotal:^15}\n")
        file.write("-" * 80 + "\n")
        file.write(f"* Costo Total: {costo_form}\n")
        file.write(f"* Tiempo Transcurrido: {tiempo_transcurrido} segundos\n")


def main():  # pylint: disable=too-many-locals
    """Función principal que ejecutara las funciones requeridas"""
    if len(sys.argv) != 3:
        print("Utilice: !python computeSales.py Catalogo.json Ventas.json")
        sys.exit(1)

    ruta_archivo1 = sys.argv[1]
    ruta_archivo2 = sys.argv[2]

    catalogo = leer_archivo_json(ruta_archivo1)
    ventas = leer_archivo_json(ruta_archivo2)

    if catalogo is not None and ventas is not None:
        errores = []
        hora_inicio = time.time()
        costo_total = round(calcular_costo_total(catalogo, ventas, errores), 2)
        tiempo_transcurrido = time.time() - hora_inicio

        if len(errores) > 0:
            print("\nSe presentaron los siguientes errores:")
            for error in errores:
                print("* " + error)

        if costo_total is not None:
            costo_form = f"${costo_total:,.2f}"
            print("\nResultado de las ventas:")
            print(
                  f"\n{'Producto':40} {'Cantidad':^10} "
                  f"{'Precio Unitario':^15} {'Subtotal':^15}"
                  )
            print("-" * 80)
            for item in ventas:
                producto = item.get('Product')
                quantity = item.get('Quantity')
                cruce = [
                    product for product in catalogo
                    if product.get('title') == producto
                ]
                if cruce:
                    coincidente = cruce[0]
                    price = coincidente.get('price')
                    subtotal = round(quantity * price, 2)
                    print(
                          f"{producto:<40} {quantity:^10} "
                          f"{price:^15} {subtotal:^15}"
                          )
            print("-" * 80)
            print(f"* Costo Total: {costo_form}")
            print(f"* Tiempo Transcurrido: {tiempo_transcurrido} segundos")

            escribir_archivo(
                              costo_form,
                              tiempo_transcurrido,
                              ventas,
                              catalogo,
                              errores
                            )


if __name__ == "__main__":
    main()

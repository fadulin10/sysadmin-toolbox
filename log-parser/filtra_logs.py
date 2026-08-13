import os
import sys
from datetime import datetime
import requests


def analizer_v1(ruta_entrada,ruta_salida):
    #creamos la variable donde almacenamos el numero de errores
    errores = 0

    # Abrimos el de lectura Y el de escritura a la vez
    with open(ruta_entrada, "r") as archivo, open(ruta_salida, "a") as f_alerta:
        for linea in archivo:
        # Si está "ERROR" o "CRITICAL" en la línea...
            if "ERROR" in linea or "CRITICAL" in linea:
                f_alerta.write(linea)
                errores += 1
    ahora = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
    if errores > 0:
            mensaje_completo = f"[{ahora}] ESCANEO COMPLETADO: Se han detectado {errores} fallos, para mas informacion revisa: {os.path.abspath(ruta_salida)}"
            print(mensaje_completo)
            enviar_alerta_web(mensaje_completo)

def enviar_alerta_web(mensaje):
    # Pegas la URL que acabas de copiar de la página web
    url_webhook = "https://webhook.site/e493b1bd-51a3-4c63-b038-b6e7c32bf04b"
    datos = {"content": mensaje}
    try:
        respuesta = requests.post(url_webhook, json=datos)
        if respuesta.status_code == 204 or respuesta.status_code == 200:
            print(" Alerta enviada a la web correctamente.")
        else:
            print(f" Error al enviar. Código: {respuesta.status_code}")
    except Exception as e:
        print(f" Error de red: {e}")

  
if len(sys.argv) != 2:
    print("Error: Parámetros incorrectos.")
    print("Debes introducir exactamente UN archivo de log.")
    print("Uso correcto: python3 analizador.py <ruta_del_log>")
    sys.exit(1)  # Corta la ejecución del script inmediatamente

log_a_buscar = sys.argv[1]

carpeta_actual = os.path.dirname(os.path.abspath(__file__))
log_alertas = os.path.join(carpeta_actual, "alertas.log")

analizer_v1(log_a_buscar, log_alertas)

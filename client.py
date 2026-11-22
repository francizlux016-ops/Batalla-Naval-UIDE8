# client.py
# Jugador 2 (cliente) del modo multijugador LAN.
# Se conecta al servidor, manda sus barcos y sus disparos, y muestra lo que
# el servidor le responde. Aquí NO se revisan las reglas del juego: eso lo
# hace el servidor.

import socket
from game_logic import dibujar, pedir_flota, pedir_disparo, nombre_casilla

IP_SERVIDOR = "192.168.50.10"
PUERTO = 5000


def enviar(conexion, texto):
    """Envía un mensaje (una línea de texto) al servidor."""
    conexion.sendall((texto + "\n").encode("utf-8"))


def recibir(archivo):
    """Recibe un mensaje (una línea). Si llega vacío, el servidor se desconectó."""
    linea = archivo.readline()
    if linea == "":
        raise ConnectionError("Se perdió la conexión con el servidor")
    return linea.strip()


def iniciar_cliente():
    ip = input("IP del servidor [" + IP_SERVIDOR + "]: ").strip()
    if ip == "":
        ip = IP_SERVIDOR
    try:
        conexion = socket.create_connection((ip, PUERTO), timeout=10)
    except OSError as error:
        print("No se pudo conectar a " + ip + ":" + str(PUERTO) + " (" + str(error) + ")")
        return
    conexion.settimeout(None)
    archivo = conexion.makefile("r", encoding="utf-8")   # para leer línea por línea

    try:
        while True:
            partes = recibir(archivo).split("|")
            tipo = partes[0]

            if tipo == "MENSAJE":
                print(partes[1])
            elif tipo == "COLOCAR":
                print("\n--- Jugador 2: coloca tus barcos ---")
                tablero, barcos, textos = pedir_flota()
                enviar(conexion, "BARCOS|" + textos[0] + "|" + textos[1])
                print("\nEsperando al Jugador 1...")
            elif tipo == "ERROR":
                print("Error:", partes[1])
            elif tipo == "TURNO":
                dibujar(partes[1], "Tu tablero")
                dibujar(partes[2], "Tablero del rival")
                print("\n=== Tu turno (Jugador 2) ===")
                fila, col = pedir_disparo()
                enviar(conexion, "DISPARO|" + nombre_casilla(fila, col))
            elif tipo == "RESULTADO":
                print("\n" + partes[1])
            elif tipo == "FIN":
                print("\n" + partes[1])
                dibujar(partes[2], "Tu tablero")
                dibujar(partes[3], "Tablero del rival")
                break
    except (ConnectionError, OSError) as error:
        print("\nAviso: " + str(error) + ". La partida terminó.")
    conexion.close()


if __name__ == "__main__":
    iniciar_cliente()

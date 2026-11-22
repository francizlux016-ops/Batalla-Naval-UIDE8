# server.py
# Jugador 1 (servidor) del modo multijugador LAN.
# Crea el socket TCP, espera al cliente, valida los disparos, controla los
# turnos y decide quién gana.
#
# Los mensajes entre servidor y cliente son líneas de texto con partes
# separadas por "|". Ejemplos:
#   servidor -> cliente:  COLOCAR   ERROR|texto   TURNO|tu_tablero|tablero_rival
#                         RESULTADO|texto|tu_tablero|tablero_rival   FIN|texto|...
#   cliente -> servidor:  BARCOS|A1 H|A3 V   DISPARO|C4

import socket
from game_logic import (
    dibujar, pedir_flota, pedir_disparo, describir_disparo, crear_flota,
    validar_casilla, convertir_casilla, disparar, todos_hundidos, tablero_a_texto,
)

PUERTO = 5000


def enviar(conexion, texto):
    """Envía un mensaje (una línea de texto) al cliente."""
    conexion.sendall((texto + "\n").encode("utf-8"))


def recibir(archivo):
    """Recibe un mensaje (una línea). Si llega vacío, el cliente se desconectó."""
    linea = archivo.readline()
    if linea == "":
        raise ConnectionError("El Jugador 2 perdió la conexión")
    return linea.strip()


def jugar(conexion, archivo):
    # 1) Cada jugador coloca sus barcos
    print("\n--- Jugador 1: coloca tus barcos ---")
    tablero1, barcos1, textos = pedir_flota()
    print("\nEsperando a que el Jugador 2 coloque sus barcos...")
    while True:
        enviar(conexion, "COLOCAR")
        partes = recibir(archivo).split("|")
        if len(partes) == 3 and partes[0] == "BARCOS":
            tablero2, barcos2, error = crear_flota(partes[1], partes[2])
        else:
            error = "Mensaje inesperado"
        if error == "":
            break
        enviar(conexion, "ERROR|Colocación inválida: " + error)

    # 2) Turnos: empieza el Jugador 1
    turno = 1
    while True:
        if turno == 1:
            # Turno del servidor (se juega con el teclado de esta computadora)
            while True:
                print("\n=== Tu turno (Jugador 1) ===")
                dibujar(tablero_a_texto(tablero1, True), "Tu tablero")
                dibujar(tablero_a_texto(tablero2, False), "Tablero del rival")
                fila, col = pedir_disparo()
                resultado, hundido = disparar(tablero2, barcos2, fila, col)
                if resultado == "REPETIDO":
                    print("Error: Ya se disparó a esa casilla")
                else:
                    break
            tablero_rival = tablero2
            barcos_rival = barcos2
        else:
            # Turno del cliente: le mandamos el estado y esperamos su disparo
            print("\nEsperando el disparo del Jugador 2...")
            while True:
                enviar(conexion, "TURNO|" + tablero_a_texto(tablero2, True) + "|" + tablero_a_texto(tablero1, False))
                partes = recibir(archivo).split("|")
                if len(partes) == 2 and partes[0] == "DISPARO" and validar_casilla(partes[1]) == "":
                    fila, col = convertir_casilla(partes[1])
                    resultado, hundido = disparar(tablero1, barcos1, fila, col)
                    if resultado == "REPETIDO":
                        enviar(conexion, "ERROR|Ya se disparó a esa casilla")
                    else:
                        break
                else:
                    enviar(conexion, "ERROR|Disparo inválido")
            tablero_rival = tablero1
            barcos_rival = barcos1

        # 3) Mostrar el resultado y avisar al cliente
        texto = describir_disparo(turno, fila, col, resultado, hundido)
        print("\n" + texto)
        estado = "|" + tablero_a_texto(tablero2, True) + "|" + tablero_a_texto(tablero1, False)

        if todos_hundidos(tablero_rival, barcos_rival):
            print("\n¡Fin de la partida! Gana el Jugador " + str(turno) + ".")
            enviar(conexion, "FIN|" + texto + " ¡Fin de la partida! Gana el Jugador " + str(turno) + "." + estado)
            return
        enviar(conexion, "RESULTADO|" + texto + estado)

        if turno == 1:
            turno = 2
        else:
            turno = 1


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conexion = None
    try:
        servidor.bind(("0.0.0.0", PUERTO))   # escucha en todas las interfaces de red
        servidor.listen(1)
        print("Servidor escuchando en el puerto " + str(PUERTO) + ". Esperando al Jugador 2...")
        conexion, direccion = servidor.accept()
        print("Jugador 2 conectado desde " + direccion[0])
        archivo = conexion.makefile("r", encoding="utf-8")   # para leer línea por línea
        enviar(conexion, "MENSAJE|Conexión establecida. Eres el Jugador 2.")
        jugar(conexion, archivo)
    except (ConnectionError, OSError) as error:
        print("\nAviso: " + str(error) + ". La partida terminó.")
    if conexion is not None:
        conexion.close()
    servidor.close()


if __name__ == "__main__":
    iniciar_servidor()

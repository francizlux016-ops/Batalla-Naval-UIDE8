# juego.py
# Programa principal: muestra el menú y tiene el modo local.
# Para jugar se ejecuta este archivo:  python3 juego.py

from game_logic import (
    dibujar, pedir_flota, pedir_disparo, describir_disparo,
    mostrar_instructivo, disparar, todos_hundidos, tablero_a_texto,
)
from server import iniciar_servidor
from client import iniciar_cliente


def limpiar_pantalla():
    """Deja la pantalla en blanco para que el otro jugador no vea los barcos."""
    print("\n" * 40)


def modo_local():
    # Cada jugador coloca sus barcos
    input("\nJugador 1: presiona Enter cuando el otro jugador no esté mirando...")
    print("--- Jugador 1: coloca tus barcos ---")
    tablero1, barcos1, textos = pedir_flota()
    input("Presiona Enter para ocultar tu tablero...")
    limpiar_pantalla()

    input("\nJugador 2: presiona Enter cuando el otro jugador no esté mirando...")
    print("--- Jugador 2: coloca tus barcos ---")
    tablero2, barcos2, textos = pedir_flota()
    input("Presiona Enter para ocultar tu tablero...")
    limpiar_pantalla()

    # Turnos: empieza el Jugador 1
    turno = 1
    while True:
        # El jugador dispara al tablero del otro
        if turno == 1:
            tablero_rival = tablero2
            barcos_rival = barcos2
        else:
            tablero_rival = tablero1
            barcos_rival = barcos1

        print("\n=== Turno del Jugador " + str(turno) + " ===")
        dibujar(tablero_a_texto(tablero_rival, False), "Tablero del rival")
        fila, col = pedir_disparo()
        resultado, hundido = disparar(tablero_rival, barcos_rival, fila, col)
        if resultado == "REPETIDO":
            print("Error: Ya se disparó a esa casilla")
            continue

        print(describir_disparo(turno, fila, col, resultado, hundido))
        if todos_hundidos(tablero_rival, barcos_rival):
            dibujar(tablero_a_texto(tablero_rival, False), "Tablero final del rival")
            print("\n¡Fin de la partida! Gana el Jugador " + str(turno) + ".")
            return

        if turno == 1:
            turno = 2
        else:
            turno = 1


def menu():
    while True:
        print("\n=== BATALLA NAVAL SIMPLIFICADA ===")
        print("1. Modo local (2 jugadores, 1 computadora)")
        print("2. Multijugador LAN - Jugador 1 (servidor)")
        print("3. Multijugador LAN - Jugador 2 (cliente)")
        print("4. Cómo jugar (instructivo)")
        print("5. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            modo_local()
        elif opcion == "2":
            iniciar_servidor()
        elif opcion == "3":
            iniciar_cliente()
        elif opcion == "4":
            mostrar_instructivo()
        elif opcion == "5":
            print("¡Hasta luego!")
            return
        else:
            print("Opción inválida.")


menu()

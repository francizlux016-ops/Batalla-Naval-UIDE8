# game_logic.py
# Reglas del juego Batalla Naval Simplificada (tablero de 5x5).
# Las funciones de este archivo las usan juego.py, server.py y client.py.
#
# Las casillas se escriben con LETRA + NÚMERO (ejemplo: C4)
#   letra  = columna (A a E, de izquierda a derecha)
#   número = fila    (1 a 5, de arriba hacia abajo)
# Los barcos se escriben con casilla + orientación (ejemplo: A1 H)
#   H = horizontal (crece hacia la derecha), V = vertical (crece hacia abajo)

TAMANO = 5            # el tablero es de 5 x 5
LETRAS = "ABCDE"      # letras de las columnas
LARGOS = [2, 3]       # un barco de 2 casillas y otro de 3

# Símbolos del tablero:
#   .  casilla sin disparar      B  barco
#   X  impacto                   o  agua (disparo fallado)


# ---------- Tablero ----------

def crear_tablero():
    """Crea un tablero de 5x5 lleno de agua (puntos)."""
    tablero = []
    for i in range(TAMANO):
        fila = []
        for j in range(TAMANO):
            fila.append(".")
        tablero.append(fila)
    return tablero


def tablero_a_texto(tablero, mostrar_barcos):
    """Convierte el tablero en un texto de 25 caracteres.
    Si mostrar_barcos es False, los barcos se esconden (se ven como agua)."""
    texto = ""
    for fila in tablero:
        for celda in fila:
            if celda == "B" and not mostrar_barcos:
                texto = texto + "."
            else:
                texto = texto + celda
    return texto


# ---------- Revisar lo que escribe el jugador ----------

def validar_casilla(texto):
    """Revisa una casilla como C4. Devuelve "" si está bien o un mensaje de error."""
    texto = texto.replace(" ", "").upper()
    if len(texto) != 2:
        return "Escribe letra y número, por ejemplo: C4"
    if texto[0] not in LETRAS or texto[1] not in "12345":
        return "La letra debe ser de A a E y el número de 1 a 5"
    return ""


def convertir_casilla(texto):
    """Convierte una casilla válida (C4) en fila y columna (empiezan en 0)."""
    texto = texto.replace(" ", "").upper()
    col = LETRAS.index(texto[0])
    fila = int(texto[1]) - 1
    return fila, col


def nombre_casilla(fila, col):
    """Convierte fila y columna en el nombre de la casilla (ejemplo: C4)."""
    return LETRAS[col] + str(fila + 1)


def validar_barco(texto):
    """Revisa un barco como A1 H. Devuelve "" si está bien o un mensaje de error."""
    texto = texto.replace(" ", "").upper()
    if len(texto) != 3 or texto[2] not in "HV":
        return "Escribe casilla y orientación H o V, por ejemplo: A1 H"
    return validar_casilla(texto[0:2])


# ---------- Barcos ----------

def casillas_del_barco(fila, col, largo, orientacion):
    """Devuelve la lista de casillas que ocuparía el barco."""
    casillas = []
    for i in range(largo):
        if orientacion == "H":
            casillas.append([fila, col + i])
        else:
            casillas.append([fila + i, col])
    return casillas


def colocar_barco(tablero, barcos, largo, texto):
    """Coloca un barco en el tablero. Devuelve "" si se pudo o un mensaje de error."""
    error = validar_barco(texto)
    if error != "":
        return error
    texto = texto.replace(" ", "").upper()
    fila, col = convertir_casilla(texto[0:2])
    orientacion = texto[2]
    casillas = casillas_del_barco(fila, col, largo, orientacion)
    for casilla in casillas:
        if casilla[0] >= TAMANO or casilla[1] >= TAMANO:
            return "El barco se sale del tablero"
        if tablero[casilla[0]][casilla[1]] == "B":
            return "El barco se superpone con otro"
    for casilla in casillas:
        tablero[casilla[0]][casilla[1]] = "B"
    barcos.append(casillas)
    return ""


def crear_flota(texto1, texto2):
    """Arma un tablero con los dos barcos (se usa en el servidor)."""
    tablero = crear_tablero()
    barcos = []
    error = colocar_barco(tablero, barcos, LARGOS[0], texto1)
    if error == "":
        error = colocar_barco(tablero, barcos, LARGOS[1], texto2)
    return tablero, barcos, error


# ---------- Disparos ----------

def barco_hundido(tablero, barco):
    """Un barco está hundido cuando todas sus casillas son X."""
    for casilla in barco:
        if tablero[casilla[0]][casilla[1]] != "X":
            return False
    return True


def disparar(tablero, barcos, fila, col):
    """Dispara a una casilla. Devuelve el resultado y el largo del barco hundido
    (0 si no se hundió ninguno). El resultado es AGUA, IMPACTO o REPETIDO."""
    if tablero[fila][col] == "X" or tablero[fila][col] == "o":
        return "REPETIDO", 0
    if tablero[fila][col] == "B":
        tablero[fila][col] = "X"
        for barco in barcos:
            if [fila, col] in barco and barco_hundido(tablero, barco):
                return "IMPACTO", len(barco)
        return "IMPACTO", 0
    tablero[fila][col] = "o"
    return "AGUA", 0


def todos_hundidos(tablero, barcos):
    """Devuelve True si ya no queda ningún barco a flote."""
    for barco in barcos:
        if not barco_hundido(tablero, barco):
            return False
    return True


def describir_disparo(jugador, fila, col, resultado, largo_hundido):
    """Arma el mensaje del disparo, por ejemplo: Jugador 1 disparó a C4: IMPACTO."""
    texto = "Jugador " + str(jugador) + " disparó a " + nombre_casilla(fila, col) + ": " + resultado
    if largo_hundido > 0:
        texto = texto + " - ¡HUNDIDO! (Barco de " + str(largo_hundido) + ")"
    return texto


# ---------- Pantalla ----------

def dibujar(texto, titulo):
    """Dibuja el tablero con cuadros. 'texto' son los 25 caracteres del tablero."""
    print("\n" + titulo)
    print("     A   B   C   D   E")
    print("   ┌───┬───┬───┬───┬───┐")
    for i in range(TAMANO):
        fila = texto[i * 5: i * 5 + 5]
        print(" " + str(i + 1) + " │ " + " │ ".join(fila) + " │")
        if i < TAMANO - 1:
            print("   ├───┼───┼───┼───┼───┤")
    print("   └───┴───┴───┴───┴───┘")


def mostrar_instructivo():
    """Explica cómo se juega."""
    print("""
╔══════════════════ CÓMO JUGAR ══════════════════╗
  OBJETIVO: hundir los 2 barcos del rival.

  CASILLAS: LETRA + NÚMERO (ejemplo: C4)
     La letra (A-E) es la columna, de izquierda a derecha.
     El número (1-5) es la fila, de arriba hacia abajo.

  1) COLOCAR TUS BARCOS (uno de 2 y uno de 3 casillas)
     Escribe:  casilla + orientación     Ejemplo:  A1 H
       H = HORIZONTAL (crece hacia la derecha)
       V = VERTICAL   (crece hacia abajo)
     Un barco de 3 en "A1 H" ocupa A1 B1 C1.
     Un barco de 3 en "A1 V" ocupa A1 A2 A3.
     No puede salirse del tablero ni tocar otro barco.

  2) DISPARAR
     Escribe solo la casilla:            Ejemplo:  C4

  SÍMBOLOS:  .  casilla sin disparar     B  tu barco
             X  impacto                  o  agua (fallaste)
╚════════════════════════════════════════════════╝""")


def pedir_flota():
    """Pide al jugador que coloque sus dos barcos.
    Devuelve el tablero, la lista de barcos y los textos escritos (ej. A1 H)."""
    mostrar_instructivo()
    tablero = crear_tablero()
    barcos = []
    textos = []
    for largo in LARGOS:
        while True:
            dibujar(tablero_a_texto(tablero, True), "Tu tablero")
            texto = input("Coloca el barco de " + str(largo) + " casillas -> casilla y H/V (ej. A1 H; H=horizontal, V=vertical): ")
            error = colocar_barco(tablero, barcos, largo, texto)
            if error == "":
                textos.append(texto)
                break
            print("Error:", error)
    dibujar(tablero_a_texto(tablero, True), "Tu tablero final")
    return tablero, barcos, textos


def pedir_disparo():
    """Pide una casilla hasta que sea válida. Devuelve fila y columna."""
    while True:
        texto = input("Dispara -> casilla (ej. C4): ")
        error = validar_casilla(texto)
        if error == "":
            return convertir_casilla(texto)
        print("Error:", error)

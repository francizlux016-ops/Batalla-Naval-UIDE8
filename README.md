# Batalla Naval Simplificada

Proyecto Integrador – Universidad Internacional del Ecuador (UIDE)
Ingeniería en Sistemas de Información · Equipo Nro 8

Juego de Batalla Naval en Python (tablero 5×5, un barco de 2 y uno de 3 casillas) con **modo local** y **modo multijugador LAN** (cliente-servidor con sockets TCP).

## Integrantes
- Francis Simba
- Joaquín Haro
- Dylan Andi

## Estructura del proyecto
```
ProyectoJuego/
├── juego.py        # Menú principal y modo local
├── server.py       # Jugador 1: servidor TCP (valida jugadas, turnos y ganador)
├── client.py       # Jugador 2: cliente TCP (interfaz y envío de disparos)
├── game_logic.py   # Reglas del juego y validaciones (compartido)
├── LICENSE         # Licencia MIT
└── README.md
```

## Requisitos
- Python 3.8 o superior. **No se necesitan librerías externas**: solo se usa `socket`, que ya viene con Python.

## Cómo ejecutar
**Modo local:** `python3 juego.py` → opción 1.

**Modo LAN (dos máquinas virtuales, subred 192.168.50.0/24, puerto 5000):**
1. VM 1 (servidor, IP 192.168.50.10): `python3 juego.py` → opción 2 (o `python3 server.py`).
2. VM 2 (cliente, IP 192.168.50.11): `python3 juego.py` → opción 3 (o `python3 client.py`) e ingresar la IP del servidor.

**Casillas: letra + número** (como en la Batalla Naval clásica). La letra (A a E) es la columna, de izquierda a derecha, y el número (1 a 5) es la fila, de arriba hacia abajo. Ejemplo: `C4`.
- **Barcos:** casilla + orientación (ej. `A1 H`). **H = horizontal** (crece hacia la derecha) y **V = vertical** (crece hacia abajo).
- **Disparos:** solo la casilla (ej. `C4`).
- **Símbolos del tablero:** `.` casilla sin disparar · `B` barco · `X` impacto · `o` agua (fallo).
El juego muestra un **instructivo** al colocar los barcos y en la opción 4 del menú.

## Diseño de red
- Protocolo: TCP. Los mensajes son líneas de texto con partes separadas por `|` (por ejemplo `DISPARO|C4`, `RESULTADO|...`).
- El servidor es la autoridad: valida cada jugada, calcula el resultado y envía el estado actualizado al cliente.
- El cliente nunca recibe la posición de los barcos del rival.
- Si un jugador pierde la conexión, el otro recibe un aviso y el programa termina sin errores.

## Licencia
Este proyecto se distribuye bajo la licencia **MIT** (ver archivo `LICENSE`).

## Declaración de autoría y créditos
- **Autoría:** el diseño (Fase 1 y 2), la arquitectura y la integración del proyecto son del equipo: Francis Simba, Joaquín Haro y Dylan Andi.
- **Librerías de terceros:** ninguna. Solo se usa la biblioteca estándar de Python (`socket`), distribuida bajo la licencia de Python Software Foundation.
- **Uso de IA:** se utilizó **Claude (Anthropic)** como asistente y asesor técnico durante esta fase.
- **Código de terceros / recursos visuales:** no se copió código de otras fuentes ni se usaron imágenes externas en el código. El logo de la UIDE aparece solo en el informe académico.
- **Diagramas:** elaborados por el equipo (Fase 2); ver carpeta `docs/`.

## Bitácora de gestión de conflictos
Ver [BITACORA_CONFLICTOS.md](BITACORA_CONFLICTOS.md).

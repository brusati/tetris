import tetris
import gamelib

ESPERA_DESCENDER = 15
FACTOR_ESPERA = 5
ESPERA_MINIMA = 7

SALIR = "Escape"
DIMENSION_CELDA = 30
IZQUIERDA = "Left"
DERECHA = "Right"
ARRIBA = "Up"
ABAJO = "Down"
PUNTAJES = "puntajes.txt"
ACTUAL = "actual"
FOTOS = "fotos"

def dibujar(juego):
	ancho, largo = tetris.dimensiones()
	gamelib.resize(DIMENSION_CELDA * ancho, DIMENSION_CELDA * largo)
	gamelib.draw_begin()
	for f in range(largo):
		fila = DIMENSION_CELDA * f
		for c in range(ancho):
			columna = DIMENSION_CELDA * c
			gamelib.draw_image('img/otros1.gif', columna, fila)
			if tetris.hay_superficie(juego, c, f):
				n = juego[FOTOS][(c, f)]
				gamelib.draw_image(f"img/{n}.gif", columna, fila)
			elif (c, f) in tetris.pieza_actual(juego):
				n = juego[FOTOS][ACTUAL]
				gamelib.draw_image(f"img/{n}.gif", columna, fila)
	gamelib.draw_end()

def puntajes(puntos):
	tabla = []
	with open(PUNTAJES, 'r') as archivo:
		for linea in archivo:
			puntaje, nombre = linea.rstrip().split(",")
			tabla.append((int(puntaje), nombre.lstrip(" ")))

		if len(tabla) >= 10 and puntos < min(tabla)[0]:
			juego = tetris.crear_juego(tetris.generar_pieza())
			puntos = 0

		else:
			nombre = gamelib.input("Estás entre los 10 mejores registros! Tu nombre es: ")
			if nombre:
				tabla.append((puntos, nombre))
				sorted(tabla)
				if len(tabla) >= 10:
					tabla.remove(min(tabla))

		c = ""
		for puntaje, nombre in tabla:
			c += f"-{nombre}: {puntaje}\n"
		gamelib.say(c)

	with open(PUNTAJES, 'w') as archivo:
		for puntaje, nombre in tabla:
			archivo.write(f"{puntaje}, {nombre}\n")

def manejar_tecla(juego, tecla):
	if tecla == IZQUIERDA:
		juego = tetris.mover(juego, -1)
	elif tecla == DERECHA:
		juego = tetris.mover(juego, 1)
	elif tecla == ARRIBA:
		juego = tetris.rotar(juego)
	elif tecla == ABAJO:
		juego, ok = tetris.avanzar(juego)
		return ok
	return False

def manejar_puntos(puntos, repeticiones, espera_descender):
	puntos += 10
	gamelib.play_sound('win_sound.wav')
	repeticiones += 1
	if repeticiones % FACTOR_ESPERA == 0 and espera_descender >= ESPERA_MINIMA:
		espera_descender -= 1
	return puntos, repeticiones, espera_descender


def main():
	juego = tetris.crear_juego()
	gamelib.resize(400, 400)
	gamelib.title("Tetris")
	espera_descender = ESPERA_DESCENDER
	timer_bajar = espera_descender
	puntos = 0
	repeticiones = 0
	salir = False

	while gamelib.loop(fps=30) and not salir:
		dibujar(juego)
		if tetris.terminado(juego):
			espera_descender = ESPERA_DESCENDER
			timer_bajar = ESPERA_DESCENDER
			repeticiones = 0
			puntajes(puntos)
			juego = tetris.crear_juego()
			puntos = 0

		for event in gamelib.get_events():
			if not event:
				break
			if event.type == gamelib.EventType.KeyPress:
				tecla = event.key
				if tecla == SALIR:
					salir = True
				ok = manejar_tecla(juego, tecla)
				if ok:
					puntos, repeticiones, espera_descender = manejar_puntos(puntos, repeticiones, espera_descender)

		timer_bajar -= 1
		if timer_bajar == 0:
			timer_bajar = espera_descender
			juego, ok = tetris.avanzar(juego)
			if ok:
				puntos, repeticiones, espera_descender = manejar_puntos(puntos, repeticiones, espera_descender)

gamelib.init(main)
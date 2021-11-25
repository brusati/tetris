import random

ANCHO_JUEGO, ALTO_JUEGO = 15, 20
IZQUIERDA, DERECHA = -1, 1
CANT_FOTOS = 10
ACTUAL = "actual"
FOTOS = "fotos"
PIEZAS = (
	(((0, 0), (1, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (0, 1), (1, 1))), #cubo
	(((0, 0), (1, 0), (1, 1), (2, 1)), ((0, 0), (0, 1), (1, -1), (1, 0))), #zig-zag
	(((0, 0), (0, 1), (1, 1), (1, 2)), ((0, 0), (1, -1), (1, 0), (2, -1))), #zig-zag hacia el otro lado
	(((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 0), (2, 0), (3, 0))), #línea
	(((0, 0), (0, 1), (0, 2), (1, 2)), ((0, 0), (0, 1), (1, 0), (2, 0)), ((0, 0), (1, 0), (1, 1), (1, 2)), ((0, 0), (1, 0), (2, -1), (2, 0))), #l
	(((0, 0), (1, 0), (2, 0), (2, 1)), ((0, 0), (1, -2), (1, -1), (1, 0)), ((0, 0), (1, 0), (2, -1), (2, 0)), ((0, 0), (0, 1), (0, 2), (1, 0))), #-l
	(((0, 0), (1, 0), (1, 1), (2, 0)), ((0, 0), (1, -1), (1, 0), (1, 1)), ((0, 0), (1, -1), (1, 0), (2, 0)), ((0, 0), (0, 1), (0, 2), (1, 1))), #t
)

def generar_pieza():
	n = random.randrange(len(PIEZAS))
	pieza = trasladar_pieza(PIEZAS[n][0], ANCHO_JUEGO // 2 - 1, 0)
	return pieza, n

def trasladar_pieza(pieza, dx, dy):
	nueva = []
	for x, y in pieza:
		nueva.append((x + dx, y + dy))
	return tuple(nueva)

def rotar(juego):
	pieza_ordenada = sorted(juego[ACTUAL])
	x, y = pieza_ordenada[0]
	pieza_en_origen = trasladar_pieza(pieza_ordenada, -1 * x, -1 * y)
	siguiente_rotacion = None
	n = 0
	for i1, j1 in enumerate(PIEZAS):
		for i2, j2 in enumerate(j1):
			if pieza_en_origen == j2: #encontré la pieza en PIEZAS
				if (i2 + 1) < len(j1):
					n = i2 + 1
				siguiente_rotacion = PIEZAS[i1][n]
	if siguiente_rotacion:
		pieza_ordenada = trasladar_pieza(siguiente_rotacion, x, y)
		for x, y in pieza_ordenada: #hay veces que no se puede hacer la rotación porque "se va" de la pantalla
			if x < 0 or x >= ANCHO_JUEGO or y >= ALTO_JUEGO or (x, y) in juego:
				return juego
	juego[ACTUAL] = pieza_ordenada
	return juego

def crear_juego():
	pieza, n = generar_pieza()
	fotos = {ACTUAL: n}
	juego = {FOTOS: fotos, ACTUAL: pieza}
	return juego

def dimensiones():
	return (ANCHO_JUEGO, ALTO_JUEGO)

def pieza_actual(juego):
	return juego[ACTUAL]

def hay_superficie(juego, x, y):
	return juego.get((x, y), False)

def mover(juego, direccion):
	pieza = juego[ACTUAL]
	nueva = []
	for x, y in pieza:
		x += direccion
		if x < 0 or x >= ANCHO_JUEGO or (x, y) in juego:
			return juego
		nueva.append((x, y))
	juego[ACTUAL] = tuple(nueva)
	return juego

def terminado(juego):
	for y in range(3):
		for x in range(ANCHO_JUEGO):
			if juego.get((x, y), False):
				return True
	return False

def avanzar(juego):
	if terminado(juego):
		return (juego, False)

	nueva = []
	pared = False

	for x, y in juego[ACTUAL]:
		y += 1
		if juego.get((x, y), False) or y == ALTO_JUEGO:
			pared = True
		nueva.append((x, y))

	suma = False
	if pared: #si hay que unir a pared consolidada
		for x, y in juego[ACTUAL]:
			juego[(x, y)] = True #agregamos la nueva parte de la pared al diccionario
			juego[FOTOS][(x, y)] = juego[FOTOS][ACTUAL]
		for y in range(ALTO_JUEGO): #elimino líneas completas
			completo = True
			for x in range(ANCHO_JUEGO):
				if not juego.get((x, y), False):
					completo = False
			if completo: #encontré completa la línea y
				suma = True
				for x in range(ANCHO_JUEGO): #elimino esa línea del diccionario
					juego[(x, y)] = False
					for j in range(y - 1, -1, -1): #hago caer lo que está arriba
						if juego.get((x, j), False):
							juego[(x, j)] = False
							juego[(x, j + 1)] = True
							juego[FOTOS][(x, j + 1)] = juego[FOTOS][(x, j)]
		pieza, n = generar_pieza()
		juego[FOTOS][ACTUAL] = n
		juego[ACTUAL] = pieza
		return (juego, suma)

	juego[ACTUAL] = tuple(nueva)
	return (juego, suma)
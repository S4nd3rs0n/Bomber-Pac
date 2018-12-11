from random import choice
from turtle import *
from freegames import floor, vector
import random 
import turtle
import time
import os

#veocidades dos personagens:
velocidade_player = 10
velocidade_inimigo = 5
velocidade_inimigo2 = 7
velocidade_inimigo3 = 10

#coordenada x y:
placar = {'score': 0}
caminho = Turtle(visible=False)
escrever = Turtle(visible=False)
direção = vector(5, 0)
tiros = []

#posisão do player:
pos = [-200, -180]
player = vector(pos[0], pos[1])

#posisão do inimigo:
inimigos = [
	[vector(0, -80), vector(velocidade_inimigo, 0)],
	[vector(-200, 100), vector(0, velocidade_inimigo)],
	[vector(160, -20), vector(0, -velocidade_inimigo)],
	[vector(100, 160), vector(-velocidade_inimigo, 0)],
]
inimigos2 = [
	[vector(-100, -100), vector(0, velocidade_inimigo2)],
	[vector(60, -170), vector(0, -velocidade_inimigo2)],
	[vector(60, 70), vector(-velocidade_inimigo2, 0)],
	[vector(-140, 70), vector(-velocidade_inimigo2, 0)],
]
mapa = [
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	1, 2, 2, 0, 1, 2, 0, 2, 2, 0, 2, 1, 2, 2, 0, 1, 2, 0, 2, 0,
	2, 0, 3, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1, 0,
	2, 0, 0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0,
	2, 0, 2, 0, 2, 0, 0, 2, 2, 0, 2, 0, 2, 3, 0, 0, 0, 0, 2, 0,
	2, 0, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0,
	2, 2, 2, 3, 2, 2, 0, 0, 2, 0, 1, 0, 2, 2, 0, 0, 2, 0, 2, 0,
	2, 0, 2, 0, 2, 2, 0, 2, 1, 0, 0, 0, 2, 0, 0, 1, 2, 0, 2, 0,
	2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,
	2, 0, 2, 2, 2, 2, 1, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 0, 0, 0,
	1, 0, 1, 0, 2, 2, 0, 0, 2, 0, 2, 0, 2, 1, 0, 0, 2, 2, 2, 0,
	0, 0, 2, 2, 2, 2, 0, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 0, 2, 0,
	2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 0, 2, 0,
	2, 0, 2, 0, 2, 2, 1, 2, 2, 0, 1, 0, 2, 0, 3, 2, 2, 2, 2, 0,
	1, 0, 2, 0, 2, 3, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0,
	0, 0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 0,
	2, 2, 2, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0,
	2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 0,
	2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 3, 2, 0, 2, 2, 1, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

#Adiciona inimigos no jogo:
def adiciona():
	aux = [
	[vector(-160, -180), vector(velocidade_inimigo, 0)],
	[vector(160, 160), vector(velocidade_inimigo, 0)]
	]
	inimigos.append(choice(aux))

#desenha o quadrado na tela:
def quadrado(x, y):
	caminho.up()
	caminho.goto(x, y)
	caminho.down()
	caminho.begin_fill()

	for count in range(4):
		caminho.forward(20)
		caminho.left(90)

	caminho.end_fill()

#retorna a posição de um ponto na tela:
def delocamento(pontos):
	x = (floor(pontos.x, 20) + 200) / 20
	y = (180 - floor(pontos.y, 20)) / 20
	index = int(x + y * 20)
	return index

#retorna se o ponto é válido:
def valido(pontos):
	index = delocamento(pontos)

	if mapa[index] == 0:
		return False

	index = delocamento(pontos + 19)

	if mapa[index] == 0:
		return False

	return pontos.x % 20 == 0 or pontos.y % 20 == 0

#desenha o mapa do jogo:
def mundo():
	bgcolor('black')
	caminho.color('brown')

	for index in range(len(mapa)):
		tile = mapa[index]

		if tile > 0:
			x = (index % 20) * 20 - 200
			y = 180 - (index // 20) * 20
			quadrado(x, y)

			if tile == 1:
				caminho.up()
				caminho.goto(x + 10, y + 10)
				caminho.dot(5, 'blue')
			if tile == 2:
				caminho.up()
				caminho.goto(x + 10, y + 10)
				caminho.dot(4, 'cyan')
			if tile == 3:
				caminho.up()
				caminho.goto(x + 10, y + 10)
				caminho.dot(6, 'gray')

def move():
#apaga a ultima posição:
	escrever.undo()
#atualiza o placar:
	escrever.write(placar['score'])
#limpa a tela:
	clear()
#movimenta o player:
	if valido(player + direção):
		player.move(direção)
#pega o idice do mapa do player:
	index = delocamento(player)
#apaga a fruta e atualiza o placar:
	if mapa[index] == 1:
		mapa[index] = 5
		placar['score'] += 5
		x = (index % 20) * 20 - 200
		y = 180 - (index // 20) * 20
		quadrado(x, y)
	up()
	goto(player.x + 10, player.y + 10)
	dot(20, 'yellow')

	if mapa[index] == 2:
		mapa[index] = 5
		placar['score'] += 1
		x = (index % 20) * 20 - 200
		y = 180 - (index // 20) * 20
		quadrado(x, y)
	up()
	goto(player.x + 10, player.y + 10)
	dot(20, 'yellow')

	if mapa[index] == 3:
		mapa[index] = 5
		placar['score'] += 10
		x = (index % 20) * 20 - 200
		y = 180 - (index // 20) * 20
		quadrado(x, y)
	up()
	goto(player.x + 10, player.y + 10)
	dot(20, 'yellow')

#movimentação das balas
	for tiro in tiros:
		if valido(tiro+direção):
			tiro.move(direção)
		goto(tiro.x + 10, tiro.y + 10)
		dot(9, 'red')	

#movimentação dos inimigos:
	for pontos, course in inimigos:
		if valido(pontos + course):
			pontos.move(course)
		else:
			options = [
				vector(velocidade_inimigo, 0),
				vector(-velocidade_inimigo, 0),
				vector(0, velocidade_inimigo),
				vector(0, -velocidade_inimigo),
			]
			plan = choice(options)
			course.x = plan.x
			course.y = plan.y

		up()
		goto(pontos.x + 10, pontos.y + 10)
		dot(20, 'red')

	update()

	for pontos, course in inimigos:
		if abs(player - pontos) < 20:
			placar['score'] -= 4

		for tiro in tiros:
			if abs(pontos - tiro) < 20:
				placar['score'] += 1
				inimigos.pop()
				tiros.pop()
	if len(inimigos) == 0:
		os.system('cls' if os.name == 'nt' else 'clear')
		exit(9)
		congratulation()
	ontimer(move, 100)

#movimentação dos inimigos2:
	for pontos, course in inimigos2:
		if valido(pontos + course):
			pontos.move(course)
		else:
			options = [
				vector(velocidade_inimigo2, 0),
				vector(-velocidade_inimigo2, 0),
				vector(0, velocidade_inimigo2),
				vector(0, -velocidade_inimigo2),
			]
			plan2 = choice(options)
			course.x = plan2.x
			course.y = plan2.y

		up()
		goto(pontos.x + 10, pontos.y + 10)
		dot(6, 'orange')

	update()

	for pontos, course in inimigos2:
		if abs(player - pontos) < 20:
			placar['score'] += 5
			adiciona()

		for tiro in tiros:
			if abs(pontos - tiro) < 20:
				inimigos2.pop()
				tiros.pop()

def change(x, y):
	if valido(player + vector(x, y)):
		direção.x = x
		direção.y = y

def atira(player):
	tiro = vector(player.x, player.y)
	print(player.x, player.y)
	tiros.append(tiro+1)

def tudo():
	setup(420, 420, 370, 0)
	hideturtle()
	tracer(False)
	escrever.goto(160, 160)
	escrever.color('white')
	escrever.write(placar['score'])
	listen()
	onkey(lambda: change(0, velocidade_player), 'w')
	onkey(lambda: change(velocidade_player, 0), 'd')
	onkey(lambda: change(0, -velocidade_player), 's')
	onkey(lambda: change(-velocidade_player, 0), 'a')
	onkey(lambda: atira(player), 'p')
	mundo()
	move()
	done()	

def logo():
	time.sleep(2)
	print(" ________")
	time.sleep(0.25)
	print("|   ___  |")
	time.sleep(0.25)
	print("|  |   |  |")
	time.sleep(0.25)
	print("|  |___|  |                        __")
	time.sleep(0.25)
	print("|        |                        |  |                __   __")
	time.sleep(0.25)
	print("|       |                         |  |      _______  |  | / /")
	time.sleep(0.25)
	print("|       |    _______   ___   ___  |  |     |   __  | |  |/ /")
	time.sleep(0.25)
	print("|   ___  |  |  ___  | |   |_|   | |  |___  |  |__| | |    /")
	time.sleep(0.25)
	print("|  |   |  | | |   | | |         | |  __  | |  _____| |   /")
	time.sleep(0.25)
	print("|  |___|  | | |___| | |  | | |  | | |__| | |  |____  |  |")
	time.sleep(0.25)
	print("|_________| |_______| |__|   |__| |______| |_______| |__|")
	time.sleep(0.25)
	print("              ________")
	time.sleep(0.25)
	print("             |   ___  |")
	time.sleep(0.25)
	print("             |  |   | |")
	time.sleep(0.25)
	print("             |  |___| |  _______   ________")
	time.sleep(0.25)
	print("             |    ____| |____   | |        |")
	time.sleep(0.25)
	print("             |   |       ____|  | |  ______|")
	time.sleep(0.25)
	print("             |   |      |  ___  | | |        ")
	time.sleep(0.25)
	print("             |   |      | |   | | | |______ ")
	time.sleep(0.25)
	print("             |   |      | |___| | |        |")
	time.sleep(0.25)
	print("             |___|      |_______| |________|")
	time.sleep(3)
	os.system('cls' if os.name == 'nt' else 'clear')
	menu()

def menu():
	print("Menu")
	a = " _____________________________________"
	b = "|                                     |"
	c = "|  Nome:______________-               |"
	d = "|                                     |"
	e = "|                                     |"
	f = "|  Cor:______________-                |"
	g = "|                                     |"
	h = "|                                     |"
	i = "|  Dificuldade:______________-        |"
	j = "|                                     |"
	k = "|_____________________________________|"

	nome = input("\n  Digite seu nome: ")
	c = evita_erro_c(nome, a, b, c, d, e, f, g, h, i, j, k)
	os.system('cls' if os.name == 'nt' else 'clear')
	f = escolher_cor(nome, a, b, c, d, e, f, g, h, i, j, k)
	i = dificuldade(nome, a, b, c, d, e, f, g, h, i, j, k)
	os.system('cls' if os.name == 'nt' else 'clear')
	print("\n", a,"\n", b,"\n", c,"\n", d,"\n", e,"\n", f,"\n", g,"\n", h,"\n", i,"\n", j,"\n", k)
	perf= input("\n Pressione 'c' para continuar ou 'r' para refazer! \n   ")
	if perf == 'c':
		tudo()
	elif perf == 'r':
		chama_fun3(nome, a, b, c, d, e, f, g, h, i, j, k)

def chama_fun3(nome, a, b, c, d, e, f, g, h, i, j, k):
	os.system('cls' if os.name == 'nt' else 'clear')
	menu()
		
def dificuldade(nome, a, b, c, d, e, f, g, h, i, j, k):
	dificil = ['fácil', 'Médio', 'Dificíl']
	print("\n Selecione o nível de dificuldade")
	print(" _______________")
	print("|               |")
	print("| f  =  Fácil   |")
	print("|               |")
	print("| m  =  Médio   |")
	print("|               |")
	print("| d  =  Díficil |")
	print("|_______________|")
	per3 = input("\n escolha o nível de dificuldade: \n   ")
	if per3 == 'f':
		i = "|  Dificuldade: "+dificil[0]+" -               |"
	elif per3 == 'm':
		i = "|  Dificuldade: "+dificil[1]+" -               |"
	elif per3 == 'd':
		i = "|  Dificuldade: "+dificil[2]+" -             |"
	else:
		chama_fun2(nome, a, b, c, d, e, f, g, h, i, j, k)
	return i
def evita_erro_c(nome, a, b, c, d, e, f, g, h, i, j, k):
	if len(nome) == 8:
		c = "|  Nome: "+ nome +" -                   |"
	elif len(nome) == 7:
		c = "|  Nome: "+ nome +" -                    |"
	elif len(nome) == 6:
		c = "|  Nome: "+ nome +" -                     |"
	elif len(nome) == 5:
		c = "|  Nome: "+ nome +" -                      |"
	elif len(nome) == 4:
		c = "|  Nome: "+ nome +" -                       |"
	elif len(nome) == 3:
		c = "|  Nome: "+ nome +" -                        |"
	elif len(nome) == 2:
		c = "|  Nome: "+ nome +" -                         |"
	elif len(nome) == 1:
		c = "|  Nome: "+ nome +" -                          |"
	while len(nome) > 8:
		os.system('cls' if os.name == 'nt' else 'clear')
		print(" ______________________________________________________")
		print("|                                                      |")
		print("| ERROR!!!!!!                                          |")
		print("| Seu nome não pode conter mais que oito caracteres!!! |")
		print("|______________________________________________________|")
		novo = input("\n Digite seu novo nome novamente: \n   ")
		nome = novo
		if len(nome) == 8:
			c = "|  Nome: "+ nome +" -                   |"
		elif len(novo) == 7:
			c = "|  Nome: "+ nome +" -                    |"
		elif len(nome) == 6:
			c = "|  Nome: "+ nome +" -                     |"
		elif len(nome) == 5:
			c = "|  Nome: "+ nome +" -                      |"
		elif len(nome) == 4:
			c = "|  Nome: "+ nome +" -                       |"
		elif len(nome) == 3:
			c = "|  Nome: "+ nome +" -                        |"
		elif len(nome) == 2:
			c = "|  Nome: "+ nome +" -                         |"
		elif len(nome) == 1:
			c = "|  Nome: "+ nome +" -                          |"
	return c
def escolher_cor(nome, a, b, c, d, e, f, g, h, i, j, k):
	cor = ['Verde', 'Roxo', 'Cinza', 'Laranja', 'Amarelo']
	print("\nDigite a primeira letra da cor do seu personagem:\n")
	print(' ___________________________________________')
	print('|                                           |')
	print('|  Verde | Roxo | Cinza | Laranja | Amarelo |')
	print('|___________________________________________|')
	percor = input("\n     ")
	if percor == 'v':
		f = "|  Cor: "+cor[0]+" -                       |"
	elif percor == 'r':
		f = "|  Cor: "+cor[1]+" -                        |"
	elif percor == 'c':
		f = "|  Cor: "+cor[2]+" -                       |"
	elif percor == 'l':
		f = "|  Cor: "+cor[3]+" -                     |"
	elif percor == 'a':
		f = "|  Cor: "+cor[4]+" -                     |"
	else:
		chama_função(nome, a, b, c, d, e, f, g, h, i, j, k)
	os.system('cls' if os.name == 'nt' else 'clear')
	return f
	
def chama_função(nome, a, b, c, d, e, f, g, h, i, j, k):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(" ______________________________________________")
	print("|                                              |")
	print("| ERROR!!!!!!                                  |")
	print("|______________________________________________|")
	escolher_cor(nome, a, b, c, d, e, f, g, h, i, j, k)
	
def chama_fun2(nome, a, b, c, d, e, f, g, h, i, j, k):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(" ______________________________________________")
	print("|                                              |")
	print("| ERROR!!!!!!                                  |")
	print("|______________________________________________|")
	dificuldade(nome, a, b, c, d, e, f, g, h, i, j, k)

logo()


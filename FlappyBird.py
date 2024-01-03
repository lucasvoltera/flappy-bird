from LinkedList import LinkedList
from BinaryTree import BinarySearchTree
from Queue import Queue
import pygame
import sys
import random 

def drawBase(): 
	'''Desenha duas bases quando é chamada e as move pela base_x_position'''
	screen.blit(base, (base_x_position, 700))
	screen.blit(base, (base_x_position + 600, 700))

def createPipe():
	'''Cria a posição dos obstáculos e os retorna como uma tupla'''
	global power_height

	# Escolhe uma altura
	random_pipe_pos = random.choice(pipe_height)
	power_height = random_pipe_pos

	# Cria os obstáculos
	bottom_pipe = pipe_image.get_rect(midtop=(700, random_pipe_pos))
	top_pipe = pipe_image.get_rect(midbottom=(700, random_pipe_pos - PIPE_GAP)) 
	return bottom_pipe, top_pipe 

def movePipes(pipes):
	'''Movimenta cada obstáculo 5 posições a esquerda e exclui os que já saíram da tela'''
	for pipe in pipes:
		pipe.centerx -= 5
	# Atualiza a lista
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes

def drawPipes(pipes):
	'''Desenha os obstáculos'''
	for pipe in pipes:
		# Como o obstáculo ultrapassa a parte de baixo da tela, não é o invertido
		if pipe.bottom >= SCREEN_HEIGHT:
			screen.blit(pipe_image, pipe)
		else:
			# Se for o obstáculo de cima, inverte
			inverted_pipe = pygame.transform.flip(pipe_image, False, True)
			screen.blit(inverted_pipe, pipe)
 
def createPower():
	'''Cria a posição dos poderes e retorna'''
	if power_queue.peek()[0] == 'coin5' or power_queue.peek()[0] == 'coin10':
		pos = random.randint(2, 4)
		new_power = power_queue.peek()[1][0].get_rect(midtop=(690, power_height - PIPE_GAP / pos - (COIN_SIZE / 2)))
	else:
		new_power = power_queue.peek()[1].get_rect(midtop=(690, power_height - PIPE_GAP / 2 - (BIRD_HEIGHT / 2)))
	return new_power

def movePower(powers):
	'''Move os poderes para a esquerda'''
	for power in powers:
		power.centerx -= 5

def drawPower(powers):
	'''Desenha os poderes'''
	for power in powers:  
		if power_queue.peek()[0] == 'coin5' or power_queue.peek()[0] == 'coin10':
			screen.blit(power_queue.peek()[1][coin_current_image], power)
		else:
			screen.blit(power_queue.peek()[1], power)

def checkPower(power):
	'''Verifica qual o tipo de poder para realizar alterações'''
	global bird, background, collision_is_possible, score, coinScore5, coinScore10

	if power[0] == 'red':
		bird = [pygame.transform.scale(pygame.image.load('img/redbird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
				pygame.transform.scale(pygame.image.load('img/redbird-midflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
				pygame.transform.scale(pygame.image.load('img/redbird-downflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))]
		change_sound.play()
		red = power_queue.pop()
		power_queue.push(red)
	elif power[0] == 'yellow':
		bird = [pygame.transform.scale(pygame.image.load('img/yellowbird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
				pygame.transform.scale(pygame.image.load('img/yellowbird-midflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
				pygame.transform.scale(pygame.image.load('img/yellowbird-downflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))]
		change_sound.play()
		yellow = power_queue.pop()
		power_queue.push(yellow)
	elif power[0] == 'blue':
		bird = [pygame.transform.scale(pygame.image.load('img/bluebird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
				pygame.transform.scale(pygame.image.load('img/bluebird-midflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
				pygame.transform.scale(pygame.image.load('img/bluebird-downflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))]
		change_sound.play()
		blue = power_queue.pop()
		power_queue.push(blue)
	elif power[0] == 'coin5':
		coinScore5 = True
		score += 5
		coin5 = power_queue.pop()
		power_queue.push(coin5)
	else:
		coinScore10 = True
		score += 10
		coin10 = power_queue.pop()
		power_queue.push(coin10)

	collision_is_possible = True

def checkCollision(pipes):
	'''Verifica se houve colisão. Se sim, retorna True e o jogo finaliza'''
	global score_is_possible

	# Verificar em todos os obstáculos se houve a colisão
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			score_is_possible = True
			return False
	# Se o personagem sair muito para cima da tela ou bater na base, o jogo acaba
	if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT - BASE_HEIGHT:
		death_sound.play()
		score_is_possible = True
		return False
	return True

def checkPowerCollision(powers):
	'''Verificar se o personagem pegou o poder. Retorna a lista de poderes atualizada'''
	global collision_is_possible

	visible_powers = []
	for power in powers:
		# Atualiza a lista
		if not bird_rect.colliderect(power):
			visible_powers.append(power)
		else:
			collision_is_possible = False
	return visible_powers

def rotateBird(bird):
	'''Rotaciona o personagem'''
	new_bird = pygame.transform.rotate(bird, -bird_movement * 3)
	return new_bird

def birdAnimation():
	'''Atualiza a imagem do personagem. Retorna uma tupla com a nova imagem e a posição'''
	new_bird = bird[bird_current_image]
	new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
	return new_bird, new_bird_rect

def scoreDisplay(state):
	'''Mostra a pontuação do jogo'''
	if state:
		# Sombra da pontuação
		shadow_display = font.render(str(int(score)), True, (70, 70, 70))
		shadow_rect = shadow_display.get_rect(center=(SCREEN_WIDTH / 2 + 2, 102))
		screen.blit(shadow_display, shadow_rect)
		# Pontuação
		score_display = font.render(str(int(score)), True, WHITE)
		score_rect = score_display.get_rect(center=(SCREEN_WIDTH / 2, 100))
		screen.blit(score_display, score_rect)
	else:
		# Pontuação quando finalizou o jogo
		score_display = font.render(f'Score: {int(score)}', True, WHITE)
		score_rect = score_display.get_rect(center=(SCREEN_WIDTH / 2, 100))
		screen.blit(score_display, score_rect)

		# Sombra melhor pontuação
		shadow_high_score_display = font.render(f'High Score: {int(high_score)}', True, (70, 70, 70))
		shadow_high_score_rect = shadow_high_score_display.get_rect(center=(SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT - BASE_HEIGHT - 48))
		screen.blit(shadow_high_score_display, shadow_high_score_rect)
		# Melhor pontuação
		high_score_display = font.render(f'High Score: {int(high_score)}', True, WHITE)
		high_score_rect = high_score_display.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - BASE_HEIGHT - 50))
		screen.blit(high_score_display,high_score_rect)

def pipeScoreCheck():
	'''Verifica se é possível aumentar a pontuação'''
	global score, score_is_possible 

	if pipe_list:
		for pipe in pipe_list:
			# Quando o obstáculo passar o personagem 
			if 95 < pipe.centerx < 105 and score_is_possible:
				score += 1 # Aumenta a pontuação
				score_sound.play()
				score_is_possible = False
			# Obstáculo saiu da tela
			if pipe.centerx < 0:
				score_is_possible = True

def coinScoreDisplay():
	global coinScore5, coinScore10
	if coinScore5:
		score_display = font_score.render('+5', True, (255, 255, 255))
	else:
		score_display = font_score.render('+10', True, (255, 255, 255))
	if score_rect.centery > -50:
		score_rect.centery -= 10
		screen.blit(score_display, score_rect)
	else:
		coinScore5 = False
		coinScore10 = False
		score_rect.centerx = SCREEN_WIDTH / 2
		score_rect.centery = SCREEN_HEIGHT / 2

# Constantes
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

BIRD_WIDTH = 51
BIRD_HEIGHT = 36
GRAVITY = .3

BASE_WIDTH = SCREEN_WIDTH 
BASE_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 250

COIN_SIZE = 45

MESSAGE_WIDTH = 276
MESSAGE_HEIGHT = 400
GAMEOVER_WIDTH = 384
GAMEOVER_HEIGHT = 84
WHITE = (255, 255, 255)

# Configurações do jogo
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('font/04B_19.TTF', 60)

# Pontuação
score_tree = BinarySearchTree()
score = 0
high_score = 0
score_is_possible = True

# Fundo de tela
background = pygame.image.load('img/background-day.png').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Base
base = pygame.image.load('img/base.png').convert()
base = pygame.transform.scale(base, (BASE_WIDTH, BASE_HEIGHT))
base_x_position = 0

# Obstáculo
pipe_image = pygame.image.load('img/pipe-green.png')
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))
pipe_list = LinkedList()
CREATEPIPE = pygame.USEREVENT
pygame.time.set_timer(CREATEPIPE, 1200)
pipe_height = [350, 400, 500, 600, 650]

# Personagem
bird = [
		pygame.transform.scale(pygame.image.load('img/bluebird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
        pygame.transform.scale(pygame.image.load('img/bluebird-midflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)),
        pygame.transform.scale(pygame.image.load('img/bluebird-downflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))
]
bird_current_image = 0
bird_image = bird[bird_current_image]
bird_rect = bird_image.get_rect(center=(100, SCREEN_HEIGHT / 2))
bird_movement = 0
BIRDIMAGE = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDIMAGE, 200)

# Poderes
red_bird = pygame.transform.scale(pygame.image.load('img/redbird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))
yellow_bird = pygame.transform.scale(pygame.image.load('img/yellowbird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))
blue_bird = pygame.transform.scale(pygame.image.load('img/bluebird-upflap.png').convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT))
power_queue = Queue()
powers = {
		'red': pygame.transform.flip(red_bird, True, False),
		'coin5' : [
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_0.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_1.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_2.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_3.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_4.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_5.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_6.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_7.png').convert_alpha(), (COIN_SIZE, COIN_SIZE))
		],
		'yellow': pygame.transform.flip(yellow_bird, True, False),
		'blue': pygame.transform.flip(blue_bird, True, False),
		'coin10' : [
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_0.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_1.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_2.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_3.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_4.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_5.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_6.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_10/sprite_7.png').convert_alpha(), (COIN_SIZE, COIN_SIZE))
		]
	}
for key, value in powers.items():
	power_queue.push([key, value])
collision_is_possible = True
power_height = 0
power_list = LinkedList()

CREATEPOWER = pygame.USEREVENT + 2
pygame.time.set_timer(CREATEPOWER, 6000)

# Moeda
coin_current_image = 0
coins = [
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_0.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_1.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_2.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_3.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_4.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_5.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_6.png').convert_alpha(), (COIN_SIZE, COIN_SIZE)),
			pygame.transform.scale(pygame.image.load('img/gold_5/sprite_7.png').convert_alpha(), (COIN_SIZE, COIN_SIZE))
		]
COINIMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(COINIMAGE, 200)

# Jogo rodando
StartGame = True
GameActive = False
dayOn = True
coinScore5 = False
coinScore10 = False

# Início do jogo
StartGame = pygame.transform.scale(pygame.image.load('img/message.png').convert_alpha(), (MESSAGE_WIDTH, MESSAGE_HEIGHT))
StartGame_rect = StartGame.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# Fim do jogo
GameOver = pygame.transform.scale(pygame.image.load('img/gameover.png').convert_alpha(), (GAMEOVER_WIDTH, GAMEOVER_HEIGHT))
GameOver_rect = GameOver.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# Som
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
change_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')

# Dia/Noite
CHANGEEVENT = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGEEVENT, 18000)

# Pontuação da moeda
font_score = pygame.font.Font('font/04B_19.ttf', 100)
score_display = font_score.render('+5', True, (255, 255, 255))
score_rect = score_display.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

while True:
	# FPS do jogo
	clock.tick(100)

	for event in pygame.event.get():
		# Enquanto o usuário não fechar a tela
		if event.type == pygame.QUIT:
			# pygame.quit()
			sys.exit()

		# Se clicar no espaço, faz o personagem subir	
		if event.type == pygame.KEYDOWN:
			# Início do jogo
			if event.key == pygame.K_SPACE and StartGame:
				GameActive = True
				StartGame = False
			# Verificar se o jogo está rodando
			if event.key == pygame.K_SPACE and GameActive:
				bird_movement = 0
				# Movimenta o personagem para cima
				bird_movement -= 8
				flap_sound.play()
			# Jogo acabou
			elif event.key == pygame.K_SPACE and not GameActive:
				GameActive = True
				# Limpar listas
				pipe_list.clear()
				power_list.clear()
				# Volta na posição inicial
				bird_rect.center = (100, SCREEN_HEIGHT / 2)
				bird_movement = 0
				# Zera o score
				score = 0
		if not StartGame:
            # Evento que cria os obstáculos
			if event.type == CREATEPIPE:
				pipe_list.extend(createPipe())

			# Evento que muda a imagem do personagem
			if event.type == BIRDIMAGE:
				bird_current_image = (bird_current_image + 1) % 3 
				bird_image, bird_rect = birdAnimation()
			
			# Evento que cria os poderes
			if event.type == CREATEPOWER:
				power_list.append(createPower())
				pygame.time.set_timer(CREATEPOWER, 1200 * random.randint(8, 12))
				if power_queue.peek()[0] == 'coin5' or power_queue.peek()[0] == 'coin10':
					coins = power_queue.peek()[1]
			
			# Evento que muda a imagem da moeda
			if event.type == COINIMAGE:
				coin_current_image = (coin_current_image + 1) % 8 
				coin_image = coins[coin_current_image]
			
			# Evento que muda dia/noite
			if event.type == CHANGEEVENT and dayOn:
				change_sound.play()
				background = pygame.image.load('img/background-night.png').convert()
				background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
				dayOn = False
			elif event.type == CHANGEEVENT and not dayOn:
				change_sound.play()
				background = pygame.image.load('img/background-day.png').convert()
				background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
				dayOn = True
			
	# Coloca o fundo do jogo
	screen.blit(background, (0, 0))

	# Jogo ainda não iniciou
	if StartGame:
		screen.blit(StartGame, StartGame_rect)
	elif GameActive:
		# Personagem
		bird_movement += GRAVITY # Cai com a gravidade
		rotated_bird = rotateBird(bird_image) # Rotacionar conforme movimento
		bird_rect.centery += bird_movement # Movimenta o personagem
		screen.blit(rotated_bird, bird_rect)
		GameActive = checkCollision(pipe_list) # Verificar se houve colisão

		# Obstáculo
		pipe_list = movePipes(pipe_list) # Movimenta o obstáculo
		drawPipes(pipe_list) # Desenha o obstáculo

		# Poder
		movePower(power_list) # Movimenta o poder
		drawPower(power_list) # Desenha o poder
		power_list = checkPowerCollision(power_list) # Verifica se o personagem pegou o poder
		if not collision_is_possible: # Se pegou o poder
			checkPower(power_queue.peek()) # Faz mudanças
		
		# Pontuação
		pipeScoreCheck()
		scoreDisplay(GameActive)

		# Pontuação da moeda
		if coinScore5 or coinScore10:
			coinScoreDisplay()

	# Jogo finalizou
	else:
		screen.blit(GameOver, GameOver_rect)
		# Inserir a última pontuação na árvore
		score_tree.insert(score)
		high_score = score_tree.max()
		scoreDisplay(GameActive)

	# Base
	base_x_position -= 5
	drawBase()
	if base_x_position <= -600:
		base_x_position = 0
	
	pygame.display.update()
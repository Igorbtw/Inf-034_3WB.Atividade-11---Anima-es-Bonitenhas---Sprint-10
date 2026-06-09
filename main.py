from pygame import *
import sys
import random

from pygame.locals import QUIT, KEYDOWN

clock = time.Clock()

kirk_img = image.load("kirky.gif")
speed_img = image.load("speedy_fofo.gif")
speed_laser_img = image.load("speedy.gif")
grass_img = image.load("grass.png")
grass_img = transform.scale(grass_img, (800, 400))
ceu_img = image.load("ceunovo.jpg")
ceu_img = transform.scale(ceu_img, (800, 400))

loc_x = 100
loc_y = 200

hero_img = transform.scale(image.load("assets/assets/Hero_walk_01.png"), (300, 400))

hero_standard = transform.scale(image.load("assets/assets/Hero_walk_14.png"), (300, 400))

dino_img = image.load("dino/row-1-column-1.png")
dino_img = transform.scale(dino_img, (50, 50))

dino_animation = False
run_animation = False
run_animation_d = False
run_animation_backwards = False
run_animation_up = False
run_animation_down = False
run_mode = False
dist = 2

z_jump = 0
is_jumping = False
jump_force = 15      
gravity = 1          
z_velocity = 0


current_frame = 0
anim_time = 0
anim_time_d = 0
kirk_walk_list = []
for i in range(4):
    imagem_original = image.load(f"assets/assets/Hero_walk_0{i+1}.png")
    imagem_tamanho_novo = transform.scale(imagem_original, (300, 400)) 
    kirk_walk_list.append(imagem_tamanho_novo)

kirk_walk_list_2 = []
for i in range(4):
    imagem_original = image.load(f"assets/assets/Hero_walk_0{i+5}.png")
    imagem_tamanho_novo = transform.scale(imagem_original, (300, 400))
    kirk_walk_list_2.append(imagem_tamanho_novo)

kirk_walk_list_up = []
for i in range(4):
    imagem_original = image.load(f"assets/assets/Hero_walk_{i+9}.png")
    imagem_tamanho_novo = transform.scale(imagem_original, (300, 400))
    kirk_walk_list_up.append(imagem_tamanho_novo)

kirk_walk_list_down = []
for i in range(4):
    imagem_original = image.load(f"assets/assets/Hero_walk_{i+13}.png")
    imagem_tamanho_novo = transform.scale(imagem_original, (300, 400))
    kirk_walk_list_down.append(imagem_tamanho_novo)

dino_normal = []
dino_vermelho = []
dino_verde = []
dino_laranja = []

for i in range(11):
    dino_normal.append(transform.scale(image.load(f"dino/row-1-column-{i+4}.png"), (50, 50)))
    dino_vermelho.append(transform.scale(image.load(f"dino_vermelho/row-1-column-{i+4}.png"), (50, 50)))
    dino_verde.append(transform.scale(image.load(f"dino_verde/row-1-column-{i+4}.png"), (50, 50)))
    dino_laranja.append(transform.scale(image.load(f"dino_laranja/row-1-column-{i+4}.png"), (50, 50)))

opcoes_de_cores = [dino_normal, dino_vermelho, dino_verde, dino_laranja]

class DinossauroNPC:
    def __init__(self, limite_x, chao_y, listas_de_cores):
        #posição inicial na tela
        self.x = random.randint(50, 700)
        self.y = random.randint(350, 550)
        
        # começa andando para a esquerda (-2) ou direita (2)
        self.velocidade_x = random.choice([-2,-1, 1, 2])
        self.velocidade_y = random.choice([-2, -1, 1, 2])
        
        self.frame_atual = random.randint(0, 10) #cada dinossauro começa em frames diferentes xd
        self.tempo_animacao = 0

        self.minha_animacao = random.choice(listas_de_cores)

    def atualizar_e_desenhar(self, tela, dt, lista_animacao):
        #movimento
        self.x = self.x + self.velocidade_x
        self.y = self.y + self.velocidade_y

        #bater na parede e virar
        if self.x <= -20 or self.x >= 790:
            self.velocidade_x = self.velocidade_x * -1
        if self.y <= 350 or self.y >= 570:
            self.velocidade_y = self.velocidade_y * -1

        #tempo da Animação
        self.tempo_animacao += dt
        if self.tempo_animacao > 80: # 80 milissegundos para trocar de frame
            self.frame_atual += 1
            if self.frame_atual >= len(lista_animacao):
                self.frame_atual = 0
            self.tempo_animacao = 0

        #desenho
        imagem_atual = lista_animacao[self.frame_atual]
        
        # se velocidade for negativa (esquerda), espelha a imagem
        if self.velocidade_x < 0:
            imagem_atual = transform.flip(imagem_atual, True, False)
            
        tela.blit(imagem_atual, (self.x, self.y))

bando_de_dinos = []
#range = quantos dinossauros tem

for i in range(50): # Pode colocar 10, 20...
    # Passamos as opções de cores para ele sortear quando nascer
    novo_dino = DinossauroNPC(800, 400, opcoes_de_cores)
    bando_de_dinos.append(novo_dino)

current_frame_gui = 0
anim_time_gui = 0
gui_receba_farinha = image.load("assets/assets/Hero_walk_01.png")


init()
screen = display.set_mode((800,600))
display.set_caption("Welkirk home")

while True:
    key_pressed = key.get_pressed()
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit
        #eventos do pygame
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE and is_jumping == False:
                is_jumping = True
                z_velocity = jump_force


    run_animation = False
    run_animation_backwards = False
    run_animation_up = False
    run_animation_down = False
    run_mode = False
    dino_animation = True


    #run_animation = False
    keys = key.get_pressed()
    clock.tick(60)
    dt = clock.get_time()
    
    if keys[K_d] and loc_x<640:
        loc_x = loc_x+dist
        run_animation = True

    if keys[K_a] and loc_x>-130:
        loc_x = loc_x-dist
        run_animation_backwards = True

    if keys[K_w] and loc_y > 120:
        loc_y = loc_y - dist
        run_animation_up = True

    if keys[K_s] and loc_y < 480:
        loc_y = loc_y + dist
        run_animation_down = True
    
    if keys[K_LSHIFT]:
        run_mode = True
    
    if run_mode == False:
        dist = 2
    if run_mode == True:
        dist = 5

    anim_time = anim_time + dt
    #print(anim_time)
    anim_time_sec = anim_time/1000

    anim_time_d = anim_time_d + dt
    anim_time_sec_d = anim_time_d/1000

    if run_mode == True:
        if run_animation or run_animation_backwards or run_animation_up or run_animation_down:
            if anim_time_sec > 0.04:  
                current_frame += 1
                
                if run_animation and current_frame > len(kirk_walk_list) - 1:
                    current_frame = 0 
                elif run_animation_backwards and current_frame > len(kirk_walk_list_2) - 1:
                    current_frame = 0 
                elif run_animation_up and current_frame > len(kirk_walk_list_up) - 1:
                    current_frame = 0 
                elif run_animation_down and current_frame > len(kirk_walk_list_down) - 1:
                    current_frame = 0 
                anim_time = 0
        else:
            current_frame = 0
            anim_time = 0

    if run_mode == False:
        if run_animation or run_animation_backwards or run_animation_up or run_animation_down:
            if anim_time_sec > 0.15:  
                current_frame += 1
                
                if run_animation and current_frame > len(kirk_walk_list) - 1:
                    current_frame = 0 
                elif run_animation_backwards and current_frame > len(kirk_walk_list_2) - 1:
                    current_frame = 0 
                elif run_animation_up and current_frame > len(kirk_walk_list_up) - 1:
                    current_frame = 0 
                elif run_animation_down and current_frame > len(kirk_walk_list_down) - 1:
                    current_frame = 0 
                anim_time = 0
        else:
            current_frame = 0
            anim_time = 0

    if is_jumping:
        z_jump = z_jump + z_velocity
        z_velocity = z_velocity - gravity # A gravidade puxa o Z pra baixo

        if z_jump <= 0:
            z_jump = 0
            is_jumping = False
            z_velocity = 0

    #desenha
    screen.fill((155,155,155))

    #screen blit elementos da tela
    screen.blit(ceu_img, (0,0))
    screen.blit(grass_img, (0,200))
    #screen.blit(kirk_img, (550,100))
    #creen.blit(speed_img, (100,100), (100,100,200,200)) #o tamanho funciona de indo da cordenada 100,100 com o tamanho 200,200
    #screen.blit(speed_laser_img, (400,300))
    


    #animacao

    for dino in bando_de_dinos:
        dino.atualizar_e_desenhar(screen, dt, dino.minha_animacao)
    if dino_animation == True and run_animation_backwards == False:
        screen.blit(dino_normal[current_frame], (loc_x+70,loc_y+250))
    if dino_animation == True and run_animation_backwards == True:
        screen.blit(transform.flip(dino_normal[current_frame], True, False), (loc_x+140,loc_y+240))
    if run_animation == True and run_animation_backwards == False and run_animation_up == False and run_animation_down == False:
        screen.blit(kirk_walk_list[current_frame], (loc_x,loc_y - z_jump))
    if run_animation_backwards == True and run_animation == False and run_animation_up == False and run_animation_down == False:
        screen.blit(kirk_walk_list_2[current_frame], (loc_x,loc_y - z_jump))
    if run_animation_up == True and run_animation_down == False:
        screen.blit(kirk_walk_list_up[current_frame], (loc_x,loc_y - z_jump))
    if run_animation_down == True and run_animation_up == False:
        screen.blit(kirk_walk_list_down[current_frame], (loc_x,loc_y - z_jump))
    if run_animation == False and run_animation_backwards == False and run_animation_up == False and run_animation_down == False:
        screen.blit(hero_standard, (loc_x,loc_y - z_jump))
    if run_animation == True and run_animation_backwards == True and run_animation_up == False and run_animation_down == False:
        screen.blit(hero_standard, (loc_x,loc_y - z_jump))
    if run_animation == False and run_animation_backwards == False and run_animation_up == True and run_animation_down == True:
        screen.blit(hero_standard, (loc_x,loc_y - z_jump))


    display.update()

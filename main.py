from pygame import *
import sys
import random
import os
import glob

from pygame.locals import QUIT, KEYDOWN

clock = time.Clock()

for padrao, nome_certo in [
    ("*spider*", "spider.png"),
    ("*May*",    "May.png"),
    ("*hk*",     "hk.png"),
]:
    for arq in glob.glob(padrao):
        if arq != nome_certo:
            os.rename(arq, nome_certo)
            break

spider_sheet = image.load("spider.png")
may_sheet    = image.load("May.png")
hk_sheet     = image.load("hk.png")

grass_img = image.load("grass.png")
grass_img = transform.scale(grass_img, (800, 400))
ceu_img = image.load("ceunovo.jpg")
ceu_img = transform.scale(ceu_img, (800, 400))

# hollow knight - heroi principal
hk_starts = [1,51,101,126,151,201,226,251,301,351,401,451,476,501,526,551,576,626,651,701,726,776,826]
HK_FW, HK_FH = 24, 52
TARGET_W, TARGET_H = 300, 400

def corta_hk(idx):
    x = hk_starts[idx]
    surf = Surface((HK_FW, HK_FH), SRCALPHA)
    surf.blit(hk_sheet, (0, 0), (x, 0, HK_FW, HK_FH))
    return transform.scale(surf, (TARGET_W, TARGET_H))

kirk_walk_list        = [corta_hk(i) for i in range(6)]
kirk_walk_list_2      = [transform.flip(corta_hk(i), True, False) for i in range(6)]
kirk_walk_list_up     = [corta_hk(i) for i in range(6, 10)]
kirk_walk_list_down   = [corta_hk(i) for i in range(10, 14)]
hero_img      = corta_hk(0)
hero_standard = corta_hk(0)

# may - companheira do jogador
MAY_FW, MAY_FH = 16, 58
MAY_TARGET_W, MAY_TARGET_H = 50, 50

def corta_may(idx):
    surf = Surface((MAY_FW, MAY_FH), SRCALPHA)
    surf.blit(may_sheet, (0, 0), (idx * MAY_FW, 0, MAY_FW, MAY_FH))
    return transform.scale(surf, (MAY_TARGET_W, MAY_TARGET_H))

may_anim = [corta_may(i) for i in range(7)]

# spider-man - npcs
SP_FW, SP_FH = 32, 32
SP_TARGET = 50

def corta_spider(row, col):
    surf = Surface((SP_FW, SP_FH), SRCALPHA)
    surf.blit(spider_sheet, (0, 0), (col * SP_FW, row * SP_FH, SP_FW, SP_FH))
    return transform.scale(surf, (SP_TARGET, SP_TARGET))

sp_base  = [corta_spider(0, c) for c in range(9)] + [corta_spider(1, c) for c in range(2)]
sp_flip  = [transform.flip(f, True, False) for f in sp_base]
sp_row2  = [corta_spider(1, c) for c in range(9)] + [corta_spider(2, c) for c in range(2)]
sp_row2f = [transform.flip(f, True, False) for f in sp_row2]

opcoes_de_cores = [sp_base, sp_flip, sp_row2, sp_row2f]

loc_x = 100
loc_y = 200

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

class DinossauroNPC:
    def __init__(self, limite_x, chao_y, listas_de_cores):
        self.x = random.randint(50, 700)
        self.y = random.randint(350, 550)

        self.velocidade_x = random.choice([-2, -1, 1, 2])
        self.velocidade_y = random.choice([-2, -1, 1, 2])

        self.frame_atual = random.randint(0, 10)
        self.tempo_animacao = 0

        self.minha_animacao = random.choice(listas_de_cores)

    def atualizar_e_desenhar(self, tela, dt, lista_animacao):
        self.x = self.x + self.velocidade_x
        self.y = self.y + self.velocidade_y

        if self.x <= -20 or self.x >= 790:
            self.velocidade_x = self.velocidade_x * -1
        if self.y <= 350 or self.y >= 570:
            self.velocidade_y = self.velocidade_y * -1

        self.tempo_animacao += dt
        if self.tempo_animacao > 80:
            self.frame_atual += 1
            if self.frame_atual >= len(lista_animacao):
                self.frame_atual = 0
            self.tempo_animacao = 0

        imagem_atual = lista_animacao[self.frame_atual]

        if self.velocidade_x < 0:
            imagem_atual = transform.flip(imagem_atual, True, False)

        tela.blit(imagem_atual, (self.x, self.y))

bando_de_dinos = []
for i in range(50):
    novo_dino = DinossauroNPC(800, 400, opcoes_de_cores)
    bando_de_dinos.append(novo_dino)

current_frame_gui = 0
anim_time_gui = 0

init()
screen = display.set_mode((800, 600))
display.set_caption("Welkirk home")

while True:
    key_pressed = key.get_pressed()
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit
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

    keys = key.get_pressed()
    clock.tick(60)
    dt = clock.get_time()

    if keys[K_d] and loc_x < 640:
        loc_x = loc_x + dist
        run_animation = True

    if keys[K_a] and loc_x > -130:
        loc_x = loc_x - dist
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
    anim_time_sec = anim_time / 1000

    anim_time_d = anim_time_d + dt
    anim_time_sec_d = anim_time_d / 1000

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
        z_velocity = z_velocity - gravity
        if z_jump <= 0:
            z_jump = 0
            is_jumping = False
            z_velocity = 0

    screen.fill((155, 155, 155))
    screen.blit(ceu_img, (0, 0))
    screen.blit(grass_img, (0, 200))

    for dino in bando_de_dinos:
        dino.atualizar_e_desenhar(screen, dt, dino.minha_animacao)

    if dino_animation == True and run_animation_backwards == False:
        screen.blit(may_anim[current_frame % len(may_anim)], (loc_x + 70, loc_y + 250))
    if dino_animation == True and run_animation_backwards == True:
        screen.blit(transform.flip(may_anim[current_frame % len(may_anim)], True, False), (loc_x + 140, loc_y + 240))

    if run_animation == True and run_animation_backwards == False and run_animation_up == False and run_animation_down == False:
        screen.blit(kirk_walk_list[current_frame % len(kirk_walk_list)], (loc_x, loc_y - z_jump))
    if run_animation_backwards == True and run_animation == False and run_animation_up == False and run_animation_down == False:
        screen.blit(kirk_walk_list_2[current_frame % len(kirk_walk_list_2)], (loc_x, loc_y - z_jump))
    if run_animation_up == True and run_animation_down == False:
        screen.blit(kirk_walk_list_up[current_frame % len(kirk_walk_list_up)], (loc_x, loc_y - z_jump))
    if run_animation_down == True and run_animation_up == False:
        screen.blit(kirk_walk_list_down[current_frame % len(kirk_walk_list_down)], (loc_x, loc_y - z_jump))
    if run_animation == False and run_animation_backwards == False and run_animation_up == False and run_animation_down == False:
        screen.blit(hero_standard, (loc_x, loc_y - z_jump))
    if run_animation == True and run_animation_backwards == True and run_animation_up == False and run_animation_down == False:
        screen.blit(hero_standard, (loc_x, loc_y - z_jump))
    if run_animation == False and run_animation_backwards == False and run_animation_up == True and run_animation_down == True:
        screen.blit(hero_standard, (loc_x, loc_y - z_jump))

    display.update()
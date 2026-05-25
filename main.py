import pygame, sys
from pygame.locals import QUIT

clock = pygame.time.Clock()

hero_img = pygame.image.load("assets/asets/Hero_Walk-01.png")





curr_frame = 0
anim_time = 0
hero_walk_list = []
for i in range(4):
    hero_walk_list.append(pygame.image.load(f"assets/assets/Hero_Walk_0{i+1}.png"))


curr_framemm = 0
an



pygame.init()
pygame.display.set_caption("Hello World!")




altura = 1200
largura = 1000
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Hello World!")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                run.animation = True
    clock.tick(60)
    dt = clock.get_time()
    
    #segundos da animação
    anim_time = anim_time = dt
    anim_time_sec = anim_time/1000

    if anim_time_sec > 0.15:
        curr_frame += 1
    if curr_frame> len(hero_walk_list) -1:
       curr_frame = 0
    anim_time_sec = 0
    #curr_frame += 1

    if run_animation:
        anim_time_mm
    #Desenho dos elementos na tela
    screen.fill((255,255,255))

    # screenblit(dog_image, (0,0))
    screen.blit(hero_walk_list[curr_frame], (0,0))


    if curr_frame_mm < 5:
        screen.blit
    pygame.display.update()

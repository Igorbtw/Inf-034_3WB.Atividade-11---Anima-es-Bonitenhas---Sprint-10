import pygame
import sys
import os
 
pygame.init()
 


BASE = os.path.dirname(os.path.abspath(__file__))
 
HK_PATH  = os.path.join(BASE, "hk.png")
MAY_PATH  = os.path.join(BASE, "may.png")
SPIDER_PATH = os.path.join(BASE, "spider.png")
 

W, H = 900, 520
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Animações PyGame")
clock = pygame.time.Clock()
FPS = 60
 

BG_COLOR   = (30, 20, 50)
GROUND_Y   = H - 80
GROUND_COL = (55, 45, 80)
LINE_COL   = (90, 70, 120)
WHITE      = (255, 255, 255)
YELLOW     = (255, 230, 80)
CYAN       = (80, 220, 255)
RED        = (255, 80, 80)
 
font = pygame.font.SysFont("consolas", 14, bold=True)
 
 

 
def make_transparent(surf, bg_rgb, tol=25):
    
    surf = surf.convert_alpha()
    arr = pygame.surfarray.pixels3d(surf)
    alpha = pygame.surfarray.pixels_alpha(surf)
    r, g, b = bg_rgb
    mask = (
        (abs(arr[:, :, 0].astype(int) - r) <= tol) &
        (abs(arr[:, :, 1].astype(int) - g) <= tol) &
        (abs(arr[:, :, 2].astype(int) - b) <= tol)
    )
    alpha[mask] = 0
    del arr, alpha
    return surf
 
 
def scale2x(surf):
    return pygame.transform.scale2x(surf)
 
 
def scale_to(surf, w, h):
    return pygame.transform.smoothscale(surf, (w, h))
 


 
class HollowKnightIdle:
    BG = (38, 91, 161)
    
    FRAME_RANGES = [
        (0,   47),   
        (48,  78),   
        (296, 328),  
        (345, 377),  
        (400, 432),  
        (776, 800),  
        (824, 851),  
    ]
    SCALE = 3      
 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.timer = 0
        self.frame_delay = 8
 
        sheet = pygame.image.load(HK_PATH).convert()
        self.frames = []
        for (x0, x1) in self.FRAME_RANGES:
            w = x1 - x0
            sub = sheet.subsurface(pygame.Rect(x0, 0, w, 52))
            sub = make_transparent(sub, self.BG)
            sub = scale_to(sub, w * self.SCALE, 52 * self.SCALE)
            self.frames.append(sub)
 
    def update(self):
        self.timer += 1
        if self.timer >= self.frame_delay:
            self.timer = 0
            self.frame = (self.frame + 1) % len(self.frames)
 
    def draw(self, surf):
        img = self.frames[self.frame]
        surf.blit(img, (self.x - img.get_width() // 2,
                        self.y - img.get_height()))
 
 

 
class MAYWalk:
    BG = (251, 168, 176)
    
    WALK_BLOBS = [
        (52, 40, 20, 32),   
        (76, 40, 20, 32),   
        (100,40, 20, 32),   
        (124,40, 20, 32),   
    ]
    IDLE_BLOB  = (52, 0, 20, 32)   
    SCALE = 5
 
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.frame = 0
        self.timer = 0
        self.frame_delay = 8
        self.active = False
        self.facing = 1
 
        sheet = pygame.image.load(MAY_PATH).convert()
 
        def cut(bx, by, bw, bh):
           
            px, py = 4, 4
            rx = max(0, bx - px)
            ry = max(0, by - py)
            rw = bw + px * 2
            rh = bh + py * 2
            sub = sheet.subsurface(pygame.Rect(rx, ry, rw, rh))
            sub = make_transparent(sub, self.BG)
            return scale_to(sub, rw * self.SCALE, rh * self.SCALE)
 
        self.walk_frames = [cut(*b) for b in self.WALK_BLOBS]
        bx, by, bw, bh = self.IDLE_BLOB
        self.idle_frame = cut(bx, by, bw, bh)
 
    def update(self, keys):
        move = False
        speed = 3
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= speed
            self.facing = -1
            move = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += speed
            self.facing = 1
            move = True
 
        self.active = move
        if move:
            self.timer += 1
            if self.timer >= self.frame_delay:
                self.timer = 0
                self.frame = (self.frame + 1) % len(self.walk_frames)
        else:
            self.frame = 0
            self.timer = 0
 
        self.x = max(40, min(W - 40, self.x))
 
    def draw(self, surf):
        if self.active:
            img = self.walk_frames[self.frame]
        else:
            img = self.idle_frame
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
        surf.blit(img, (int(self.x) - img.get_width() // 2,
                        int(self.y) - img.get_height()))
 
 

 
class SPIDER:
    BG = (0, 64, 128)
    CELL = (55, 64)
    SHEET_ORIGIN_Y = 8
    SCALE = 3
    SPEED = 4
    GRAVITY = 0.6
    JUMP_VY = -13
 
    
    IDLE  = [(0, 0)]
    WALK  = [(0, 1), (0, 2), (0, 3)]
    RUN   = [(0, 4), (1, 0), (1, 1)]
    JUMP  = [(1, 2)]    
    FALL  = [(1, 3)]     
    LAND  = [(1, 4)]     
    SKID  = [(2, 1)]     
 
    def __init__(self, x):
        self.x = float(x)
        self.y = float(GROUND_Y)
        self.vy = 0.0
        self.on_ground = True
        self.facing = 1
        self.state = "idle"
        self.frame_idx = 0
        self.timer = 0
        self.frame_delay = 7
 
        sheet = pygame.image.load(SPIDER_PATH).convert()
        cw, ch = self.CELL
 
        def cut(row, col):
            x0 = col * cw
            y0 = self.SHEET_ORIGIN_Y + row * ch
            sub = sheet.subsurface(pygame.Rect(x0, y0, cw, ch))
            sub = make_transparent(sub, self.BG)
            return scale_to(sub, cw * self.SCALE, ch * self.SCALE)
 
        self.clips = {
            "idle": [cut(*rc) for rc in self.IDLE],
            "walk": [cut(*rc) for rc in self.WALK],
            "run":  [cut(*rc) for rc in self.RUN],
            "jump": [cut(*rc) for rc in self.JUMP],
            "fall": [cut(*rc) for rc in self.FALL],
        }
 
    def jump(self):
        if self.on_ground:
            self.vy = self.JUMP_VY
            self.on_ground = False
 
    def _set_state(self, s):
        if self.state != s:
            self.state = s
            self.frame_idx = 0
            self.timer = 0
 
    def update(self, keys):
        moving = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.SPEED
            self.facing = 1
            moving = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.SPEED
            self.facing = -1
            moving = True
 
        
        if not self.on_ground:
            self.vy += self.GRAVITY
        self.y += self.vy
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0
            self.on_ground = True
 
        
        if not self.on_ground:
            self._set_state("jump" if self.vy < 0 else "fall")
        elif moving:
            self._set_state("run" if abs(self.vy) < 0.1 else "walk")
            # usa walk se devagar, run se rápido — aqui só run
            self._set_state("walk")
        else:
            self._set_state("idle")
 
        self.x = max(30, min(W - 30, self.x))
 
        self.timer += 1
        if self.timer >= self.frame_delay:
            self.timer = 0
            frames = self.clips[self.state]
            self.frame_idx = (self.frame_idx + 1) % len(frames)
 
    def draw(self, surf):
        frames = self.clips[self.state]
        img = frames[self.frame_idx % len(frames)]
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
        cw, ch = self.CELL
        sw, sh = cw * self.SCALE, ch * self.SCALE
        draw_x = int(self.x) - sw // 2
        draw_y = int(self.y) - sh
        surf.blit(img, (draw_x, draw_y))
 
 

 
def label(surf, txt, x, y, color=WHITE):
    s = font.render(txt, True, color)
    surf.blit(s, (x, y))
 
 

 
 
def draw_section_labels(surf):
    
    label(surf, "ANIMAÇÃO 1", 30, GROUND_Y - 220, CYAN)
    label(surf, "ANIMAÇÃO 2", W // 2 - 50, GROUND_Y - 180, YELLOW)
    label(surf, "ANIMAÇÃO 3 (vc controla)", W - 230, GROUND_Y - 200, RED)
 
 

 
def main():
    
    hk    = HollowKnightIdle(x=120, y=GROUND_Y)
    may    = MAYWalk(x=W // 2, y=GROUND_Y)
    spider = SPIDER(x=W - 150)
 
    
    bg_surf = pygame.Surface((W, H))
    for y in range(H):
        t = y / H
        r = int(30 + (55 - 30) * t)
        g = int(20 + (45 - 20) * t)
        b = int(50 + (80 - 50) * t)
        pygame.draw.line(bg_surf, (r, g, b), (0, y), (W, y))
    pygame.draw.rect(bg_surf, GROUND_COL, (0, GROUND_Y, W, H - GROUND_Y))
    pygame.draw.line(bg_surf, LINE_COL, (0, GROUND_Y), (W, GROUND_Y), 3)
 
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
 
           
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                spider.jump()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP, pygame.K_SPACE):
                    spider.jump()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
 
        
        keys = pygame.key.get_pressed()
        may.update(keys)
        spider.update(keys)
 
        
        hk.update()  
 
        
        screen.blit(bg_surf, (0, 0))
        hk.draw(screen)
        may.draw(screen)
        spider.draw(screen)
        draw_section_labels(screen)
       
 
        pygame.display.flip()
        clock.tick(FPS)
 
 
if __name__ == "__main__":
    main()
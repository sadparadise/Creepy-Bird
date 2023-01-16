import sys, pygame, random

pygame.init()

run = True
alive = True

size = width, height = 500, 700

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creeepy Bird")

cntr = 2500
scr = 0
fnt_scr = pygame.font.SysFont("inconsolata.ttf", 20)
txt_scr = fnt_scr.render("0", True, (255, 255, 255))
box_scr = 0, 0

fnt_go = pygame.font.SysFont("inconsolata.ttf", 50)
txt_go = fnt_go.render("GAME OVER", True, (255, 255, 255))
box_go = 0, 0

bg_color = 0, 0, 0

plr_color = 255, 0, 0
plr_size = [30, 30]
plr_pos = [(width - plr_size[0])/5, (height - plr_size[1])/2]

pip_color = 0, 255, 0
pip_spd = 0.05
pip_size = [[45, random.randint(50, 500)], [45, random.randint(50, 500)]]
pip_pos = [[width + 250, 0], [width + 500, 0]]

grvt = 0.00015
jmp_frc = 0.150
accl = 0.0

def jump():
    global accl
    accl = -jmp_frc

def game_over():
    screen.blit(txt_go, box_go)        

def restart():
    global alive, plr_pos, plr_size, pip_pos, pip_size, width, height, cntr, scr
    alive = True
    plr_pos = [(width - plr_size[0])/5, (height - plr_size[1])/2]
    pip_size = [[45, random.randint(50, 500)], [45, random.randint(50, 500)]]
    pip_pos = [[width + 250, 0], [width + 500, 0]]
    cntr = 2500
    scr = 0

pygame.mixer.init()
pygame.mixer.music.load("fiona-apple-tymps-the-sick-in-the-head-song.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_r:
                restart()
            if event.key == pygame.K_SPACE:
                jump()

    if alive:
        for pos in pip_pos:
            if plr_pos[0] > pos[0]:
                cntr += 1
                break

        scr = cntr // 2780

        accl += grvt

        if plr_pos[1] + plr_size[1] >= height:
            alive = False

        plr_pos[1] += accl

        for pos, size in zip(pip_pos, pip_size):
            pos[0] -= pip_spd
            if pos[0] + size[0] <= 0:
                pos[0] = width
                size[1] = random.randint(50, 500)
            if ((pos[0] <= plr_pos[0] and plr_pos[0] <= pos[0] + size[0]) or \
               (pos[0] <= plr_pos[0] + plr_size[0] and plr_pos[0] + plr_size[0] <= pos[0] + size[0])) and \
               (size[1] >= plr_pos[1] or size[1] + 150 <= plr_pos[1] + plr_size[1]):
                   alive = False

        screen.fill(bg_color)
        pygame.draw.rect(screen, plr_color, plr_pos + plr_size)
        for pos, size in zip(pip_pos, pip_size):
            pygame.draw.rect(screen, pip_color, pos + size)
            pygame.draw.rect(screen, pip_color, pos[:1] + [size[1] + 150] + [45, height - size[1] - 45])
        txt_scr = fnt_go.render(str(scr), True, (255, 255, 255))
        screen.blit(txt_scr, box_scr)
    else:
        screen.fill(bg_color)
        pygame.draw.rect(screen, plr_color, plr_pos + plr_size)
        for pos, size in zip(pip_pos, pip_size):
            pygame.draw.rect(screen, pip_color, pos + size)
            pygame.draw.rect(screen, pip_color, pos[:1] + [size[1] + 150] + [45, height - size[1] - 45])
        game_over()

    pygame.display.update()

pygame.quit()
sys.exit()

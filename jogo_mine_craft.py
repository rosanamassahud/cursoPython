# minicraft.py - Mini Minecraft simplificado com pygame
# Requisitos: pygame
# Execute: python jogo_mine_craft.py

import pygame
import sys
import random

# --- Configurações ---
SCREEN_W, SCREEN_H = 960, 640
TILE = 32                      # tamanho do bloco (px)
WORLD_W, WORLD_H = 200, 60     # dimensão do mundo em blocos (largura x altura)
GRAVITY = 0.6
JUMP_VELOCITY = -11
PLAYER_W, PLAYER_H = 20, 28
CAMERA_LERP = 0.15             # suaviza movimento da câmera

FPS = 60

# Cores (R,G,B)
SKY = (135, 206, 235)
DIRT = (120, 85, 60)
GRASS = (99, 150, 69)
STONE = (120, 120, 120)
SAND = (194, 178, 128)
WOOD = (150, 100, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 255)

# Tipos de bloco
BLOCKS = {
    0: ("Vazio", None),
    1: ("Grama", GRASS),
    2: ("Terra", DIRT),
    3: ("Pedra", STONE),
    4: ("Areia", SAND),
    5: ("Madeira", WOOD),
}

# --- Inicialização pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# --- Mundo (grid) ---
world = [[0 for _ in range(WORLD_H)] for _ in range(WORLD_W)]

def generate_terrain():
    """Cria um terreno simples com variação de altura."""
    # Base de altura
    base = WORLD_H // 2
    # gerar altura com perlin-like simples (ruído suave)
    heights = []
    h = base
    for x in range(WORLD_W):
        h += random.choice([-1, 0, 0, 1])  # passo aleatório pequeno
        h = max(WORLD_H//3, min(WORLD_H-6, h))
        heights.append(h)
    # preencher blocos: acima de h vazio; h = grama; abaixo = terra/stone
    for x in range(WORLD_W):
        for y in range(WORLD_H):
            if y < heights[x]:
                world[x][y] = 0
            elif y == heights[x]:
                world[x][y] = 1   # grama
            elif y <= heights[x] + 3:
                world[x][y] = 2   # terra
            else:
                # mais fundo -> alterna entre pedra e terra
                world[x][y] = 3 if (y - heights[x]) > 6 else 2

    # criar algumas bolhas de areia perto de superfície aleatoriamente
    for _ in range(40):
        x = random.randint(0, WORLD_W-1)
        y = heights[x] + 1
        if y < WORLD_H:
            world[x][y] = 4

    # árvores pontuais
    for _ in range(40):
        x = random.randint(2, WORLD_W-3)
        # altura da superfície
        y = heights[x]
        # tronco
        h_trunk = random.randint(3, 5)
        for t in range(1, h_trunk+1):
            if y - t >= 0:
                world[x][y - t] = 5
        # copa simples
        for cx in range(x-2, x+3):
            for cy in range(y - h_trunk - 2, y - h_trunk + 1):
                if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H:
                    if random.random() > 0.3:
                        world[cx][cy] = 1

generate_terrain()

# --- Player ---
class Player:
    def __init__(self, x, y):
        # posição em pixels
        self.x = x
        self.y = y
        # velocidade
        self.vx = 0
        self.vy = 0
        # estado
        self.on_ground = False
        # inventário simples: indices de bloco
        self.inventory = [1, 2, 5]  # slots 1-3 (grama, terra, madeira)
        self.selected = 0  # índice selecionado no inventário (0..len-1)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, PLAYER_W, PLAYER_H)

player = Player(WORLD_W * TILE // 2, 0)

# --- Câmera ---
camera_x = player.x - SCREEN_W // 2
camera_y = player.y - SCREEN_H // 2

def world_to_screen(wx, wy):
    """Converte coordenadas de bloco (wx,wy em blocos) para pixels na tela."""
    return int(wx * TILE - camera_x), int(wy * TILE - camera_y)

def pixel_to_block(px, py):
    """Converte pixels da tela para coordenadas do bloco no mundo (inteiro)."""
    wx = int((px + camera_x) // TILE)
    wy = int((py + camera_y) // TILE)
    return wx, wy

def get_block_at(wx, wy):
    if 0 <= wx < WORLD_W and 0 <= wy < WORLD_H:
        return world[wx][wy]
    return None

def set_block_at(wx, wy, b):
    if 0 <= wx < WORLD_W and 0 <= wy < WORLD_H:
        world[wx][wy] = b

# --- Colisão simples baseada em grade ---
def colliding_with_world(rect):
    """Retorna lista de blocos sólidos com os quais rect colide."""
    hits = []
    left = rect.left // TILE
    right = rect.right // TILE
    top = rect.top // TILE
    bottom = rect.bottom // TILE
    for bx in range(left, right+1):
        for by in range(top, bottom+1):
            if 0 <= bx < WORLD_W and 0 <= by < WORLD_H and world[bx][by] != 0:
                tile_rect = pygame.Rect(bx*TILE, by*TILE, TILE, TILE)
                if rect.colliderect(tile_rect):
                    hits.append((bx, by, tile_rect))
    return hits

# --- Loop principal ---
running = True
mouse_held = False
break_mode = True  # True = break (esquerdo) / False = place (direito)

while running:
    dt = clock.tick(FPS) / 1000.0
    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            # pular
            if event.key in (pygame.K_w, pygame.K_SPACE, pygame.K_UP):
                if player.on_ground:
                    player.vy = JUMP_VELOCITY
                    player.on_ground = False
            # trocar slot inventário com 1-3
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                idx = int(event.unicode) - 1
                if 0 <= idx < len(player.inventory):
                    player.selected = idx
            # salvar / reset (debug)
            if event.key == pygame.K_r:
                world = [[0 for _ in range(WORLD_H)] for _ in range(WORLD_W)]
                generate_terrain()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            bx, by = pixel_to_block(mx, my)
            if event.button == 1:  # clique esquerdo -> quebrar
                if 0 <= bx < WORLD_W and 0 <= by < WORLD_H:
                    if world[bx][by] != 0:
                        # quebrar e adicionar ao inventário (simplesmente print; aqui não armazenamos)
                        world[bx][by] = 0
            elif event.button == 3:  # clique direito -> colocar
                # coloca apenas se vazio e há suporte ou planta no ar (simplificação permitida)
                if 0 <= bx < WORLD_W and 0 <= by < WORLD_H:
                    if world[bx][by] == 0:
                        # não permitir colocar dentro do jogador
                        tile_rect = pygame.Rect(bx*TILE, by*TILE, TILE, TILE)
                        if not tile_rect.colliderect(player.rect):
                            world[bx][by] = player.inventory[player.selected]
        elif event.type == pygame.MOUSEWHEEL:
            # roda inventário
            if event.y > 0:
                player.selected = (player.selected - 1) % len(player.inventory)
            else:
                player.selected = (player.selected + 1) % len(player.inventory)

    # --- Input contínuo ---
    keys = pygame.key.get_pressed()
    move_speed = 160
    player.vx = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.vx = -move_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.vx = move_speed

    # --- Física ---
    # aplicar gravidade
    player.vy += GRAVITY
    # aplicar movimento horizontal primeiro com colisão
    new_x = player.x + player.vx * dt
    player_rect_x = pygame.Rect(new_x, player.y, PLAYER_W, PLAYER_H)
    hits = colliding_with_world(player_rect_x)
    if hits:
        # colidiu; resolver: impede movimento horizontal
        # tenta movimento mínimo até encostar
        if player.vx > 0:
            # mover até a borda esquerda do bloco colidido
            min_tx = min(hit[2].left for hit in hits)
            player.x = min_tx - PLAYER_W - 0.001
        elif player.vx < 0:
            max_tx = max(hit[2].right for hit in hits)
            player.x = max_tx + 0.001
        player.vx = 0
    else:
        player.x = new_x

    # movimento vertical
    new_y = player.y + player.vy
    player_rect_y = pygame.Rect(player.x, new_y, PLAYER_W, PLAYER_H)
    hits = colliding_with_world(player_rect_y)
    if hits:
        # colidiu verticalmente -> ajustar e zerar vy se estiver caindo
        # encontrar bloqueio mais próximo
        if player.vy > 0:  # caindo -> posiciona em cima do bloco
            min_by = min(hit[2].top for hit in hits)
            player.y = min_by - PLAYER_H - 0.001
            player.vy = 0
            player.on_ground = True
        elif player.vy < 0:  # subindo -> encosta na base do bloco
            max_by = max(hit[2].bottom for hit in hits)
            player.y = max_by + 0.001
            player.vy = 0
    else:
        player.y = new_y
        player.on_ground = False

    # --- Atualizar câmera (segue jogador) ---
    target_cam_x = player.x + PLAYER_W//2 - SCREEN_W//2
    target_cam_y = player.y + PLAYER_H//2 - SCREEN_H//2
    camera_x += (target_cam_x - camera_x) * CAMERA_LERP
    camera_y += (target_cam_y - camera_y) * CAMERA_LERP

    # limitar câmera para não mostrar além do mundo
    max_cam_x = WORLD_W * TILE - SCREEN_W
    max_cam_y = WORLD_H * TILE - SCREEN_H
    camera_x = max(0, min(camera_x, max_cam_x))
    camera_y = max(0, min(camera_y, max_cam_y))

    # --- Render ---
    screen.fill(SKY)

    # desenhar blocos visíveis
    left_tile = max(0, int(camera_x // TILE) - 1)
    right_tile = min(WORLD_W-1, int((camera_x + SCREEN_W) // TILE) + 1)
    top_tile = max(0, int(camera_y // TILE) - 1)
    bottom_tile = min(WORLD_H-1, int((camera_y + SCREEN_H) // TILE) + 1)

    for bx in range(left_tile, right_tile+1):
        for by in range(top_tile, bottom_tile+1):
            b = world[bx][by]
            if b != 0:
                sx, sy = world_to_screen(bx, by)
                color = BLOCKS.get(b, ("?", BLACK))[1] or BLACK
                pygame.draw.rect(screen, color, (sx, sy, TILE, TILE))
                # contorno leve
                pygame.draw.rect(screen, (0,0,0,50), (sx, sy, TILE, TILE), 1)

    # desenhar grade (opcional, deixa "pixel art")
    #for gx in range((left_tile* TILE) - int(camera_x % TILE), SCREEN_W, TILE):
    #    pygame.draw.line(screen, (0,0,0,15), (gx,0), (gx, SCREEN_H))
    #for gy in range((top_tile* TILE) - int(camera_y % TILE), SCREEN_H, TILE):
    #    pygame.draw.line(screen, (0,0,0,15), (0,gy), (SCREEN_W, gy))

    # desenhar jogador
    player_screen_rect = pygame.Rect(player.x - camera_x, player.y - camera_y, PLAYER_W, PLAYER_H)
    pygame.draw.rect(screen, (200, 50, 50), player_screen_rect)
    # olhos (simples)
    eye_w = 3
    pygame.draw.rect(screen, WHITE, (player_screen_rect.x + 4, player_screen_rect.y + 6, eye_w, eye_w))
    pygame.draw.rect(screen, WHITE, (player_screen_rect.x + 12, player_screen_rect.y + 6, eye_w, eye_w))

    # desenhar posição do mouse em bloco (destacar)
    mx, my = pygame.mouse.get_pos()
    mbx, mby = pixel_to_block(mx, my)
    if 0 <= mbx < WORLD_W and 0 <= mby < WORLD_H:
        sx, sy = world_to_screen(mbx, mby)
        pygame.draw.rect(screen, HIGHLIGHT, (sx, sy, TILE, TILE), 2)

    # UI - inventário
    inv_x = 8
    inv_y = SCREEN_H - 48
    slot_w = 44
    for i, slot in enumerate(player.inventory):
        rect = pygame.Rect(inv_x + i*(slot_w+6), inv_y, slot_w, slot_w)
        pygame.draw.rect(screen, (50,50,50), rect)
        if slot != 0:
            color = BLOCKS.get(slot, ("?", BLACK))[1] or BLACK
            inner = rect.inflate(-8, -8)
            pygame.draw.rect(screen, color, inner)
        if i == player.selected:
            pygame.draw.rect(screen, WHITE, rect, 3)
        else:
            pygame.draw.rect(screen, BLACK, rect, 2)
        # texto do slot
        txt = font.render(f"{i+1}: {BLOCKS.get(slot)[0]}", True, WHITE)
        screen.blit(txt, (rect.x, rect.y - 18))

    # instruções
    info_lines = [
        "W/SPACE = pular    A/D = mover    Clique esquerdo = quebrar    Clique direito = colocar",
        "R = regenerar   1-3 = escolher bloco   Scroll = trocar slot",
        f"Pos bloco: ({mbx}, {mby})   Bloco atual: {BLOCKS[player.inventory[player.selected]][0]}",
    ]
    for i, line in enumerate(info_lines):
        txt = font.render(line, True, BLACK)
        screen.blit(txt, (8, 8 + i*18))

    pygame.display.flip()

pygame.quit()
sys.exit()

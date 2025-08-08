import pygame
import math
import os
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Counter 1")

# Настройки лабиринта
TILE_SIZE = 64
FOV = math.pi / 3  # Поле зрения (60 градусов)
HALF_FOV = FOV / 2
RAY_COUNT = WIDTH // 2
STEP_ANGLE = FOV / RAY_COUNT
MAX_DEPTH = 200
WALL_HEIGHT = 700

SPAWN_COUNTER = 1

# Настройки игрока
player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
player_angle = math.pi / 2
player_speed = 3
rotation_speed = 0.05
player_health = 100

# Настройки врагов
ENEMY_SPEED = 0.5
ENEMY_SIZE = 100
ENEMY_DISTANCE = 1
enemies = []

# Карта лабиринта
maze_map = [
    [2, 2, 3, 2, 3, 2, 3, 2, 3, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 2, 2, 2, 0, 3],
    [3, 0, 0, 2, 0, 0, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 2, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 2, 0, 2],
    [3, 3, 2, 3, 2, 3, 2, 3, 4, 2]
]

def level2():
    global maze_map
    maze_map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                    [1, 0, 2, 3, 0, 2, 2, 2, 0, 1],
                    [1, 0, 2, 0, 0, 0, 0, 2, 0, 1],
                    [1, 0, 2, 0, 2, 0, 0, 2, 0, 1],
                    [1, 0, 2, 0, 2, 0, 0, 0, 0, 1],
                    [1, 0, 2, 0, 2, 3, 3, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

def level3():
    global maze_map
    maze_map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]
    
def level4():
    global maze_map
    maze_map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 4, 0, 0, 0, 4, 1],
                    [1, 0, 4, 0, 4, 0, 4, 0, 4, 1],
                    [1, 0, 4, 0, 4, 0, 4, 0, 4, 1],
                    [1, 0, 4, 0, 4, 0, 4, 0, 4, 1],
                    [1, 0, 4, 0, 4, 0, 4, 0, 4, 1],
                    [1, 0, 4, 0, 4, 0, 4, 0, 4, 1],
                    [1, 0, 4, 0, 4, 0, 4, 0, 4, 1],
                    [1, 0, 4, 0, 0, 0, 4, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

def level5():
    global maze_map
    maze_map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

class Weapon:
    def __init__(self):
        self.cooldown = 0
        self.texture = pygame.Surface((40, 20))
        self.texture.fill((150, 150, 150))
        pygame.draw.rect(self.texture, (100, 100, 100), (0, 0, 40, 20), 2)
        
    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt * 1000
    
    def shoot(self):
        if self.cooldown <= 0:
            self.cooldown = 500  
            return True
        return False

weapon = Weapon()

def is_visible(player_x, player_y, enemy_x, enemy_y):
    """Проверяет, виден ли враг через стены"""
    dx = enemy_x - player_x
    dy = enemy_y - player_y
    distance = math.sqrt(dx*dx + dy*dy)
    
    # Нормализуем направление
    if distance > 0:
        dx /= distance
        dy /= distance
    
    # Проверяем пошагово от игрока к врагу
    steps = int(distance)
    for i in range(1, steps):
        x = player_x + dx * i
        y = player_y + dy * i
        
        # Если на пути есть стена - враг не виден
        if check_collision(x, y, True):
            return False
    return True

# Загрузка текстур
def load_textures():
    textures = {
        1: pygame.Surface((TILE_SIZE, TILE_SIZE)),  # Стандартная стена
        2: None,  # Текстура 1
        3: None,  # Текстура 2
        4: None,  # Текстура 3
        'enemy': None  # Текстура врага
    }
    
    # Стандартная стена
    textures[1].fill((100, 100, 100))
    pygame.draw.rect(textures[1], (70, 70, 70), (0, 0, TILE_SIZE, TILE_SIZE), 3)
    
    # Загрузка текстур из файлов
    try:
        if os.path.exists("texture1.png"):
            textures[2] = pygame.transform.scale(pygame.image.load("texture1.png").convert(), (TILE_SIZE, TILE_SIZE))
        else:
            textures[2] = pygame.Surface((TILE_SIZE, TILE_SIZE))
            textures[2].fill((100, 200, 100))
            
        if os.path.exists("texture2.png"):
            textures[3] = pygame.transform.scale(pygame.image.load("texture2.png").convert(), (TILE_SIZE, TILE_SIZE))
        else:
            textures[3] = pygame.Surface((TILE_SIZE, TILE_SIZE))
            textures[3].fill((100, 100, 200))

        if os.path.exists("texture3.png"):
            textures[4] = pygame.transform.scale(pygame.image.load("texture3.png").convert(), (TILE_SIZE, TILE_SIZE))
        else:
            textures[4] = pygame.Surface((TILE_SIZE, TILE_SIZE))
            textures[4].fill((100, 100, 200))
            
        if os.path.exists("enemy.png"):
            enemy_img = pygame.image.load("enemy.png").convert_alpha()
            textures['enemy'] = pygame.transform.scale(enemy_img, (ENEMY_SIZE*2, ENEMY_SIZE*2))
        else:
            textures['enemy'] = pygame.Surface((ENEMY_SIZE*2, ENEMY_SIZE*2), pygame.SRCALPHA)
            pygame.draw.circle(textures['enemy'], (255, 0, 0), (ENEMY_SIZE, ENEMY_SIZE), ENEMY_SIZE)
    except Exception as e:
        print(f"Ошибка загрузки текстур: {e}")
    
    return textures

textures = load_textures()

# Создание врагов
def spawn_enemies(count=3):
    for _ in range(count):
        while True:
            x = random.randint(1, len(maze_map[0])-2) * TILE_SIZE + TILE_SIZE//2
            y = random.randint(1, len(maze_map)-2) * TILE_SIZE + TILE_SIZE//2
            if maze_map[int(y/TILE_SIZE)][int(x/TILE_SIZE)] == 0:
                enemies.append({
                    'x': x,
                    'y': y,
                    'speed': ENEMY_SPEED,
                    'health': 100,
                    'texture': 'enemy'
                })
                break

# Функция для проверки столкновений
def check_collision(x, y, is_enemy=False):
    map_x, map_y = int(x / TILE_SIZE), int(y / TILE_SIZE)
    if 0 <= map_x < len(maze_map[0]) and 0 <= map_y < len(maze_map):
        return maze_map[map_y][map_x] > 0
    return True

# Функция рейкастинга
def cast_rays(player_x, player_y, player_angle):
    ray_results = []
    for ray in range(RAY_COUNT):
        ray_angle = (player_angle - HALF_FOV) + (ray / RAY_COUNT) * FOV
        
        ray_x, ray_y = player_x, player_y
        ray_cos, ray_sin = math.cos(ray_angle), math.sin(ray_angle)
        
        wall_hit = False
        wall_type = 1
        distance = 0
        vertical = False
        
        for depth in range(MAX_DEPTH * TILE_SIZE):
            ray_x += ray_cos
            ray_y += ray_sin
            
            map_x, map_y = int(ray_x / TILE_SIZE), int(ray_y / TILE_SIZE)
            
            if map_x < 0 or map_y < 0 or map_x >= len(maze_map[0]) or map_y >= len(maze_map):
                distance = MAX_DEPTH * TILE_SIZE
                wall_hit = True
                break
                
            if maze_map[map_y][map_x] > 0:
                wall_type = maze_map[map_y][map_x]
                distance = math.sqrt((ray_x - player_x)**2 + (ray_y - player_y)**2)
                distance *= math.cos(player_angle - ray_angle)
                vertical = abs(ray_cos) > abs(ray_sin)
                wall_hit = True
                break
        
        ray_results.append({
            'wall_hit': wall_hit,
            'wall_type': wall_type,
            'distance': distance,
            'vertical': vertical,
            'ray_x': ray_x,
            'ray_y': ray_y
        })
    
    return ray_results

# Отрисовка меню
def draw_menu():
    screen.fill((0, 0, 0))
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    
    title = font_large.render("Simple Counter 1", True, (255, 255, 255))
    singleplayer_text = font_medium.render("1. Одиночная игра", True, (255, 255, 255))
    multiplayer_text = font_medium.render("2. Мультиплеер", True, (255, 255, 255))
    quit_text = font_medium.render("ESC. Выход", True, (255, 255, 255))
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(singleplayer_text, (WIDTH // 2 - singleplayer_text.get_width() // 2, 250))
    screen.blit(multiplayer_text, (WIDTH // 2 - multiplayer_text.get_width() // 2, 320))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 390))
    
    pygame.display.flip()

# Отрисовка меню мультиплеера
def draw_multiplayer_menu():
    screen.fill((0, 0, 0))
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    
    title = font_large.render("Мультиплеер", True, (255, 255, 255))
    host_text = font_medium.render("1. Создать сервер", True, (255, 255, 255))
    join_text = font_medium.render("2. Подключиться", True, (255, 255, 255))
    back_text = font_medium.render("ESC. Назад", True, (255, 255, 255))
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(host_text, (WIDTH // 2 - host_text.get_width() // 2, 250))
    screen.blit(join_text, (WIDTH // 2 - join_text.get_width() // 2, 320))
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 390))
    
    pygame.display.flip()

# Одиночная игра
def singleplayer_game():
    global player_x, player_y, player_angle, player_health, enemies, SPAWN_COUNTER, ENEMY_DISTANCE, ENEMY_SIZE, ENEMY_SPEED
    
    player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
    player_angle = math.pi / 2
    player_health = 100
    enemies = []
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0

        if len(enemies) < 1:
            if SPAWN_COUNTER == 4:
                ENEMY_DISTANCE = 100
                ENEMY_SIZE = 500
                ENEMY_SPEED = 0.7
                spawn_enemies(1)
            elif SPAWN_COUNTER == 9:
                ENEMY_DISTANCE = 200
                ENEMY_SIZE = 50
                ENEMY_SPEED = 3
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                spawn_enemies(1)
            elif SPAWN_COUNTER == 14:
                ENEMY_DISTANCE = 0
                ENEMY_SIZE = 30
                ENEMY_SPEED = 2.5
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                spawn_enemies(SPAWN_COUNTER)
            elif SPAWN_COUNTER == 19:
                ENEMY_DISTANCE = 500
                ENEMY_SIZE = 1000
                ENEMY_SPEED = 0.5
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                spawn_enemies(1)

            elif SPAWN_COUNTER == 5:
                level2()
                player_health += 10
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                ENEMY_SPEED = 0.5
                ENEMY_SIZE = 100
                ENEMY_DISTANCE = 1 
                spawn_enemies(SPAWN_COUNTER)
            elif SPAWN_COUNTER == 10:
                level3()
                player_health += 10
                ENEMY_SPEED = 0.5
                ENEMY_SIZE = 100
                ENEMY_DISTANCE = 1 
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                spawn_enemies(SPAWN_COUNTER)
            elif SPAWN_COUNTER == 15:
                level4()
                player_health += 10
                ENEMY_SPEED = 0.5
                ENEMY_SIZE = 100
                ENEMY_DISTANCE = 1 
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                spawn_enemies(SPAWN_COUNTER)
            elif SPAWN_COUNTER == 20:
                level5()
                player_health += 10
                ENEMY_SPEED = 0.5
                ENEMY_SIZE = 100
                ENEMY_DISTANCE = 1 
                player_x, player_y = TILE_SIZE * 1.5, TILE_SIZE * 1.5
                spawn_enemies(SPAWN_COUNTER)
            else:
                ENEMY_SPEED = 0.5
                ENEMY_SIZE = 100
                ENEMY_DISTANCE = 1 
                spawn_enemies(SPAWN_COUNTER)
            SPAWN_COUNTER += 1
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
                elif event.key == pygame.K_SPACE:
                    if weapon.shoot():
                        for enemy in enemies[:]:
                            dx = enemy['x'] - player_x
                            dy = enemy['y'] - player_y
                            angle = math.atan2(dy, dx)
                            angle_diff = abs((angle - player_angle + math.pi) % (2 * math.pi) - math.pi)
                            
                            if angle_diff < 0.1 and is_visible(player_x, player_y, enemy['x'], enemy['y']):
                                enemy['health'] -= 25
                                if enemy['health'] <= 0:
                                    enemies.remove(enemy)
        
        weapon.update(dt)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_angle -= rotation_speed * dt * 60
        if keys[pygame.K_d]:
            player_angle += rotation_speed * dt * 60
        
        if keys[pygame.K_w] or keys[pygame.K_s]:
            move_speed = player_speed * dt * 60
            if keys[pygame.K_s]:
                move_speed *= -0.5
                
            new_x = player_x + math.cos(player_angle) * move_speed
            new_y = player_y + math.sin(player_angle) * move_speed
            
            if not check_collision(new_x, player_y):
                player_x = new_x
            if not check_collision(player_x, new_y):
                player_y = new_y
        
        for enemy in enemies:
            dx = player_x - enemy['x']
            dy = player_y - enemy['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0:
                dx /= dist
                dy /= dist
                
                new_x = enemy['x'] + dx * enemy['speed'] * dt * 60
                new_y = enemy['y'] + dy * enemy['speed'] * dt * 60
                
                if not check_collision(new_x, new_y, True):
                    enemy['x'] = new_x
                    enemy['y'] = new_y
            
            if dist < ENEMY_DISTANCE + 20:
                player_health -= 10 * dt
                if player_health <= 0:
                    show_game_over_screen()
                    running = False
        
        ray_results = cast_rays(player_x, player_y, player_angle)
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        pygame.draw.rect(screen, (30, 30, 70), (0, 0, WIDTH, HEIGHT // 2))

        for i, result in enumerate(ray_results):
            if result['wall_hit']:
                wall_height = min(int(WALL_HEIGHT / (result['distance'] + 0.0001) * TILE_SIZE), HEIGHT * 2)
                
                texture = textures.get(result['wall_type'], textures[1])
                tex_offset = (result['ray_y'] if result['vertical'] else result['ray_x']) % TILE_SIZE
                tex_offset = int(tex_offset)
                
                wall_slice = pygame.transform.scale(
                    texture.subsurface(tex_offset, 0, 1, TILE_SIZE),
                    (2, wall_height)
                )
                screen.blit(wall_slice, (i * 2, (HEIGHT - wall_height) // 2))
        
        enemy_sprites = []
        for enemy in enemies:
            dx = enemy['x'] - player_x
            dy = enemy['y'] - player_y
            distance = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx)
            angle_diff = (angle - player_angle + math.pi) % (2 * math.pi) - math.pi
            
            if abs(angle_diff) < HALF_FOV and distance > 0.5 and is_visible(player_x, player_y, enemy['x'], enemy['y']):
                screen_x = int((angle_diff / FOV + 0.5) * WIDTH)
                scale = min(1.0, 100 / distance)
                size = int(ENEMY_SIZE * scale * 2)
                
                enemy_sprites.append({
                    'x': screen_x,
                    'size': size,
                    'distance': distance,
                    'texture': enemy['texture']
                })
        
        # Сортировка и отрисовка врагов
        enemy_sprites.sort(key=lambda e: -e['distance'])
        
        for enemy in enemy_sprites:
            texture = textures[enemy['texture']]
            scaled_texture = pygame.transform.scale(texture, (enemy['size'], enemy['size']))
            screen.blit(
                scaled_texture,
                (enemy['x'] - enemy['size']//2, HEIGHT//2 - enemy['size']//2)
            )
        
        # Отрисовка оружия
        if weapon.cooldown > 400 or weapon.cooldown % 100 < 50:
            screen.blit(weapon.texture, (WIDTH//2 - 20, HEIGHT - 50))
        
        # Отображение патронов
        font = pygame.font.SysFont(None, 24)
        ammo_text = "Готов к стрельбе" if weapon.cooldown <= 0 else "Перезарядка..."
        ammo_surface = font.render(ammo_text, True, (0, 0, 0))
        screen.blit(ammo_surface, (WIDTH - 150, HEIGHT - 30))
        vave = font.render(f"Волна: {SPAWN_COUNTER - 1}", True, (0, 0, 0))
        screen.blit(vave, (WIDTH - 250, HEIGHT - 30))
        
        # Миникарта
        map_size = min(WIDTH // 4, HEIGHT // 4)
        cell_size = map_size // len(maze_map)
        map_surface = pygame.Surface((len(maze_map[0]) * cell_size, len(maze_map) * cell_size))
        map_surface.set_alpha(180)
        
        for y in range(len(maze_map)):
            for x in range(len(maze_map[y])):
                if maze_map[y][x] == 1:
                    pygame.draw.rect(map_surface, (100, 100, 100), (x * cell_size, y * cell_size, cell_size, cell_size))
                elif maze_map[y][x] == 2:
                    pygame.draw.rect(map_surface, (100, 200, 100), (x * cell_size, y * cell_size, cell_size, cell_size))
                elif maze_map[y][x] == 3:
                    pygame.draw.rect(map_surface, (100, 100, 200), (x * cell_size, y * cell_size, cell_size, cell_size))
        
        # Отрисовка врагов на миникарте
        for enemy in enemies:
            pygame.draw.circle(
                map_surface, (255, 0, 0),
                (int(enemy['x'] / TILE_SIZE * cell_size), int(enemy['y'] / TILE_SIZE * cell_size)),
                max(2, cell_size // 4)
            )
        
        # Отрисовка игрока
        pygame.draw.circle(
            map_surface, (0, 255, 0),
            (int(player_x / TILE_SIZE * cell_size), int(player_y / TILE_SIZE * cell_size)),
            max(2, cell_size // 3)
        )
        
        # Направление взгляда
        end_x = int((player_x / TILE_SIZE * cell_size) + math.cos(player_angle) * cell_size)
        end_y = int((player_y / TILE_SIZE * cell_size) + math.sin(player_angle) * cell_size)
        pygame.draw.line(
            map_surface, (0, 255, 0),
            (int(player_x / TILE_SIZE * cell_size), int(player_y / TILE_SIZE * cell_size)),
            (end_x, end_y), 2
        )
        
        screen.blit(map_surface, (10, 10))
        
        # Отображение здоровья
        health_text = f"Здоровье: {int(player_health)}"
        font = pygame.font.SysFont(None, 24)
        health_surface = font.render(health_text, True, (0, 0, 0))
        screen.blit(health_surface, (10, HEIGHT - 30))
        
        pygame.display.flip()

def show_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 72)
    text = font.render("Игра окончена!", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    """Главный цикл программы"""
    clock = pygame.time.Clock()
    singleplayer_game()
        
    clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
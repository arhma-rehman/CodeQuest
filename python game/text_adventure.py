import pygame,random,sys,os
pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
PLAYER_SIZE ,ENEMY_SIZE,TREASURE_SIZE,GIFT_SIZE,HURDLE_SIZE=64,30,40,60,50
MAX_ENEMIES,MAX_TRESURE ,MAX_HURDLES ,i = 7,7,8,5
LEVEL_1_SCORE_THRESHOLD = 700
player_x,player_y = WIDTH // 2 - PLAYER_SIZE // 2,  HEIGHT - PLAYER_SIZE - 20# Initialize game variables
player_speed ,current_level = 2,1
enemies,treasures,hurdles = [],[],[]
score ,high_score =0, 0
GIFT_APPEAR_TIME,gift_timer=5000,0
gift=None
game_over = False
player_img = pygame.image.load(os.path.join("assets", "player.png"))
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))
player_img2 = pygame.image.load(os.path.join("assets", "frog2.png"))
player_img2 = pygame.transform.scale(player_img2, (PLAYER_SIZE, PLAYER_SIZE))
hurdle_img = pygame.image.load(os.path.join("assets", "hurdle.png"))
hurdle_img = pygame.transform.scale(hurdle_img, (HURDLE_SIZE, HURDLE_SIZE))
gift_img = pygame.image.load(os.path.join("assets", "treasure.png"))
gift_img = pygame.transform.scale(gift_img, (GIFT_SIZE, GIFT_SIZE))
star_img = pygame.image.load(os.path.join("assets", "star.png"))
star_img = pygame.transform.scale(star_img, (TREASURE_SIZE, TREASURE_SIZE))
background_img = pygame.image.load(os.path.join("assets", "bck.jpeg"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
selected_image = None
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog Game")
font = pygame.font.Font(None, 36)
def create_enemy():
    while True:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(50, HEIGHT - ENEMY_SIZE - 50)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
        if not any(enemy_rect.colliderect(existing_enemy) for existing_enemy in enemies) and not any(
                enemy_rect.colliderect(existing_hurdle) for existing_hurdle in hurdles):
            return enemy_rect
def create_treasure():
    while True:
        treasure_x = random.randint(0, WIDTH - TREASURE_SIZE)
        treasure_y = random.randint(50, HEIGHT - TREASURE_SIZE - 50)
        treasure_image = pygame.image.load(os.path.join("assets", "gold_coin.png"))
        treasure_image = pygame.transform.scale(treasure_image, (TREASURE_SIZE, TREASURE_SIZE))
        treasure_rect = treasure_image.get_rect(topleft=(treasure_x, treasure_y))
        if not any(treasure_rect.colliderect(existing[0]) for existing in treasures) and not any(treasure_rect.colliderect(existing_hurdle) for existing_hurdle in hurdles):
            return treasure_rect, treasure_image
def create_hurdle():
    while True:
        hurdle_x = random.randint(0, WIDTH - HURDLE_SIZE)
        hurdle_y = random.randint(50, HEIGHT - HURDLE_SIZE - 50)
        hurdle_rect = pygame.Rect(hurdle_x, hurdle_y, HURDLE_SIZE, HURDLE_SIZE)
        if not any(hurdle_rect.colliderect(existing_hurdle) for existing_hurdle in hurdles) and not any(hurdle_rect.colliderect(existing_enemy) for existing_enemy in enemies):
            return hurdle_rect
def create_gift():
    while True:
        gift_x = random.randint(0, WIDTH - TREASURE_SIZE)
        gift_y = random.randint(50, HEIGHT - TREASURE_SIZE - 50)
        gift_rect = pygame.Rect(gift_x, gift_y, TREASURE_SIZE, TREASURE_SIZE)
        if not any(gift_rect.colliderect(existing_treasure[0]) for existing_treasure in treasures) and not any(gift_rect.colliderect(existing_hurdle) for existing_hurdle in hurdles):
            return gift_rect
def handle_gift_appearance():
    global gift, gift_timer
    current_time = pygame.time.get_ticks()
    if gift is None and current_time - gift_timer > GIFT_APPEAR_TIME:
        gift = create_gift()  # Create a new gift
        gift_timer = current_time  # Reset the timer
    if gift is not None:
        screen.blit(gift_img, (gift.x, gift.y))  # Blit the gift image onto the screen
        if current_time - gift_timer > GIFT_APPEAR_TIME + 3000:  # 5000 milliseconds (5 seconds)
            gift = None  # Remove the gift from the screen
            gift_timer = current_time
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
for _ in range(MAX_ENEMIES):
    enemies.append(create_enemy())
for _ in range(MAX_TRESURE):
    treasures.append(create_treasure())
for _ in range(MAX_HURDLES):
    hurdles.append(create_hurdle())
def game_over_screen():
    global game_over
    update_high_score()
    game_over = True
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    try_again_font = pygame.font.Font(None, 36)
    try_again_text = try_again_font.render("Try Again", True, (0, 0, 0))
    try_again_rect = try_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_rect.collidepoint(pygame.mouse.get_pos()):
                    restart_game()
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, (0, 0, 0), try_again_rect, 2)
        screen.blit(try_again_text, try_again_rect.topleft)
        pygame.display.update()
def image_selection_menu():
    global selected_image
    menu_running = True
    option_width = PLAYER_SIZE + 20
    player_option_rect = pygame.Rect(WIDTH // 2 - option_width, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
    another_option_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_option_rect.collidepoint(pygame.mouse.get_pos()):
                    selected_image = player_img
                    menu_running = False
                elif another_option_rect.collidepoint(pygame.mouse.get_pos()):
                    selected_image = pygame.image.load(os.path.join("assets", "frog2.png"))
                    selected_image = pygame.transform.scale(selected_image, (PLAYER_SIZE, PLAYER_SIZE))
                    menu_running = False
        screen.fill(WHITE)
        title_text = font.render("Select Your Character Image:", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
        screen.blit(player_img, player_option_rect)
        screen.blit(player_img2, another_option_rect)
        pygame.display.update()
def restart_game():
    global player_x, player_y, player_speed, enemies, treasures, hurdles, score, high_score,  game_over, current_level,i
    player_x, player_y = WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 20
    player_speed, score ,current_level,i = 2, 0,1,5
    enemies, treasures, hurdles = [], [], []
    game_over = False
    for _ in range(MAX_ENEMIES):
        enemies.append(create_enemy())
    for _ in range(MAX_TRESURE):
        treasures.append(create_treasure())
    for _ in range(MAX_HURDLES):
        hurdles.append(create_hurdle())
    image_selection_menu()
image_selection_menu()
running, player_moved, score_incremented = True, False, False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    handle_gift_appearance()
    elapsed_time =clock.tick(60)
    elapsed_seconds= elapsed_time / 1000.0
    player_speed = 5.0
    if not game_over:
        keys = pygame.key.get_pressed()
        prev_player_x, prev_player_y = player_x, player_y
        player_moved = False
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            player_moved = True
        if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
            player_x += player_speed
            player_moved = True
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
            player_moved = True
        if keys[pygame.K_DOWN] and player_y < HEIGHT - PLAYER_SIZE:
            player_y += player_speed
            player_moved = True
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        enemy_collision = False
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                enemy_collision = True
                if not score_incremented:
                    score += 50
                    score_incremented = True
                enemies.remove(enemy)
                enemies.append(create_enemy())
        treasure_collision = False
        for treasure_rect, _ in treasures:      # Inside your main game loop, where you handle collisions
            if player_rect.colliderect(treasure_rect):      # Your collision handling code here
                if not score_incremented:
                    score,score_incremented =score+100, True
                treasures.remove((treasure_rect, _))  # Remove the collided treasure
                treasures.append(create_treasure())  # Add a new treasure
        for hurdle in hurdles:
            if player_rect.colliderect(hurdle):
                player_collided_with_hurdle = True
                score, i = score-50,i-1
                player_x = max(player_x, hurdle.left - PLAYER_SIZE)
                player_y = max(player_y, hurdle.top - PLAYER_SIZE)
                if i==0:
                    game_over = True
                hurdles.remove(hurdle)
                hurdles.append(create_hurdle())
        gift_collision = False
        if gift is not None:
            if player_rect.colliderect(gift):
                gift_collision = True
                if not score_incremented:
                    score += 500  # Increase the score by 500 for collecting a gift
                    i=i+1
                    score_incremented = True
                gift, gift_timer = None ,pygame.time.get_ticks() # Remove the gift from the screen
        if player_moved:
            score_incremented = False
        if current_level == 1 and score >= LEVEL_1_SCORE_THRESHOLD: # Check if player should move to level 2
            current_level = 2
            MAX_ENEMIES, MAX_HURDLES, MAX_TRESURE = 5, 5, 5
            for _ in range(MAX_ENEMIES):
                enemies.append(create_enemy())
            for _ in range(MAX_TRESURE):
                treasures.append(create_treasure())
            for _ in range(MAX_HURDLES):
                hurdles.append(create_hurdle())
    screen.blit(background_img, (0, 0))
    for hurdle in hurdles:
        screen.blit(hurdle_img, hurdle)
    for enemy in enemies:
        screen.blit(star_img,enemy)
    for treasure_rect, treasure_image in treasures:
        screen.blit(treasure_image, treasure_rect)
    if gift is not None:
        screen.blit(gift_img, gift)
    if selected_image is not None:
        screen.blit(selected_image, (player_x, player_y))
    score_text = font.render(f"Score:", True, (0, 0, 0))
    high_score_text = font.render(f"High Score:", True, (0, 0, 0))
    level_text = font.render(f"Level:", True, (0, 0, 0))
    life_text = font.render(f"Life:", True, (0, 0, 0))
    score_value_text = font.render(f"{score}", True, (255, 0, 0))# Render the numerical values in red
    high_score_value_text = font.render(f"{high_score}", True, (255, 0, 0))
    level_value_text = font.render(f"{current_level}", True, (255, 0, 0))
    life_value_text = font.render(f"{i}", True, (255, 0, 0))
    total_width = ( score_text.get_width() + score_value_text.get_width() + high_score_text.get_width() + high_score_value_text.get_width() +level_text.get_width() + level_value_text.get_width() + life_text.get_width() + life_value_text.get_width() + 50 )
    score_x = (WIDTH - total_width) // 2
    score_value_x = score_x + score_text.get_width() + 5  # Add some space between text and value
    high_score_x = score_value_x + score_value_text.get_width() + 10  # Add some space between texts
    high_score_value_x = high_score_x + high_score_text.get_width() + 5  # Add some space between text and value
    level_x = high_score_value_x + high_score_value_text.get_width() + 10  # Add some space between texts
    level_value_x = level_x + level_text.get_width() + 5  # Add some space between text and value
    life_x = level_value_x + level_value_text.get_width() + 10  # Add some space between texts
    life_value_x = life_x + life_text.get_width() + 5  # Add some space between text and value
    screen.blit(score_text, (score_x, 20))
    screen.blit(score_value_text, (score_value_x, 20))
    screen.blit(high_score_text, (high_score_x, 20))
    screen.blit(high_score_value_text, (high_score_value_x, 20))
    screen.blit(level_text, (level_x, 20))
    screen.blit(level_value_text, (level_value_x, 20))
    screen.blit(life_text, (life_x, 20))
    screen.blit(life_value_text, (life_value_x, 20))
    if game_over:
        game_over_screen()
    pygame.display.update()
pygame.quit()
sys.exit()




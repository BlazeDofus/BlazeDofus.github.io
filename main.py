import pygame
import asyncio # Required for the web version

# Initialize Pygame
pygame.init()

# Setup the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Pong")
clock = pygame.time.Clock()
score_player = 0
score_opponent = 0
font = pygame.font.Font(None, 74)

# Colors (R, G, B)
WHITE = (0, 0, 255)
BLACK = (200, 200, 0)
PADDLE_W, PADDLE_H = 15, 100
BALL_SIZE = 15


# Actors
# pygame.Rect(x, y, width, height)
player = pygame.Rect(10, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
opponent = pygame.Rect(WIDTH - 25, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

ball_speed_x = 9
ball_speed_y = 5
player_speed = 0
opponent_speed = 4

async def main():
    global ball_speed_x, ball_speed_y, player_speed, score_player, score_opponent
    running = True
    while running:
        # 1. Event Handling (Check if we clicked the X to close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Key Pressed Down? Start moving.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -8
                if event.key == pygame.K_DOWN:
                    player_speed = 8
            # Key Released? Stop moving.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed = 0
        # 2. Game Logic
          # Move Ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y
         # Ball Wall Collision (Top/Bottom)
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
           # Move Player
        player.y += player_speed
        
        # Keep player on screen (Constraint)
        if player.top < 0: player.top = 0
        if player.bottom > HEIGHT: player.bottom = HEIGHT
          # Move Opponent (Simple AI)
        if opponent.centery < ball.y:
            opponent.y += opponent_speed
        if opponent.centery > ball.y:
            opponent.y -= opponent_speed

        # Ball Paddle Collision
        # .colliderect() checks if two rectangles are touching!
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1
        # Player Scored (Ball went off right side)
        if ball.left <= 0:
            score_opponent += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= -1
        
        # Opponent Scored (Ball went off left side)
        if ball.right >= WIDTH:
            score_player += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= -1




        # 3. Drawing
        screen.fill(BLACK)
          # Draw Net
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        
        # Draw Actors
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, opponent)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw Score
        player_text = font.render(str(score_player), True, WHITE)
        screen.blit(player_text, (WIDTH//2 - 50, 10))
        
        opponent_text = font.render(str(score_opponent), True, WHITE)
        screen.blit(opponent_text, (WIDTH//2 + 20, 10))

        # Update Display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
        
        # IMPORTANT: This allows the browser to breathe!
        await asyncio.sleep(0)

# Run the game
asyncio.run(main())

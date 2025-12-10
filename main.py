import pygame
import asyncio
import random

# Initialize Pygame
pygame.init()

# Window Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 25  # Size of one grid square

# Calculate grid boundaries
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake")
clock = pygame.time.Clock()
pygame.mixer.music.load("mus1c.wav")
pygame.mixer.music.play(-1)

# Colors
BLACK = (0, 0, 0)
Blue = (0, 0, 255)
DARK_Blue = (0, 0, 200)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Helper function to place food in a valid random location
def place_food(snake_body):
    while True:
        # Generate random coordinates aligned with the grid
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        new_food = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        
        # Check if new food collides with any part of the snake body
        if not any(part.colliderect(new_food) for part in snake_body):
            return new_food

# Helper function to reset the game state
def reset_game():
    initial_snake = [
        pygame.Rect(100, 100, CELL_SIZE, CELL_SIZE),
        pygame.Rect(75, 100, CELL_SIZE, CELL_SIZE),
        pygame.Rect(50, 100, CELL_SIZE, CELL_SIZE)
    ]
    initial_direction = (1, 0) # Start moving right
    # The food placement function now takes the initial snake body
    initial_food = place_food(initial_snake) 
    return initial_snake, initial_direction, initial_direction, initial_food, 0 # snake, direction, next_direction, food, score


async def main():
    running = True
    
    # Initialize game state using the helper function
    snake, direction, next_direction, food, score = reset_game()

    # Game Speed (Milliseconds between moves)
    move_timer = 0
    MOVE_DELAY = 100 
    
    while running:
        dt = clock.tick(60) # Delta time (time since last frame)
        move_timer += dt
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Use next_direction to buffer input
                if event.key == pygame.K_UP and direction != (0, 1):
                            next_direction = (0, -1)
                if event.key == pygame.K_DOWN and direction != (0, -1):
                        next_direction = (0, 1)
                if event.key == pygame.K_LEFT and direction != (1, 0):
                        next_direction = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0):
                            next_direction = (1, 0)

        
        # 2. Update Game Logic
        if move_timer > MOVE_DELAY:
            move_timer = 0
            
            # Update actual direction from buffered input
            direction = next_direction

            # Calculate New Head position
            current_head = snake[0]
            new_x = current_head.x + (direction[0] * CELL_SIZE)
            new_y = current_head.y + (direction[1] * CELL_SIZE)
            new_head = pygame.Rect(new_x, new_y, CELL_SIZE, CELL_SIZE)
            
            # --- Check Collisions (Game Over Conditions) ---

            # Check Wall Collision
            if (new_head.left < 0 or new_head.right > WIDTH or 
                new_head.top < 0 or new_head.bottom > HEIGHT):
                # Reset Game state upon collision
                snake, direction, next_direction, food, score = reset_game()
                continue # Skip the rest of the logic for this frame

            # Check Self Collision
            # We must check the *new* head against the *existing* body segments
            if any(new_head.colliderect(part) for part in snake):
                # Reset Game state upon collision
                snake, direction, next_direction, food, score = reset_game()
                continue # Skip the rest of the logic for this frame
            
            # --- Move Snake / Handle Food ---
            
            # Add the new head to the front of the list
            # FIX 1: Python uses `list.insert(index, element)` not `list.Insert`
            snake.insert(0, new_head)

            # Check collision with food
            if new_head.colliderect(food):
                score += 1
                # We do *not* call snake.pop() here, so the snake grows by one segment.
                
                
                # Move food to random spot (use the robust helper function)
                food = place_food(snake)
            else:
                # If we didn't eat, we pop the tail to maintain length (movement)
                snake.pop()

            # move_snake() goes here
            
        # 3. Drawing
        screen.fill(BLACK)
        
        # Draw Score (Optional, but useful)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Draw Food
        pygame.draw.rect(screen, RED, food)
        
        # Draw Snake
        for i, part in enumerate(snake):
            if i == 0:
                color = Blue # Head
            else:
                color = DARK_Blue # Body
            pygame.draw.rect(screen, color, part)

        
        pygame.display.flip()
        await asyncio.sleep(0) # Yield control back to the async event loop

asyncio.run(main())


import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CARD_WIDTH = 150
CARD_HEIGHT = 225
CARD_COLOR = (255, 255, 255)
CARD_BORDER_COLOR = (0, 0, 0)
FONT_SIZE = 24
SYMBOL_FONT_SIZE = 48
CARD_FONT_COLOR = (0, 0, 0)
SYMBOL_COLOR = (255, 0, 0)

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Uno Card")

# Create a font
font = pygame.font.Font(None, FONT_SIZE)
symbol_font = pygame.font.Font(None, SYMBOL_FONT_SIZE)

# Create a function to draw a Uno card
def draw_card(x, y, card_color, text, symbol=None):
    card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
    card_surface.fill(card_color)
    pygame.draw.rect(card_surface, CARD_BORDER_COLOR, (0, 0, CARD_WIDTH, CARD_HEIGHT), 5)

    text_surface = font.render(text, True, CARD_FONT_COLOR)
    text_rect = text_surface.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 2))

    card_surface.blit(text_surface, text_rect)

    if symbol:
        symbol_surface = symbol_font.render(symbol, True, SYMBOL_COLOR)
        symbol_rect = symbol_surface.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 4))

        card_surface.blit(symbol_surface, symbol_rect)

    screen.blit(card_surface, (x, y))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw a Uno card at (100, 100) with the text "5" and the "Red" symbol
    draw_card(100, 100, (255, 0, 0), "5", "🔴")

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

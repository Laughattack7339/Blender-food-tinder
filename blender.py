import pygame
import random

pygame.init()

WIDTH = 1000
HEIGHT = 600

grey = (200, 200, 200)
green = (4, 107, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blender; food Tinder")

run = True
food_images = ["pizza_hut.png", "mcdonalds.png", "tacobell.png", "culvers.png", "wendys.png"]
food_rects = []
final_choice = False

# List to store the food options swiped right
swiped_rights = []

# Load and scale images
for image_path in food_images:
    img = pygame.image.load(image_path)
    img = pygame.transform.scale(img, (200, 200))
    food_rects.append((img, pygame.Rect(400, 200, 200, 200)))

random.shuffle(food_rects)

active_box = None
current_food = 0
swiped = False
all_swiped_left = False

text_font = pygame.font.SysFont("Permanent Marker", 100)

def draw_text(text, font, text_color, text_x, text_y):
    text_img = font.render(text, True, text_color)
    screen.blit(text_img, (text_x, text_y))

def reset_round():
    global current_food, food_rects, final_choice
    if len(swiped_rights) > 1:
        # If there are multiple right-swiped options, set them as the new options
        food_rects = swiped_rights[:]
        swiped_rights.clear()
        random.shuffle(food_rects)
        current_food = 0
    elif len(swiped_rights) == 1:
        # If only one option remains, it's the final choice
        final_choice = True
    else:
        # No choices left, go hungry message
        all_swiped_left = True

while run:
    screen.fill(grey)

    if final_choice:
        img, rect = swiped_rights[0]
        screen.blit(img, rect)
        draw_text("You want...", text_font, (0, 0, 0), 250, 250)
    elif current_food < len(food_rects):
        img, rect = food_rects[current_food]
        screen.blit(img, rect)
    else:
        reset_round()  # Reset the round if all images in the current selection have been swiped

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and rect.collidepoint(event.pos):
                active_box = rect

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and active_box:
                if rect.x < 300:  # Swipe left
                    swiped = True
                elif rect.x > 500:  # Swipe right
                    swiped = True
                    swiped_rights.append(food_rects[current_food])  # Add to right swipes for narrowing
                active_box = None

        elif event.type == pygame.MOUSEMOTION and active_box:
            active_box.x += event.rel[0]

    # Handle swipe animation
    if swiped:
        if rect.x < 300:  # Swipe left animation
            rect.x -= 10
        elif rect.x > 500:  # Swipe right animation
            rect.x += 10

        # Once the image moves off-screen, move to the next food image
        if rect.x > WIDTH or rect.x < -200:
            current_food += 1
            swiped = False

    # Show "Go hungry then" message if all items were swiped left
    if all_swiped_left:
        draw_text("Go hungry then", text_font, (0, 0, 0), 250, 250)

    pygame.display.update()

pygame.quit()

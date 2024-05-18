# Nafisa Anzum RK-45
# Nur Jannat Meherin RK-37

#In Our Project Balls are represented by aliens that attacks the ship.And the rectangle represents the ship that will defend the attack.The ship have 3 lives.

#Importing Neccessary libraries
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import os

# Define the initial position of the rectangle
rect_x = 0.0

# Define bullet parameters
bullet_x = 0.0
bullet_y = 0.0
bullet_speed = 0.05
bullet_active = False

# Define alien bullet parameters
alien_bullets = []

# Define circle (alien) parameters
circle_centers = []
circle_active = []

# Define additional rows of circles (red and light green)
red_circle_centers = []
red_circle_active = []

green_circle_centers = []
green_circle_active = []

# Define movement parameters for the bunch of balls
movement_direction = 1  # 1 for right, -1 for left
movement_speed = 0.0006  # Speed of movement
movement_boundary = 0.95  # Boundary for the movement

# Initialize score and lives
score = 0
lives = 3

#Function to handle keyboard input
def key_callback(window, key, scancode, action, mods):
    global rect_x, bullet_active, bullet_x, bullet_y
    if key == glfw.KEY_LEFT and (action == glfw.PRESS or action == glfw.REPEAT):# Left Move
        rect_x -= 0.1
        if rect_x < -1.0:
            rect_x = -1.0
    elif key == glfw.KEY_RIGHT and (action == glfw.PRESS or action == glfw.REPEAT):# Right Move
        rect_x += 0.1
        if rect_x > 0.8:
            rect_x = 0.8
    elif key == glfw.KEY_SPACE and action == glfw.PRESS: # Throw Bullet at Aliens
        if not bullet_active:
            bullet_active = True
            bullet_x = rect_x + 0.1  # Set bullet starting position
            bullet_y = -0.8  # Set bullet starting y position

#draw the ship
def draw_rectangle():
    glBegin(GL_QUADS)
    glVertex2f(rect_x, -0.9)
    glVertex2f(rect_x + 0.2, -0.9)
    glVertex2f(rect_x + 0.2, -1.0)
    glVertex2f(rect_x, -1.0)
    glEnd()

#draw the aliens
def draw_circles(circle_centers, circle_active, color):
    glColor3f(*color)  # Set color
    radius = 0.05  # Radius of the circle
    for i, center in enumerate(circle_centers):
        if circle_active[i]:
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(center[0], center[1])
            for angle in range(0, 361, 10):
                x = center[0] + math.sin(math.radians(angle)) * radius
                y = center[1] + math.cos(math.radians(angle)) * radius
                glVertex2f(x, y)
            glEnd()

#Draw the bullet of the ship
def draw_bullet():
    if bullet_active:
        glColor3f(1.0, 1.0, 1.0)  # White color
        glBegin(GL_LINES)
        glVertex2f(bullet_x, bullet_y)
        glVertex2f(bullet_x, bullet_y + 0.05)  # Draw bullet as a line of 5 pixels
        glEnd()

#Draw the alien bullets
def draw_alien_bullets():
    for bullet in alien_bullets:
        glColor3f(*bullet[2])  # Bullet color
        glBegin(GL_LINES)
        glVertex2f(bullet[0], bullet[1])
        glVertex2f(bullet[0], bullet[1] - 0.05)  # Draw bullet as a line of 5 pixels
        glEnd()

#Checking the collision of the aliens by the bullets thrown by ship
def check_collision():
    global bullet_active, score
    if bullet_active:
        for i, center in enumerate(circle_centers):
            if circle_active[i]:
                dist = math.sqrt((bullet_x - center[0]) ** 2 + (bullet_y - center[1]) ** 2)
                if dist < 0.05:  # Radius of circle is 0.05
                    circle_active[i] = False  # Deactivate the hit circle
                    bullet_active = False  # Deactivate bullet
                    score += 10  # Increment score by 10
                    break
        # Check collisions for red circles
        for i, center in enumerate(red_circle_centers):
            if red_circle_active[i]:
                dist = math.sqrt((bullet_x - center[0]) ** 2 + (bullet_y - center[1]) ** 2)
                if dist < 0.05:  # Radius of circle is 0.05
                    red_circle_active[i] = False  # Deactivate the hit circle
                    bullet_active = False  # Deactivate bullet
                    score += 10  # Increment score by 10
                    break
        # Check collisions for green circles
        for i, center in enumerate(green_circle_centers):
            if green_circle_active[i]:
                dist = math.sqrt((bullet_x - center[0]) ** 2 + (bullet_y - center[1]) ** 2)
                if dist < 0.05:  # Radius of circle is 0.05
                    green_circle_active[i] = False  # Deactivate the hit circle
                    bullet_active = False  # Deactivate bullet
                    score += 10  # Increment score by 10
                    break

#Checking the collision of the ship by the bullets thrown by aliens
def check_alien_bullet_collision():
    global rect_x, lives
    for bullet in alien_bullets:
        if bullet[1] <= -0.9:
            if rect_x <= bullet[0] <= rect_x + 0.2:
                print("Ship hit!")
                alien_bullets.remove(bullet)
                lives -= 1
                if lives == 0:
                    print("Game Over!") # prints game over in the terminal and end the game
                    break

#To remove the bullets that crosses the upper boundary
def update_bullet():
    global bullet_y, bullet_active
    if bullet_active:
        bullet_y += bullet_speed
        if bullet_y > 1.0:  # If bullet goes beyond the top boundary, deactivate it
            bullet_active = False

#To remove the bullets that crosses the lower boundary
def update_alien_bullets():
    for bullet in alien_bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < -1.0:  # If bullet goes beyond the bottom boundary, remove it
            alien_bullets.remove(bullet)

#Updating the motions of the circles(Aliens)
def update_circle_positions():
    global movement_direction
    # Determine the leftmost and rightmost x positions of the circles
    all_circles = circle_centers + red_circle_centers + green_circle_centers
    min_x = min(center[0] for center in all_circles)
    max_x = max(center[0] for center in all_circles)

    # Check if the bunch of balls has reached a boundary and reverse direction if needed
    if max_x >= movement_boundary:
        movement_direction = -1
    elif min_x <= -movement_boundary:
        movement_direction = 1

    # Update the positions of all circles
    for centers in [circle_centers, red_circle_centers, green_circle_centers]:
        for i in range(len(centers)):
            centers[i] = (centers[i][0] + movement_direction * movement_speed, centers[i][1])

#Function to handle showing score and lives
#If an alien is vanished by bullet 10 points will be added and by getting attacked the number of lives will decrease by one
def draw_callback(window):
    global score, lives
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    if lives <= 0:
        glColor3f(1.0, 0.0, 0.0)  # Red color for "Game Over"
        render_text("Game Over", -0.2, 0.0)
    else:
        # Draw the rectangle (ship)
        glColor3f(1.0, 0.0, 0.0)  # Red color
        draw_rectangle()

        # Draw the circles (aliens)
       

        draw_circles(circle_centers, circle_active, (1.0, 1.0, 0.0))  # Yellow circles
        draw_circles(red_circle_centers, red_circle_active, (1.0, 0.0, 0.0))  # Red circles
        draw_circles(green_circle_centers, green_circle_active, (0.0, 1.0, 0.0))  # Light green circles

        # Draw the ship's bullet
        draw_bullet()

        # Draw the alien bullets
        draw_alien_bullets()

        # Check for collision between bullet and circles
        check_collision()

        # Check for collision between alien bullets and ship
        check_alien_bullet_collision()

        # Update bullet position
        update_bullet()

        # Update alien bullet positions
        update_alien_bullets()

        # Update circle positions
        update_circle_positions()

    glfw.swap_buffers(window)

# Function to draw numbers using glVertex
def numberMaker(number, x, y, size):
    # Each number is represented by a series of lines
    numbers = {
        '0': [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
        '1': [(0.5, 0), (0.5, 1)],
        '2': [(0, 1), (1, 1), (1, 0.5), (0, 0.5), (0, 0), (1, 0)],
        '3': [(0, 1), (1, 1), (1, 0.5), (0.5, 0.5), (1, 0.5), (1, 0), (0, 0)],
        '4': [(0, 1), (0, 0.5), (1, 0.5), (1, 1), (1, 0)],
        '5': [(1, 1), (0, 1), (0, 0.5), (1, 0.5), (1, 0), (0, 0)],
        '6': [(1, 1), (0, 1), (0, 0), (1, 0), (1, 0.5), (0, 0.5)],
        '7': [(0, 1), (1, 1), (1, 0)],
        '8': [(0, 1), (1, 1), (1, 0), (0, 0), (0, 1), (0, 0.5), (1, 0.5)],
        '9': [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0.5), (1, 0.5)]
    }
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(size, size, size)
    glColor3f(1.0, 1.0, 1.0)  # Set the color to white
    glBegin(GL_LINE_STRIP)
    for segment in numbers[number]:
        glVertex2f(segment[0], segment[1])
    glEnd()
    glPopMatrix()

#Function to render text shown in the screen
def render_text(text, x, y):
    # Create a simple rendering of the text using lines
    for ch in text:
        if '0' <= ch <= '9':
            numberMaker(ch, x, y, 0.1)
        elif ch == ' ':
            x += 0.05
        else:
            # Implement other characters as needed
            pass
        x += 0.12  # Adjust spacing as needed

# Function to render the score and lives
def scoreCount(window):
    global score, lives
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    score_str = str(score)
    x_offset = -0.9
    for char in score_str:
        numberMaker(char, x_offset, 0.8, 0.1)
        x_offset += 0.15  # Adjust as necessary for spacing

    # Draw lives
    lives_str = f"Lives: {lives}"
    render_text(lives_str, -0.9, 0.7)
    
    glfw.swap_buffers(window)

#To handle which alien will shoot at the moment
def alien_fire_bullet():
    active_aliens = [(center, (1.0, 1.0, 0.0)) for i, center in enumerate(circle_centers) if circle_active[i]]
    active_aliens += [(center, (1.0, 0.0, 0.0)) for i, center in enumerate(red_circle_centers) if red_circle_active[i]]
    active_aliens += [(center, (0.0, 1.0, 0.0)) for i, center in enumerate(green_circle_centers) if green_circle_active[i]]
    if active_aliens:
        shooter, color = random.choice(active_aliens)
        alien_bullets.append([shooter[0], shooter[1], color])

#Creating windows
def create_window(title, x_offset):
    window = glfw.create_window(800, 600, title, None, None)
    if not window:
        glfw.terminate()
        return None
    # Check if running under Wayland and skip setting window position if true
    if not os.getenv('WAYLAND_DISPLAY'):
        glfw.set_window_pos(window, x_offset, 100)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    return window

#Main Function
def main():
    global circle_centers, circle_active
    global red_circle_centers, red_circle_active
    global green_circle_centers, green_circle_active

    # Initialize the GLFW library
    if not glfw.init():
        return

    # Create main window
    main_window = create_window("2D Cosmic Clash", 100)
    if not main_window:
        return

    # Create second window
    second_window = create_window("Score Window", 1000)
    if not second_window:
        glfw.destroy_window(main_window)
        return

    # Initialize circle centers and active status
    radius = 0.05  # Radius of the circle
    gap = 0.1  # Gap between circles
    num_circles = 7  # Number of circles
    start_x = -0.8  # Starting x position of the first circle

    center_y = 0.9  # Y coordinate of the yellow circles
    for _ in range(num_circles):
        circle_centers.append((start_x + radius, center_y))
        circle_active.append(True)
        start_x += radius * 2 + gap

    center_y -= radius * 2 + gap  # Y coordinate of the red circles
    start_x = -0.8  # Reset starting x position
    for _ in range(num_circles):
        red_circle_centers.append((start_x + radius, center_y))
        red_circle_active.append(True)
        start_x += radius * 2 + gap

    center_y -= radius * 2 + gap  # Y coordinate of the light green circles
    start_x = -0.8  # Reset starting x position
    for _ in range(num_circles):
        green_circle_centers.append((start_x + radius, center_y))
        green_circle_active.append(True)
        start_x += radius * 2 + gap

    # Loop until the user closes the window
    while not glfw.window_should_close(main_window) and not glfw.window_should_close(second_window):
        # Poll for and process events
        glfw.poll_events()

        # Render main window
        glfw.make_context_current(main_window)
        draw_callback(main_window)

        # Render score window
        glfw.make_context_current(second_window)
        scoreCount(second_window)

        # Randomly fire alien bullets
        if random.random() < 0.01 and lives > 0:  # Adjust probability as needed and only fire if lives remain
            alien_fire_bullet()

    # Terminate GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()

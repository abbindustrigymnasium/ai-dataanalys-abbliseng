# import logging
# import threading
# import time

# def thread_function(name):
#     print("Hewwo from "+str(name)+"!")
#     time.sleep(2)
#     print("Bahbah from "+str(name)+" 0/")

# if __name__ == "__main__":
#     print("Starting this bad boi")
#     for i in range(10):
#         x = threading.Thread(target=thread_function, args=(i,))
#         x.start()
#     # print("Time to gooo")
#     print("Going! :D")
# n = 1

# for i in range(1, n):
#     print(i)

import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

font = pygame.font.Font("Chopsic.ttf", 72)

text = font.render("Hello, World", True, (0, 128, 0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
    
    screen.fill((255, 255, 255))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(60)
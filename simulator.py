'''
    dot-war : simulator 
    lky473736
'''

import pygame
import random

pygame.init()

# 스크린 크기 정의
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Random Pixels Movement")

# 색깔 정의
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# 박스 정의
box_x = 150
box_y = 150
box_width = 500
box_height = 500
box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

# 픽셀들의 정보를 나타내기
pixel_size = 5 
num_pixels = 1000  
speed_increase = 1  

'''
    speed_increase를 1 초과 수치로 올리면 중앙으로 pixel이 수렴하는 현상 발생
'''

pixels = []

# red
for _ in range(num_pixels // 2) :
    pixel_x = random.randint(box_x, box_x + box_width // 2 - pixel_size)
    pixel_y = random.randint(box_y, box_y + box_height - pixel_size)
    speed_x = random.uniform(-2, 2)
    speed_y = random.uniform(-2, 2)
    change_direction_interval = random.randint(20, 100)
    pixels.append([pixel_x, pixel_y, speed_x, speed_y, change_direction_interval, red])

# blue
for _ in range(num_pixels // 2) :
    pixel_x = random.randint(box_x + box_width // 2, box_x + box_width - pixel_size)
    pixel_y = random.randint(box_y, box_y + box_height - pixel_size)
    speed_x = random.uniform(-2, 2)
    speed_y = random.uniform(-2, 2)
    change_direction_interval = random.randint(20, 100)
    pixels.append([pixel_x, pixel_y, speed_x, speed_y, change_direction_interval, blue])

clock = pygame.time.Clock()

info_font = pygame.font.Font(None, 24)

###### system ######
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)
    grid_size = 10
    grid = {}

    for i, pixel in enumerate(pixels):
        # 현재 픽셀의 위치
        grid_x = int(pixel[0] // grid_size)
        grid_y = int(pixel[1] // grid_size)

        if (grid_x, grid_y) not in grid :
            grid[(grid_x, grid_y)] = []
        grid[(grid_x, grid_y)].append(i)

        # collide 체크 (부딪히면 튕겨나가게끔 조성하기)
        for dx in [-1, 0, 1] :
            for dy in [-1, 0, 1] :
                if (grid_x + dx, grid_y + dy) in grid :
                    for j in grid[(grid_x + dx, grid_y + dy)] :
                        if i != j :
                            if abs(pixels[i][0] - pixels[j][0]) < pixel_size and abs(pixels[i][1] - pixels[j][1]) < pixel_size :
                                pixels[i][2] *= speed_increase
                                pixels[i][3] *= speed_increase
                                pixels[j][2] *= speed_increase
                                pixels[j][3] *= speed_increase
                                
                                # 속도가 더 높은 pixel의 색깔로 infection
                                pixels[i][5] = pixels[j][5] = pixels[i][5] if random.random() < 0.5 else pixels[j][5]

        # direction 변경
        if random.randint(0, pixel[4]) == 0:
            pixel[2] = random.uniform(-2, 2)
            pixel[3] = random.uniform(-2, 2)

        pixel[0] += pixel[2]
        pixel[1] += pixel[3]

        # 벽에 부딪힐 때 반사
        if not (box_x <= pixel[0] <= box_x + box_width - pixel_size) :
            pixel[2] *= -1
            
        if not (box_y <= pixel[1] <= box_y + box_height - pixel_size) :
            pixel[3] *= -1

    for pixel in pixels :
        pygame.draw.rect(screen, pixel[5], (pixel[0], pixel[1], pixel_size, pixel_size))

    # 픽셀 counting
    red_count = sum(1 for pixel in pixels if pixel[5] == red)
    blue_count = len(pixels) - red_count
    
    red_info = f"red : {red_count}"
    blue_info = f"blue : {blue_count}"
    screen.blit(info_font.render(red_info, True, black), (10, 10))
    screen.blit(info_font.render(blue_info, True, black), (10, 30))

    pygame.draw.rect(screen, black, box_rect, 2)
    pygame.display.flip()

    # 50프레임 > 60프레임 > 100프레임
    clock.tick(50)  

pygame.quit()

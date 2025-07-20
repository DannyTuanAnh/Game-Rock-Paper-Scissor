import pygame, sys
import socket
import threading


# Thông tin server
HOST = '127.0.0.1'
PORT = 50074

# khởi động thư viện pygame
pygame.init()

# thiết lập màn hình
WIDTH, HEIGHT = 580, 700
screen = pygame.display.set_mode((580, 700))

# thiết lập fps
clock = pygame.time.Clock()

# chèn background
start_bg = pygame.image.load('asset/start.jpg')
play_img = pygame.image.load('asset/play.png')
play_bg = pygame.image.load('asset/bg.jpg')
rock_img = pygame.image.load('asset/rock.png')
paper_img = pygame.image.load('asset/paper.png')
scissor_img = pygame.image.load('asset/scissor.png')

# Tạo Rect cho từng hình để kiểm tra va chạm
play_rect = play_img.get_rect(center = (290, 550))
# Kích thước của nút start nhỏ hơn
start_width = 180
start_height =60
# Tạo rect nhỏ hơn nằm ở trọng tâm của play_button
play_button_rect = pygame.Rect(0, 0, start_width, start_height)
play_button_rect.center = play_rect.center

scissor_rect = scissor_img.get_rect(center=(70, 600))
# Kích thước của nút đấm nhỏ hơn
scissor_width = 50
scissor_height =70
# Tạo rect nhỏ hơn nằm ở trọng tâm của play_button
scissor_button_rect = pygame.Rect(0, 0, scissor_width, scissor_height)
scissor_button_rect.center = scissor_rect.center

rock_rect = rock_img.get_rect(center=(270, 600))
# Kích thước của nút đấm nhỏ hơn
rock_width = 60
rock_height =60
# Tạo rect nhỏ hơn nằm ở trọng tâm của rock_rect
rock_button_rect = pygame.Rect(0, 0, rock_width, rock_height)
rock_button_rect.center = rock_rect.center

paper_rect = paper_img.get_rect(center= (500, 600))
# Kích thước của nút đấm nhỏ hơn
paper_width = 60
paper_height =60
# Tạo rect nhỏ hơn nằm ở trọng tâm của paper_rect
paper_button_rect = pygame.Rect(0, 0, paper_width, paper_height)
paper_button_rect.center = paper_rect.center

game_stated = False

def draw_start_screen():
    screen.blit(start_bg, (0, 0))
    screen.blit(play_img, play_rect)

def draw_game_screen():
    screen.blit(play_bg, (0, 0))
    screen.blit(rock_img, rock_rect)
    screen.blit(paper_img, paper_rect)
    screen.blit(scissor_img, scissor_rect)

# vòng lặp để hiển thị màn hình
while True:
    
    # bắt sự kiện
    for event in pygame.event.get():
        
        
        # Kiểm tra sự kiện nếu người dùng thoát ra ngoài
        if event.type == pygame.QUIT:
            pygame.quit()
            # thoát hệ thống
            sys.exit()
        # Kiểm tra sự kiện click chuột  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_pos):
                game_stated = True
                
            if game_stated:
                if rock_button_rect.collidepoint(mouse_pos):
                    print("Bạn đã chọn: rock")
                elif paper_button_rect.collidepoint(mouse_pos):
                    print("Bạn đã chọn: paper")
                elif scissor_button_rect.collidepoint(mouse_pos):
                    print("Bạn đã chọn: scissor")   
    if game_stated:
        draw_game_screen()
    else:
        draw_start_screen()
            
    # cửa sổ hiển thị
    pygame.display.update()
    
    # chỉnh thông số fps
    clock.tick(120)


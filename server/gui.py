import pygame
import socket
import threading

# Thông tin server
HOST = '127.0.0.1'
PORT = 50074

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client: Rock Scissor Paper")
font = pygame.font.SysFont(None, 30)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Các lựa chọn
buttons = []
choices = ["rock", "scissor", "paper"]
message_lines = []  # để hiển thị tin nhắn từ server
user_choice = ""
send_choice = False
waiting_result = False
received_result = ""

# Socket setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Hàm hiển thị chữ
def draw_text(text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

# Nút
def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + 10, y + 10))
    return rect

# Nhận tin nhắn từ server liên tục
def receive_thread():
    global message_lines, waiting_result, received_result
    while True:
        try:
            msg = client.recv(1024).decode()
            if waiting_result:
                received_result = msg
                waiting_result = False
            else:
                message_lines.append(msg)
        except:
            break

# Gửi lựa chọn tới server
def send_choice_to_server(choice):
    global waiting_result
    client.sendall(choice.encode())
    waiting_result = True

threading.Thread(target=receive_thread, daemon=True).start()

# Nút lựa chọn
def setup_buttons():
    btns = []
    for i, choice in enumerate(choices):
        rect = draw_button(choice.upper(), 100 + i * 140, 280, 100, 40)
        btns.append((choice, rect))
    return btns

buttons = setup_buttons()

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Vẽ khung text
    y = 20
    draw_text("Tin nhắn từ server:", 20, y)
    for line in message_lines[-5:]:
        y += 30
        draw_text(line, 20, y)

    # Hiển thị kết quả nếu có
    if received_result:
        draw_text(f"Kết quả: {received_result}", 20, y + 40)

    # Vẽ nút lựa chọn
    draw_text("Chọn của bạn:", 20, 250)
    for choice, rect in buttons:
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = font.render(choice.upper(), True, BLACK)
        screen.blit(label, (rect.x + 10, rect.y + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for choice, rect in buttons:
                if rect.collidepoint(pos) and not waiting_result:
                    user_choice = choice
                    send_choice_to_server(user_choice)
                    received_result = ""

    pygame.display.flip()

client.close()
pygame.quit()

import socket
import threading
import queue

# Thiết lập localhost và port cho server
HOST = "192.168.84.41" #ip máy chủ
PORT = 50047

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[SERVER] Đang chạy tại {HOST}: {PORT}...")

# Hàng đợi client đang chờ ghép cặp
waiting_clients = queue.Queue()
client_addr = queue.Queue()

# Hàm xác định kết quả trò chơi
def get_result(choice1, choice2):
    rules = {
        'rock': 'scissor',
        'scissor': 'paper',
        'paper': 'rock'
    }
    if choice1 == choice2:
        return 0
    elif rules[choice1] == choice2:
        return 1
    else:
        return 2

# nhận lựa chọn từ 2 client
def receive_choice(client1, client2):
    choice1 = client1.recv(1024).decode().strip().lower()
    choice2 = client2.recv(1024).decode().strip().lower()
    return choice1, choice2

# Xử lý trận đấu giữa 2 client
def handle_match(client1, client2):
    try: 
        # Gửi thông báo ghép cặp thành công
        client1.sendall(b"Da ghep cap! Ban co 3 vong dau!\n")
        client2.sendall(b"Da ghep cap! Ban co 3 vong dau!\n")
        count_result1 = 0
        count_result2 = 0
        i = 3
        client1_addr = client_addr.get()
        client2_addr = client_addr.get()
        
        while i > 0:
            client1.sendall(f"Vong {4 - i}\nChon rock / scissor / paper".encode())
            client2.sendall(f"Vong {4 - i}\nChon rock / scissor / paper".encode())
            choice1, choice2 = receive_choice(client1, client2)
            
            # Kiểm tra dữ liệu vào
            valid_choices = ['rock', 'paper', 'scissor']
            if choice1 not in valid_choices:
                client1.sendall(b"Lua chon cua ban khong hop le! Tran dau ket thuc\n")
                client2.sendall(b"Doi thu da chon sai, tran dau ket thuc.\n")
                return
            if choice2 not in valid_choices:
                client2.sendall(b"Lua chon cua ban khong hop le! Tran dau ket thuc\n")
                client1.sendall(b"Doi thu da chon sai, tran dau ket thuc.\n")
                return

            # in ra server
            print(f"[MATCH][ROUND {4 - i}] Client1 ({client1_addr}) chon: {choice1} | Client 2 ({client2_addr}) chon: {choice2}")

            # tính kết quả
            result = get_result(choice1, choice2)

            # Gửi kết quả cho cả hai
            if result == 1:
                client1.sendall(f"YOU WIN <33 \nBan chon: {choice1}, Doi thu chon: {choice2}.\n".encode())
                client2.sendall(f"YOU LOSE :(( \nBan chon: {choice2}, Doi thu chon: {choice1}.\n".encode())
                count_result1 += 1
            elif result == 2:
               client1.sendall(f"YOU LOSE :(( \nBan chon: {choice1}, Doi thu chon: {choice2}.\n".encode())
               client2.sendall(f"YOU WIN <33  \nBan chon: {choice2}, Doi thu chon: {choice1}.\n".encode())
               count_result2 += 1
            else:
               client1.sendall(f"HOA \nBan chon: {choice1}, Doi thu cung chon: {choice2}.\n".encode())
               client2.sendall(f"HOA  \nBan chon: {choice2}, Doi thu cung chon: {choice1}.\n".encode())
            
            i -= 1 # giảm số vòng đấu
            
        # Sau 3 vòng đấu, so sánh kết quả
        # hỏi có muốn chơi tiếp không
        if count_result1 > count_result2:
            client1.sendall(b"Ban da thang cuoc! Chuc mung!\n\n[SERVER]: Ban co muon choi tiep khong? (yes/no) ")
            client2.sendall(b"Ban da thua cuoc! Cam on da choi!\n\n[SERVER]: Ban co muon choi tiep khong? (yes/no) ")
        elif count_result1 < count_result2:
            client1.sendall(b"Ban da thua cuoc! Cam on da choi!\n\n[SERVER]: Ban co muon choi tiep khong? (yes/no) ")
            client2.sendall(b"Ban da thang cuoc! Chuc mung!\n\n[SERVER]: Ban co muon choi tiep khong? (yes/no) ")
        else:
            client1.sendall(b"Tran dau ket thuc voi ket qua hoa! Cam on da choi!\n\n[SERVER]: Ban co muon choi tiep khong? (yes/no) ")
            client2.sendall(b"Tran dau ket thuc voi ket qua hoa! Cam on da choi!\n\n[SERVER]: Ban co muon choi tiep khong? (yes/no) ")
        
        # Nhận lựa chọn tiếp tục chơi hoặc thoát từ cả hai client
        again1 = client1.recv(1024).decode().strip().lower()
        again2 = client2.recv(1024).decode().strip().lower()
            
        if again1 == "no" and again2 == "no":
            client1.sendall(b"Cam on da choi! Hen gap lai!\n")
            client2.sendall(b"Cam on da choi! Hen gap lai!\n")
            # đóng cả hai kết nối
            client1.close()  
            client2.close()  
        elif again1 == "no" and again2 == "yes":
            client1.sendall(b"Cam on da choi! Hen gap lai!\n")
            client2.sendall(b"Doi thu da roi, vui long doi ghep cap.\n")
            continue_clients(client2, client2_addr)
            # đóng kết nối client1
            client1.close()   
        elif again1 == "yes" and again2 == "no":
            client1.sendall(b"Doi thu da roi, vui long doi ghep cap.\n")
            client2.sendall(b"Cam on da choi! Hen gap lai!\n")
            continue_clients(client1, client1_addr)
            # đóng kết nối client2
            client2.close()  
        else:
            client1.sendall(b"Da bat dau tran moi!\n")
            client2.sendall(b"Da bat dau tran moi!\n")
            # Tiếp tục trận đấu mới
            client_addr.put(client1_addr)
            client_addr.put(client2_addr)
            # hiển thị client tiếp tục cho server
            print(f"[CONTINUE] Client1 ({client1_addr}) và Client2 ({client2_addr}) tiếp tục chơi.")
            handle_match(client1, client2)
    except Exception as e:
        print("[ERROR] Trong match: ", e) 

#   xử lý kết nối từ client, đưa client vào hàng đợi
def handle_client(conn, addr):
    try:
        conn.sendall(b"Chao mung! Dang ghep cap....\n")
        waiting_clients.put(conn)
        client_addr.put(addr)
        
        # vòng lặp chạy cho tới khi nào có đủ 2 client để ghép cặp
        while True:
            #Nếu có đủ 2 client thì tạo trận
            if waiting_clients.qsize() >= 2:
                client1 = waiting_clients.get() 
                client2 = waiting_clients.get() 
                match_thread = threading.Thread(target = handle_match, args = (client1, client2))
                match_thread.start()
    except Exception as e:
        print("[ERROR] Trong handle_client: ", e)

# nếu 1 trong 2 không muốn chơi tiếp thì người còn lại sẽ tiếp tục ghép cặp
def continue_clients(conn, addr):
    try:
        conn.sendall("Chờ ghép cặp với người chơi mới...\n".encode())
        # Thêm người chơi vào hàng chờ
        waiting_clients.put(conn)
        client_addr.put(addr)
        print(f"[CONNECT] Client cũ {addr}")
    except Exception as e:
        print(f"Lỗi khi đưa {addr} vào hàng chờ tiếp tục: {e}")
        

# luồng chính 
def accept_clients():
    while True:
        client_conn, client_addr = server_socket.accept()
        print(f"[CONNECT] Client mới từ {client_addr}")
        threading.Thread(target=handle_client, args=(client_conn, client_addr)).start()
        
# Bắt đầu server
accept_clients()

# xử lý logic vì khi 2 client đi vào đang đợi nhập 
# 1client khác đi vào thì sẽ hiện đang đợi ghép cặp nhưng nếu tắt terminal
# thì server vẫn còn nhận client đó nên khi có tiếp 1 client thứ 4 vào thì
# nó sẽ được ghép cặp với cái client xóa terminal
# thêm 1 hàng đợi client_addr cho lưu thông tin port
# khi 1 client chọn không tiếp tục và client khác chọn tiếp tục thì cả 2 đều bị văng ra 
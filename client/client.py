import socket

# Thông tin kết nối server
HOST = "127.0.0.1" 
PORT = 50074

def main():
    try:
        # Tạo socket và kết nối tới server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # Nhận thông báo từ server 
        welcome_msg = client_socket.recv(1024).decode()
        print("[SERVER]:", welcome_msg)
        
        # Chờ server ghép cặp và bắt đầu trận
        match_msg = client_socket.recv(1024).decode()
        print("[SERVER]:", match_msg)
        
        # Nhập lựa chọn từ người chơi
        i = 3
        while i > 0: 
            round_msg = client_socket.recv(1024).decode()
            print("[SERVER]:", round_msg)
            choice = input("Nhap lua chon: ").strip().lower()
            client_socket.sendall(choice.encode())

            # Nhận kết quả từ server
            result = client_socket.recv(1024).decode()
            print("[KET QUA]:", result)
            i -= 1
        final = client_socket.recv(1024).decode()
        print("[SERVER]:", final)
        again = input("Nhap lua chon: ").strip().lower()
        client_socket.sendall(again.encode())
    except ConnectionRefusedError:
        print("Khong ket noi duoc toi server. Server chua chay?")
    except Exception as e:
        print("Loi xay ra:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
import socket
import threading
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Security Setup ---
SHARED_SALT = b'\x82\x11\xec\x01\x0b\xeb\x12\x07\xeb\x8d\xf5\x0f\x0c\x8e\x12\x0f'

def derive_key(password: str):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SHARED_SALT,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

class SecureChat:
    def __init__(self, username, password):
        self.username = username
        self.fernet = Fernet(derive_key(password))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def encrypt_payload(self, text):
        data = json.dumps({"user": self.username, "msg": text})
        return self.fernet.encrypt(data.encode())

    def decrypt_payload(self, token):
        try:
            data = json.loads(self.fernet.decrypt(token).decode())
            return f"\n[{data['user']}]: {data['msg']}"
        except:
            return "\n!! Decryption Error: Wrong Password or Corrupt Data !!"

    def listen_loop(self, conn):
        while self.running:
            try:
                raw_data = conn.recv(2048)
                if not raw_data:
                    print("\n[SYSTEM]: Connection closed by partner.")
                    self.running = False
                    break
                print(self.decrypt_payload(raw_data))
                print(f"[{self.username}]: ", end="", flush=True)
            except ConnectionResetError:
                print("\n[SYSTEM]: Connection was forcibly reset by the peer.")
                self.running = False
                break
            except Exception as e:
                print(f"\n[SYSTEM]: Unexpected Error: {e}")
                self.running = False
                break

# --- Execution ---
my_name = input("Enter your username: ")
room_pass = input("Enter room password: ")
chat = SecureChat(my_name, room_pass)

mode = input("(H)ost or (J)oin? ").lower()
try:
    if mode == 'h':
        chat.sock.bind(('0.0.0.0', 65432)) 
        chat.sock.listen(1)
        print("Waiting for partner...")
        conn, addr = chat.sock.accept()
        print(f"Connected to {addr}")
    else:
        target = input("Partner IP (use 127.0.0.1 for local): ")
        chat.sock.connect((target, 65432))
        conn = chat.sock

    threading.Thread(target=chat.listen_loop, args=(conn,), daemon=True).start()

    print("--- Chat Started (Type 'exit' to quit) ---")
    while chat.running:
        message = input(f"[{my_name}]: ")
        if message.lower() == 'exit': 
            chat.running = False
            break
        # Only send if there's actual text and connection is alive
        if message.strip() and chat.running:
            try:
                conn.send(chat.encrypt_payload(message))
            except:
                print("[SYSTEM]: Failed to send message. Connection lost.")
                break
finally:
    chat.sock.close()
    print("Program exited.")
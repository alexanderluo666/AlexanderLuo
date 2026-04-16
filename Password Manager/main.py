import json
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, filename="vault.json"):
        self.filename = filename
        self.key = None
        self.vault_data = {"meta": {}, "entries": []}

    def _derive_key(self, master_password, salt=None):
        """Converts a plain text password into a secure 32-byte key."""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key, salt

    def initialize_vault(self, master_password):
        """Creates a new vault file with a fresh salt."""
        self.key, salt = self._derive_key(master_password)
        self.vault_data["meta"]["salt"] = base64.b64encode(salt).decode('utf-8')
        self.save_to_disk()
        print("New vault initialized.")

    def unlock_vault(self, master_password):
        """Loads the salt from the JSON and generates the matching key."""
        if not os.path.exists(self.filename):
            print("Vault file not found. Initialize first.")
            return False
            
        with open(self.filename, "r") as f:
            self.vault_data = json.load(f)
            
        salt = base64.b64decode(self.vault_data["meta"]["salt"])
        self.key, _ = self._derive_key(master_password, salt)
        return True

    def add_password(self, service, username, password):
        """Encrypts a password and adds it to the internal list."""
        f = Fernet(self.key)
        encrypted_pw = f.encrypt(password.encode()).decode('utf-8')
        
        self.vault_data["entries"].append({
            "service": service,
            "username": username,
            "password": encrypted_pw
        })
        self.save_to_disk()

    def get_passwords(self):
        """Decrypts and returns all stored passwords."""
        f = Fernet(self.key)
        results = []
        for entry in self.vault_data["entries"]:
            decrypted_pw = f.decrypt(entry["password"].encode()).decode('utf-8')
            results.append(f"{entry['service']} | {entry['username']}: {decrypted_pw}")
        return results

    def save_to_disk(self):
        with open(self.filename, "w") as f:
            json.dump(self.vault_data, f, indent=4)

# --- Example Usage ---
if __name__ == "__main__":
    pm = PasswordManager()
    
    # Use 'initialize_vault' for the first run, then 'unlock_vault' thereafter
    mp = input("Enter Master Password: ")
    
    if not os.path.exists("vault.json"):
        pm.initialize_vault(mp)
    else:
        pm.unlock_vault(mp)

    while True:
        choice = input("\n1. Add Password\n2. View Passwords\n3. Exit\n> ")
        if choice == "1":
            s = input("Service: ")
            u = input("Username: ")
            p = input("Password: ")
            pm.add_password(s, u, p)
        elif choice == "2":
            for line in pm.get_passwords():
                print(line)
        else:
            break
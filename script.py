import base64
import hashlib
import os
import sys
#import getpass
#import json
import signal
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from cryptography.fernet import Fernet

# Color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
WHITE = "\033[37m"


# Function to display initial layout
def display_initial_layout():
    # Get terminal width or set a default width
    if os.isatty(sys.stdout.fileno()):  # Check if running in a terminal
        terminal_width = os.get_terminal_size().columns
    else:
        terminal_width = 80  # Default width for web output
    layout_lines = [
        f"  {MAGENTA} ＤΣＶΣＬꗞＰΣᗪ 乃ㄚ{RESET}",
    ]
    
    # Calculate padding for center alignment
    for line in layout_lines:
        padded_line = line.center(terminal_width)  # Center the line
        print(padded_line)
    
    print_logo()          # Print the first logo centered
    #print_second_logo()   # Print the second logo left-aligned


# First logo function
def print_logo():
    logo_lines = [
        "\033[31m     ____        _              \033[0m",  # Red
        "\033[33m    | __ )      | | _____ _   _ \033[0m",  # Yellow
        "\033[33m    |  _ \ _____| |/ / _ \ | | |\033[0m",  # White
        "\033[33m    | |_) |_____|   <  __/ |_| |\033[0m",  # Yellow
        "\033[31m    |____/      |_|\_\___|\__, |\033[0m",  # Red
        "\033[31m                           |___/\033[0m"   # White
    ]
    
    # Centered printing of first logo
    terminal_width = os.get_terminal_size().columns
    for line in logo_lines:
        padded_line = line.center(terminal_width)
        print(padded_line)
    
    # Divider line after logo
    print(f"{WHITE}{'=' * terminal_width}{RESET}")


# Second logo function (printed from the left)
"""def print_second_logo():#
   # logo_lines_2 = [
    #    "\033[31m                                   __                                         .__     .__            __                  .__   \033[0m"
    #     "\033[31m    ____ _______  ___.__.______ _/  |_  ____    ____ _______ _____   ______  |  |__  |__|  ____   _/  |_  ____    ____  |  |  \033[0m", 
    #      "\033[31m _/ ___\\_  __ \<   |  |\____ \\   __\/  _ \  / ___\\_  __ \\__  \  \____ \ |  |  \ |  |_/ ___\  \   __\/  _ \  /  _ \ |  |  \033[0m", 
          "\033[31m \  \___ |  | \/ \___  ||  |_> >|  | (  <_> )/ /_/  >|  | \/ / __ \_|  |_> >|   Y  \|  |\  \___   |  | (  <_> )(  <_> )|  |__\033[0m", 
           "\033[31m \___  >|__|    / ____||   __/ |__|  \____/ \___  / |__|   (____  /|   __/ |___|  /|__| \___  >  |__|  \____/  \____/ |____/\033[0m", 
           "\033[31m     \/         \/     |__|                /_____/              \/ |__|         \/          \/                                \033[0m"
    ]

    # Print the second logo starting from the left (no center alignment)
    #for line in logo_lines_2:
      #  print(line)

    # Divider line after second logo
    terminal_width = os.get_terminal_size().columns
   """# print(f"{WHITE}{'=' * terminal_width}{RESET}")

def signal_handler(sig, frame):
    print(f"\n{RED}Exiting the program...{RESET}")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def caesar_encrypt(plaintext: str, shift: int) -> str:
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                encrypted += chr((ord(char) - 97 + shift_amount) % 26 + 97)
            else:
                encrypted += chr((ord(char) - 65 + shift_amount) % 26 + 65)
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    return caesar_encrypt(ciphertext, -shift)

def base64_encode(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

def base64_decode(data: str) -> str:
    try:
        return base64.b64decode(data.encode()).decode()
    except Exception:
        print(f"{RED}Error: Invalid Base64 input.{RESET}")
        return None

def fernet_encrypt(plaintext: str, key: bytes) -> str:
    try:
        fernet = Fernet(key)
        return fernet.encrypt(plaintext.encode()).decode()
    except Exception as e:
        print(f"{RED}Error during Fernet encryption: {e}{RESET}")
        return None

def fernet_decrypt(ciphertext: str, key: bytes) -> str:
    try:
        fernet = Fernet(key)
        return fernet.decrypt(ciphertext.encode()).decode()
    except Exception as e:
        print(f"{RED}Error during Fernet decryption: {e}{RESET}")
        return None

def aes_encrypt(plaintext: str, key: bytes) -> tuple[str, bytes]:
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode(), key
    except Exception as e:
        print(f"{RED}Error during AES encryption: {e}{RESET}")
        return None, None

def aes_decrypt(ciphertext: str, key: bytes) -> str:
    try:
        raw = base64.b64decode(ciphertext.encode())
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ct), AES.block_size)
        return plaintext.decode()
    except Exception as e:
        print(f"{RED}Error during AES decryption: {e}{RESET}")
        return None

def rsa_encrypt(plaintext: str, public_key: RSA.RsaKey) -> str:
    try:
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return base64.b64encode(ciphertext).decode()
    except Exception as e:
        print(f"{RED}Error during RSA encryption: {e}{RESET}")
        return None

def rsa_decrypt(ciphertext: str, private_key_data: bytes) -> str:
    try:
        private_key = RSA.import_key(private_key_data)
        cipher = PKCS1_OAEP.new(private_key)
        plaintext = cipher.decrypt(base64.b64decode(ciphertext.encode()))
        return plaintext.decode()
    except Exception as e:
        print(f"{RED}Error during RSA decryption: {e}{RESET}")
        return None

def hash_md5(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

def hash_sha512(data: str) -> str:
    return hashlib.sha512(data.encode()).hexdigest()

def hash_sha3_512(data: str) -> str:
    return hashlib.sha3_512(data.encode()).hexdigest()

def get_valid_input(prompt: str, valid_options: list[str]) -> str:
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        if choice == 'q':
            return 'q'
        print(f"{RED}Invalid option. Please try again or enter 'q' to quit.{RESET}")

def save_to_file(data: str, file_extension: str):
    while True:
        filename = input(f"Enter a filename to save the data (with .{file_extension} extension): ")
        if not filename.endswith(f'.{file_extension}'):
            filename += f'.{file_extension}'
        try:
            with open(filename, 'w') as f:
                f.write(data)
            print(f"{YELLOW}Data saved to {filename}{RESET}")
            break
        except Exception as e:
            print(f"{RED}Error saving file: {e}. Please try again.{RESET}")

def read_from_file(prompt: str) -> str:
    while True:
        filename = input(prompt)
        try:
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"{RED}File not found. Please try again.{RESET}")
        except Exception as e:
            print(f"{RED}Error reading file: {e}. Please try again.{RESET}")

def get_input_method() -> str:
    return get_valid_input(f"{YELLOW}Choose input method:\n1: Type content\n2: Upload from file\nEnter choice (1/2): {RESET}", ['1', '2'])

def get_content(input_method: str, prompt: str) -> str:
    if input_method == '1':
        return input(prompt)  # For typing content
    else:
        return read_from_file(prompt)  # For uploading from file

def display_help():
    help_text = f"""
{GREEN}Cryptographic Tool Help Menu{RESET}

This tool provides various cryptographic functions including encryption, decryption, and hashing.

{YELLOW}Main Menu Options:{RESET}
1: Encryption - Encrypt your data using various algorithms like AES, RSA, etc.
2: Decryption - Decrypt previously encrypted data using the same methods.
3: Hashing - Generate hash values (fingerprints) for your data.
4: Help - Display this help menu for guidance.
5: Exit - Quit the program.

{YELLOW}Available Encryption/Decryption Methods:{RESET}

- Caesar Cipher: Simple substitution cipher. Example: shifting letters by 3.
- Base64: Encoding scheme for binary data. Converts data into a text format.
- Fernet: Symmetric encryption using cryptography library. Requires a secure key.
- AES: Advanced Encryption Standard. Use a key that is 16, 24, or 32 bytes long.
- RSA: Public-key cryptosystem. Requires a key pair (public and private).

{YELLOW}Available Hashing Methods:{RESET}

- MD5: 128-bit hash function. Not recommended for security-sensitive applications.
- SHA-512: Part of SHA-2 set of cryptographic hash functions. More secure than MD5.
- SHA3-512: Part of SHA-3 set of cryptographic hash functions. Latest standard.

{YELLOW}General Usage:{RESET}

You can choose to input data by typing or uploading from a file. 
For encryption methods that generate keys, you'll be prompted to save or display the key. 
Always keep your encryption keys secure and don't share them.
You can {RED}exit{RESET} the program at any time by entering {GREEN}'ctrl+c'{RESET} at any prompt.


"""
    print(help_text)

def main():

    display_initial_layout()

    while True:
        print(f"{CYAN}\n1: Encryption\n2: Decryption\n3: Hashing\n4: Help\n5: Exit{RESET}")
        choice = get_valid_input("Select an option: ", ['1', '2', '3', '4', '5'])

        if choice == '1':  # Encryption
            print(f"{YELLOW}\nChoose encryption method:\n1: Caesar Cipher\n2: Base64\n3: Fernet\n4: AES\n5: RSA{RESET}")
            enc_choice = get_valid_input("Select an option: ", ['1', '2', '3', '4', '5'])

            input_method = get_input_method()

            if enc_choice == '1':  # Caesar Cipher
                plaintext = get_content(input_method, "If typing, enter your plaintext directly. If uploading, type the filename to upload your plaintext: ")
                while True:
                    try:
                        shift = int(input("Enter shift value: "))
                        break
                    except ValueError:
                        print(f"{RED}Invalid input. Please enter a number.{RESET}")
                ciphertext = caesar_encrypt(plaintext, shift)
                save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the encrypted ciphertext or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                if save_or_display_option == 'file':
                    save_to_file(ciphertext, 'caesar')
                else:
                    print(f"{GREEN}Encrypted ciphertext: {ciphertext}{RESET}")

            elif enc_choice == '2':  # Base64
                plaintext = get_content(input_method, "If typing, enter your plaintext directly. If uploading, type the filename to upload your plaintext: ")
                ciphertext = base64_encode(plaintext)
                save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the Base64 encoded data or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                if save_or_display_option == 'file':
                    save_to_file(ciphertext, 'base64')

            elif enc_choice == '3':  # Fernet
                key = Fernet.generate_key()
                print(f"{YELLOW}Generated Fernet key (store it securely): {key.decode()}{RESET}")
                save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the Fernet key or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                if save_or_display_option == 'file':
                    save_to_file(key.decode(), 'fernet_key')
                else:
                    print(f"{YELLOW}Fernet Key: {key.decode()}{RESET}")

                plaintext = get_content(input_method, "If typing, enter your plaintext directly. If uploading, type the filename to upload your plaintext: ")
                ciphertext = fernet_encrypt(plaintext, key)
                if ciphertext:
                    save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the encrypted ciphertext or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                    if save_or_display_option == 'file':
                        save_to_file(ciphertext, 'fernet')
                    else:
                        print(f"{GREEN}Encrypted ciphertext: {ciphertext}{RESET}")

            elif enc_choice == '4':  # AES
                plaintext = get_content(input_method, "If typing, enter your plaintext directly. If uploading, type the filename to upload your plaintext: ")
                key_length = get_valid_input("Select key length (1: 16 bytes, 2: 24 bytes, 3: 32 bytes): ", ['1', '2', '3'])

                if key_length == '1':
                    key = os.urandom(16)
                elif key_length == '2':
                    key = os.urandom(24)
                else:
                    key = os.urandom(32)

                save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the AES key or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                if save_or_display_option == 'file':
                    save_to_file(key.hex(), 'aes_key')
                else:
                    print(f"{YELLOW}AES Key: {key.hex()}{RESET}")

                ciphertext, _ = aes_encrypt(plaintext, key)
                if ciphertext:
                    save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the encrypted ciphertext or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                    if save_or_display_option == 'file':
                        save_to_file(ciphertext, 'aes')
                    else:
                        print(f"{GREEN}Encrypted ciphertext: {ciphertext}{RESET}")

            elif enc_choice == '5':  # RSA
                private_key = RSA.generate(2048)
                public_key = private_key.publickey()

                plaintext = get_content(input_method, "If typing, enter your plaintext directly. If uploading, type the filename to upload your plaintext: ")
                ciphertext = rsa_encrypt(plaintext, public_key)
                if ciphertext:
                    save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the encrypted message or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                    if save_or_display_option == 'file':
                        save_to_file(ciphertext, 'rsa')
                    else:
                        print(f"{GREEN}Encrypted message: {ciphertext}{RESET}")

                save_or_display_option = get_valid_input(f"{YELLOW}Do you want to save the RSA private key or display it? (Type 'file' or 'display'): {RESET}", ['file', 'display'])
                if save_or_display_option == 'file':
                    save_to_file(private_key.export_key().decode(), 'rsa_private_key.pem')
                else:
                    print(f"{YELLOW}RSA Private Key: {private_key.export_key().decode()}{RESET}")

        elif choice == '2':  # Decryption
            print(f"{YELLOW}\nChoose decryption method:\n1: Caesar Cipher\n2: Base64\n3: Fernet\n4: AES\n5: RSA{RESET}")
            dec_choice = get_valid_input("Select an option: ", ['1', '2', '3', '4', '5'])

            input_method = get_input_method()

            if dec_choice == '1':  # Caesar Cipher
                ciphertext = get_content(input_method, "If typing, enter your ciphertext directly. If uploading, type the filename to upload your ciphertext: ")
                while True:
                    try:
                        shift = int(input("Enter shift value: "))
                        break
                    except ValueError:
                        print(f"{RED}Invalid input. Please enter a number.{RESET}")
                plaintext = caesar_decrypt(ciphertext, shift)
                print(f"{GREEN}Decrypted plaintext: {plaintext}{RESET}")

            elif dec_choice == '2':  # Base64
                ciphertext = get_content(input_method, "If typing, enter your Base64 encoded string directly. If uploading, type the filename to upload your Base64 string: ")
                plaintext = base64_decode(ciphertext)
                if plaintext:
                    print(f"{GREEN}Base64 Decoded: {plaintext}{RESET}")

            elif dec_choice == '3':  # Fernet
                key = get_content(input_method, "If typing, enter your Fernet key directly. If uploading, type the filename to upload your Fernet key: ")
                ciphertext = get_content(input_method, "If typing, enter your ciphertext directly. If uploading, type the filename to upload your ciphertext: ")
                plaintext = fernet_decrypt(ciphertext, key)
                if plaintext:
                    print(f"{GREEN}Decrypted plaintext: {plaintext}{RESET}")

            elif dec_choice == '4':  # AES
                ciphertext = get_content(input_method, "If typing, enter your ciphertext directly. If uploading, type the filename to upload your ciphertext: ")
                key = bytes.fromhex(get_content(input_method, "If typing, enter your AES key in hex directly. If uploading, type the filename to upload your AES key: "))
                plaintext = aes_decrypt(ciphertext, key)
                if plaintext:
                    print(f"{GREEN}Decrypted plaintext: {plaintext}{RESET}")

            elif dec_choice == '5':  # RSA
                ciphertext = get_content(input_method, "If typing, enter your RSA encrypted message directly. If uploading, type the filename to upload your RSA encrypted message: ")
                private_key = get_content(input_method, "If typing, enter your RSA private key in PEM format directlycls. If uploading, type the filename to upload your RSA private key: ")
                plaintext = rsa_decrypt(ciphertext, private_key)
                if plaintext:
                    print(f"{GREEN}Decrypted plaintext: {plaintext}{RESET}")

        elif choice == '3':  # Hashing
            print(f"{YELLOW}\nChoose hashing method:\n1: MD5\n2: SHA-512\n3: SHA3-512{RESET}")
            hash_choice = get_valid_input("Select an option: ", ['1', '2', '3'])
            input_method = get_input_method()
            data = get_content(input_method, "If typing, enter data to hash directly. If uploading, type the filename to upload your data: ")
            if hash_choice == '1':
                print(f"{GREEN}MD5 Hash: {hash_md5(data)}{RESET}")
            elif hash_choice == '2':
                print(f"{GREEN}SHA-512 Hash: {hash_sha512(data)}{RESET}")
            elif hash_choice == '3':
                print(f"{GREEN}SHA3-512 Hash: {hash_sha3_512(data)}{RESET}")

        elif choice == '4':  # Help
            display_help()

        elif choice == '5':  # Exit
            print(f"{RED}Exiting the program.{RESET}")
            break
  
if __name__ == "__main__":
    main()
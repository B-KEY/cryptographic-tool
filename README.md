# Cryptographic Tool

A comprehensive cryptographic tool that provides various encryption, decryption, and hashing functionalities.

## Features

- Multiple encryption methods:
  - Caesar Cipher
  - Base64 Encoding/Decoding
  - Fernet (Symmetric Encryption)
  - AES (Advanced Encryption Standard)
  - RSA (Public Key Cryptography)
  
- Hashing algorithms:
  - MD5
  - SHA-512
  - SHA3-512

- User-friendly interface with colored output
- File input/output support
- Interactive command-line interface

## Requirements

python 
pycryptodome
cryptography

## Installation

1. Clone the repository:

bash
git clone https://github.com/B-KEY/cryptographic-tool.git
cd crypto-tool

2. Install required packages:

bash
pip install pycryptodome cryptography

## Usage

Run the script:
```bash
python script.py
```

Follow the interactive menu to:
1. Encrypt data
2. Decrypt data
3. Generate hashes
4. View help
5. Exit

## Security Notice

- This tool is for educational purposes
- Always use secure methods to store and transfer encryption keys
- MD5 is included for legacy purposes but is not recommended for security-sensitive applications
# Grafana-Gdecrypt

**Grafana-Gdecrypt** is a lightweight Python utility designed to decrypt secrets stored in Grafana v8+ and v9+ databases. This tool is particularly useful for post-exploitation scenarios following a directory traversal vulnerability (such as **CVE-2021-43798**), where an attacker has obtained the `grafana.db` and the `secret_key` from `grafana.ini`.

The utility automates the extraction and decryption of `basicAuthPassword` and other sensitive blobs found in the `data_source` table.

## Features

- **Modern & Legacy Support:** Automatically detects and handles both `AES-GCM` (v8+) and `AES-CFB` (legacy) encryption modes.
    
- **Key Derivation:** Implements PBKDF2-HMAC-SHA256 derivation with 10,000 iterations, mimicking Grafana's internal Go logic.
    
- **Dynamic Salt Handling:** Automatically extracts the 8-byte salt prefix from blobs or allows for manual salt overrides.
    
- **Input:** Accepts payloads in **Base64** format.
    

## Prerequisites

- Python 3.x
    
- `pycryptodome` library
    

## Installation

Clone the repository and install the required dependencies:

```
git clone [https://github.com/Edward-w-Jack/grafana-gdecrypt.git](https://github.com/Edward-w-Jack/grafana-gdecrypt.git)
cd grafana-gdecrypt
pip install -r requirements.txt
```

## Usage

To decrypt a secret, you must provide the `secret_key` (found in `grafana.ini`) and the encrypted string (found in the `data_source` or `user` table of `grafana.db`).

```
python3 gdecrypt.py -s "YOUR_GRAFANA_SECRET_KEY" -p "ENCRYPTED_PASSWORD_BLOB"
```

### Optional Arguments

- `-s`, `--secret`: The `secret_key` from the Grafana configuration.
    
- `-p`, `--password`: The encrypted password/secret (Base64).
    
- `--salt`: Optional manual salt string if the blob deviates from the standard 8-byte prefix.
    

## Technical Context

In Grafana v8+, secrets are packed into a specific byte structure before storage. This tool parses that structure:

1. **Algorithm Header:** (Optional) Prefixed with `*` (e.g., `*aes-gcm*`).
    
2. **Salt:** 8 bytes used for the PBKDF2 key derivation.
    
3. **Nonce/IV:** Initialization vector for the AES cipher.
    
4. **Ciphertext:** The encrypted payload.
    
5. **Auth Tag:** (GCM only) 16-byte tag for integrity verification.
    

## Credits & Attribution

- **Author:** Developed by **@asquishynerd** as part of security research and post-exploitation study.
    
- **Logic Source:** Ported and expanded from the Go implementation provided by [jas502n/Grafana-CVE-2021-43798](https://github.com/jas502n/Grafana-CVE-2021-43798 "null").
    
- **Development Assistance:** Researched and developed with the collaborative assistance of **Gemini** (Google's AI).
    

## Disclaimer

This tool is intended for educational purposes and authorized security auditing only. The author is not responsible for any misuse or damage caused by this utility.

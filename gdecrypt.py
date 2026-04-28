import base64
import hashlib
import argparse
import sys
from Crypto.Cipher import AES

def decrypt(payload_b64, secret, salt_str=""):
    try:
        payload = base64.b64decode(payload_b64)
    except Exception:
        return "Error: Invalid Base64 input."

    # Algorithm derivation logic
    alg = "aes-cfb"
    if payload[0] == ord('*'):
        payload = payload[1:]
        delim_idx = payload.find(ord('*'))
        if delim_idx != -1:
            alg_b64 = payload[:delim_idx]
            alg = base64.b64decode(alg_b64).decode('utf-8')
            payload = payload[delim_idx + 1:]

    # Use provided salt or extract default 8-byte salt from payload
    if salt_str:
        salt = salt_str.encode()
        encrypted_data = payload # If manual salt is provided, assume no salt prefix
    else:
        salt = payload[:8]
        encrypted_data = payload[8:]

    # Key Derivation
    key = hashlib.pbkdf2_hmac('sha256', secret.encode(), salt, 10000, 32)

    try:
        if alg == "aes-gcm":
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:-16]
            tag = encrypted_data[-16:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        else:
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
            return cipher.decrypt(ciphertext).decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {e}"

def main():
    parser = argparse.ArgumentParser(description="Grafana Password & Data Source Decryptor")
    parser.add_argument("-p", "--password", required=True, help="The encrypted Base64 password/secret from the DB")
    parser.add_argument("-s", "--secret", required=True, help="The secret_key from grafana.ini")
    parser.add_argument("--salt", help="Optional: Manual salt string if not prefixed in the blob")

    args = parser.parse_args()

    result = decrypt(args.password, args.secret, args.salt)
    print(f"\n[+] Result: {result}")

if __name__ == "__main__":
    main()

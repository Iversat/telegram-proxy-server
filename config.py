import sys
import json
import secrets
import os
import urllib.request
import binascii
from cryptography.fernet import Fernet
from dotenv import load_dotenv

USERS_FILE = 'users.enc'
ENV_FILE = '.env'
TLS_DOMAIN = "yandex.ru"


def init_env():
    if not os.path.exists(ENV_FILE):
        key = Fernet.generate_key().decode()
        with open(ENV_FILE, 'w') as f:
            f.write(f"ENCRYPTION_KEY={key}\n")
            f.write("PORT=1080\n")
            f.write("SERVER=\n")
    load_dotenv(ENV_FILE)


def get_cipher():
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        init_env()
        key = os.getenv('ENCRYPTION_KEY')
    return Fernet(key.encode())


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    cipher = get_cipher()
    try:
        with open(USERS_FILE, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception:
        return {}


init_env()
PORT = int(os.getenv('PORT', 1080))
_users_data = load_users()
USERS = {k: v['secret'] for k, v in _users_data.items() if v.get('status', 'off') == 'on'}


def save_users(users):
    cipher = get_cipher()
    data = json.dumps(users, indent=4).encode()
    encrypted_data = cipher.encrypt(data)
    with open(USERS_FILE, 'wb') as f:
        f.write(encrypted_data)


def get_server_address():
    env_server = os.getenv('SERVER')
    if env_server:
        return env_server
    try:
        return urllib.request.urlopen('https://api.ipify.org', timeout=3).read().decode('utf-8')
    except Exception:
        return "YOUR_SERVER_IP"


def generate_secret():
    return secrets.token_hex(16)


def get_faketls_secret(base_secret):
    domain_hex = binascii.hexlify(TLS_DOMAIN.encode('utf-8')).decode('utf-8')
    return f"ee{base_secret}{domain_hex}"


def print_help():
    print("Commands:")
    print("  python3 config.py help")
    print("  python3 config.py list")
    print("  python3 config.py add <name>")
    print("  python3 config.py del <name>")
    print("  python3 config.py on <name>")
    print("  python3 config.py off <name>")
    print("  python3 config.py link <name|number>")


def main():
    init_env()
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1]

    if cmd == 'help':
        print_help()
        return

    users = load_users()
    sorted_users = list(users.keys())

    if cmd == 'list':
        if not users:
            print("Empty.")
        for i, u in enumerate(sorted_users, 1):
            data = users[u]
            print(f"{i}. {u} | Secret: {data['secret'][:8]}... | Status: {data['status']}")
        return

    if len(sys.argv) < 3:
        print_help()
        return

    arg = sys.argv[2]
    user = None

    if arg.isdigit() and cmd == 'link':
        index = int(arg) - 1
        if 0 <= index < len(sorted_users):
            user = sorted_users[index]
        else:
            return
    else:
        user = arg

    if cmd == 'add':
        if user in users:
            return
        secret = generate_secret()
        users[user] = {'secret': secret, 'status': 'on'}
        save_users(users)

        port = os.getenv('PORT', '1080')
        ip = get_server_address()
        fake_tls = get_faketls_secret(secret)
        link = f"tg://proxy?server={ip}&port={port}&secret={fake_tls}"
        print(f"Added: {user}\nLink: {link}")

    elif cmd == 'link':
        if user in users:
            secret = users[user]['secret']
            port = os.getenv('PORT', '1080')
            ip = get_server_address()
            fake_tls = get_faketls_secret(secret)
            link = f"tg://proxy?server={ip}&port={port}&secret={fake_tls}"
            print(f"User: {user} | Status: {users[user]['status']}\nLink: {link}")

    elif cmd == 'del':
        if user in users:
            del users[user]
            save_users(users)
            print(f"Deleted: {user}")

    elif cmd == 'off':
        if user in users:
            users[user]['status'] = 'off'
            save_users(users)
            print(f"Disabled: {user}")

    elif cmd == 'on':
        if user in users:
            users[user]['status'] = 'on'
            save_users(users)
            print(f"Enabled: {user}")


if __name__ == '__main__':
    main()

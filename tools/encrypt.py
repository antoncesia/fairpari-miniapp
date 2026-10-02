"""Шифрует прототип паролем и собирает публикуемый index.html.

Исходник src/index.plain.html и файл с паролем в репозиторий не попадают (.gitignore).
В index.html лежит только шифротекст (AES-256-GCM, ключ из пароля через PBKDF2-SHA256)
и экран ввода пароля, расшифровка идёт в браузере.

Запуск из корня репозитория:
    pip install cryptography
    PROTO_PASSWORD_FILE=../fairpari-miniapp.password.txt python3 tools/encrypt.py
"""
import base64
import os
import pathlib
import secrets
import sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.plain.html"
GATE = ROOT / "tools" / "gate.html"
OUT = ROOT / "index.html"
ITER = 310_000


def read_password() -> str:
    path = os.environ.get("PROTO_PASSWORD_FILE")
    if not path:
        sys.exit("Укажите файл с паролем: PROTO_PASSWORD_FILE=путь python3 tools/encrypt.py")
    pw = pathlib.Path(path).expanduser().read_text(encoding="utf-8").strip().splitlines()[-1].strip()
    if len(pw) < 10:
        sys.exit("Пароль короче 10 символов — задайте длиннее.")
    return pw


def main() -> None:
    pw = read_password()
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode("utf-8"))
    ct = AESGCM(key).encrypt(iv, SRC.read_bytes(), None)
    payload = base64.b64encode(salt + iv + ct).decode("ascii")
    html = GATE.read_text(encoding="utf-8").replace("__PAYLOAD__", payload).replace("__ITER__", str(ITER))
    OUT.write_text(html, encoding="utf-8")
    print(f"index.html собран: {OUT.stat().st_size // 1024} КБ, шифротекст {len(ct) // 1024} КБ")


if __name__ == "__main__":
    main()

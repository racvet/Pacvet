import os
import sys
import time
import json
import re
import socket
import hashlib
import base64
import random
import string
import subprocess
from datetime import datetime
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import whois
import dns.resolver
from bs4 import BeautifulSoup

class Colors:
    PURPLE = '\033[95m'
    LIGHT = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('clear')

def banner():
    clear()
    print(Colors.PURPLE + "=" * 70)
    print(Colors.BOLD + Colors.LIGHT + "     💀  РАСВЕТ PRO  💀")
    print(Colors.PURPLE + "=" * 70)
    print(Colors.CYAN + "   🔫  20+ МОДУЛЕЙ ДЛЯ OSINT  🔫")
    print(Colors.PURPLE + "=" * 70 + Colors.RESET)
    print("")

# ===== МОДУЛЬ 1: ПОИСК ПО НОМЕРУ =====
def phone_info():
    phone = input("📱 Введите номер с +: ")
    try:
        num = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(num):
            print(Colors.RED + "❌ Неверный номер" + Colors.RESET)
            return
        print(Colors.GREEN + "\n📊 РЕЗУЛЬТАТ:" + Colors.RESET)
        print(f"  Страна: {geocoder.description_for_number(num, 'ru')}")
        print(f"  Оператор: {carrier.name_for_number(num, 'ru')}")
        print(f"  Код страны: +{num.country_code}")
        print(f"  Тип: {'Мобильный' if phonenumbers.number_type(num) == 1 else 'Стационарный'}")
        print(f"  Часовой пояс: {', '.join(timezone.time_zones_for_number(num))}")
        print(f"  Формат: {phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        
        # Соцсети и мессенджеры
        clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        print(Colors.CYAN + "\n🌐 ССЫЛКИ:" + Colors.RESET)
        print(f"  Telegram: https://t.me/{clean}")
        print(f"  WhatsApp: https://wa.me/{phone}")
        print(f"  Viber: https://viber.click/{phone}")
        print(f"  Signal: https://signal.me/#p/{clean}")
        print(f"  Google: https://www.google.com/search?q={phone}")
        print(f"  Yandex: https://yandex.ru/search/?text={phone}")
    except Exception as e:
        print(Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

# ===== МОДУЛЬ 2: ПОИСК ПО IP =====
def ip_info():
    ip = input("🌐 Введите IP: ")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        d = r.json()
        if d.get('status') == 'fail':
            print(Colors.RED + "❌ Неверный IP" + Colors.RESET)
            return
        print(Colors.GREEN + "\n📊 РЕЗУЛЬТАТ:" + Colors.RESET)
        print(f"  Страна: {d.get('country', 'Неизвестно')}")
        print(f"  Город: {d.get('city', 'Неизвестно')}")
        print(f"  Регион: {d.get('regionName', 'Неизвестно')}")
        print(f"  Провайдер: {d.get('isp', 'Неизвестно')}")
        print(f"  Широта: {d.get('lat', 'Неизвестно')}")
        print(f"  Долгота: {d.get('lon', 'Неизвестно')}")
    except Exception as e:
        print(Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

# ===== МОДУЛЬ 3: УТЕЧКИ ПО EMAIL =====
def email_breach():
    email = input("📧 Введите email: ")
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            breaches = r.json()
            names = [b['Name'] for b in breaches]
            print(Colors.GREEN + "\n📊 РЕЗУЛЬТАТ:" + Colors.RESET)
            print(f"  Email: {email}")
            print(f"  Утечки: Найден в {len(breaches)} утечках")
            print(f"  Сервисы: {', '.join(names[:5])}" + ("..." if len(names) > 5 else ""))
        elif r.status_code == 404:
            print(Colors.GREEN + "✅ Email не найден в утечках" + Colors.RESET)
        else:
            print(Colors.RED + "❌ Ошибка API" + Colors.RESET)
    except Exception as e:
        print(Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

# ===== МОДУЛЬ 4: ПОИСК ПО НИКУ =====
def username_search():
    nick = input("👤 Введите ник: ")
    sites = {
        "GitHub": f"https://github.com/{nick}",
        "Instagram": f"https://www.instagram.com/{nick}",
        "Twitter": f"https://twitter.com/{nick}",
        "VK": f"https://vk.com/{nick}",
        "Reddit": f"https://www.reddit.com/user/{nick}",
        "YouTube": f"https://www.youtube.com/@{nick}",
        "TikTok": f"https://www.tiktok.com/@{nick}",
        "Pinterest": f"https://www.pinterest.com/{nick}",
        "Telegram": f"https://t.me/{nick}",
        "GitLab": f"https://gitlab.com/{nick}",
        "Medium": f"https://medium.com/@{nick}",
        "Tumblr": f"https://{nick}.tumblr.com"
    }
    print(Colors.GREEN + "\n🔍 ССЫЛКИ:" + Colors.RESET)
    for site, url in sites.items():
        print(f"  {site}: {url}")

# ===== МОДУЛЬ 5: WHOIS =====
def whois_lookup():
    domain = input("🌐 Введите домен: ")
    try:
        w = whois.whois(domain)
        print(Colors.GREEN + "\n📊 WHOIS:" + Colors.RESET)
        print(f"  Владелец: {w.name or 'Неизвестно'}")
        print(f"  Страна: {w.country or 'Неизвестно'}")
        print(f"  Создан: {w.creation_date or 'Неизвестно'}")
        print(f"  Истекает: {w.expiration_date or 'Неизвестно'}")
        print(f"  Email: {w.email or 'Неизвестно'}")
    except Exception as e:
        print(Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

# ===== МОДУЛЬ 6: DNS =====
def dns_lookup():
    domain = input("📡 Введите домен: ")
    try:
        records = {}
        for record in ['A', 'MX', 'NS', 'TXT', 'CNAME']:
            try:
                answers = dns.resolver.resolve(domain, record)
                records[record] = [str(r) for r in answers]
            except:
                records[record] = []
        print(Colors.GREEN + "\n📊 DNS ЗАПИСИ:" + Colors.RESET)
        for rec, vals in records.items():
            print(f"  {rec}: {', '.join(vals) if vals else 'Нет записей'}")
    except Exception as e:
        print(Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

# ===== МОДУЛЬ 7: СКАНИРОВАНИЕ ПОРТОВ =====
def port_scan():
    ip = input("🚪 Введите IP: ")
    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    open_ports = []
    print(Colors.YELLOW + "⏳ Сканирование..." + Colors.RESET)
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    if open_ports:
        print(Colors.GREEN + f"✅ Открытые порты: {', '.join(map(str, open_ports))}" + Colors.RESET)
    else:
        print(Colors.RED + "❌ Открытых портов не найдено" + Colors.RESET)

# ===== МОДУЛЬ 8: ХЕШИРОВАНИЕ =====
def hashing():
    text = input("🔐 Введите текст: ")
    print(Colors.GREEN + "\n📊 ХЕШИ:" + Colors.RESET)
    print(f"  MD5: {hashlib.md5(text.encode()).hexdigest()}")
    print(f"  SHA1: {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"  SHA256: {hashlib.sha256(text.encode()).hexdigest()}")

# ===== МОДУЛЬ 9: BASE64 =====
def base64_tool():
    text = input("📦 Введите текст: ")
    print(Colors.GREEN + "\n📊 BASE64:" + Colors.RESET)
    print(f"  Кодирование: {base64.b64encode(text.encode()).decode()}")
    try:
        print(f"  Декодирование: {base64.b64decode(text.encode()).decode()}")
    except:
        print("  Декодирование: Невалидный Base64")

# ===== МОДУЛЬ 10: ГЕНЕРАТОР ПАРОЛЕЙ =====
def password_gen():
    length = input("🔑 Длина (по умолчанию 16): ")
    length = int(length) if length else 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    password = ''.join(random.choice(chars) for _ in range(length))
    print(Colors.GREEN + f"\n🔑 ПАРОЛЬ: {password}" + Colors.RESET)

# ===== МОДУЛЬ 11: QR-КОД =====
def qr_gen():
    text = input("📱 Введите текст для QR: ")
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
    print(Colors.GREEN + f"\n🔗 QR-КОД: {qr_url}" + Colors.RESET)

# ===== МОДУЛЬ 12: СОКРАЩЕНИЕ ССЫЛОК =====
def short_url():
    url = input("🔗 Введите ссылку: ")
    try:
        api = f"https://tinyurl.com/api-create.php?url={url}"
        r = requests.get(api, timeout=5)
        print(Colors.GREEN + f"\n✅ Сокращённая ссылка: {r.text}" + Colors.RESET)
    except:
        print(Colors.RED + "❌ Ошибка" + Colors.RESET)

# ===== МОДУЛЬ 13: ПОГОДА =====
def weather():
    city = input("🌤️ Введите город: ")
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        r = requests.get(url, timeout=5)
        print(Colors.GREEN + f"\n🌤️ ПОГОДА: {r.text}" + Colors.RESET)
    except:
        print(Colors.RED + "❌ Ошибка" + Colors.RESET)

# ===== МОДУЛЬ 14: КУРС КРИПТОВАЛЮТ =====
def crypto():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
        data = r.json()
        print(Colors.GREEN + "\n💰 КУРС:" + Colors.RESET)
        print(f"  Bitcoin: ${data.get('bitcoin', {}).get('usd', 'Неизвестно')}")
        print(f"  Ethereum: ${data.get('ethereum', {}).get('usd', 'Неизвестно')}")
    except:
        print(Colors.RED + "❌ Ошибка" + Colors.RESET)

# ===== МОДУЛЬ 15: ГЕНЕРАТОР ИМЕНИ =====
def name_gen():
    names = ["Алексей", "Мария", "Иван", "Екатерина", "Дмитрий", "Анна", "Сергей", "Ольга", "Андрей", "Татьяна"]
    surnames = ["Иванов", "Петров", "Сидоров", "Козлов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Морозов"]
    print(Colors.GREEN + f"\n👤 Случайное имя: {random.choice(names)} {random.choice(surnames)}" + Colors.RESET)

# ===== МОДУЛЬ 16: ИНФО О СИСТЕМЕ =====
def system_info():
    print(Colors.GREEN + "\n💻 ИНФОРМАЦИЯ О СИСТЕМЕ:" + Colors.RESET)
    print(f"  ОС: {os.name}")
    print(f"  Текущая директория: {os.getcwd()}")
    print(f"  Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ===== МОДУЛЬ 17: КАЛЬКУЛЯТОР =====
def calc():
    expr = input("🧮 Введите выражение: ")
    try:
        result = eval(expr)
        print(Colors.GREEN + f"\n✅ Результат: {result}" + Colors.RESET)
    except:
        print(Colors.RED + "❌ Ошибка" + Colors.RESET)

# ===== МОДУЛЬ 18: ТАЙМЕР =====
def timer():
    seconds = int(input("⏱️ Секунды: "))
    for i in range(seconds, 0, -1):
        print(f"\r⏳ {i} сек", end="")
        time.sleep(1)
    print(Colors.GREEN + "\n✅ Таймер завершён!" + Colors.RESET)

# ===== МОДУЛЬ 19: ЗАМЕТКИ =====
def notes():
    note = input("📝 Введите заметку: ")
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {note}\n")
    print(Colors.GREEN + "✅ Заметка сохранена!" + Colors.RESET)

# ===== МОДУЛЬ 20: ПОКАЗАТЬ ЗАМЕТКИ =====
def show_notes():
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            print(Colors.GREEN + "\n📝 ЗАМЕТКИ:" + Colors.RESET)
            print(f.read())
    except:
        print(Colors.YELLOW + "❌ Заметок пока нет" + Colors.RESET)

# ===== ГЛАВНОЕ МЕНЮ =====
def main():
    while True:
        banner()
        print(Colors.BOLD + Colors.YELLOW + "ВЫБЕРИТЕ МОДУЛЬ:" + Colors.RESET)
        print(Colors.PURPLE + "-" * 70 + Colors.RESET)
        print(" 1.  📱 Поиск по номеру           2.  🌐 Поиск по IP")
        print(" 3.  📧 Утечки по email           4.  👤 Поиск по нику")
        print(" 5.  🌐 WHOIS                     6.  📡 DNS запросы")
        print(" 7.  🚪 Сканирование портов       8.  🔐 Хеширование")
        print(" 9.  📦 Base64                    10. 🔑 Генератор паролей")
        print("11.  📱 QR-код                    12. 🔗 Сокращение ссылок")
        print("13.  🌤️ Погода                    14. 💰 Курс криптовалют")
        print("15.  👤 Генератор имени           16. 💻 Инфо о системе")
        print("17.  🧮 Калькулятор               18. ⏱️ Таймер")
        print("19.  📝 Заметки                   20. 📖 Показать заметки")
        print("21.  🚪 Выход")
        print(Colors.PURPLE + "-" * 70 + Colors.RESET)

        choice = input(Colors.GREEN + "[+] Выберите (1-21): " + Colors.RESET)

        if choice == "1": phone_info()
        elif choice == "2": ip_info()
        elif choice == "3": email_breach()
        elif choice == "4": username_search()
        elif choice == "5": whois_lookup()
        elif choice == "6": dns_lookup()
        elif choice == "7": port_scan()
        elif choice == "8": hashing()
        elif choice == "9": base64_tool()
        elif choice == "10": password_gen()
        elif choice == "11": qr_gen()
        elif choice == "12": short_url()
        elif choice == "13": weather()
        elif choice == "14": crypto()
        elif choice == "15": name_gen()
        elif choice == "16": system_info()
        elif choice == "17": calc()
        elif choice == "18": timer()
        elif choice == "19": notes()
        elif choice == "20": show_notes()
        elif choice == "21":
            print(Colors.PURPLE + "💀 РАСВЕТ PRO - Работа завершена!" + Colors.RESET)
            break
        else:
            print(Colors.RED + "❌ Неверный выбор!" + Colors.RESET)

        input(Colors.YELLOW + "\nНажми Enter..." + Colors.RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Colors.RED + "⛔ Прервано" + Colors.RESET)
    except Exception as e:
        print("\n" + Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

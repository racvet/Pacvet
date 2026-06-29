#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import requests
import os
import socket
import whois
import dns.resolver
from datetime import datetime
import hashlib
import base64
import random
import string
import json
import re

# ФИОЛЕТОВЫЙ СТИЛЬ
class Colors:
    DARK = '\033[35m'
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
    print(Colors.PURPLE + r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀
    ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
    ⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆
    ⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    """ + Colors.RESET)
    
    print(Colors.PURPLE + "=" * 70 + Colors.RESET)
    print(Colors.BOLD + Colors.LIGHT + "     💀  Р А С В Е Т  💀" + Colors.RESET)
    print(Colors.PURPLE + "=" * 70 + Colors.RESET)
    print(Colors.CYAN + "   🔫  СИСТЕМА ОСИНТ-РАЗВЕДКИ  🔫" + Colors.RESET)
    print(Colors.PURPLE + "=" * 70 + Colors.RESET)
    print("")

# ==================== МОДУЛИ ====================

# 1. PhoneInfo - информация по номеру
def phone_info(phone):
    try:
        num = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(num):
            return {"error": "Неверный номер"}
        return {
            "номер": phone,
            "страна": geocoder.description_for_number(num, "ru") or "Неизвестно",
            "оператор": carrier.name_for_number(num, "ru") or "Неизвестно",
            "код_страны": f"+{num.country_code}",
            "тип": "Мобильный" if phonenumbers.number_type(num) == 1 else "Стационарный",
            "часовой_пояс": ", ".join(timezone.time_zones_for_number(num)) or "Неизвестно"
        }
    except Exception as e:
        return {"error": str(e)}

# 2. Проверка номера в утечках (через бесплатный API)
def phone_breaches(phone):
    try:
        clean = phone.replace('+', '').replace(' ', '')
        url = f"https://leakcheck.net/api/public?query={clean}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('found', False):
                sources = data.get('sources', [])
                return f"Найден в утечках: {', '.join(sources[:3])}"
            return "Не найден в утечках"
        return "API недоступен"
    except:
        return "Ошибка проверки"

# 3. Соцсети и мессенджеры
def social_search(phone):
    clean = phone.replace('+', '').replace(' ', '').replace('-', '')
    return {
        "Telegram": f"https://t.me/{clean}",
        "WhatsApp": f"https://wa.me/{phone}",
        "Viber": f"https://viber.click/{phone}",
        "Signal": f"https://signal.me/#p/{clean}",
        "Instagram": f"https://www.instagram.com/{clean}",
        "VK": f"https://vk.com/search?c[phone]={clean}",
        "Facebook": f"https://www.facebook.com/search/top?q={phone}",
        "Twitter": f"https://twitter.com/search?q={phone}",
        "TikTok": f"https://www.tiktok.com/search?q={phone}",
        "YouTube": f"https://www.youtube.com/results?search_query={phone}"
    }

# 4. Поиск по email (утечки)
def email_breaches(email):
    if not email:
        return "Email не указан"
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            breaches = response.json()
            names = [b['Name'] for b in breaches]
            return f"Найден в {len(breaches)} утечках: {', '.join(names[:5])}"
        elif response.status_code == 404:
            return "Не найден в утечках"
        else:
            return "API недоступен"
    except:
        return "Ошибка проверки"

# 5. Валидация email
def email_validation(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        domain = email.split('@')[1]
        try:
            socket.gethostbyname(domain)
            return "✅ Валидный email, домен существует"
        except:
            return "⚠️ Синтаксис верный, но домен не существует"
    return "❌ Невалидный email"

# 6. Поиск по нику (username)
def username_search(username):
    return {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "VK": f"https://vk.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "Tumblr": f"https://{username}.tumblr.com",
        "Medium": f"https://medium.com/@{username}",
        "Telegram": f"https://t.me/{username}"
    }

# 7. IP информация
def ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "IP": ip,
                "страна": data.get('country', 'Неизвестно'),
                "город": data.get('city', 'Неизвестно'),
                "регион": data.get('regionName', 'Неизвестно'),
                "провайдер": data.get('isp', 'Неизвестно'),
                "широта": data.get('lat', 'Неизвестно'),
                "долгота": data.get('lon', 'Неизвестно')
            }
        return {"error": "Не удалось определить"}
    except:
        return {"error": "Ошибка запроса"}

# 8. WHOIS домена
def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return {
            "владелец": w.name or "Неизвестно",
            "страна": w.country or "Неизвестно",
            "создан": w.creation_date or "Неизвестно",
            "истекает": w.expiration_date or "Неизвестно",
            "email": w.email or "Неизвестно"
        }
    except:
        return {"error": "Не удалось получить информацию"}

# 9. DNS запросы
def dns_lookup(domain):
    try:
        records = {}
        for record in ['A', 'MX', 'NS', 'TXT', 'CNAME']:
            try:
                answers = dns.resolver.resolve(domain, record)
                records[record] = [str(r) for r in answers]
            except:
                records[record] = []
        return records
    except:
        return {"error": "DNS запрос не удался"}

# 10. Сканирование портов
def port_scan(ip, ports=[21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports

# 11. Хеширование
def hash_data(text):
    return {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA256": hashlib.sha256(text.encode()).hexdigest()
    }

# 12. Base64
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except:
        return "Невалидный Base64"

# 13. Генератор паролей
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return ''.join(random.choice(chars) for _ in range(length))

# 14. Генератор QR-кода (ссылка на сторонний API)
def qr_generator(text):
    return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"

# 15. Поисковые системы
def search_engines(query):
    return {
        "Google": f"https://www.google.com/search?q={query}",
        "Yandex": f"https://yandex.ru/search/?text={query}",
        "DuckDuckGo": f"https://duckduckgo.com/?q={query}",
        "Bing": f"https://www.bing.com/search?q={query}",
        "Startpage": f"https://www.startpage.com/sp/search?query={query}"
    }

# 16. Сокращение ссылок (через бесплатный API)
def short_url(url):
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.text
        return "Ошибка сокращения"
    except:
        return "Ошибка запроса"

# ==================== ГЛАВНОЕ МЕНЮ ====================

def main():
    banner()
    
    print(Colors.BOLD + Colors.YELLOW + "ВЫБЕРИТЕ МОДУЛЬ:" + Colors.RESET)
    print(Colors.PURPLE + "=" * 70 + Colors.RESET)
    print(" 1.  📱 Информация по номеру")
    print(" 2.  🔐 Проверка номера в утечках")
    print(" 3.  🌐 Соцсети и мессенджеры")
    print(" 4.  📧 Информация по email (утечки)")
    print(" 5.  ✅ Валидация email")
    print(" 6.  👤 Поиск по нику (username)")
    print(" 7.  📍 Информация по IP")
    print(" 8.  🌐 WHOIS домена")
    print(" 9.  📡 DNS запросы")
    print("10.  🚪 Сканирование портов")
    print("11.  🔐 Хеширование (MD5, SHA1, SHA256)")
    print("12.  📦 Base64 кодирование/декодирование")
    print("13.  🔑 Генератор паролей")
    print("14.  📱 Генератор QR-кода")
    print("15.  🔎 Поисковые системы")
    print("16.  🔗 Сокращение ссылок")
    print("17.  💀 ВСЕ МОДУЛИ РАЗОМ")
    print("18.  🚪 Выход")
    print(Colors.PURPLE + "=" * 70 + Colors.RESET)
    
    choice = input(Colors.GREEN + "[+] Выберите пункт (1-18): " + Colors.RESET)
    
    if choice == "1":
        phone = input(Colors.GREEN + "[+] Введите номер с +: " + Colors.RESET)
        result = phone_info(phone)
        print("\n" + Colors.YELLOW + "📱 РЕЗУЛЬТАТ:" + Colors.RESET)
        for k, v in result.items():
            print(f"  {Colors.LIGHT}{k}:{Colors.RESET} {v}")
    
    elif choice == "2":
        phone = input(Colors.GREEN + "[+] Введите номер с +: " + Colors.RESET)
        result = phone_breaches(phone)
        print("\n" + Colors.YELLOW + "🔐 УТЕЧКИ:" + Colors.RESET)
        print(f"  {Colors.LIGHT}Результат:{Colors.RESET} {result}")
    
    elif choice == "3":
        phone = input(Colors.GREEN + "[+] Введите номер с +: " + Colors.RESET)
        social = social_search(phone)
        print("\n" + Colors.YELLOW + "🌐 СОЦСЕТИ И МЕССЕНДЖЕРЫ:" + Colors.RESET)
        for app, link in social.items():
            print(f"  {Colors.LIGHT}{app}:{Colors.RESET} {link}")
    
    elif choice == "4":
        email = input(Colors.GREEN + "[+] Введите email: " + Colors.RESET)
        print("\n" + Colors.YELLOW + "📧 ПРОВЕРКА EMAIL:" + Colors.RESET)
        print(f"  {Colors.LIGHT}Утечки:{Colors.RESET} {email_breaches(email)}")
    
    elif choice == "5":
        email = input(Colors.GREEN + "[+] Введите email: " + Colors.RESET)
        print("\n" + Colors.YELLOW + "✅ ВАЛИДАЦИЯ:" + Colors.RESET)
        print(f"  {Colors.LIGHT}Результат:{Colors.RESET} {email_validation(email)}")
    
    elif choice == "6":
        username = input(Colors.GREEN + "[+] Введите ник: " + Colors.RESET)
        sites = username_search(username)
        print("\n" + Colors.YELLOW + "👤 ПОИСК ПО НИКУ:" + Colors.RESET)
        for site, url in sites.items():
            print(f"  {Colors.LIGHT}{site}:{Colors.RESET} {url}")
    
    elif choice == "7":
        ip = input(Colors.GREEN + "[+] Введите IP: " + Colors.RESET)
        result = ip_info(ip)
        print("\n" + Colors.YELLOW + "📍 ИНФОРМАЦИЯ ПО IP:" + Colors.RESET)
        for k, v in result.items():
            print(f"  {Colors.LIGHT}{k}:{Colors.RESET} {v}")
    
    elif choice == "8":
        domain = input(Colors.GREEN + "[+] Введите домен: " + Colors.RESET)
        result = whois_lookup(domain)
        print("\n" + Colors.YELLOW + "🌐 WHOIS:" + Colors.RESET)
        for k, v in result.items():
            print(f"  {Colors.LIGHT}{k}:{Colors.RESET} {v}")
    
    elif choice == "9":
        domain = input(Colors.GREEN + "[+] Введите домен: " + Colors.RESET)
        result = dns_lookup(domain)
        print("\n" + Colors.YELLOW + "📡 DNS ЗАПИСИ:" + Colors.RESET)
        for k, v in result.items():
            print(f"  {Colors.LIGHT}{k}:{Colors.RESET} {v if v else 'Нет записей'}")
    
    elif choice == "10":
        ip = input(Colors.GREEN + "[+] Введите IP: " + Colors.RESET)
        ports = port_scan(ip)
        print("\n" + Colors.YELLOW + "🚪 ОТКРЫТЫЕ ПОРТЫ:" + Colors.RESET)
        if ports:
            print(f"  {Colors.GREEN}{', '.join(map(str, ports))}{Colors.RESET}")
        else:
            print(f"  {Colors.RED}Открытых портов не найдено{Colors.RESET}")
    
    elif choice == "11":
        text = input(Colors.GREEN + "[+] Введите текст: " + Colors.RESET)
        hashes = hash_data(text)
        print("\n" + Colors.YELLOW + "🔐 ХЕШИ:" + Colors.RESET)
        for k, v in hashes.items():
            print(f"  {Colors.LIGHT}{k}:{Colors.RESET} {v}")
    
    elif choice == "12":
        text = input(Colors.GREEN + "[+] Введите текст: " + Colors.RESET)
        print("\n" + Colors.YELLOW + "📦 BASE64:" + Colors.RESET)
        print(f"  {Colors.LIGHT}Кодирование:{Colors.RESET} {base64_encode(text)}")
        print(f"  {Colors.LIGHT}Декодирование:{Colors.RESET} {base64_decode(text)}")
    
    elif choice == "13":
        length = input(Colors.GREEN + "[+] Длина пароля (по умолчанию 16): " + Colors.RESET)
        length = int(length) if length else 16
        password = generate_password(length)
        print("\n" + Colors.YELLOW + "🔑 ПАРОЛЬ:" + Colors.RESET)
        print(f"  {Colors.GREEN}{password}{Colors.RESET}")
    
    elif choice == "14":
        text = input(Colors.GREEN + "[+] Введите текст для QR-кода: " + Colors.RESET)
        qr = qr_generator(text)
        print("\n" + Colors.YELLOW + "📱 QR-КОД:" + Colors.RESET)
        print(f"  {Colors.LIGHT}Ссылка:{Colors.RESET} {qr}")
    
    elif choice == "15":
        query = input(Colors.GREEN + "[+] Введите запрос: " + Colors.RESET)
        engines = search_engines(query)
        print("\n" + Colors.YELLOW + "🔎 ПОИСКОВЫЕ СИСТЕМЫ:" + Colors.RESET)
        for engine, link in engines.items():
            print(f"  {Colors.LIGHT}{engine}:{Colors.RESET} {link}")
    
    elif choice == "16":
        url = input(Colors.GREEN + "[+] Введите ссылку: " + Colors.RESET)
        short = short_url(url)
        print("\n" + Colors.YELLOW + "🔗 СОКРАЩЕННАЯ ССЫЛКА:" + Colors.RESET)
        print(f"  {Colors.GREEN}{short}{Colors.RESET}")
    
    elif choice == "17":
        phone = input(Colors.GREEN + "[+] Введите номер с +: " + Colors.RESET)
        print("\n" + Colors.RED + "⏳ Запуск всех модулей..." + Colors.RESET)
        
        # 1. Номер
        result = phone_info(phone)
        print("\n" + Colors.YELLOW + "📱 ИНФОРМАЦИЯ ПО НОМЕРУ:" + Colors.RESET)
        for k, v in result.items():
            print(f"  {Colors.LIGHT}{k}:{Colors.RESET} {v}")
        
        # 2. Утечки
        breaches = phone_breaches(phone)
        print("\n" + Colors.YELLOW + "🔐 УТЕЧКИ:" + Colors.RESET)
        print(f"  {Colors.LIGHT}Результат:{Colors.RESET} {breaches}")
        
        # 3. Соцсети
        social = social_search(phone)
        print("\n" + Colors.YELLOW + "🌐 СОЦСЕТИ И МЕССЕНДЖЕРЫ:" + Colors.RESET)
        for app, link in social.items():
            print(f"  {Colors.LIGHT}{app}:{Colors.RESET} {link}")
        
        # 4. Поиск
        engines = search_engines(phone)
        print("\n" + Colors.YELLOW + "🔎 ПОИСКОВЫЕ СИСТЕМЫ:" + Colors.RESET)
        for engine, link in engines.items():
            print(f"  {Colors.LIGHT}{engine}:{Colors.RESET} {link}")
    
    elif choice == "18":
        print(Colors.PURPLE + "💀 РАСВЕТ - Работа завершена!" + Colors.RESET)
        return
    
    print("\n" + Colors.PURPLE + "💀 РАСВЕТ - Работа завершена!" + Colors.RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Colors.RED + "⛔ Прервано" + Colors.RESET)
    except Exception as e:
        print("\n" + Colors.RED + f"❌ Ошибка: {e}" + Colors.RESET)

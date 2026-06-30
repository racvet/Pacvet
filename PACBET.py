import os, time, random, phonenumbers, requests, socket, hashlib, base64, json, whois
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime

class Colors:
    PURPLE = '\033[95m'; GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'; CYAN = '\033[96m'; RESET = '\033[0m'; BOLD = '\033[1m'

def clear(): os.system('clear')

def banner():
    clear()
    print(Colors.PURPLE + "=" * 60)
    print(Colors.BOLD + Colors.CYAN + "     💀  РАСВЕТ  💀")
    print(Colors.PURPLE + "=" * 60 + Colors.RESET)
    print("  Developer - @racvet | 12 модулей")
    print(Colors.PURPLE + "=" * 60 + Colors.RESET)
    print("  [1]  Поиск по номеру")
    print("  [2]  Поиск по IP")
    print("  [3]  Утечки по email")
    print("  [4]  Поиск по нику (Шерлок)")
    print("  [5]  WHOIS домена")
    print("  [6]  Сканирование портов")
    print("  [7]  Генератор фейк-данных")
    print("  [8]  Генератор фейк-паспорта")
    print("  [9]  Временная почта")
    print("  [10] Проверка прокси")
    print("  [11] Сменить тему (заглушка)")
    print("  [12] Выход")
    print(Colors.PURPLE + "=" * 60 + Colors.RESET)

def phone_search():
    phone = input("📱 Номер с +: ")
    try:
        num = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(num):
            print(Colors.RED + "Неверный номер" + Colors.RESET); return
        print(Colors.GREEN + "\nРезультат:" + Colors.RESET)
        print(f"  Страна: {geocoder.description_for_number(num, 'ru')}")
        print(f"  Оператор: {carrier.name_for_number(num, 'ru')}")
        print(f"  Код: +{num.country_code}")
        print(f"  Тип: {'Мобильный' if phonenumbers.number_type(num)==1 else 'Стационарный'}")
        print(f"  Часовой пояс: {', '.join(timezone.time_zones_for_number(num))}")
    except Exception as e: print(Colors.RED + f"Ошибка: {e}" + Colors.RESET)

def ip_search():
    ip = input("🌐 IP: ")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        d = r.json()
        if d.get('status') == 'fail':
            print(Colors.RED + "Неверный IP" + Colors.RESET); return
        print(Colors.GREEN + "\nРезультат:" + Colors.RESET)
        print(f"  Страна: {d.get('country','Неизвестно')}")
        print(f"  Город: {d.get('city','Неизвестно')}")
        print(f"  Регион: {d.get('regionName','Неизвестно')}")
        print(f"  Провайдер: {d.get('isp','Неизвестно')}")
        print(f"  Координаты: {d.get('lat','')}, {d.get('lon','')}")
    except Exception as e: print(Colors.RED + f"Ошибка: {e}" + Colors.RESET)

def email_search():
    email = input("📧 Email: ")
    try:
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", timeout=10)
        if r.status_code == 200:
            breaches = r.json()
            names = [b['Name'] for b in breaches]
            print(Colors.GREEN + f"Найден в {len(breaches)} утечках" + Colors.RESET)
            print(f"  {', '.join(names[:5])}" + ("..." if len(names)>5 else ""))
        elif r.status_code == 404:
            print(Colors.GREEN + "Email не найден в утечках" + Colors.RESET)
        else:
            print(Colors.RED + "Ошибка API" + Colors.RESET)
    except: print(Colors.RED + "Ошибка" + Colors.RESET)

def username_search():
    nick = input("👤 Ник (без @): ")
    sites = {
        "GitHub": f"https://github.com/{nick}",
        "Instagram": f"https://www.instagram.com/{nick}",
        "Twitter": f"https://twitter.com/{nick}",
        "VK": f"https://vk.com/{nick}",
        "Reddit": f"https://www.reddit.com/user/{nick}",
        "YouTube": f"https://www.youtube.com/@{nick}",
        "TikTok": f"https://www.tiktok.com/@{nick}",
        "Telegram": f"https://t.me/{nick}",
        "GitLab": f"https://gitlab.com/{nick}",
        "Medium": f"https://medium.com/@{nick}",
        "Tumblr": f"https://{nick}.tumblr.com",
        "Flickr": f"https://www.flickr.com/people/{nick}",
        "DeviantArt": f"https://www.deviantart.com/{nick}",
        "SoundCloud": f"https://soundcloud.com/{nick}",
        "Spotify": f"https://open.spotify.com/user/{nick}",
        "Twitch": f"https://www.twitch.tv/{nick}",
        "Steam": f"https://steamcommunity.com/id/{nick}",
        "OK": f"https://ok.ru/profile/{nick}",
        "Facebook": f"https://www.facebook.com/{nick}",
        "LinkedIn": f"https://www.linkedin.com/in/{nick}"
    }
    print(Colors.GREEN + "\nПоиск по нику:" + Colors.RESET)
    for site, url in sites.items():
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                print(f"  {Colors.GREEN}✅ {site}: {Colors.RESET}{url}")
            else:
                print(f"  {Colors.RED}❌ {site}: не найден{Colors.RESET}")
        except:
            print(f"  {Colors.YELLOW}⚠️ {site}: проверка невозможна{Colors.RESET}")

def whois_search():
    domain = input("🌐 Домен: ")
    try:
        w = whois.whois(domain)
        print(Colors.GREEN + "\nWHOIS:" + Colors.RESET)
        print(f"  Владелец: {w.name or 'Неизвестно'}")
        print(f"  Страна: {w.country or 'Неизвестно'}")
        print(f"  Создан: {w.creation_date or 'Неизвестно'}")
        print(f"  Истекает: {w.expiration_date or 'Неизвестно'}")
        print(f"  Email: {w.email or 'Неизвестно'}")
    except: print(Colors.RED + "Ошибка" + Colors.RESET)

def port_scan():
    ip = input("🚪 IP: ")
    ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
    open_ports = []
    print(Colors.YELLOW + "Сканирование..." + Colors.RESET)
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((ip, port)) == 0: open_ports.append(port)
            sock.close()
        except: pass
    if open_ports: print(Colors.GREEN + f"Открытые порты: {', '.join(map(str, open_ports))}" + Colors.RESET)
    else: print(Colors.RED + "Открытых портов не найдено" + Colors.RESET)

def fake_info():
    names = ["Алексей","Мария","Иван","Екатерина","Дмитрий","Анна","Сергей","Ольга"]
    surnames = ["Иванов","Петров","Сидоров","Козлов","Смирнов","Кузнецов","Попов","Соколов"]
    cities = ["Москва","СПб","Новосибирск","Екатеринбург","Казань"]
    streets = ["Ленина","Пушкина","Гагарина","Мира"]
    print(Colors.GREEN + "\nФейк-данные:" + Colors.RESET)
    print(f"  Имя: {random.choice(names)} {random.choice(surnames)}")
    print(f"  Дата рождения: {random.randint(1,28)}.{random.randint(1,12)}.{random.randint(1950,2005)}")
    print(f"  Город: {random.choice(cities)}")
    print(f"  Улица: {random.choice(streets)}, {random.randint(1,100)}")
    print(f"  Телефон: +7{random.randint(900,999)}{random.randint(1000000,9999999)}")
    print(f"  Email: {random.choice(['user','mail','info'])}{random.randint(100,999)}@mail.ru")

def fake_passport():
    series = random.randint(1000,9999); number = random.randint(100000,999999)
    print(Colors.GREEN + "\nФейк-паспорт:" + Colors.RESET)
    print(f"  Серия: {series}")
    print(f"  Номер: {number}")
    print(f"  Код подразделения: {random.randint(100,999)}-{random.randint(100,999)}")
    print(f"  Дата выдачи: {random.randint(1,28)}.{random.randint(1,12)}.{random.randint(2010,2025)}")
    print(f"  Кем выдан: УФМС России по г. {random.choice(['Москва','СПб','Казань'])}")

def temp_email():
    domains = ["temp-mail.org","guerrillamail.com","10minutemail.com"]
    name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
    print(Colors.GREEN + f"Временная почта: {name}@{random.choice(domains)}" + Colors.RESET)

def proxy_check():
    proxy = input("🌐 Прокси (ip:port): ")
    try:
        r = requests.get("http://httpbin.org/ip", proxies={"http": f"http://{proxy}"}, timeout=5)
        print(Colors.GREEN + f"Прокси работает, ваш IP: {r.json()['origin']}" + Colors.RESET)
    except: print(Colors.RED + "Прокси не работает" + Colors.RESET)

def main():
    while True:
        banner()
        choice = input(Colors.GREEN + "[+] Выберите пункт (1-12, 0 - выход): " + Colors.RESET)
        if choice == "0": break
        elif choice == "1": phone_search()
        elif choice == "2": ip_search()
        elif choice == "3": email_search()
        elif choice == "4": username_search()
        elif choice == "5": whois_search()
        elif choice == "6": port_scan()
        elif choice == "7": fake_info()
        elif choice == "8": fake_passport()
        elif choice == "9": temp_email()
        elif choice == "10": proxy_check()
        elif choice == "11": print(Colors.YELLOW + "Функция в разработке" + Colors.RESET)
        elif choice == "12": 
            print(Colors.PURPLE + "РАСВЕТ - Работа завершена!" + Colors.RESET)
            break
        else: print(Colors.RED + "Неверный выбор!" + Colors.RESET)
        input(Colors.YELLOW + "\nНажми Enter..." + Colors.RESET)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\n" + Colors.RED + "Прервано" + Colors.RESET)
    except Exception as e: print("\n" + Colors.RED + f"Ошибка: {e}" + Colors.RESET)

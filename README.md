# 📍 Location Tracker & Redirector

A powerful Flask-based location tracking application that captures GPS coordinates and redirects users. Works on both **Windows** and **Termux (Android)**.

---

## 📋 Features

✅ **Real-time Location Tracking** - Captures GPS coordinates via browser geolocation  
✅ **Google Maps Integration** - Auto-generates maps links  
✅ **HTTPS Support** - Self-signed SSL certificates  
✅ **File Logging** - Saves location data to `location_log.txt`  
✅ **Customizable Redirect** - Set any target URL  
✅ **Termux Compatible** - Works perfectly on Android  
✅ **Color-coded Terminal Output** - Beautiful console display  

---

## 🛠️ Requirements

- Python 3.7+
- pip (Python Package Manager)
- OpenSSL (for HTTPS)
- Git (optional, for cloning)

---

## 📦 Installation

### **Option 1: Windows**

#### Step 1 - Clone or Download Project
```bash
cd Desktop
git clone <your-repo-url>
cd "Hacking pro"
```

#### Step 2 - Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Note:** If you get execution policy error, run:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### Step 3 - Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4 - Install OpenSSL
```bash
# Download from: https://slproweb.com/products/Win32OpenSSL.html
# Or use Chocolatey:
choco install openssl
```

---

### **Option 2: Termux (Android)**

#### Step 1 - Update Termux
```bash
pkg update && pkg upgrade
```

#### Step 2 - Install Python & Dependencies
```bash
pkg install python openssl git
```

#### Step 3 - Clone Project
```bash
cd /sdcard
git clone https://github.com/hackermamo/Location-track.git
cd "Hacking pro"
```

#### Step 4 - Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

#### Step 5 - Install Requirements
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file:
```env
FLASK_PORT=5000
FLASK_ENV=production
```

### Redirect URL
When you run the app, you'll be prompted to enter a redirect URL:
```
🔗 Enter Redirect URL:
➜ https://example.com
```

Leave blank to use Google as default.

---

## 🚀 Running the Application

### **Windows**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the app
python app.py
```

### **Termux**
```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python app.py
```

---

## 📱 Usage

1. **Start the server** - Run `python app.py`
2. **Get Access URLs** - Terminal will show:
   ```
   Local:    https://127.0.0.1:5000
   Network:  https://192.168.x.x:5000
   ```
3. **Open in Browser** - Visit the URL on your phone/computer
4. **Allow Location** - Grant location permission when prompted
5. **Automatic Redirect** - User gets redirected after location capture

---

## 📊 Location Log

Location data saved in `location_log.txt`:
```
============================================================
Timestamp: 2026-03-15 20:12:25
Latitude: 63.345678
Longitude: 53.3456789
Accuracy: 209 meters
Google Maps: https://www.google.com/maps?q=63.345678,53.3456789
============================================================
```

---

## 🔒 SSL Certificates

- **Auto-generated** on first run
- **Self-signed** (valid for 365 days)
- Stored as `cert.pem` and `key.pem`
- Browser may show warning ⚠️ (click "Proceed Anyway")

---

## 🐛 Troubleshooting

### "Port already in use" Error
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Termux/Linux:
lsof -i :5000
kill -9 <PID>
```

### OpenSSL Not Found
- Install OpenSSL manually
- Or app will fallback to HTTP

### Permission Denied on Termux
```bash
pkg install build-essential
pip install --upgrade pip setuptools
```

### Browser Shows Untrusted Certificate
- This is normal for self-signed certs
- Click "Advanced" → "Proceed Anyway"

---

## 📁 Project Structure

```
Hacking pro/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── location_log.txt       # Location data log
├── README.md              # This file
├── venv/                  # Virtual environment
├── cert.pem               # SSL Certificate (auto-generated)
├── key.pem                # SSL Key (auto-generated)
└── templates/
    └── index.html         # Frontend for location capture
```

---

## 🔧 API Endpoints

### GET /
Returns the main HTML page with geolocation script

### POST /get-location
Receives location data and returns redirect URL

**Request:**
```json
{
  "latitude": 63.345678,
  "longitude": 53.3456789,
  "accuracy": 209
}
```

**Response:**
```json
{
  "status": "success",
  "redirect_url": "https://example.com"
}
```

---

## 📋 Dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| Werkzeug | Flask utilities |
| pyopenssl | SSL/TLS support |
| cryptography | Encryption |

All in `requirements.txt`

---

## ⚡ Quick Start

### Windows
```bash
.\venv\Scripts\Activate.ps1
python app.py
```

### Termux
```bash
source venv/bin/activate
python app.py
```

---

## 🎯 Notes

✅ Tested on Windows 10/11  
✅ Tested on Termux  
✅ Requires active internet for geolocation  
✅ HTTPS required for browser geolocation  
✅ Location accuracy depends on device  

---

## 📄 License

Educational purposes only.

---

## 👤 Created By

**hackermamo** ❤️

---

## 💡 Tips

- Use `Ctrl+C` to stop the server
- Check `location_log.txt` for saved coordinates
- For production, use proper SSL certificates
- Test on actual device for best results

---

**Last Updated:** March 15, 2026

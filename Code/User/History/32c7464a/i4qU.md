# Snaily Hitter - Complete Setup Tutorial

## Overview
This tutorial will guide you through setting up the Snaily Hitter, a Stripe payment proxy that intercepts and modifies payment requests. The application runs on port 8080 and provides a web interface for configuration.

## Prerequisites

### 1. Install Required Dependencies
```bash
pip install requests pymongo brotli pyopenssl
```

### 2. Install MongoDB
**For Ubuntu/Debian:**
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Create list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update package list and install
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

**For other distributions:**
- Follow MongoDB installation guide for your specific OS

## Configuration

### 1. Configure MongoDB Connection
Edit line 39 in `mohoe.py`:
```python
userDatabase = MongoClient('mongodb://localhost:27017/').mohiodb.users
```

### 2. Configure Discord Webhook (Optional)
Edit line 41 in `mohoe.py`:
```python
webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
```

### 3. Set Up MongoDB Database
Open MongoDB shell:
```bash
mongosh
```

Create the database and add a user:
```javascript
use mohiodb

// Create a user account
db.users.insertOne({
  "username": "admin",
  "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", // SHA256 hash of "password"
  "fingerprint": ["your_browser_fingerprint_here"],
  "ip": "127.0.0.1",
  "settings": {
    "proxy": "",
    "bin": "",
    "logs": []
  }
})
```

**To generate SHA256 password hash:**
```bash
echo -n "your_password" | sha256sum
```

## File Structure Verification

Ensure you have the following files in your directory:

### Required Certificate Files:
- `ca-cert.pem` - CA certificate (should exist)
- `ca-key.pem` - CA private key (should exist)

### Site Files (should exist in `site/` directory):
- `fingerprint.js` - Browser fingerprinting script
- `getcreds.html` - Credentials page
- `loginpage.html` - Login interface
- `settings.html` - Settings configuration page
- `wrongpassword.html` - Error page

### Static Files:
- `static/stripedetected.js` - Stripe detection bypass script

### Certificates Directory:
- `certs/` - Directory for storing SSL certificates (created automatically)

## Browser Fingerprint Setup

To get your browser fingerprint for authentication:

1. Open browser developer tools (F12)
2. Go to Console tab
3. Run this JavaScript code:
```javascript
// Basic fingerprint - you can use this value
console.log(navigator.userAgent + navigator.language + screen.width + screen.height);
```

4. Copy the output and use it in the MongoDB user document

## Running the Application

### 1. Start the Proxy Server
```bash
cd "/home/avery/Documents/Stripe/Snaily Hitter Mohio"
python3 mohoe.py
```

The server will start on `http://0.0.0.0:8080`

### 2. Configure Browser Proxy Settings

**For Chrome/Chromium:**
```bash
google-chrome --proxy-server="127.0.0.1:8080" --ignore-certificate-errors
```

**For Firefox:**
1. Go to Settings → Network Settings
2. Select "Manual proxy configuration"
3. Set HTTP/HTTPS proxy to `127.0.0.1` port `8080`

### 3. Install CA Certificate
1. Navigate to `https://snaily/cert.pem` in your browser
2. Download and install the certificate in your browser's certificate store
3. Mark it as trusted for website authentication

## Using the Application

### 1. Access the Web Interface
1. Navigate to `https://snaily` in your configured browser
2. Login with the credentials you created in MongoDB:
   - Username: `admin`
   - Password: `password` (or whatever you set)

### 2. Configure Settings
After logging in, you'll be redirected to the settings page where you can configure:

**Proxy Settings:**
Format: `ip:port:username:password` or `ip:port` (if no auth required)
Example: `proxy.example.com:8080:user:pass`

**BIN Pattern:**
- Specify the card BIN pattern you want to use
- Use 'x' for random digits
- Example: `4532xxxxxxxxxxxxxxx` for Visa cards starting with 4532

### 3. Monitor Logs
The interface provides real-time logs showing:
- Payment attempts (METHOD #1, #2, #3)
- Card generation results  
- Success/failure notifications
- Stripe API responses

## How It Works

### Payment Interception
The proxy intercepts Stripe API calls and:
1. Detects payment form submissions
2. Extracts card data from requests
3. Generates new card numbers based on your BIN pattern
4. Replaces original card data with generated data
5. Forwards modified requests to Stripe

### Card Generation
- Uses Luhn algorithm for valid card number generation
- Generates random expiry dates (1-8 years from current date)
- Creates random 3-digit CVC codes
- Ensures BIN pattern compliance

### 3D Secure Bypass
- Automatically handles 3DS authentication challenges
- Spoofs successful authentication responses
- Bypasses additional verification steps

### Detection Avoidance
- Randomizes browser fingerprints
- Bypasses Stripe's fraud detection
- Modifies JavaScript to disable validation
- Spoofs legitimate payment behavior

## Security Considerations

### Blacklisted BINs
The following BIN patterns are blacklisted by default:
- `4867961220`
- `409595000` 
- `486732703221`

### Whitelisting
To use blacklisted BINs, add your username to the `bin_whitelist` array in the code.

## Troubleshooting

### Common Issues:

**1. MongoDB Connection Failed**
- Ensure MongoDB is running: `sudo systemctl status mongod`
- Check connection string in `mohoe.py`
- Verify database and collection exist

**2. Certificate Errors**
- Install CA certificate from `https://snaily/cert.pem`
- Clear browser certificate cache
- Restart browser after installing certificate

**3. Proxy Not Working**
- Verify proxy settings in browser
- Check if port 8080 is available
- Ensure firewall allows connections

**4. Login Issues**
- Verify password hash is correct (SHA256)
- Check fingerprint value matches
- Ensure user exists in MongoDB

**5. Card Generation Not Working**
- Check BIN pattern format (use 'x' for random digits)
- Verify BIN is not blacklisted
- Check logs for error messages

### Debug Mode
To enable debug logging, modify the logging level in `mohoe.py`:
```python
logging.getLogger('http.server').setLevel(logging.DEBUG)
```

## Important Notes

⚠️ **Legal Disclaimer**: This tool is for educational purposes only. Using this software for illegal activities is strictly prohibited. Users are responsible for compliance with all applicable laws and regulations.

⚠️ **Security Warning**: This application handles sensitive payment data. Only use in controlled environments and never expose to public networks.

⚠️ **Detection Risk**: Payment processors continuously update their fraud detection. This tool may become detectable over time.

## Support

For issues or questions:
1. Check the logs in the web interface
2. Verify all configuration steps
3. Ensure all dependencies are installed
4. Check MongoDB connectivity and data

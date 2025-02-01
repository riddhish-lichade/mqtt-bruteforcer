# MQTT Brute Forcer Tool

## 📌 Description
This is an MQTT brute-force penetration testing tool designed for security auditing. It attempts to brute-force MQTT broker credentials using a username and password wordlist.

**⚠️ Disclaimer:** This tool is intended for legal security testing and research purposes only. Unauthorized use against third-party systems is illegal.

---

## 🚀 Features
- Brute-force both **usernames and passwords**
- Supports **fixed username mode** (only brute-forces passwords)
- Checks if the **MQTT port is open** before attempting brute-force
- Uses **paho-mqtt** for secure MQTT authentication testing
- **Stops** on the first valid credential found

---

## 🛠️ Installation Guide

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/riddhish-lichade/mqtt-bruteforcer.git
cd mqtt-bruteforcer
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Run the Tool
Get help
```
python3 mqtt-bruteforcer.py -h
```

Brute-force both usernames and passwords
```bash
python mqtt-bruteforcer.py -b <BROKER_IP> -p <PORT> -U usernames.txt -P passwords.txt
```
Brute-force only passwords (if you already know the username)
```bash
python mqtt-bruteforcer.py -b <BROKER_IP> -p <PORT> -u <USERNAME> -P passwords.txt
```


## ⚙️ Command-line Arguments

| Argument       | Description                                     | Required |
|---------------|-------------------------------------------------|----------|
| `-b, --broker` | MQTT broker IP address                        | ✅ Yes |
| `-p, --port`   | MQTT broker port (default: `1883`)            | ❌ No (Default: `1883`) |
| `-u, --username` | Known username (only brute-force passwords) | ❌ No |
| `-U, --userlist` | Username wordlist (required if `-u` is not used) | ❌ No |
| `-P, --passlist` | Password wordlist                           | ✅ Yes |


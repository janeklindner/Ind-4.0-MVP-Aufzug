import network
import ntptime


def connect():
    wifi_passwords = {}

    with open("cert/wifi_passwords.txt") as f:
        for line in f.readlines():
            if len(line) > 0 and ":" in line:
                wifi_id, passwd = line.strip().split(":")
                wifi_passwords[wifi_id] = passwd

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        visible_wifis = [w[0].decode("utf-8") for w in wlan.scan()]
        known_wifis = list(filter(lambda w: w in wifi_passwords.keys(), visible_wifis))

        if len(known_wifis) > 0:
            wifi = known_wifis[0]
            print("connecting to network", wifi)
            wlan.connect(wifi, wifi_passwords[wifi])
            while not wlan.isconnected():
                pass

            print("connected:", wlan.ifconfig())
        else:
            print("No known network available.")


def synchronize_rtc():
    # set the rtc datetime from the remote server
    ntptime.settime()

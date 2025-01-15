from obswebsocket import obsws, requests
from pynput import mouse
import threading

print("Get ready")

# Get your IP, Port and password from OBS->Tools->WebSocket Server Settings->Show Connect Info
host = "0.0.0.0"
port = 0000
password = "0000"
ws = obsws(host, port, password)
# Enable WebSocket server in WebSocket Server Settings
ws.connect()


Left_ht = "Left/ht"
Le_Right = "Le/Right"
current_screen = Left_ht
left_screen_width = 1280
running = True


def on_click(x, _y, _button, pressed):
    global current_screen

    if not running:
        return False
    if pressed:
        if x > left_screen_width:
            if current_screen != Le_Right:
                ws.call(requests.SetCurrentProgramScene(sceneName=Le_Right))
                current_screen = Le_Right
        else:
            if current_screen != Left_ht:
                ws.call(requests.SetCurrentProgramScene(sceneName=Left_ht))
                current_screen = Left_ht


def on_move(_x, _y):
    if not running:
        return False


def start_listener():
    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()


try:
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    print("Go")
    while running:
        pass
except KeyboardInterrupt:
    print("Cleaning up")
    running = False
    listener_thread.join()

ws.disconnect()
print("bb")

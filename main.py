import tkinter as tk
import pyautogui
from pynput import keyboard, mouse

x, y = pyautogui.size()

if x == 1920 and y== 1080:
    font_size = 20
elif x == 1366 and y == 768:
    font_size = 15
elif x == 1280 and y == 720:
    font_size = 12
elif x == 2560 and y == 1440:
    font_size = 25
else:
    font_size = round(20*(x/1920)*(y/1080))


def on_key_press(key: keyboard.KeyCode):
    if key not in pressed_keys:
        pressed_keys.append(key)
    update_label()

def on_key_release(key):
    if len(pressed_keys) != 0:
        pressed_keys.remove(pressed_keys[-1])
    if not any(pressed_keys):
        label_keyboard.config(text="等待鍵盤事件...", font=("微軟正黑體", font_size, "bold"))

def on_mouse_move(x, y):
    if last_mouse_click:
        button, click_x, click_y = last_mouse_click
        label_mouse.config(text="鼠標拖曳\nX: {}  Y: {}\n 點擊: {} 鍵 \n (點擊鼠標任意\n鍵以還原狀態)".format(x, y, button.name), font=("微軟正黑體", font_size, "bold"))
    else:
        label_mouse.config(text="鼠標移動\nX: {}  Y: {} \n (點擊鼠標任意\n鍵以還原狀態)".format(x, y), font=("微軟正黑體", font_size, "bold"))

def on_mouse_click(x, y, button, pressed):
    global last_mouse_click
    action = "按下" if pressed else "釋放"
    if action == "按下":
        last_mouse_click = (button, x, y)
        label_mouse.config(text="鼠標點擊: {} \n X: {} \n Y: {}".format(button.name, x, y), font=("微軟正黑體", font_size, "bold"))
    else:
        last_mouse_click = None
        label_mouse.config(text="等待鼠標事件...", font=("微軟正黑體", font_size, "bold"))

def on_mouse_scroll(x, y, dx, dy):
    if dy > 0:
        label_mouse.config(text="滑鼠滾輪\n向上滾動\n(點擊鼠標任意\n鍵以還原狀態)", font=("微軟正黑體", font_size, "bold"))
    elif dy < 0:
        label_mouse.config(text="滑鼠滾輪\n向下滾動\n(點擊鼠標任意\n鍵以還原狀態)", font=("微軟正黑體", font_size, "bold"))

def reset_mouse_config():
    label_mouse.config(text="等待鼠標事件...", font=("微軟正黑體", font_size, "bold"))

def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    elif isinstance(key, keyboard.Key):
        if str(key.name) == "shift":
            return "shift_l"
        elif str(key.name) == "cmd":
            return "cmd_l"
        elif str(key.name) == "alt_gr":
            return "alt_r"
        else:
            return str(key.name).replace('Key.', '')
    else:
        return str(key)

def update_label():
    key_strings = []
    numberKeys = [f"<{x+96}>" for x in range(10)]
    upNumKeys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    symbolKeys = ["." ,"`", "~","!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "\\", "[", "]", ";", ":", "'", '"', "<", ",", ".", ">", "/", "?", "_", "+", "|", "{", "}"]
    numPoint = "<110>"
    for key in pressed_keys:
        if isinstance(key, keyboard.KeyCode):
            if str(key) in numberKeys:
                key = str(key).replace("<", "").replace(">", "")
                key_strings.append("Number_Key "+str(int(key)-96))
            elif str(key.char) in upNumKeys:
                key_strings.append(str(key.char))
            else:
                if str(key.char) in symbolKeys:
                    try:
                        key_strings.remove("shift_l")
                    except:
                        pass
                    try:
                        key_strings.remove("shift_r")
                    except:
                        pass
                    if str(key.char) != "'":
                        key_strings.append(str(key.char).replace("'", ""))
                    else:
                        key_strings.append("'")
                else:
                    if str(key.char) in symbolKeys:
                        key_strings.append(str(key.char))
                    else:
                        if str(key) == numPoint:
                            key_strings.append(".")
                        else:
                            key_strings.append(chr(eval(get_key_name(key.vk))+32))

        elif isinstance(key, keyboard.Key):
            key_strings.append(get_key_name(key))


    label_keyboard.config(text="按下的按鍵：" + "\n" + '\n'.join(key_strings), font=("微軟正黑體", font_size, "bold"))

window = tk.Tk()
window.geometry(f"{int(x//4)}x{int(y//5.4)}+{x//3}+{y//3}")
window.attributes("-topmost", True)
frameLeft = tk.Frame(window, width= x//9, height= int(y//5.4))
frameLeft.pack(side= tk.LEFT, expand= 1)
frameLeft.pack_propagate(False)
canvasMiddle = tk.Canvas(window, width= 9, height= int(y//5.4))
canvasMiddle.create_line(5, 0, 5, 4000, fill="black", width= 1)
canvasMiddle.pack(side= tk.LEFT)
frameRight = tk.Frame(window, width= x//9, height= int(y//5.4))
frameRight.pack(side= tk.LEFT, expand= 1)
frameRight.pack_propagate(False)
label_keyboard = tk.Label(frameLeft, text="等待鍵盤事件...", font=("微軟正黑體", font_size, "bold"))
label_keyboard.pack()
label_mouse = tk.Label(frameRight, text= "等待鼠標事件...", font=("微軟正黑體", font_size, "bold"))
label_mouse.pack()

pressed_keys = []
last_mouse_click = None

keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()

mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_mouse_click, on_scroll= on_mouse_scroll)
mouse_listener.start()

window.mainloop()

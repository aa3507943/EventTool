import tkinter as tk
import pyautogui
from pynput import keyboard, mouse

x, y = pyautogui.size()

def on_key_press(key: keyboard.KeyCode):
    if key not in pressed_keys:
        pressed_keys.append(key)
    update_label()

def on_key_release(key):
    if len(pressed_keys) != 0:
        pressed_keys.remove(pressed_keys[-1])
    if not any(pressed_keys):
        label.config(text="等待按鍵或鼠標事件...", font=("Arial", 30))

def on_mouse_move(x, y):
    if last_mouse_click:
        button, click_x, click_y = last_mouse_click
        label.config(text="鼠標拖曳\nX: {}  Y: {}\n 點擊: {} 鍵 ".format(x, y, button.name), font=("Arial", 30))
    else:
        label.config(text="鼠標移動\nX: {}  Y: {}".format(x, y), font=("Arial", 30))

def on_mouse_click(x, y, button, pressed):
    global last_mouse_click
    action = "按下" if pressed else "釋放"
    if action == "按下":
        last_mouse_click = (button, x, y)
        label.config(text="鼠標點擊: {} \n X: {} \n Y: {}".format(button.name, x, y), font=("Arial", 30))
    else:
        last_mouse_click = None
        label.config(text="等待按鍵或鼠標事件...", font=("Arial", 30))

def on_mouse_scroll(x, y, dx, dy):
    if dy > 0:
        label.config(text="滑鼠滾輪向上滾動", font=("Arial", 30))
    else:
        label.config(text="滑鼠滾輪向下滾動", font=("Arial", 30))

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


    label.config(text="按下的按鍵：" + "\n" + '\n'.join(key_strings), font=("Arial", 30))

window = tk.Tk()
window.geometry(f"600x300+{x//3}+{y//3}")
window.attributes("-topmost", True)
label = tk.Label(window, text="等待按鍵或鼠標事件...", font=("Arial", 30))
label.pack()
pressed_keys = []
last_mouse_click = None

keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()

mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_mouse_click)
mouse_listener.start()

mouse_listener.scroll_listener = mouse.Listener(on_scroll=on_mouse_scroll)
mouse_listener.scroll_listener.start()

window.mainloop()

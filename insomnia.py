import pyautogui
import threading
import time
import tkinter as tk


# ------------------------------------------------------------------------------
# Method Definitions
# ------------------------------------------------------------------------------
def guardian():
    def run():
        global insomniac
        global label
        global sleep_time

        last_move = time.strftime('%I:%M:%S %p', time.localtime())
        while (insomniac):
            still_time = 0
            while (still_time < sleep_time and insomniac):
                label.set("Last Move: %s\nNext Toggle: %s" % (
                    str(last_move), '%02d:%02d' % ((sleep_time - still_time) / 60, (sleep_time - still_time) % 60)))
                previous_position = pyautogui.position()
                time.sleep(1)
                if (pyautogui.position() == previous_position):
                    still_time += 1
                else:
                    still_time = 0
                    last_move = time.strftime('%I:%M:%S %p', time.localtime())

            if (insomniac):
                label.set("Last Move: %s\nNext Toggle: %s" % (
                    str(last_move), '%02d:%02d' % ((sleep_time - still_time) / 60, (sleep_time - still_time) % 60)))
                pyautogui.press('volumeup')
                pyautogui.press('volumedown')
                time.sleep(1)

    thread = threading.Thread(target=run)
    if (not thread.is_alive()):
        thread.start()


def guard_on():
    global insomniac
    insomniac = True
    b_guard.configure(bg='green')
    b_guard.configure(state='disabled')
    b_sleep.configure(bg='red')
    b_sleep.configure(state='normal')
    guardian()


def sleep_on():
    global insomniac
    insomniac = False
    b_guard.configure(bg='red')
    b_guard.configure(state='normal')
    b_sleep.configure(bg='green')
    b_sleep.configure(state='disabled')
    label.set('Insomnia\nInactive')


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
sleep_time = 600
insomniac = False

# ------------------------------------------------------------------------------
# GUI Creation
# ------------------------------------------------------------------------------
root = tk.Tk()
root.title("Insomnia")
root.geometry("300x150+0+0")

# Label has to go down here so it can use root as the master for the StringVar
label = tk.StringVar(root)
label.set('Insomnia\nInactive')

l_frame = tk.Frame(root)
l_frame.pack(side='top', fill='both')

b_frame = tk.Frame(root)
b_frame.pack(side='bottom', fill='both', expand=True)

l_text = tk.Label(l_frame, textvariable=label)
l_text.pack(fill='both', expand=True)

b_guard = tk.Button(b_frame, text="Guard", bg='red', disabledforeground='black', command=guard_on)
b_guard.pack(side='left', fill='both', expand=True)

b_sleep = tk.Button(b_frame, text="Sleep", bg='green', disabledforeground='black', command=sleep_on)
b_sleep.pack(side='right', fill='both', expand=True)
b_sleep.configure(state='disabled')

# ------------------------------------------------------------------------------
# Run Program
# ------------------------------------------------------------------------------
root.mainloop()

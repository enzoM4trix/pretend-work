import curses
import threading
import time
import sys
import pyautogui
import random

# Control functions in thread
works = True
workskey = True
info = "Move mouse OFF"
info2 = "Prevent screensaver OFF"

pyautogui.FAILSAFE = False

def moveMouse():
    screenWidth, screenHeight = pyautogui.size()
    while works:
        pyautogui.moveTo(random.randint(1,screenWidth), random.randint(1,screenHeight), duration=5, tween=pyautogui.easeInOutQuad)
        pyautogui.press('down')
        #time.sleep(60)

def exitmenu():
    global works
    global workskey
    works = False  # stop thread movemouse
    workskey = False
    print("Exiting program...")
    time.sleep(1)
    sys.exit()
def preventScreenSaver():
    global workskey
    while workskey:
        pyautogui.press('down')
        time.sleep(60)


# Menu curses
def menu(stdscr):
    global info
    global info2
    global movemouse_menu
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    options = ["Move mouse", "Prevent screen saver", "Exit"]
    choose = 0
    movemousestarted = False
    preventscreensaverstarted = False

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.border()

        title = "Pretend Work"
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        for i, option in enumerate(options):
            x = (width - len(option)) // 2
            y = 3 + i
            if i == choose:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, option)
        if info:
            stdscr.addstr(6,2,info)
        if info2:
            stdscr.addstr(8,2,info2)

        stdscr.refresh()
        keychoose = stdscr.getch()

        if keychoose == curses.KEY_UP and choose > 0:
            choose -= 1
        elif keychoose == curses.KEY_DOWN and choose < len(options) - 1:
            choose += 1
        elif keychoose in [curses.KEY_ENTER, 10, 13]:
            if choose == 0:
                if not movemousestarted:
                    global works
                    works = True
                    # Run function only once on 2nd time stop function
                    threading.Thread(target=moveMouse, daemon=True).start()
                    movemousestarted = True
                    info = "Move mouse ON"
                else:
                    works = False
                    movemousestarted = False
                    info = "Move mouse OFF"
            elif choose == 1:
                if not preventscreensaverstarted:
                    global workskey
                    workskey = True
                    threading.Thread(target=preventScreenSaver, daemon=True).start()
                    preventscreensaverstarted = True
                    info2 = "Prevent screensaver ON"
                else:
                    workskey = False
                    preventscreensaverstarted = False
                    info2 = "Prevent screensaver OFF"
            elif choose == 2:
                curses.endwin()
                exitmenu()
                break
        elif keychoose == ord('q'):
            break

curses.wrapper(menu)

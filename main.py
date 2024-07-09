import time
import threading
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.key_binding import KeyBindings


current_task = ''
paused = False
# start_time = check_and_assign_none

def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def track_time():
    global paused
    start_time = time.time()
    paused = False
    while True:
    if not paused:
        elapsed_time = time.time() - start_time
    time.sleep(1)
    return

def display_timer(task_name):
    global paused
    start_time = time.time()
    paused = False
    while True:
        if not paused:
            elapsed_time = time.time() - start_time
            clear()
            print(f"Task: {task_name}")
            print(f"Time Elapsed: {format_time(elapsed_time)}")
        time.sleep(1)



def main():
    global paused

    bindings = KeyBindings()

    @bindings.add('p')
    def _(event):
        nonlocal paused
        paused = not paused
        clear()
        print("Timer Paused" if paused else "Timer Resumed")

    @bindings.add('q')
    def _(event):
        clear()
        print("Timer Stopped")
        event.app.exit()

    @bindings.add('n')
    def _(event):
        nonlocal task_name
        clear()
        print("Enter the new task name:")
        task_name = prompt("Task Name: ")
        nonlocal start_time
        start_time = time.time()
        nonlocal paused
        paused = False

    print("Enter the task name:")
    task_name = prompt("Task Name: ")
    start_time = time.time()
    paused = False

    timer_thread = threading.Thread(target=display_timer, args=(task_name,))
    timer_thread.daemon = True
    timer_thread.start()

    prompt("", key_bindings=bindings)

if __name__ == "__main__":
    main()

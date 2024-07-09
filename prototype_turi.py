import time
import threading
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.key_binding import KeyBindings

# Global variables
start_time = None
task_name = None
elapsed_time = 0

actively_display = True
pause_timer = False

display_thread = None
stop_display_event = threading.Event()
pause_event_functions = threading.Event()
threading_lock = threading.Lock()

def format_time(seconds):
	return time.strftime('%H:%M:%S', time.gmtime(seconds))

def track_time():
	global start_time, elapsed_time
	while not pause_event_functions.is_set():
		# if not pause_event_functions.is_set() or not stop_display_event.is_set():
		with threading_lock:
			if start_time is not None:
				elapsed_time = time.time() - start_time
		time.sleep(1)


def display_time():
	global elapsed_time
	while ( not stop_display_event.is_set() ) and ( not pause_event_functions.is_set() ):
		with threading_lock:
			current_elapsed_time = elapsed_time
		clear()
		formatted_time = format_time(current_elapsed_time)
		print(f"Task: {task_name}")
		print(f"Time Elapsed: {formatted_time}")
		time.sleep(1)


def setup_bindings():
	global  task_name, start_time, actively_display, display_thread, stop_display_event
	bindings = KeyBindings()

	@bindings.add('p')
	def _(event):
		global pause_timer, display_thread, pause_event_functions
		pause_timer = not pause_timer
		# clear()
		print( f'Timer is {"resumed" if not actively_display else "paused"}!')
		if pause_timer:
			pause_event_functions.set() ### this is pausing the timer i guess
		elif not pause_timer:
			pause_event_functions.clear()

			track_thread = threading.Thread(target=track_time, daemon=True)
			display_thread = threading.Thread(target=display_time)
			track_thread.start()
			display_thread.start()

	@bindings.add('n')
	def _(event):
		global pause_timer, task_name, display_thread, pause_event_functions
		pause_timer = True
		pause_event_functions.set() ### this is pausing the timer i guess
		stop_display_event.set()
		# clear()
		print("Enter the new task name:")
		task_name = prompt("Task Name: ")
		# print( f'Timer is {"resumed" if not actively_display else "paused"}!')
		if not pause_timer:
			pass
		elif  pause_timer:
			pause_event_functions.clear()

			track_thread = threading.Thread(target=track_time, daemon=True)
			display_thread = threading.Thread(target=display_time)
			track_thread.start()
			display_thread.start()

	@bindings.add('q')
	def _(event):
		clear()
		print("Timer Stopped")
		stop_display_event.set()
		event.app.exit()	

	@bindings.add('d')
	def _(event):
		global actively_display, display_thread, stop_display_event
		actively_display = not actively_display
		print(f'Display timer is {"resumed" if actively_display else "paused"}')
		stop_display_event.set()
		if actively_display:
			stop_display_event.clear()
			display_thread = threading.Thread(target=display_time)
			display_thread.start()

	return bindings


def main():
	global task_name, start_time, display_thread
	print("Enter the task name:")
	task_name = prompt("Task Name: ")
	start_time = time.time()

	track_thread = threading.Thread(target=track_time, daemon=True)
	display_thread = threading.Thread(target=display_time)
	
	track_thread.start()
	display_thread.start()

	bindings = setup_bindings()
	prompt("", key_bindings=bindings)

if __name__ == "__main__":
	main()


### here is the error log
'''
Unhandled exception in event loop:
  File "/home/larsitsmeash/miniconda3/lib/python3.11/asyncio/events.py", line 80, in _run
    self._context.run(self._callback, *self._args)
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/input/vt100.py", line 162, in callback_wrapper
    callback()
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/application/application.py", line 714, in read_from_input_in_context
    context.copy().run(read_from_input)
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/application/application.py", line 694, in read_from_input
    self.key_processor.process_keys()
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/key_binding/key_processor.py", line 273, in process_keys
    self._process_coroutine.send(key_press)
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/key_binding/key_processor.py", line 188, in _process
    self._call_handler(matches[-1], key_sequence=buffer[:])
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/key_binding/key_processor.py", line 323, in _call_handler
    handler.call(event)
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/key_binding/key_bindings.py", line 127, in call
    result = self.handler(event)
             ^^^^^^^^^^^^^^^^^^^
  File "/home/larsitsmeash/Ash-lib/dev-projects/Turi/prototype_ptlkt_04.py", line 73, in _
    task_name = prompt("Task Name: ")
                ^^^^^^^^^^^^^^^^^^^^^
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/shortcuts/prompt.py", line 1425, in prompt
    return session.prompt(
           ^^^^^^^^^^^^^^^
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/shortcuts/prompt.py", line 1035, in prompt
    return self.app.run(
           ^^^^^^^^^^^^^
  File "/home/larsitsmeash/miniconda3/lib/python3.11/site-packages/prompt_toolkit/application/application.py", line 1002, in run
    return asyncio.run(coro)
           ^^^^^^^^^^^^^^^^^
  File "/home/larsitsmeash/miniconda3/lib/python3.11/asyncio/runners.py", line 186, in run
    raise RuntimeError(
Exception asyncio.run() cannot be called from a running event loop

sys:1: RuntimeWarning: coroutine 'Application.run_async' was never awaited
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
'''

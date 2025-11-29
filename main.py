from RealtimeSTT import AudioToTextRecorder
import dearpygui.dearpygui as dpg
import threading
import sys

WINDOW_TAG = "transcription_window"

running = False
rec_thread = None

def transcribe():
    global running
    recorder = AudioToTextRecorder(model="tiny.en", language="en", spinner=False)

    while running:
        text = recorder.text()
        dpg.add_text(f"You: {text}", parent=WINDOW_TAG)
        dpg.set_y_scroll(WINDOW_TAG, 999999)

def start_transcription():
    global running, rec_thread
    if running:
        return
    running = True
    rec_thread = threading.Thread(target=transcribe, daemon=True)
    rec_thread.start()

def stop_transcription():
    global running
    running = False

def on_close():
    """Called when the user closes the window or quits."""
    global running
    running = False
    sys.exit(0)

def main():
    dpg.create_context()
    dpg.create_viewport(title="Live Transcriber", width=600, height=460)

    # Register close callback
    dpg.set_exit_callback(on_close)

    with dpg.window(label="Transcription", tag=WINDOW_TAG, width=580, height=410, on_close=on_close):
        dpg.add_text("Press Start to begin listening.")

        with dpg.group(horizontal=True):
            dpg.add_button(label="Start", callback=start_transcription)
            dpg.add_button(label="Stop", callback=stop_transcription)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(WINDOW_TAG, True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()

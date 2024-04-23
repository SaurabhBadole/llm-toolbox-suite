# utils.py

import os

def convertMillis(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    btn_txt = ''
    if hours > 0:
        btn_txt += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        btn_txt += f'{minutes:02d}:{seconds:02d}'
    return btn_txt

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def save_chat_session(chat_history):
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        for message in chat_history:
            temp_file.write(message.content.encode("utf-8") + b"\n")
        return temp_file.name

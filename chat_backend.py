import socket
import threading
import numpy as np
import os
import time
from qam_utils import qam_modulate, qam_demodulate
from config import RECEIVER_IP, PORT, STARTER_BIT
from datetime import datetime
from audio_utils import play_audio, save_wav_file

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))

CHUNK_SIZE = 512  # audio chunk size
SEND_DELAY = 0.01  # fine-tuned delay

def send_data(full_bytes, M):
    bits = np.unpackbits(np.frombuffer(full_bytes, dtype=np.uint8))
    full_bits = np.concatenate((STARTER_BIT, bits))
    symbols = qam_modulate(full_bits, M)
    for i in range(0, len(symbols), CHUNK_SIZE):
        chunk = symbols[i:i+CHUNK_SIZE].astype(np.complex64).tobytes()
        sock.sendto(chunk, (RECEIVER_IP, PORT))
        time.sleep(SEND_DELAY)

def send_status_online(M):
    msg = "STATUS:ONLINE".encode('utf-8') + b"<END>"
    send_data(msg, M)

def send_message(msg, M):
    msg_bytes = msg.encode('utf-8') + b"<END>"
    send_data(msg_bytes, M)

def send_image_file(filepath, M):
    with open(filepath, 'rb') as f:
        data = f.read()
    ext = os.path.splitext(filepath)[1][1:]
    msg = f"IMAGE:{ext}:".encode('utf-8') + data + b"<END>"
    send_data(msg, M)

def send_audio_file(filepath, M):
    with open(filepath, 'rb') as f:
        audio_bytes = f.read()
    total_chunks = (len(audio_bytes) + CHUNK_SIZE - 1) // CHUNK_SIZE
    for i in range(total_chunks):
        chunk = audio_bytes[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
        header = f"AUDIO_CHUNK:{i}:{total_chunks}:".encode('utf-8')
        msg = header + chunk + b"<END>"
        send_data(msg, M)

def receive(chat_window, qam_option, mark_online_callback):
    buffer = bytearray()
    audio_chunks = {}
    expected_audio_chunks = None
    receive.status_replied = False

    while True:
        try:
            data, addr = sock.recvfrom(8192)
            buffer.extend(data)
            if len(buffer) < 8 or len(buffer) % 8 != 0:
                continue

            symbols = np.frombuffer(buffer.copy(), dtype=np.complex64)
            M = int(qam_option.get())
            bits = qam_demodulate(symbols, M)

            i = 0
            while i <= len(bits) - len(STARTER_BIT):
                if np.array_equal(bits[i:i+len(STARTER_BIT)], STARTER_BIT):
                    msg_bits = bits[i+len(STARTER_BIT):]
                    packed = np.packbits(msg_bits).tobytes()

                    if b"<END>" not in packed:
                        break

                    full_msg = packed.split(b"<END>")[0]

                    if full_msg.startswith(b"STATUS:"):
                        if not receive.status_replied:
                            send_status_online(M)
                            receive.status_replied = True
                        mark_online_callback()
                        chat_window.insert('end', "[Status] Friend is online\n")
                        buffer.clear()
                        break

                    if full_msg.startswith(b"IMAGE:"):
                        parts = full_msg.split(b":", 2)
                        ext = parts[1].decode("utf-8")
                        content = parts[2]
                        filename = f"received_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                        with open(filename, "wb") as f:
                            f.write(content)
                        chat_window.insert('end', f"[Image] saved as {filename}\n")
                        buffer.clear()
                        break

                    if full_msg.startswith(b"AUDIO_CHUNK:"):
                        try:
                            header, chunk_data = full_msg.split(b":", 3)[0:3], full_msg.split(b":", 3)[3]
                            index = int(header[1])
                            total = int(header[2])
                            audio_chunks[index] = chunk_data
                            expected_audio_chunks = total

                            if expected_audio_chunks and len(audio_chunks) == expected_audio_chunks:
                                audio_data = b''.join(audio_chunks[i] for i in sorted(audio_chunks))
                                filename = f"received_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                                with open(filename, 'wb') as f:
                                    f.write(audio_data)
                                chat_window.insert('end', f"[Audio] saved as {filename}\n")
                                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                                play_audio(audio_array, 44100)  # or detect samplerate
                                audio_chunks.clear()
                        except Exception as e:
                            print(f"[Audio chunk error] {e}")

                        buffer.clear()
                        break

                    try:
                        text = full_msg.decode("utf-8", errors="ignore")
                        chat_window.insert('end', "Friend: " + text + "\n")
                        buffer.clear()
                        break
                    except:
                        buffer.clear()
                        break
                i += 1
        except Exception as e:
            print(f"[Receive Error] {e}")
            continue

def start_receiver_thread(chat_window, qam_option, mark_online_callback):
    thread = threading.Thread(target=receive, args=(chat_window, qam_option, mark_online_callback), daemon=True)
    thread.start()

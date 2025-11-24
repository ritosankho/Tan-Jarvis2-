import asyncio
import websockets
import threading
from queues import log_queue
from queues import incoming_queue
from queues import log_queue

import queue

#import tan_code  # Import your Tan AI file

# Queue for Tan → GUI messages
clients = set()

# Function for Tan to log messages to GUI
def log_to_gui(message):
    
    
    log_queue.put(message)     # ← THIS IS ENOUGH
    print("THREAD PUT:", message)



async def send_logs():
    print("send_logs running, queue =", log_queue)
    while True:
        try:
            msg = log_queue.get_nowait()
        except queue.Empty:
            await asyncio.sleep(0.1)
            continue

        dead_clients = []
        for ws in clients:
            try:
                await ws.send(msg)
            except:
                dead_clients.append(ws)

        for ws in dead_clients:
            clients.remove(ws)

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"[GUI Input] {message}")
            
            incoming_queue.put(message) 
            log_queue.put("[USER] " + message)
            
        
    finally:
        clients.remove(websocket)


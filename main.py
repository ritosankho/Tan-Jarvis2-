import tan_code
import gui_server
import threading
import asyncio
import websockets
async def main():
    async with websockets.serve(gui_server.handler, "localhost", 6789):
        await gui_server.send_logs()

def run_server():
    asyncio.run(main())

# Run WebSocket server in a background thread
if __name__ == "__main__":

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    tan_code.start_ai(gui_server.log_to_gui)


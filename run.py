import argparse
import os
import socket
import sys
import threading

from dotenv import load_dotenv

load_dotenv()

from backend import app as app_module
from backend.instances import socketio

PORT = 5000


def parse_args():
    parser = argparse.ArgumentParser(description="Monasteries server")
    parser.add_argument(
        "--dev", action="store_true",
        help="development mode: localhost only, Flask debugger, verbose logs "
             "(frontend runs separately: cd frontend && npm run dev)",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="open the Tk debug visualizer next to the server",
    )
    return parser.parse_args()


def lan_ip() -> str:
    """Address other machines on the LAN can use (no packets are sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def run_server(mode: str):
    is_dev = mode == "dev"
    flask_app = app_module.create_app(mode)
    socketio.run(
        flask_app,
        host="127.0.0.1" if is_dev else "0.0.0.0",
        port=PORT,
        debug=is_dev,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
    )


def main():
    args = parse_args()
    mode = "dev" if args.dev else "prod"

    if mode == "prod":
        index = os.path.join(app_module.FRONTEND_DIST, "index.html")
        if not os.path.isfile(index):
            sys.exit("Frontend is not built. Run: cd frontend && npm run build")
        print(f"\n  Monasteries (LAN) -> http://{lan_ip()}:{PORT}\n")
    else:
        print(f"\n  Monasteries (dev) -> API on http://127.0.0.1:{PORT}, "
              f"open the frontend at http://localhost:5173\n")

    if args.debug:
        threading.Thread(target=run_server, args=(mode,), daemon=True).start()

        from backend.manager_instance import game_manager
        from debug.debug_visualizer import DebugVisualizer

        DebugVisualizer(game_manager).run()
    else:
        run_server(mode)


if __name__ == "__main__":
    main()
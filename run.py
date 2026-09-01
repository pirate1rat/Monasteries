import sys
import threading

from backend import app as app_module
from backend.instances import socketio

# ── server ─────────────────────────────────────────────────────────────────

def run_server():
    flask_app = app_module.create_app()
    socketio.run(
        flask_app, debug=False,
        port=5000,
        use_reloader=False,
        host="0.0.0.0"
    )


if __name__ == "__main__":
    debug_ui = "--debug" in sys.argv

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    if debug_ui:
        from backend.manager_instance import game_manager
        from debug.debug_visualizer import DebugVisualizer

        DebugVisualizer(game_manager).run()
    else:
        server_thread.join()
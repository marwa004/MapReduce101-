from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Lock
import time

class Coordinator:
    def __init__(self, input_files):
        self.tasks = [{"id": i, "file": f, "status": "idle"} for i, f in enumerate(input_files)]
        self.task_lock = Lock()
        self.worker_timeouts = {}  # Track when workers were last active

    def get_task(self):
        with self.task_lock:
            for task in self.tasks:
                if task["status"] == "idle":
                    task["status"] = "in-progress"
                    self.worker_timeouts[task["id"]] = time.time()
                    return task
        return None  # No tasks available

    def report_task_done(self, task_id):
        with self.task_lock:
            for task in self.tasks:
                if task["id"] == task_id:
                    task["status"] = "completed"
                    return True
        return False

    def monitor_tasks(self):
        while True:
            time.sleep(5)  # Check every 5 seconds
            with self.task_lock:
                now = time.time()
                for task in self.tasks:
                    if task["status"] == "in-progress" and now - self.worker_timeouts[task["id"]] > 10:
                        task["status"] = "idle"  # Mark as idle for reassignment
                        print(f"Task {task['id']} reassigned due to timeout.")

# Coordinator setup
input_files = ["file1.txt", "file2.txt", "file3.txt"]
coordinator = Coordinator(input_files)
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(coordinator)

# Run task monitor in a separate thread
Thread(target=coordinator.monitor_tasks, daemon=True).start()

print("Coordinator is running on port 8000...")
server.serve_forever()

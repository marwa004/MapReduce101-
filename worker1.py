import xmlrpc.client
import time

def process_task(task):
    # Simulate processing: read input file, perform a dummy operation, write output
    input_file = task["file"]
    output_file = f"output_{task['id']}.txt"
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        data = infile.read()
        result = data.upper()  # Example operation
        outfile.write(result)
    print(f"Processed task {task['id']} and wrote to {output_file}")

server_address = "http://localhost:8000"
proxy = xmlrpc.client.ServerProxy(server_address)

while True:
    try:
        task = proxy.get_task()
        if task:
            print(f"Received task {task['id']}")
            process_task(task)
            proxy.report_task_done(task["id"])
        else:
            print("No tasks available, sleeping...")
            time.sleep(2)
    except Exception as e:
        print(f"Error communicating with coordinator: {e}")
        time.sleep(5)

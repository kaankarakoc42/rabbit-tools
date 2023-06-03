import argparse
from glob import glob
import concurrent.futures

def process_data(data):
    return data

def process_lines(file_path, num_lines, substring):
    found = []
    with open(file_path, "r") as file:
        for line in file:
            if substring in line:
                found.append(line.strip())
        return found   

def job(args,task):
    print(f"Started working on file {task}")
    rv = process_lines(task, 100, args.string)
    print(f"Ended working on file {task}")
    a=os.path.splitext(os.path.basename(task))[1].split("_")[-1]
    print(a)
    with open(os.path.join(args.output, f"results_{a}.txt"), "w") as file:
        file.write("\n".join(rv))


if __name__ == "__main__":
    # Komut satırı argümanlarını tanımla
    parser = argparse.ArgumentParser(description='Large file splitter')
    parser.add_argument('-folder','-f', type=str, help='Path of the folder')
    parser.add_argument('-output','-o', type=str, help='Path of the output directory')
    parser.add_argument('-string','-s', type=str, help='string')
    # Argümanları ayrıştır
    args = parser.parse_args()
 
    num_threads = 5
    tasks = glob(args.folder+"/*")  # Example tasks

    # Create a thread pool executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)

    # Submit the initial tasks to the executor
    running_tasks = []
    for task in tasks[:num_threads]:
        future = executor.submit(job,args,task)
        running_tasks.append(future)

    # Continue submitting new tasks as threads finish
    for task in tasks[num_threads:]:
        # Wait for any of the running tasks to finish
        completed_task = concurrent.futures.wait(running_tasks, return_when=concurrent.futures.FIRST_COMPLETED).done.pop()

        # Start a new thread with the new task
        new_task = executor.submit(job,args, task)
        running_tasks.remove(completed_task)
        running_tasks.append(new_task)

    # Wait for all remaining tasks to finish
    concurrent.futures.wait(running_tasks)

    # Continue with the rest of the code
    print("Main thread execution resumed")
        

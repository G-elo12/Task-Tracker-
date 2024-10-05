import json
import datetime
import os

task_file = "Task.json"

def load_tasks():
    if not os.path.exists(task_file):
        return []
    
    with open(task_file, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(task_file, "w") as file:
        json.dump(tasks, file, indent=4)

def run():
    tasks = load_tasks()
    print("""
l----------------------------------------l
l                   tasks                l
l----------------------------------------l
""")
    print("""
              COMANDOS VÁLIDOS
|----------------------------------------------|
|> Task View all                                |
|> Task View in-progress                        |
|> Task View done                               |
|> Task Add 'description'                       |
|> Task Delete 'id'                             |
|> Task Update 'id'                             |
|> exit                                         |
|----------------------------------------------|
""")
    while True:
        
        choice = input("> ")

        if choice.lower().startswith('task view'):
            condition = choice.split(' ')[2] if len(choice.split(' ')) > 2 else "all"
            display_tasks(tasks, condition)
        
        elif choice.lower().startswith('task add'):
            description = ' '.join(choice.split(' ')[2:])
            add_task(tasks, description)
        
        elif choice.lower().startswith('task delete'):
            try:
                task_id = int(choice.split(' ')[2])
                delete_task(tasks, task_id)
            except (IndexError, ValueError):
                print("Invalid format. Use: Task Delete 'id'")

        elif choice.lower().startswith('task update'):
            try:
                task_id = int(choice.split(' ')[2])
                update_task(tasks, task_id)
            except (IndexError, ValueError):
                print("Invalid format. Use: Task Update 'id'")
        
        elif choice.lower() == 'exit':
            print("Exiting...")
            break
        
        else:
            print("Invalid command. Please try again.")

def display_tasks(tasks, condition="all"):
    """Display the list of tasks based on the specified condition."""
    if not tasks:
        print("No tasks available.")
        return

    if condition == "all":
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}")
    elif condition == "in-progress":
        found = False
        for task in tasks:
            if task["status"] == "in progress":
                print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}")
                found = True
        if not found:
            print("No tasks are in progress.")
    elif condition == "done":
        found = False
        for task in tasks:
            if task["status"] == "done":
                print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}")
                found = True
        if not found:
            print("No tasks are done.")

def add_task(tasks, description): 
    new_id = len(tasks) + 1
    new_task = {
        "id": new_id,
        "description": description,
        "status": "in progress",
        "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updatedAt": ""
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{description}' created successfully (●'◡'●)")

def delete_task(tasks, task_id):
    found = False
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task with ID {task_id} deleted successfully.")
            found = True
            break
    if not found:
        print(f"Task with ID {task_id} not found.")

def update_task(tasks, task_id):
    """Update the status of a task between 'done', 'in progress', or 'todo'."""
    found = False
    for task in tasks:
        if task["id"] == task_id:
            print(f"Current status: {task['status']}")
            new_status = input("Enter new status ('done', 'in progress', or 'todo'): ").lower()
            if new_status in ["done", "in progress", "todo"]:
                task["status"] = new_status
                task["updatedAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_tasks(tasks)
                print(f"Task with ID {task_id} updated successfully to status '{new_status}'.")
                found = True
            else:
                print("Invalid status. Please enter 'done', 'in progress', or 'todo'.")
            break
    if not found:
        print(f"Task with ID {task_id} not found.")

if __name__ == "__main__":
    run()

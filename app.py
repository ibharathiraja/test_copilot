from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Bug 1: Using mutable default argument
def get_tasks(tasks_list=[]):
    return tasks_list

# Bug 2: Missing error handling for file operations
def load_tasks():
    with open('tasks.json', 'r') as f:
        return json.load(f)

# Bug 3: Not closing file properly
def save_tasks(tasks):
    f = open('tasks.json', 'w')
    json.dump(tasks, f)
    # Bug: File not closed

@app.route('/')
def index():
    try:
        tasks = load_tasks()
    except:
        tasks = []
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task']
    # Bug 4: No input validation
    tasks = load_tasks()
    # Bug 5: No ID generation, can cause duplicates
    new_task = {
        'id': len(tasks) + 1,
        'name': task_name,
        'completed': False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    # Bug 6: No error handling if task_id not found
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    # Bug 7: Inefficient deletion without list comprehension
    for i in range(len(tasks)):
        if tasks[i]['id'] == task_id:
            del tasks[i]
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Bug 8: Debug mode enabled in production-like code
    app.run(debug=True, host='0.0.0.0')

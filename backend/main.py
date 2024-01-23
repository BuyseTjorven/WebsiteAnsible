from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from threading import Thread
import ansible_runner
import os

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# Define routes and their corresponding functions
# Run Ansible playbook asynchronously 
def run_ansible_playbook_async(playbook_path, inventory_path, extra_vars):
    try:
        runner = ansible_runner.run(
            playbook=playbook_path,
            inventory=inventory_path,
            extravars=extra_vars
        )
        print("Playbook run status:", runner.status)
        print("Playbook run stats:", runner.stats)
    except Exception as e:
        print("Error running the Ansible playbook:", e)

@app.route('/')
def hello():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    playbook_path = os.path.join(base_dir, "Ansible", "playbook.yml")
    inventory_path = os.path.join(base_dir, "Ansible", "inventory.ini")
    ansible_thread = Thread(target=run_ansible_playbook_async, args=(playbook_path, inventory_path, {}))
    ansible_thread.start()
    return jsonify(message="Ansible playbook gestart")

# You can add more routes and functions as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=120, debug=True)

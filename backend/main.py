from flask import Flask, request, render_template
import configparser
from flask_cors import CORS
from threading import Thread
import ansible_runner
import os
from flask import jsonify

app = Flask(__name__)
CORS(app, origins="*") # This will enable CORS for all routes

@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    password = request.form['password']
    ip = request.remote_addr  # Gets the client IP address
    update_inventory(ip, password)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    playbook_path = os.path.join(base_dir, "Ansible", "playbook.yml")
    inventory_path = os.path.join(base_dir, "Ansible", "inventory.ini")
    ansible_thread = Thread(target=run_ansible_playbook_async, args=(playbook_path, inventory_path, {}))
    ansible_thread.start()
    return jsonify(message='TrueNAS configuratie gestart!'), 200
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


def update_inventory(ip, password):
    config = configparser.ConfigParser()
    config.read('inventory.ini')
    if 'webserver' in config:
        config['webserver']['ansible_host'] = ip
        config['webserver']['ansible_ssh_pass'] = password
    else:
        config.add_section('webserver')
        config.set('webserver', 'ansible_host', ip)
        config.set('webserver', 'ansible_ssh_pass', password)

    with open('inventory.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9005,debug=True)
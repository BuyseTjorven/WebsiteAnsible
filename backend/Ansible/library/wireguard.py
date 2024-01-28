import requests
from ansible.module_utils.basic import AnsibleModule

def check_if_deployed(module, app_name):
    api_url = f"http://{module.params['host']}/api/v2.0/chart/release"
    response = requests.get(api_url, headers={"Authorization": f"Bearer {module.params['api_key']}"})

    if response.status_code == 200:
        releases = response.json()
        for release in releases:
            if release['name'] == app_name:
                return True
    return False

def deploy_wgeasy(module):
    if check_if_deployed(module, module.params['release_name']):
        module.exit_json(changed=False, msg=f"{module.params['release_name']} is already deployed, skipping.")
        return

    api_url = f"http://{module.params['host']}/api/v2.0/chart/release"

    # Replace the next values with the actual values required for WG Easy
    wgeasy_config = {
        "catalog": "TRUENAS",
        "item": "wg-easy",
        "release_name": module.params['release_name'],
        "train": "charts",
        "version": '2.0.12',
        "values": {
            # Add the specific configuration for WG Easy here
        }
    }

    response = requests.post(api_url, headers={"Authorization": f"Bearer {module.params['api_key']}"}, json=wgeasy_config)

    if response.status_code in [200, 201]:
        module.exit_json(changed=True, msg="WG Easy deployed successfully.")
    else:
        module.fail_json(msg="Failed to deploy WG Easy: " + response.text)

def main():
    module_args = {
        'host': {'type': 'str', 'required': True},
        'api_key': {'type': 'str', 'required': True, 'no_log': True},
        'release_name': {'type': 'str', 'required': True},
        'version': {'type': 'str', 'required': True},  # The version number should be added here
        # Include other parameters as needed for WG Easy
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    deploy_wgeasy(module)

if __name__ == '__main__':
    main()

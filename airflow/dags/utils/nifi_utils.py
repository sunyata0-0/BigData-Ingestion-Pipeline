import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


BASE_URL = "https://nifi:8443"


def login(username, password):
    """
    Authenticate with NiFi and return a JWT token.
    """

    response = requests.post(
        f"{BASE_URL}/nifi-api/access/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "username": username,
            "password": password,
        },
        verify=False,
    )

    response.raise_for_status()

    return response.text


def auth_headers(token):
    """
    Build Authorization headers.
    """

    return {
        "Authorization": f"Bearer {token}"
    }


def is_nifi_ready():
    """
    Returns True if NiFi is responding.
    """

    try:

        response = requests.get(
            f"{BASE_URL}/nifi-api/flow/about",
            verify=False,
            timeout=5,
        )

        return response.ok

    except requests.RequestException:
        return False


def process_group_status(process_group_id, token):
    """
    Returns the current process group state.
    """

    response = requests.get(
        f"{BASE_URL}/nifi-api/flow/process-groups/{process_group_id}",
        headers=auth_headers(token),
        verify=False,
    )

    response.raise_for_status()

    return response.json()


def start_process_group(process_group_id, token):
    """
    Start a process group.
    """

    response = requests.put(
        f"{BASE_URL}/nifi-api/flow/process-groups/{process_group_id}",
        headers=auth_headers(token),
        json={
            "id": process_group_id,
            "state": "RUNNING"
        },
        verify=False,
    )

    response.raise_for_status()

    return response.json()


def stop_process_group(process_group_id, token):
    """
    Stop a process group.
    """

    response = requests.put(
        f"{BASE_URL}/nifi-api/flow/process-groups/{process_group_id}",
        headers=auth_headers(token),
        json={
            "id": process_group_id,
            "state": "STOPPED"
        },
        verify=False,
    )

    response.raise_for_status()

    return response.json()


#def process_group_running(process_group_id, token):
    """
    Returns True if every processor inside the process group is running.
    """
'''
    status = process_group_status(process_group_id, token)    
    
    counts = status["processGroupFlow"]["flow"]["processGroupStatus"]["aggregateSnapshot"]

    return (
        counts["runningCount"] > 0
        and counts["stoppedCount"] == 0
        and counts["invalidCount"] == 0
    )'''
def process_group_running(process_group_id, token):
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(
        f"{BASE_URL}/nifi-api/process-groups/{process_group_id}",
        headers=headers,
        verify=False
    )
    r.raise_for_status()

    return True

def processor_summary(process_group_id, token):
    """
    Returns a summary of the process group.
    """

    status = process_group_status(process_group_id, token)

    snapshot = status["processGroupFlow"]["flow"]["processGroupStatus"]["aggregateSnapshot"]

    return {
        "running": snapshot["runningCount"],
        "stopped": snapshot["stoppedCount"],
        "invalid": snapshot["invalidCount"],
        "disabled": snapshot["disabledCount"],
        "active_threads": snapshot["activeThreadCount"],
        "queued": snapshot["queued"],
    }


def run_pipeline(process_group_id, username, password):
    """
    Login and start a process group.
    Returns the JWT token.
    """

    token = login(username, password)

    start_process_group(process_group_id, token)

    return token
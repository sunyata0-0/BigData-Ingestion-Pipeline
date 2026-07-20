import docker
from docker.errors import NotFound

client = docker.from_env()


def try_get_container(container_name):
    
    try:
        container = client.containers.get(container_name)
        container.reload()
        return container

    except NotFound:
        return None


def is_running(container_name):
    
    container = try_get_container(container_name)
    
    if container is None:
        return False
    
    return container.status == "running"


def start_container(container_name):
    
    container = try_get_container(container_name)
    
    if container is None:
        return {
            "name": container_name,
            "started": False,
            "status": "missing"
        }

    if container.status == "running":
        return {
            "name": container_name,
            "started": False,
            "status": "running"
        }

    container.start()
    container.reload()

    return {
        "name": container_name,
        "started": True,
        "status": container.status
    }


def stop_container(container_name):
    
    container = try_get_container(container_name)
    
    if container is None:
        return

    if container.status == "running":
        container.stop()


def restart_container(container_name):

    container = try_get_container(container_name)
    
    if container is None:
        return
    
    container.restart()


def container_status(container_name):

    container = try_get_container(container_name)
    
    if container is None:
        return "missing"

    return container.status


def list_running():

    return [
        c.name
        for c in client.containers.list()
    ]


def container_summary(container_names):

    summary = {}

    for name in container_names:
        summary[name] = container_status(name)

    return summary
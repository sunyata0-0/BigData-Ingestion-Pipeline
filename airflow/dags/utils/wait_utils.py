import socket
import time

import requests
import urllib3

# NiFi uses a self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def wait(seconds):
    """
    Sleep for a number of seconds.
    """
    time.sleep(seconds)


def wait_for_port(host, port, timeout=120, interval=2):
    """
    Wait until a TCP port becomes available.

    Returns True if available before timeout.
    Raises TimeoutError otherwise.
    """

    start = time.time()

    while time.time() - start < timeout:

        try:
            with socket.create_connection((host, port), timeout=5):
                return True

        except OSError:
            time.sleep(interval)

    raise TimeoutError(
        f"{host}:{port} did not become available within {timeout} seconds."
    )


def wait_for_http(url, timeout=120, interval=2):
    """
    Wait until an HTTP endpoint responds with a success status.

    Returns True if successful.
    Raises TimeoutError otherwise.
    """

    start = time.time()

    while time.time() - start < timeout:

        try:
            response = requests.get(url, timeout=5)

            if response.status_code < 500:
                return True

        except requests.RequestException:
            pass

        time.sleep(interval)

    raise TimeoutError(
        f"{url} did not become available within {timeout} seconds."
    )


def wait_for_https(url, timeout=120, interval=2, verify=False):
    """
    Wait until an HTTPS endpoint responds with a success status.

    verify=False is useful for NiFi's self-signed certificate.
    """

    start = time.time()

    while time.time() - start < timeout:

        try:
            response = requests.get(
                url,
                verify=verify,
                timeout=5,
            )

            if response.status_code < 500:
                return True

        except requests.RequestException:
            pass

        time.sleep(interval)

    raise TimeoutError(
        f"{url} did not become available within {timeout} seconds."
    )


def wait_until(predicate, timeout=120, interval=2):
    """
    Wait until any function returns True.

    Example:
        wait_until(lambda: is_running("mysql"))
    """

    start = time.time()

    while time.time() - start < timeout:

        if predicate():
            return True

        time.sleep(interval)

    raise TimeoutError(
        "Condition was not satisfied before timeout."
    )
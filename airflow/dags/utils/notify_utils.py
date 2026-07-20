import requests
from datetime import datetime


def send_discord(webhook_url, title, description, color=0x5865F2):
    """
    Send an embed message to Discord.
    """

    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }

    response = requests.post(
        webhook_url,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()


def notify_success(webhook_url, message):
    """
    Green success message.
    """

    send_discord(
        webhook_url,
        "Pipeline Succeeded ✅",
        message,
        0x57F287
    )


def notify_failure(webhook_url, message):
    """
    Red failure message.
    """

    send_discord(
        webhook_url,
        "Pipeline Failed ❌",
        message,
        0xED4245
    )


def notify_warning(webhook_url, message):
    """
    Yellow warning message.
    """

    send_discord(
        webhook_url,
        "Pipeline Warning ⚠️",
        message,
        0xFEE75C
    )


def notify_info(webhook_url, message):
    """
    Blue information message.
    """

    send_discord(
        webhook_url,
        "Pipeline Information ℹ️",
        message,
        0x5865F2
    )


def format_runtime(seconds):
    """
    Convert seconds into a human-readable string.
    """

    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {minutes}m {seconds}s"

    if minutes:
        return f"{minutes}m {seconds}s"

    return f"{seconds}s"


def build_summary(runtime, containers, process_group_id):
    """
    Build a formatted summary for Discord.
    """

    lines = [
        "### Runtime",
        format_runtime(runtime),
        "",
        "### Containers"
    ]

    for name, status in containers.items():
        lines.append(f"• **{name}** : `{status}`")

    lines.extend([
        "",
        "### NiFi",
        f"Process Group: `{process_group_id}`"
    ])

    return "\n".join(lines)
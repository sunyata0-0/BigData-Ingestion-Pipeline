import requests


class DiscordService:

    def __init__(self, config):
        self.webhook = config["DISCORD_WEBHOOK"]


    def send(self, message, notification_type="info"):
        
        styles = {

            "success": (
                "Pipeline Succeeded ✅",
                0x57F287
            ),

            "warning": (
                "Pipeline Warning ⚠️",
                0xFEE75C
            ),

            "error": (
                "Pipeline Failed ❌",
                0xED4245
            ),

            "info": (
                "Pipeline Information ℹ️",
                0x5865F2
            )

        }

        title, color = styles.get(
            notification_type,
            styles["info"]
        )

        payload = {

            "embeds": [

                {

                    "title": title,

                    "description": message,

                    "color": color,

                    "footer": {

                        "text": "Big Data Dashboard"

                    }

                }

            ]

        }

        response = requests.post(
            self.webhook,
            json=payload,
            timeout=10
        )

        if response.status_code not in (200, 204):
            raise RuntimeError(response.text)

        return {
            "success": True,
            "message": "Notification sent successfully."
        }
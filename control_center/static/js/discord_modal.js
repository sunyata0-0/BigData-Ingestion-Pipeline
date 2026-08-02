document.addEventListener("DOMContentLoaded", () => {

    const textarea = document.getElementById("discord-message");

    const sendButton = document.getElementById("discord-send-btn");

    const status = document.getElementById("discord-status");

    if (!textarea || !sendButton || !status)
        return;


    let notificationType = "info";

    const buttons = document.querySelectorAll(".discord-template");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            buttons.forEach(b =>
                b.classList.remove("discord-template--active")
            );

            button.classList.add("discord-template--active");

            if (button.id.endsWith("success"))
                notificationType = "success";

            else if (button.id.endsWith("warning"))
                notificationType = "warning";

            else if (button.id.endsWith("error"))
                notificationType = "error";

            else
                notificationType = "info";

        });

    });

    document.getElementById("discord-template-info")
        ?.classList.add("discord-template--active");


    sendButton.addEventListener("click", async () => {

        const message = textarea.value.trim();

        status.textContent = "";
        status.classList.remove(
            "discord-status--success",
            "discord-status--error"
        );

        if (!message) {

            status.textContent = "Please enter a message.";

            status.classList.add("discord-status--error");

            return;

        }

        sendButton.disabled = true;

        sendButton.textContent = "Sending...";

        try {

            const response = await fetch("/discord/send", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message,
                    type: notificationType
                })

            });

            const data = await response.json();

            if (!response.ok || !data.success)
                throw new Error(data.message);

            status.textContent = data.message;

            status.classList.add("discord-status--success");

            textarea.value = "";

        }

        catch (error) {

            status.textContent =
                error.message || "Failed to send notification.";

            status.classList.add("discord-status--error");

        }

        finally {

            sendButton.disabled = false;

            sendButton.textContent = "Send Notification";

        }

    });

});
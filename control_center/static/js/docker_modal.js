async function loadDockerStatus() {

    try {

        const response = await fetch("/docker/status");
        const services = await response.json();

        services.forEach(service => {

            const row = document.querySelector(
                `[data-service="${service.service}"]`
            );

            if (!row)
                return;

            const badge = row.querySelector(".badge");

            if (service.running) {

                badge.textContent = "Running";
                badge.className = "badge badge--green";

            }

            else {

                badge.textContent = "Stopped";
                badge.className = "badge badge--red";

            }

        });

    }

    catch (error) {

        console.error(error);

    }

}



async function restartService(service, button) {

    button.disabled = true;
    button.textContent = "Restarting...";

    try {

        const response = await fetch(

            `/docker/restart/${service}`,

            {
                method: "POST"
            }

        );

        const result = await response.json();

        if (!result.success)
            alert(result.message);

    }

    catch (error) {

        alert("Unable to restart service.");

    }

    button.disabled = false;
    button.textContent = "Restart";

    loadDockerStatus();

}



document.addEventListener("DOMContentLoaded", () => {

    loadDockerStatus();

    setInterval(
        loadDockerStatus,
        5000
    );

    document

        .querySelectorAll(".service-row__action")

        .forEach(button => {

            button.addEventListener(

                "click",

                () => {

                    restartService(

                        button.dataset.service,
                        button

                    );

                }

            );

        });

});
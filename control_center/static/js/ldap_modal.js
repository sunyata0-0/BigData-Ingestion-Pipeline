document.addEventListener("DOMContentLoaded", () => {

    const revealButton =
        document.getElementById("ldap-reveal-btn");

    const passwordInput =
        document.getElementById("ldap-admin-password");

    if (!revealButton) return;


    revealButton.addEventListener("click", revealPasswords);


    async function revealPasswords() {

        const password = passwordInput.value.trim();

        if (!password) {

            alert("Enter the administrator password.");

            return;

        }

        try {

            const response = await fetch(
                "/ldap/passwords",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok || !data.success) {

                alert(data.message);

                return;

            }

            document
                .querySelector('[data-user="mahdi"] .ldap-user__dots')
                .textContent =
                    data.passwords.mahdi;

            document
                .querySelector('[data-user="viewer"] .ldap-user__dots')
                .textContent =
                    data.passwords.viewer;


            passwordInput.value = "";


            document.getElementById(
                "ldap-confirm-toggle"
            ).checked = false;

        }

        catch (error) {

            console.error(error);

            alert("Unable to contact the server.");

        }

    }

});
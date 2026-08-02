document.addEventListener("DOMContentLoaded", () => {

    const firstName = document.getElementById("mysql-first-name");
    const lastName = document.getElementById("mysql-last-name");
    const department = document.getElementById("mysql-department");
    const salary = document.getElementById("mysql-salary");

    const insertButton = document.getElementById("mysql-insert-btn");
    const status = document.getElementById("mysql-status");

    if (!insertButton) return;

    insertButton.addEventListener("click", insertRow);

    async function insertRow() {

        status.textContent = "Inserting row...";
        status.className = "mysql-status";

        const payload = {
            first_name: firstName.value.trim(),
            last_name: lastName.value.trim(),
            department: department.value,
            salary: Number(salary.value)
        };

        if (
            !payload.first_name ||
            !payload.last_name ||
            !payload.department ||
            !payload.salary
        ) {
            showError("Please fill in every field.");
            return;
        }

        insertButton.disabled = true;

        try {

            const response = await fetch("/mysql/insert", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!result.success) {
                showError(result.message);
                return;
            }

            status.textContent = result.message;
            status.className = "mysql-status mysql-status--success";

            firstName.value = "";
            lastName.value = "";
            department.selectedIndex = 0;
            salary.value = "";

        }

        catch (error) {

            console.error(error);
            showError("Unable to insert row.");

        }

        finally {

            insertButton.disabled = false;

        }

    }

    function showError(message) {

        status.textContent = message;
        status.className = "mysql-status mysql-status--error";

    }

});
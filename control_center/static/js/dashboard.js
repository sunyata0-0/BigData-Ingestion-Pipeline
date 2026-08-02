console.log("Dashboard loaded");

const uploadButton = document.getElementById("upload-btn");
const input = document.getElementById("file-input");

if (uploadButton && input) {

    uploadButton.addEventListener("click", () => {
        input.click();
    });

    /*input.addEventListener("change", async () => {

        if (input.files.length === 0)
            return;

        const formData = new FormData();
        formData.append("file", input.files[0]);

        try {

            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            alert(result.message);

        }

        catch (error) {

            alert("Upload failed.");

            console.error(error);

        }

    });*/

}//h

input.addEventListener("change", async () => {

    if (input.files.length === 0)
        return;

    const formData = new FormData();
    formData.append("file", input.files[0]);

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        alert(result.message);

    }
    catch (error) {

        alert("Upload failed.");

        console.error(error);

    }

});


const workflowButton = document.getElementById("run-workflow-btn");

if (workflowButton) {

    workflowButton.addEventListener("click", async () => {

        const response = await fetch("/airflow/run", {
            method: "POST"
        });

        const result = await response.json();

        alert(result.message);

    });

}
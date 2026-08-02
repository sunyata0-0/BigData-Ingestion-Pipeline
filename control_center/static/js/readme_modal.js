document.addEventListener("DOMContentLoaded", () => {

    const githubButton =
        document.getElementById("readme-open-github");

    if (!githubButton)
        return;

    githubButton.addEventListener("click", () => {

        window.open(
            "https://github.com/sunyata0-0/BigData-Ingestion-Pipeline",
            "_blank"
        );

    });

});
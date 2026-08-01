document.addEventListener("DOMContentLoaded", () => {

    const fileList = document.getElementById("hdfs-file-list");
    const currentPath = document.getElementById("hdfs-current-path");
    const backButton = document.getElementById("hdfs-back-btn");
    const refreshButton = document.getElementById("hdfs-refresh-btn");

    const loadingState = document.getElementById("hdfs-loading-state");
    const emptyState = document.getElementById("hdfs-empty-state");
    const errorState = document.getElementById("hdfs-error-state");

    if (!fileList) return;

    let path = "/";

    loadDirectory(path);

    refreshButton?.addEventListener("click", () => {

        loadDirectory(path);

    });

    backButton?.addEventListener("click", () => {

        if (path === "/")
            return;

        const parts = path.split("/").filter(Boolean);

        parts.pop();

        path = "/" + parts.join("/");

        if (path === "")
            path = "/";

        loadDirectory(path);

    });

    function hideStates() {

        loadingState.hidden = true;
        emptyState.hidden = true;
        errorState.hidden = true;

    }

    function updateBackButton() {

        const disabled = (path === "/");

        backButton.disabled = disabled;
        backButton.setAttribute(
            "aria-disabled",
            disabled ? "true" : "false"
        );

    }

    async function loadDirectory(directory) {

        try {

            path = directory;

            currentPath.textContent = path;

            updateBackButton();

            hideStates();

            loadingState.hidden = false;

            fileList.innerHTML = "";

            const response = await fetch(
                `/hdfs/list?path=${encodeURIComponent(path)}`
            );

            if (!response.ok)
                throw new Error("Request failed");

            const data = await response.json();

            hideStates();

            fileList.innerHTML = "";

            if (data.length === 0) {

                emptyState.hidden = false;
                return;

            }

            data.forEach(item => {

                const row = document.createElement("div");

                row.className = "hdfs-row";

                row.innerHTML = `
                    <div class="hdfs-row__icon">
                        ${item.type === "directory" ? "📁" : "📄"}
                    </div>

                    <div class="hdfs-row__name">
                        ${item.name}
                    </div>

                    <div class="hdfs-row__type">
                        ${item.type}
                    </div>

                    <div class="hdfs-row__size">
                        ${item.type === "directory" ? "-" : item.size}
                    </div>

                    <div class="hdfs-row__modified">
                        ${item.modified}
                    </div>
                `;

                if (item.type === "directory") {

                    row.style.cursor = "pointer";

                    row.addEventListener("click", () => {

                        loadDirectory(item.path);

                    });

                }

                fileList.appendChild(row);

            });

        }

        catch (error) {

            console.error(error);

            hideStates();

            fileList.innerHTML = "";

            errorState.hidden = false;

        }

    }

});
document.addEventListener("DOMContentLoaded", () => {

    const output = document.getElementById("hive-output");

    if (!output)
        return;

    const buttons = {

        databases: document.getElementById("hive-databases-btn"),
        tables: document.getElementById("hive-tables-btn"),
        schema: document.getElementById("hive-schema-btn"),
        preview: document.getElementById("hive-preview-btn")

    };


    buttons.databases?.addEventListener("click", () => {
        loadDatabases();
    });

    buttons.tables?.addEventListener("click", () => {
        loadTables();
    });

    buttons.schema?.addEventListener("click", () => {
        loadSchema();
    });

    buttons.preview?.addEventListener("click", () => {
        loadPreview();
    });


    async function request(url) {

        output.innerHTML = `
            <div class="hive-output__state--placeholder">
                <div class="hive-output__icon">⏳</div>
                <p>Loading...</p>
            </div>
        `;

        /*output.innerHTML = `
        <div class="hive-output__state--placeholder">
            <span class="file-state__spinner"></span>
            <p>Loading...</p>
        </div>
        `;*/

        await new Promise(resolve => setTimeout(resolve,10));

        const response = await fetch(url);

        if (!response.ok)
            throw new Error();

        return await response.json();

    }


    async function loadDatabases() {

        try {

            const data = await request("/hive/databases");

            output.innerHTML = `
                <div class="hive-output__heading">
                    Databases
                </div>

                <ul class="hive-list">
                    ${data.map(db => `
                        <li class="hive-list__item">
                            <span class="hive-list__icon">🗄️</span>
                            <span class="hive-list__name">${db}</span>
                        </li>
                    `).join("")}
                </ul>
            `;

        }

        catch {

            showError();

        }

    }


    async function loadTables() {

        try {

            const data = await request("/hive/tables");

            output.innerHTML = `
                <div class="hive-output__heading">
                    Tables
                </div>

                <ul class="hive-list">
                    ${data.map(table => `
                        <li class="hive-list__item">
                            <span class="hive-list__icon">📋</span>
                            <span class="hive-list__name">${table}</span>
                        </li>
                    `).join("")}
                </ul>
            `;

        }

        catch {

            showError();

        }

    }


    async function loadSchema() {

        try {

            const data = await request("/hive/schema");

            output.innerHTML = `
                <div class="hive-output__heading">
                    customers schema
                </div>

                <div class="hive-table-wrap">

                    <table class="hive-table">

                        <thead>
                            <tr>
                                <th>Column</th>
                                <th>Type</th>
                            </tr>
                        </thead>

                        <tbody>

                            ${data.map(column => `
                                <tr>
                                    <td>${column.column}</td>
                                    <td>${column.type}</td>
                                </tr>
                            `).join("")}

                        </tbody>

                    </table>

                </div>
            `;

        }

        catch {

            showError();

        }

    }


    async function loadPreview() {

        try {

            const data = await request("/hive/preview");

            if (data.length === 0) {

                output.innerHTML = `
                    <div class="hive-output__state--placeholder">
                        <div class="hive-output__icon">📭</div>
                        <p>No rows found.</p>
                    </div>
                `;

                return;

            }

            const columns = [
                "id",
                "first_name",
                "last_name",
                "department",
                "salary"
            ];

            output.innerHTML = `
                <div class="hive-output__heading">
                    customers (20 rows)
                </div>

                <div class="hive-table-wrap">

                    <table class="hive-table">

                        <thead>
                            <tr>
                                ${columns.map(c => `<th>${c}</th>`).join("")}
                            </tr>
                        </thead>

                        <tbody>

                            ${data.map(row => `
                                <tr>
                                    ${columns.map(c => `<td>${row[c]}</td>`).join("")}
                                </tr>
                            `).join("")}

                        </tbody>

                    </table>

                </div>
            `;

        }

        catch {

            showError();

        }

    }


    function showError() {

        output.innerHTML = `
            <div class="hive-output__state--placeholder">
                <div class="hive-output__icon">⚠️</div>
                <p>Unable to retrieve Hive information.</p>
            </div>
        `;

    }

});
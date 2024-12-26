document.getElementById("updateButton").addEventListener("click", async () => {
    const response = await fetch("/update");
    const data = await response.json();

    const tableBody = document.getElementById("weatherTableBody");
    tableBody.innerHTML = "";

    for (const [country, info] of Object.entries(data)) {
        const row = document.createElement("tr");

        const countryCell = document.createElement("td");
        countryCell.textContent = country;
        row.appendChild(countryCell);

        const capitalCell = document.createElement("td");
        capitalCell.textContent = info.capital;
        row.appendChild(capitalCell);

        const temperatureCell = document.createElement("td");
        temperatureCell.textContent = info.temperature !== null ? info.temperature : "N/A";
        row.appendChild(temperatureCell);

        tableBody.appendChild(row);
    }
});
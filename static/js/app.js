function show_plot() {
    const scheme = document.getElementById("scheme").value.trim();
    const type = document.getElementById('type').value;

    // Validation
    if (!scheme) {
        showError("Please enter a scheme code");
        return;
    }
    if (!type) {
        showError("Please select a forecasting algorithm");
        return;
    }

    const requestData = { "scheme": scheme, "type": type };
    const div = document.getElementById('data');
    div.innerHTML = '';

    const client = new XMLHttpRequest();
    client.open("POST", "/");

    // Show loader
    document.getElementById("loader").classList.add("active");
    document.getElementById("error").style.display = "none";

    client.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    client.send(JSON.stringify(requestData));

    client.onreadystatechange = function() {
        if (this.readyState == 4) {
            document.getElementById("loader").classList.remove("active");

            if (this.status == 200) {
                try {
                    const result = JSON.parse(this.responseText);
                    renderCombinedChart(result, type);
                } catch (e) {
                    showError("Error parsing response. Please try again.");
                }
            } else {
                showError("Invalid scheme code or algorithm error. Please check your inputs.");
            }
        }
    };
}

function renderCombinedChart(result, type) {
    const div = document.getElementById('data');
    div.innerHTML = '';

    if (!result.chart_data) {
        showError("No chart data received from server.");
        return;
    }

    const chartData = result.chart_data;
    const schemeName = result.details && result.details.scheme_name ? result.details.scheme_name : "Selected Scheme";
    const rmse = Number.isFinite(result.rmse) ? result.rmse.toFixed(4) : "N/A";

    const html = `
        <div class="plot-container" style="grid-column: 1 / -1;">
            <div class="plot-title">${type} - Last 100 Days + 30 Day Forecast</div>
            <p style="margin: 0 0 12px 0; color: #555; font-size: 13px;">
                ${schemeName} | RMSE: ${rmse}
            </p>
            <div style="height: 420px;">
                <canvas id="navChart"></canvas>
            </div>
        </div>
    `;
    div.innerHTML = html;

    const ctx = document.getElementById('navChart').getContext('2d');
    if (window.navChartInstance) {
        window.navChartInstance.destroy();
    }

    window.navChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: 'Actual NAV (Last 100 Days)',
                    data: chartData.actual,
                    borderColor: '#1f2937',
                    backgroundColor: 'rgba(31, 41, 55, 0.08)',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.25,
                    spanGaps: false
                },
                {
                    label: `${type} Forecast (30 Days)`,
                    data: chartData.forecast,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.12)',
                    borderWidth: 2,
                    pointRadius: 0,
                    borderDash: [6, 4],
                    tension: 0.25,
                    spanGaps: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            if (context.raw == null) {
                                return null;
                            }
                            return `${context.dataset.label}: ${Number(context.raw).toFixed(3)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxTicksLimit: 10
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'NAV'
                    }
                }
            }
        }
    });
}

function showError(message) {
    document.getElementById("error").textContent = message;
    document.getElementById("error").style.display = "block";
    document.getElementById("loader").classList.remove("active");
}

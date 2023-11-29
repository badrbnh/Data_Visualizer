google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(() => {
    // Make the API call to get data
    $.ajax({
        url: 'http://127.0.0.1:5000/api/v1/data',
        success: (resp) => {
            console.log(resp); // Log the entire response
            drawChart(resp);
        },
        error: (error) => {
            console.error("Error fetching data from the server:", error.statusText);
        }
    });
});

function drawChart(data) {
    // Create the data table.
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn('number', 'Distance to Station (meters)');
    dataTable.addColumn('number', 'House Age (years)');
    dataTable.addColumn('number', 'Price per Square Foot');

    // Add rows from the parsed data
    data.forEach((row) => {
        const distance = row['Distance to Station (meters)'] || 0;
        const age = row['House Age (years)'] || 0;
        const pricePerSquareFoot = row['Price per Square Foot'] || 0;
        dataTable.addRow([distance, age, pricePerSquareFoot]);
    });

    var options = {
        'title': 'House Data Scatter Plot',
        'width': 680,
        'height': 280,
        'chartArea': {left: 60, top: 40, width: '80%', height: '70%'},
        'legend': 'none', // Remove legend for simplicity
        'pointSize': 8, // Adjust the size of data points
    };

    // Instantiate and draw the chart
    $("#convert-button").on("click", ()=>{var chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));
    chart.draw(dataTable, options);})
}
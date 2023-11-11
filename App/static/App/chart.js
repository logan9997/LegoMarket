function get_chart() {
    var chart_id = JSON.parse(document.getElementById('chart-id').textContent)
    var chart = document.getElementById(chart_id);
    return chart
}

function get_data() {
    var data = JSON.parse(document.getElementById('chart-data').textContent);
    return data;
}

function get_labels() {
    var labels = JSON.parse(document.getElementById('chart-labels').textContent);
    return labels;
}

function get_gradient() {
    var gradient = chart.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(250,174,50,1)');   
    gradient.addColorStop(1, 'rgba(250,174,50,0)');
    return gradient;
}

function get_options() {
    options = {
      scales: {
        x: {
          grid: {
            display: false
            },
          display:false
        },
        y: {
          beginAtZero: true,
            grid: {
              display: false
            }
          }
      },
      plugins: {
        legend: {
          display: false
        }
      },
      fill :true
    }
    return options
}

new Chart(chart, {
    type: 'line',
    data: {
        labels: get_labels(),
        datasets: [{
        data: get_data(),
            backgroundColor: get_gradient(),
            borderColor: 'rgb(255, 10, 86,1)',
        }]
    },
    options: get_options()
});
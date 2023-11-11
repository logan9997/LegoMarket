function get_graph() {
    var graph = document.getElementById('graph');
    return graph
}

function get_data() {
    var data = JSON.parse(document.getElementById('graph-data').textContent);
    return data;
}

function get_labels() {
    var labels = JSON.parse(document.getElementById('graph-labels').textContent);
    return labels;
}

function get_gradient() {
    var gradient = graph.getContext('2d').createLinearGradient(0, 0, 0, 400);
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

new Chart(graph, {
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
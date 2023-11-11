class CreateChart {
	get_canvas() {
		let chart_id = JSON.parse(document.getElementById('chart-id').textContent)
		let chart = document.getElementById(chart_id);
		return chart
	}

	get_data() {
		let data = JSON.parse(document.getElementById('chart-data').textContent);
		return data;
	}

	get_labels() {
		let labels = JSON.parse(document.getElementById('chart-labels').textContent);
		return labels;
	}

	get_gradient() {
		let gradient = this.get_canvas().getContext('2d').createLinearGradient(0, 0, 0, 400);
		gradient.addColorStop(0, 'rgba(250,174,50,1)');   
		gradient.addColorStop(1, 'rgba(250,174,50,0)');
		return gradient;
	}

	get_options() {
		let options = {
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

	create_chart() {
		new Chart(this.get_canvas(), {
			type: 'line',
			data: {
				labels: this.get_labels(),
				datasets: [{
				data: this.get_data(),
					backgroundColor: this.get_gradient(),
					borderColor: 'rgb(255, 10, 86,1)',
				}]
			},
			options: this.get_options()
		});
	}
}
class UpdateMetric {

	constructor() {
		let chart = new CreateChart
		this.data = chart.get_data()
		this.dates = chart.get_labels()
		this.current_metric = document.getElementById('current-metric')
		this.current_date = document.getElementById('current-date')
		this.metric_select = new URLSearchParams(window.location.search).get('metric_select')
	}

	get_current_metric(current_metric) {
		if (this.metric_select.includes('price')) {
			current_metric = `£${current_metric}` 
		}
		return current_metric
}


	update_hovered_metric(index) {
		this.current_metric.innerText = this.get_current_metric(this.data[index])
		this.current_date.innerText = this.dates[index]
	}

	reset_hovered_metric() {
		this.current_metric.innerText = this.get_current_metric(this.data[this.data.length-1])
		this.current_date.innerText = ''
	}
}

class CreateChart {

	constructor() {
		this.is_hovered = true
		this.set_mouseout_listener()
	}

	get_canvas() {
		let chart_id = JSON.parse(document.getElementById('chart-id').textContent)
		let chart = document.getElementById(chart_id);
		return chart
	}

	set_mouseout_listener() {
		let chart = this.get_canvas()
		chart.addEventListener('mouseout', (e) => {
			if (this.is_hovered) {
				let update_metric = new UpdateMetric()
				update_metric.reset_hovered_metric()   
				this.is_hovered = false
			}
		})
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
					position: 'right',
					grid: {
						display: false
					},
				},
			},
			plugins: {
				legend: {
					display: false
				}
			},
			fill :true,
			hover: {
				intersect: false
			},
			onHover: function (event, chartElement) {
				if (chartElement.length > 0) {
					var index = chartElement[0].index;
					let update_metric = new UpdateMetric()
					update_metric.update_hovered_metric(index)
					this.is_hovered = true
				}
            },
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
					pointRadius: 0,
  				    pointBorderColor: 'rgba(0, 0, 0, 0)',
					pointBackgroundColor: 'rgba(0, 0, 0, 0)',
			  		pointHoverBackgroundColor: 'rgb(255, 99, 132)',
  					pointHoverBorderColor: 'rgb(255, 99, 132)'
				}]
			},
			options: this.get_options()
		});
	}
}
class UpdateMetric {

	constructor() {
		let chart = new CreateChart
		this.data = chart.get_data()
		this.dates = chart.get_labels()
		this.current_metric = document.getElementById('current-metric')
		this.current_date = document.getElementById('current-date')
		this.metric_difference = document.getElementById('metric-difference')
		this.metric_percentage_difference = document.getElementById('metric-percentage-difference')		
		this.metric_select = this.get_metric_select()
		this.end_index = this.data.length-1

	}

	get_metric_select() {
		let metric_select = new URLSearchParams(window.location.search).get('metric_select')
		if (metric_select == null) {
			return 'price_new'
		}
		return metric_select
	}

	get_current_metric(current_metric) {
		if (this.metric_select.includes('price')) {
			current_metric = `£${current_metric}` 
		}
		return current_metric
	}

	get_metric_difference(index) {
		let difference = this.add_sign(this.data[index] - this.data[0])
		difference = Math.round(difference * 100) / 100
		return this.zero_pad(difference)
	}

	zero_pad(number) {
		number = String(number)
		if (!number.includes('.')) {
			return number
		}

		let remove_chars = ['(', ')', '%']
		for (let i = 0; i < remove_chars.length; i ++) {
			if (number.includes(remove_chars[i])) {
				number = number.replace(remove_chars[i], '')
			}
		}

		let number_split = number.split('.')
		let int = number_split[0]
		let decimal = number_split[1]
		if (decimal.length == 1) {
			decimal = `${decimal}0`
		}
		return `${int}.${decimal}`
	}

	get_metric_percentage_difference(index) {
		let hovered_metric = this.data[index]
		if (hovered_metric == 0) {
			return 100
		}
		let percentage_difference = (hovered_metric - this.data[0]) / hovered_metric * 100
		percentage_difference = Math.round(percentage_difference * 100) / 100
		percentage_difference =  `(${this.add_sign(percentage_difference)}%)`
		return this.zero_pad(percentage_difference)
	}

	add_sign(number) {
		if (number >= 0) {
			return `+${number}`
		}
		return number
	}

	set_colour(element, current_metric_value, oldest_metric_value) {
		if (current_metric_value >= oldest_metric_value) {
			element.style.color = 'green';
		} else {
			element.style.color = 'red';
		} 
	}

	update_hovered_metric(index) {
		this.current_metric.innerText = this.get_current_metric(this.data[index])
		this.current_date.innerText = this.dates[index]
		this.metric_difference.innerText = this.get_metric_difference(index)
		this.metric_percentage_difference.innerText = this.get_metric_percentage_difference(index)

		this.set_colour(this.current_metric, this.data[index], this.data[0])
		this.set_colour(this.metric_difference, this.data[index], this.data[0])
		this.set_colour(this.metric_percentage_difference, this.data[index], this.data[0])

	}

	reset_hovered_metric() {
		this.current_metric.innerText = this.get_current_metric(this.data[this.end_index])
		this.current_date.innerText = ''
		this.metric_difference.innerText = this.get_metric_difference(this.end_index)
		this.metric_percentage_difference.innerText = this.get_metric_percentage_difference(this.end_index) 

		this.set_colour(this.current_metric, this.data[this.end_index], this.data[0])
		this.set_colour(this.metric_difference, this.data[this.end_index], this.data[0])
		this.set_colour(this.metric_percentage_difference, this.data[this.end_index], this.data[0])

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
		chart.addEventListener('mouseout', () => {
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

	get_min_value(iterable) {
		let min = 9999999
		for (let i = 0; i < iterable.length; i ++) {
			if (iterable[i] < min) {
				min = iterable[i]
			}
		}
		console.log(min)
		return min
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
					min: this.get_min_value(this.get_data())
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
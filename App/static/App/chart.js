class UpdateChartMetrics {

    constructor() {
		this.current_metric_name = document.getElementById('current-metric-name').innerHTML
        this.current_metric = document.getElementById('current-metric')
        this.metric_difference = document.getElementById('metric-difference')
        this.metric_percentage_difference = document.getElementById('metric-percentage-difference')
        this.current_date = document.getElementById('current-date')
    }

	add_currency_sign(number) {
        if (number >= 0) {
            number = `+£${number}`
        } else {
            number = `-£${Math.abs(number)}`
        }
        return number
	}

	add_sign(number) {
		if (number >= 0) {
			number = `+${number}`
		} 
		return number
	}

	zero_pad(number) {
		let number_string = number.toString()
		if (number_string.includes('.')) {
			let integer = number_string.split('.')[0]
			let decimal = number_string.split('.')[1]
			if (decimal.length != 2) {
				decimal = `${decimal}0`
			}
			number = `${integer}.${decimal}`
		}
		return number
	}

	remove_decimal(number) {
		let number_string = number.toString()
		if (number_string.includes('.')) {
			let integer = number_string.split('.')[0]
			number = parseInt(integer, 10)
		}
		return number
	}

	set_colour(number, element) {
		if (number >= 0) {
			element.style.color = 'green'
		} else {
			element.style.color = 'red'
		}
	}

    set_current_metric(earliest_metric, current_metric) {
		if (this.current_metric_name.includes('Price')) {
        	this.current_metric.innerHTML = `£${this.zero_pad(current_metric)}`
		} else {
			this.current_metric.innerHTML = current_metric
		}
		let metric_difference = current_metric - earliest_metric
		this.set_colour(metric_difference, this.current_metric)
		this.set_colour(metric_difference, this.metric_difference)
    }

	get_metric_difference(earliest, oldest) {
		let metric_difference = oldest - earliest
		metric_difference = metric_difference.toFixed(2)
		if (this.current_metric_name.includes('Price')) {
			metric_difference = this.add_currency_sign(metric_difference)
			metric_difference = this.zero_pad(metric_difference)
		} else {
			metric_difference = this.remove_decimal(metric_difference)
			metric_difference = this.add_sign(metric_difference)
		}
		return metric_difference
	}

    set_metric_difference(metric_difference) {
		this.metric_difference.innerHTML = metric_difference
    }

	get_metric_percentage_difference(earliest, latest) {
		console.log(earliest, latest)
		let metric_percentage_difference = 0
		if (earliest != latest) {
			if (earliest == 0) {
				return 100
			}
	        metric_percentage_difference = (earliest - latest) / earliest * -100
		}
		return metric_percentage_difference
	}

    set_metric_percentage_difference(metric_percentage_difference) {
		this.set_colour(metric_percentage_difference, this.metric_percentage_difference)
        metric_percentage_difference = `(${this.add_sign(metric_percentage_difference.toFixed(2))}%)`
        this.metric_percentage_difference.innerHTML = metric_percentage_difference
    }

	set_current_date(date) {
		this.current_date.innerHTML = date 
	}

}

class CreateChart {

	constructor() {
		this.data = this.get_data()
		this.labels = this.get_labels()
		this.set_mouseout_listener()
		this.set_initial_metric_colours()
		this.set_metric_values(this.data.length - 1)
	}

	set_metric_values(index) {
		let update_chart_metrics = new UpdateChartMetrics()
		update_chart_metrics.set_current_metric(this.data[0], this.data[index])

		let metric_difference = update_chart_metrics.get_metric_difference(this.data[0], this.data[index])
		update_chart_metrics.set_metric_difference(metric_difference)

		let metric_percentage_difference = update_chart_metrics.get_metric_percentage_difference(this.data[0], this.data[index])
		update_chart_metrics.set_metric_percentage_difference(metric_percentage_difference)

		update_chart_metrics.set_current_date(this.labels[index])

	}

	set_initial_metric_colours() {
		const remove_chars = ['(', ')', '%', '+']
		let update_chart_metrics = new UpdateChartMetrics()

		let elemets_colours_to_set = [
			update_chart_metrics.current_metric, 
			update_chart_metrics.metric_difference, 
			update_chart_metrics.metric_percentage_difference
		]
		for (let i = 0; i < 3; i ++) {
			let value = elemets_colours_to_set[i].innerHTML
			for (let j = 0; j < value.length; j ++) {
				if (remove_chars.includes(value[j])) {
					value = value.replace(value[j], '')
				}
				value = parseFloat(value)
				if (value >= 0) {
					elemets_colours_to_set[i].style.color = 'green'
				} else {
					elemets_colours_to_set[i].style.color = 'red'
				}
			}
		}
	}

	get_canvas() {
		let chart_id = 'chart-canvas'
		let chart = document.getElementById(chart_id);
		return chart
	}

	set_mouseout_listener() {
		let chart = this.get_canvas()
		chart.addEventListener('mouseout', () => {
			let data = this.data
			let index = data.length - 1
			this.set_metric_values(index)			
		})
	}

	get_data() {
		let data = document.getElementById('chart-data').textContent
		data = JSON.parse(data);
		return data;
	}

	get_labels() {
		let labels = document.getElementById('chart-labels').textContent
		labels = JSON.parse(labels);
		return labels;
	}

	get_gradient() {
		let gradient = this.get_canvas().getContext('2d').createLinearGradient(0, 0, 0, 400);
		gradient.addColorStop(0, 'rgba(250,174,50,1)');   
		gradient.addColorStop(1, 'rgba(250,174,50,0)');
		return gradient;
	}

	get_min_value(iterable) {
		let min = iterable[0]
		for (let i = 1; i < iterable.length; i ++) {
			if (iterable[i] < min) {
				min = iterable[i]
			}
		}
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
					min: this.get_min_value(this.data)
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
					let index = chartElement[0].index;
					new CreateChart().set_metric_values(index)
				}
            },
		}
		return options
	}

	create_chart() {
		return new Chart(this.get_canvas(), {
			type: 'line',
			data: {
				labels: this.get_labels(),
				datasets: [{
					data: this.data,
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
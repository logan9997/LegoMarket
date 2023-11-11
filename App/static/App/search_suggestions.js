class SearchSuggestions {
    constructor() {
        this.search_suggestions_container = document.getElementById('search-suggestions-container')
    }

    show_search_suggestions() {
        this.clear_search_suggestions()

        const max_matches = 12
        var matches = 0
        var input = document.getElementById('id_search_value')
        var input_value = input.value.toLowerCase()
        var item_names = JSON.parse(document.getElementById('item-names').textContent)
        var item_ids = JSON.parse(document.getElementById('item-ids').textContent)

        if (input_value.length >= 3) {
            for (let i = 0; i < item_ids.length; i++) {
                if (item_names[i].toLowerCase().includes(input_value) || item_ids[i].toLowerCase().includes(input_value)) {
                    matches += 1
                    var search_suggestion = this.get_search_suggestion_html(item_ids[i], item_names[i]) 
                    this.search_suggestions_container.appendChild(search_suggestion)
                    if (matches >= max_matches) {
                        break
                    }
                }
            }
        }
    }

    get_search_suggestion_html(item_id, item_name) {
        var container = document.createElement('div');
        var html = `
        <h3>${item_id}</h3>
        <span>${item_name}</span>
        <img src="img_path" alt="?">
        `
        container.innerHTML = html
        return container
    }

    clear_search_suggestions() {
        this.search_suggestions_container.innerHTML = ''
    }
}
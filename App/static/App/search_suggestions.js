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
        if (matches == 0) {
            this.search_suggestions_container.style.visibility = 'hidden'
        }
    }

    get_search_suggestion_html(item_id, item_name) {
        var container = document.createElement('div');
        container.setAttribute('width', '10rem')
        var img_path = window.location.origin + `/static/App/images/${item_id}.png`
        var item_path = window.location.origin + `/item/${item_id}/`
        var html = `
        <div class="search-suggestion">
            <img src="${img_path}">
            <div class="item-name-item-id-container">
                <span class="item-name">${item_name}</span>
                <a href="${item_path}" class="item-id">${item_id}</a>
            </div>
        </div>
        `
        container.innerHTML = html
        return container
    }

    clear_search_suggestions() {
        this.search_suggestions_container.innerHTML = ''
    }
}
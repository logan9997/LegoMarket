class SearchSuggestions {
    constructor() {
        this.search_suggestions_container = document.getElementById('search-suggestions-container')
        this.form = document.getElementById('item-search-form')
        this.input = document.getElementById('id_search_value')
        
        this.item_names = JSON.parse(document.getElementById('item-names').textContent)
        this.item_ids = JSON.parse(document.getElementById('item-ids').textContent)
    }

    show_search_suggestions() {
        this.clear_search_suggestions()
        this.input_value = this.input.value.toLowerCase()

        const max_matches = 12
        var matches = 0

        if (this.input_value.length >= 3) {
            for (let i = 0; i < this.item_ids.length; i++) {
                if (this.item_names[i].toLowerCase().includes(this.input_value) || this.item_ids[i].toLowerCase().includes(this.input_value)) {
                    matches += 1
                    console.log('new match', this.item_ids[i])
                    var search_suggestion = this.get_search_suggestion_html(this.item_ids[i], this.item_names[i]) 
                    this.search_suggestions_container.appendChild(search_suggestion)
                    if (matches >= max_matches) {
                        break
                    }
                }
            }
        }
        this.set_search_suggestions_visibility(matches)
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

    set_search_suggestions_visibility(matches) {
        this.search_suggestions_container.style.visibility = 'visible'
        if (matches == 0) {
            this.search_suggestions_container.style.visibility = 'hidden'
        }
    }
}
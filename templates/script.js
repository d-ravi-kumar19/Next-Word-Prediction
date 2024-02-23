
const search_input = document.getElementById('search_text');
const suggestions = document.getElementById('suggestions');
let selectedIndex = -1;

function showSuggestions() {
    const searchText = search_input.value.toLowerCase();
    while (suggestions.firstChild) {
        suggestions.removeChild(suggestions.firstChild);
    }

    if (searchText.trim() === '') {
        suggestions.style.display = 'none';
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'search_text=' + encodeURIComponent(searchText)
    })
        .then(response => response.json())
        .then(matchingWords => {
            if (matchingWords.length > 0) {
                matchingWords.forEach((word, index) => {
                    const suggestion = document.createElement('div');
                    suggestion.textContent = word;
                    suggestion.onclick = function () {
                        selectSuggestion(index);
                    };
                    suggestion.style.cursor = 'pointer';
                    suggestions.appendChild(suggestion);
                });
                selectedIndex = -1;
                suggestions.style.display = 'block';
            } else {
                selectedIndex = -1;
                suggestions.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function selectSuggestion(index) {
    selectedIndex = index;
    search_input.value = suggestions.childNodes[index].textContent;
    suggestions.style.display = 'none';
}

function handleArrowKeys(event) {
    const key = event.key;
    if (key === 'ArrowUp') {
        event.preventDefault();
        if (selectedIndex > 0) {
            selectedIndex--;
            highlightSuggestion();
        }
    } else if (key === 'ArrowDown') {
        event.preventDefault();
        if (selectedIndex < suggestions.childNodes.length - 1) {
            selectedIndex++;
            highlightSuggestion();
        }
    } else if (key === 'Enter') {
        event.preventDefault();
        if (selectedIndex !== -1) {
            selectSuggestion(selectedIndex);
        }
    }
}

function highlightSuggestion() {
    for (let i = 0; i < suggestions.childNodes.length; i++) {
        if (i === selectedIndex) {
            suggestions.childNodes[i].style.backgroundColor = '#ddd';
        } else {
            suggestions.childNodes[i].style.backgroundColor = 'transparent';
        }
    }
}

search_input.addEventListener('keyup', showSuggestions);
document.addEventListener('keydown', handleArrowKeys);


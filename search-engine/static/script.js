document.getElementById('advancedSearchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const searchParams = new URLSearchParams();
    for (const pair of formData.entries()) {
        searchParams.append(pair[0], pair[1]);
    }
    fetch('/search', {
        method: 'POST',
        body: searchParams,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Handle response data
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function addSearchRow() {
    const searchRow = document.createElement('div');
    searchRow.className = 'search-row';
    searchRow.innerHTML = `
        <select name="operator[]">
            <option value="AND">AND</option>
            <option value="OR">OR</option>
            <option value="NOT">NOT</option>
        </select>
        <input type="text" name="searchTerm[]" placeholder="Search Term">
        <span class="in-label">in</span>
        <select name="metadata[]">
            <option value="title">Title</option>
            <option value="Publisher">Publisher</option>
            <option value="abstract">Abstract</option>
            <option value="Published in">Published in</option>
            <option value="Authors">Authors</option>
            <option value="IEEE Keywords">IEEE Keywords</option>
            <option value="Author Keywords">Author Keywords</option>
        </select>
    `;
    document.getElementById('advancedSearchForm').insertBefore(searchRow, document.querySelector('.buttons'));
}

function removeSearchRow() {
    const searchRows = document.querySelectorAll('.search-row');
    if (searchRows.length > 1) {
        searchRows[searchRows.length - 1].remove();
    }
}

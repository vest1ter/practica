document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const showResultsBtn = document.getElementById('showResultsBtn');
    const resultsCount = document.getElementById('resultsCount');
    const resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];

    let searchResults = [];

    searchBtn.addEventListener('click', () => {
        const position_name = document.getElementById('position_name').value;
        const employment = document.getElementById('employment').value;
        const experience = document.getElementById('experience').value;
        const city = document.getElementById('city').value;

        showResultsBtn.style.display = 'none';
        resultsTable.innerHTML = '';

        const requestData = {
            position_name: position_name || null,
            employment: employment || null,
            experience: experience ? parseInt(experience) : null,
            city: city || null
        };

        fetch('http://127.0.0.1:8000/count/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(count => {
            resultsCount.textContent = `Found ${count} results.`;
            if (count > 0) {
                showResultsBtn.style.display = 'block';
                searchResults = requestData;
            } else {
                showResultsBtn.style.display = 'none';
                resultsTable.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Error fetching count:', error);
            resultsCount.textContent = 'Uncorrect input or server error.';
            showResultsBtn.style.display = 'none';
            resultsTable.innerHTML = '';
        });
    });

    showResultsBtn.addEventListener('click', () => {
        fetch('http://127.0.0.1:8000/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(searchResults)
        })
        .then(response => response.json())
        .then(data => {
            resultsTable.innerHTML = '';
            data.forEach(item => {
                const row = resultsTable.insertRow();
                const cellId = row.insertCell(0);
                const cellName = row.insertCell(1);
                const cellDescription = row.insertCell(2);
                cellId.textContent = item.position_name;
                cellName.textContent = item.company_name;
                cellDescription.textContent = item.offer_link;
            });
            resultsTable.parentElement.style.display = 'table';
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    });
});

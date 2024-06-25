document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const searchBtn = document.getElementById('searchBtn');
    const showResultsBtn = document.getElementById('showResultsBtn');
    const resultsCount = document.getElementById('resultsCount');
    const resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];

    let searchResults = [];

    searchBtn.addEventListener('click', () => {
        const position_name = document.getElementById('position_name').value;
        const skills = document.getElementById('skills').value;
        const experience = document.getElementById('experience').value;

        const requestData = {
            position_name: position_name || null,
            skills: skills || null,
            experience: experience ? parseInt(experience) : null
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
            resultsCount.textContent = 'Error fetching count.';
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
                cellId.textContent = item.id;
                cellName.textContent = item.name;
                cellDescription.textContent = item.description;
            });
            resultsTable.parentElement.style.display = 'table';
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    });
});

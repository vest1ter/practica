document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const searchBtn = document.getElementById('searchBtn');
    const showResultsBtn = document.getElementById('showResultsBtn');
    const resultsCount = document.getElementById('resultsCount');
    const resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];

    let searchResults = [];

    searchBtn.addEventListener('click', () => {
        const position_name = document.getElementById('position_name').value;
        const city = document.getElementById('city').value;
        const employment = document.getElementById('employment').value;
        const experience = document.getElementById('experience').value;

        showResultsBtn.style.display = 'none';
        resultsTable.innerHTML = '';

        const requestData = {
            position_name: position_name || null,
            city: city || null,
            employment: employment || null,
            experience: experience ? parseInt(experience) : null
        };

        fetch('http://localhost:8000/count/', {
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
            resultsCount.textContent = 'Ошибка ввода, убедитесь что название города приведено на русском языке и все поля зполнены';
            showResultsBtn.style.display = 'none';
            resultsTable.innerHTML = '';
        });
    });

    showResultsBtn.addEventListener('click', () => {
        fetch('http://localhost:8000/search/', {
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
                const cellName = row.insertCell(0);
                const cellCompany = row.insertCell(1);
                const cellSalary = row.insertCell(2);
                const cellLink = row.insertCell(3);
                cellName.textContent = item.position_name;
                cellCompany.textContent = item.company_name;
                cellSalary.textContent = item.salary;
                cellLink.innerHTML = `<a href="${item.offer_link}" target="_blank">Ссылка на вакансию</a>`;
            });
            resultsTable.parentElement.style.display = 'table';
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    });
});

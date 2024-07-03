// app_page2.js

document.addEventListener('DOMContentLoaded', () => {
    const allVacanciesTable = document.getElementById('allVacanciesTable');

    // Проверяем наличие элемента на странице
    if (!allVacanciesTable) {
        console.error('Required element not found on the page.');
        return;
    }

    fetch('http://localhost:8000/vacancies')
        .then(response => response.json())
        .then(data => {
            allVacanciesTable.innerHTML = ''; // Очищаем таблицу перед добавлением новых данных
            data.forEach(item => {
                const row = allVacanciesTable.insertRow();
                const cellName = row.insertCell(0);
                const cellCompany = row.insertCell(1);
                const cellSalary = row.insertCell(2);
                const cellLink = row.insertCell(3);
                cellName.textContent = item.position_name;
                cellCompany.textContent = item.company_name;
                cellSalary.textContent = item.salary;
                cellLink.innerHTML = `<a href="${item.offer_link}" target="_blank">Ссылка на вакансию</a>`;
            });
            allVacanciesTable.parentElement.style.display = 'table';
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

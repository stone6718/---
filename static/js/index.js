function appendToResult(value) {
    document.getElementById('result').value += value;
}

function clearResult() {
    document.getElementById('result').value = '';
}

function calculate() {
    const expression = document.getElementById('result').value;
    const result = eval(expression);
    document.getElementById('result').value = result;
    saveToDatabase(expression, result);
}

function toggleDarkMode() {
    const body = document.body;
    const button = document.getElementById('darkModeButton');
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        button.textContent = '화이트 모드';
    } else {
        button.textContent = '다크 모드';
    }
}

function saveToDatabase(expression, result) {
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression: expression, result: result })
    });
}

function fetchRecords() {
    fetch('/records')
        .then(response => response.json())
        .then(data => {
            const recordsDiv = document.getElementById('records');
            recordsDiv.innerHTML = '';
            data.forEach(record => {
                recordsDiv.innerHTML += `<p>${record[0]} = ${record[1]}</p>`;
            });
            openPopup();
        });
}

function openPopup() {
    document.getElementById('popup').style.display = 'block';
    document.getElementById('popupOverlay').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
    document.getElementById('popupOverlay').style.display = 'none';
}
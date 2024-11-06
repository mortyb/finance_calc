document.getElementById("finance-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const category = document.getElementById("category").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const record_type = document.getElementById("record_type").value;

    const response = await fetch("/add_record/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ category, amount, record_type }),
    });

    if (response.ok) {
        alert("Запись успешно добавлена!");
        fetchRecords();  // Обновление истории
        fetchBalance();  // Обновление баланса после добавления новой записи
    } else {
        alert("Ошибка при добавлении записи");
    }
});

async function fetchRecords() {
    const response = await fetch("/records/");
    const records = await response.json();
    const recordsDiv = document.getElementById("records");
    recordsDiv.innerHTML = "";

    records.forEach(record => {
        const recordDiv = document.createElement("div");
        recordDiv.textContent = `${record.record_type}: ${record.category} - $${record.amount}`;
        recordsDiv.appendChild(recordDiv);
    });
}

// Функция для получения текущего баланса
async function fetchBalance() {
    const response = await fetch("/balance/");
    const data = await response.json();
    const balanceElement = document.getElementById("balance");
    balanceElement.textContent = `$${data.balance.toFixed(2)}`;
}

// Загружаем записи и баланс при загрузке страницы
window.onload = function() {
    fetchRecords();
    fetchBalance();
};

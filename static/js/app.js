function addRow() {
    let table = document.querySelector("#studentTable tbody");
    let count = table.rows.length + 1;

    let row = document.createElement("tr");

    row.innerHTML = `
    <td class="serial">${count}</td>
    <td><input name="name[]" required></td>
    <td><input name="attended[]" type="number" oninput="calculate(this)" required></td>
    <td><span class="percent">0%</span></td>
    <td><button type="button" class="delete-btn" onclick="deleteRow(this)">❌</button></td>
    `;

    table.appendChild(row);
}

function deleteRow(btn) {
    btn.closest("tr").remove();
    updateSerial();
}

function updateSerial() {
    document.querySelectorAll(".serial").forEach((el, i) => {
        el.innerText = i + 1;
    });
}

function calculate(el) {
    let total = document.getElementById("totalClasses").value;
    let attended = el.value;

    if (attended > total) {
        alert("Invalid input!");
        el.value = "";
        return;
    }

    let percent = total > 0 ? (attended / total) * 100 : 0;
    el.closest("tr").querySelector(".percent").innerText = percent.toFixed(1) + "%";
}

function updateAll() {
    document.querySelectorAll('input[name="attended[]"]').forEach(el => calculate(el));
}

function toggleMode() {
    document.body.classList.toggle("light-mode");
}

function loading(btn) {
    btn.classList.add("loading");
}
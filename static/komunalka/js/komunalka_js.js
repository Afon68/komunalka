function convertISOToLocal(isoString) {
const date = new Date(isoString);
const dateEntry = date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'

});
return dateEntry.replace(",", ".")
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".utc-date").forEach(function (el) {
        console.log("Скрипт загружен!");
        const iso = el.textContent.trim();
        // Защита от пустых или неверных строк
        if (iso && !isNaN(Date.parse(iso))) {
            el.textContent = convertISOToLocal(iso);
        }
    });
});

// document.addEventListener("DOMContentLoaded", function () {
    function toggleSection(checkboxId, sectionId) {
        const checkbox = document.getElementById(checkboxId);
        const section = document.getElementById(sectionId);
            console.log("Код загружен!");
        checkbox.addEventListener('change', () => {
            section.classList.toggle('hidden', !checkbox.checked);
        });
        // Показывать при начальной загрузке, если галочка уже стоит
        section.classList.toggle('hidden', !checkbox.checked);
    }

    toggleSection('id_has_gas_checkbox', 'gas-options');
    toggleSection('id_has_water_checkbox', 'water-options');
    toggleSection('id_has_water_checkbox', 'hot_section');
    toggleSection('id_has_hot_water_checkbox', 'hot_water-options');
    toggleSection('id_has_electricity_checkbox', 'electrika-options');

// })
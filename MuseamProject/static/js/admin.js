// Обработчик событий для всех ссылок боковой панели
document.querySelectorAll('.sidebar a').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        
        // Получаем ID содержимого, связанного с ссылкой
        const id = this.getAttribute('href').substring(1);
        
        // Скрываем все страницы контента
        document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');
        
        // Показываем выбранную страницу
        document.getElementById(id).style.display = 'block';
        
        // Скрываем приветственные сообщения
        document.getElementById('welcome-message').style.display = 'none';
        document.getElementById('welcome-text').style.display = 'none';
        document.getElementById('welcome-message-admin').style.display = 'none';
    });
});

// Функция для редактирования сотрудника
function editEmployee(id) {
    // Код для редактирования информации о сотруднике
    // Например, заполняем форму данными сотрудника для редактирования
    alert("Редактировать сотрудника с ID: " + id);
}

// Функция для удаления сотрудника
function deleteEmployee(id) {
    // Подтверждение удаления сотрудника
    if (confirm("Вы уверены, что хотите удалить сотрудника с ID: " + id + "?")) {
        // Выполните запрос на удаление
        alert("Сотрудник с ID " + id + " удален.");
    }
}

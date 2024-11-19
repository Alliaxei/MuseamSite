document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            // Получаем ID содержимого, связанного со ссылкой
            const id = this.getAttribute('href').substring(1);

            // Скрываем все страницы контента
            document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');

            // Показываем выбранную страницу
            document.getElementById(id).style.display = 'block';

            // Скрываем приветственные сообщения
            document.getElementById('welcome-message').style.display = 'none';
            document.getElementById('welcome-text').style.display = 'none';

        });
    });
});

function updateEmployeeTable(data) {
    if (data.success) {
            document.getElementById('employee_table_body').innerHTML = data.table_html;

            document.querySelectorAll('#employee_table_body form').forEach(form => {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);
            })

            document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');
            document.getElementById('employees').style.display = 'block';
            closeEmployeeModal();
            document.getElementById('employee-form').reset();
        } else if (data.error) {
            alert("Ошибка " + data.error);
        }
}
function updateExhibitionTable(data) {
    if (data.success) {
        document.getElementById('exhibit_table_body').innerHTML  = data.exhibit_table_html;

        document.querySelectorAll('#exhibition_table_body form').forEach(form => {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
        })
        document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');
        document.getElementById('exhibits').style.display = 'block';
        closeExhibitionModal();
        document.getElementById('exhibition-form').reset();
    } else if (data.error) {
        alert("Ошибка " + data.error);
    }
}
function updateHallTable(data) {
    if (data.success) {
        document.getElementById('hall_table_body').innerHTML = data.hall_table_html;

        document.querySelectorAll('#hall_table_body form').forEach(form => {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
        })
        document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');
        document.getElementById('halls').style.display = 'block';
        closeHallModal();
        document.getElementById('hall-form').reset();
    } else if (data.error) {
        alert("Ошибка " + data.error);
    }
}
function updateReportTable(data) {
    if (data.success) {
        document.getElementById('report_table_body').innerHTML = data.report_table_html;

        document.querySelectorAll('#report_table_body form').forEach(form => {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
        })
        document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');
        document.getElementById('reports').style.display = 'block';
    } else if (data.error) {
        alert("Ошибка " + data.error)
    }
}
document.getElementById('hall-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => updateHallTable(data))
    .catch((error) => console.log(error));
})
document.getElementById('hall_table_body').addEventListener('submit', function(e) {
      if (e.target && e.target.matches('#hall-form-delete')) {
        e.preventDefault();
        const formData = new FormData(e.target);

        fetch(e.target.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => updateHallTable(data))
        .catch(error => console.log(error));
    }
})
document.getElementById('hall-edit-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateHallTable(data);
                closeHallModalEdit();
            } else if (data.error) {
                alert("Ошибка: " + data.error);
            }
        })
        .catch((error) => console.log(error));
})

document.getElementById('exhibition-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => updateExhibitionTable(data))
    .catch((error) => console.log(error));
})
document.getElementById('exhibition-form-edit').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateExhibitionTable(data);
                closeExhibitionModalEdit();
            } else if (data.error) {
                alert("Ошибка: " + data.error);
            }
        })
        .catch((error) => console.log(error));
})
document.getElementById('exhibit_table_body').addEventListener('submit', function(e) {
    if (e.target && e.target.matches('#exhibit-form-delete')) {
        e.preventDefault();
        const formData = new FormData(e.target);

        fetch(e.target.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => updateExhibitionTable(data))
        .catch(error => console.log(error));
    }
});

document.getElementById('employee_table_body').addEventListener('submit', function(e) {
      if (e.target && e.target.matches('#employee-form-delete')) { // реагирует только на формы удаления
            e.preventDefault();
            const formData = new FormData(e.target); // создается объект formData, который собирает данные с формы

            fetch(e.target.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // для указания, что запрос исходит от AJAX
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => updateEmployeeTable(data))
            .catch(error => console.error("Ошибка при удалении сотрудника:", error));
        }
    });
document.getElementById('employee-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => updateEmployeeTable(data))
    .catch(error => console.error("Ошибка " + error));
});
document.getElementById('employee-form-edit').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateEmployeeTable(data);
                closeEmployeeModalEdit();
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch((error) => console.log(error));
})

document.getElementById('report_table_body').addEventListener('submit', function(e) {
    if (e.target && e.target.matches('#report-form-delete')) {
        e.preventDefault();
        const formData = new FormData(e.target);
        fetch(e.target.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                 'X-CSRFToken': csrfToken
            }
        })
            .then(response => response.json())
            .then(data => updateReportTable(data))
            .catch(error => console.log(error));
    }

})

function openEmployeeModal() {
    document.getElementById('employeeModal').style.display = 'flex';
}
function closeEmployeeModal() {
    document.getElementById('employeeModal').style.display = 'none';
}
function openEmployeeModalEdit() {
    document.getElementById('employeeModalEdit').style.display = 'flex';
}
function closeEmployeeModalEdit() {
    document.getElementById('employeeModalEdit').style.display = 'none';
}
function editEmployeeModal(employee_id) {
    console.log("Вызов editEmployeeModal");
    fetch(`/getEmployeeData/${employee_id}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('employee_name_edit').value = data.name;
                document.getElementById('employee_login_edit').value = data.login;
                document.getElementById('employee_email_edit').value = data.email;

                document.getElementById('employee-form-edit').querySelector('input[name="employee_id"]').value = data.id;
                document.getElementById('employee-form-edit').action = `/editEmployee/${employee_id}/`;
                openEmployeeModalEdit();
            }
        })
        .catch((error) => console.log(error));
}

function openExhibitionModal() {
    document.getElementById('exhibitionModal').style.display = 'flex';
}
function openExhibitionModalEdit() {
    document.getElementById('exhibitionModalEdit').style.display = 'flex';
}
function closeExhibitionModalEdit() {
    document.getElementById('exhibitionModalEdit').style.display = 'none';
}
function closeExhibitionModal() {
    document.getElementById('exhibitionModal').style.display = 'none';
}
function editExhibitionModal(exhibit_id) {
    fetch(`/getExhibitData/${exhibit_id}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('name_edit').value = data.name;
            document.getElementById('author_edit').value = data.author;
            document.getElementById('origin_edit').value = data.origin;
            document.getElementById('quantity_edit').value = data.quantity;
            document.getElementById('category_edit').value = data.category;
            document.getElementById('history_edit').value = data.history;
            document.getElementById('condition_edit').value = data.condition;

            const hallSelect = document.getElementById('hall_edit');
            for (let option of hallSelect.options) {
                if (option.text == String(data.hall)) {
                    option.selected = true;
                    break;
                }
            }

            document.getElementById('exhibition-form-edit').querySelector('input[name="exhibit_id"]').value = data.id;
            document.getElementById('exhibition-form-edit').action = `/editExhibition/${exhibit_id}/`;

            openExhibitionModalEdit();
        })
        .catch(error => console.log(error));
}

function openHallModal() {
    document.getElementById('hallModal').style.display = 'flex';
}
function openHallModalEdit() {
    document.getElementById('hallModalEdit').style.display = 'flex';
}
function closeHallModalEdit() {
    document.getElementById('hallModalEdit').style.display = 'none';
}
function closeHallModal() {
    document.getElementById('hallModal').style.display = 'none';
}
function editHallModal(hall_id) {
    fetch(`/getHallData/${hall_id}/`,{
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('hall_number_edit').value = data.number;
            document.getElementById('hall_theme_edit').value = data.thematic;
            document.getElementById('hall-edit-form').querySelector('input[name="hall_id"]').value = data.id;

            document.getElementById('hall-edit-form').action = `/editHall/${hall_id}/`;

            openHallModalEdit();
        })
        .catch(error => console.log("Ошибка получения данных зала: ", error));
}

 document.getElementById('quantity').addEventListener('input', function (event) {
        const input = event.target;
        input.value = input.value.replace(/\D/g, '');
    });
 document.getElementById('quantity_edit').addEventListener('input', function (event) {
        const input = event.target;
        input.value = input.value.replace(/\D/g, '');
    });
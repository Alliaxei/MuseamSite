document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const id = this.getAttribute('href').substring(1);

            document.querySelectorAll('.content-page').forEach(page => page.style.display = 'none');
            document.getElementById(id).style.display = 'block';

            document.getElementById('welcome-message').style.display = 'none';
            document.getElementById('welcome-text').style.display = 'none';
        });
    });
});

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
        closeReportModal();
        document.getElementById('report-form').reset();
    } else if (data.error) {
        alert("Ошибка " + data.error)
    }
}

document.getElementById('report-form').addEventListener('submit', function(e) {
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
    .then(data => updateReportTable(data))
    .catch((error) => console.log(error));
})

function openReportModal() {
    document.getElementById('reportModal').style.display = 'flex';
}
function closeReportModal() {
    document.getElementById('reportModal').style.display = 'none';
}

function toggleAdditionalFields() {
    const reportType = document.getElementById('report_type').value;
    document.getElementById('hall-field').style.display = (reportType === 'by_hall') ? 'block' : 'none';
    document.getElementById('theme-field').style.display = (reportType === 'by_theme' || reportType === 'count_by_theme') ? 'block' : 'none';
}
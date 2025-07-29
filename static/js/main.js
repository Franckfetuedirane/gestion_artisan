// Main JavaScript file for Gestion Artisanale

document.addEventListener('DOMContentLoaded', function () {
    // Initialisation des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialisation des popovers Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Gestion des alertes auto-fermantes
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Animation des cartes au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .stats-card').forEach(card => {
        observer.observe(card);
    });

    // Gestion des formulaires de recherche
    const searchForms = document.querySelectorAll('.search-form form');
    searchForms.forEach(form => {
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', function () {
                form.submit();
            });
        });
    });

    // Mise à jour des statuts via AJAX
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function () {
            const url = this.dataset.url;
            const newStatus = this.value;
            const row = this.closest('tr');

            // Afficher un spinner
            const originalContent = this.innerHTML;
            this.innerHTML = '<div class="spinner"></div>';

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `statut=${newStatus}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Mettre à jour l'affichage
                        const badge = row.querySelector('.status-badge');
                        if (badge) {
                            badge.textContent = data.statut;
                            badge.className = `badge status-${newStatus}`;
                        }

                        // Afficher un message de succès
                        showNotification('Statut mis à jour avec succès', 'success');
                    } else {
                        showNotification('Erreur lors de la mise à jour', 'error');
                        this.value = this.dataset.originalValue;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('Erreur lors de la mise à jour', 'error');
                    this.value = this.dataset.originalValue;
                })
                .finally(() => {
                    this.innerHTML = originalContent;
                });
        });
    });

    // Fonction pour obtenir le cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Fonction pour afficher des notifications
    function showNotification(message, type = 'info') {
        const alertClass = type === 'error' ? 'alert-danger' :
            type === 'success' ? 'alert-success' : 'alert-info';

        const notification = document.createElement('div');
        notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-fermer après 3 secondes
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    // Gestion des graphiques (si Chart.js est disponible)
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }

    // Gestion des filtres de tableau
    const filterInputs = document.querySelectorAll('.table-filter');
    filterInputs.forEach(input => {
        input.addEventListener('keyup', function () {
            const filterValue = this.value.toLowerCase();
            const table = this.closest('.table-responsive').querySelector('table');
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(filterValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Gestion des modales de confirmation
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            const message = this.dataset.confirm;
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Gestion des formulaires avec validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showNotification('Veuillez remplir tous les champs obligatoires', 'error');
            }
        });
    });

    // Gestion des images de prévisualisation
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                const preview = this.parentNode.querySelector('.image-preview');

                if (preview) {
                    reader.onload = function (e) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    };
                    reader.readAsDataURL(file);
                }
            }
        });
    });

    // Gestion du calcul automatique des montants
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const priceInputs = document.querySelectorAll('.price-input');
    const totalInputs = document.querySelectorAll('.total-input');

    function calculateTotal() {
        quantityInputs.forEach((quantityInput, index) => {
            const priceInput = priceInputs[index];
            const totalInput = totalInputs[index];

            if (quantityInput && priceInput && totalInput) {
                const quantity = parseFloat(quantityInput.value) || 0;
                const price = parseFloat(priceInput.value) || 0;
                const total = quantity * price;
                totalInput.value = total.toFixed(2);
            }
        });
    }

    quantityInputs.forEach(input => {
        input.addEventListener('input', calculateTotal);
    });

    priceInputs.forEach(input => {
        input.addEventListener('input', calculateTotal);
    });

    // Gestion de la recherche en temps réel
    const searchInputs = document.querySelectorAll('.live-search');
    searchInputs.forEach(input => {
        let timeout;
        input.addEventListener('input', function () {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const searchValue = this.value.toLowerCase();
                const container = document.querySelector(this.dataset.target);

                if (container) {
                    const items = container.querySelectorAll('.searchable-item');
                    items.forEach(item => {
                        const text = item.textContent.toLowerCase();
                        if (text.includes(searchValue)) {
                            item.style.display = '';
                        } else {
                            item.style.display = 'none';
                        }
                    });
                }
            }, 300);
        });
    });
});

// Fonction pour initialiser les graphiques
function initializeCharts() {
    // Graphique des ventes (si l'élément existe)
    const salesChart = document.getElementById('salesChart');
    if (salesChart) {
        const ctx = salesChart.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: salesChart.dataset.labels ? JSON.parse(salesChart.dataset.labels) : [],
                datasets: [{
                    label: 'Ventes (€)',
                    data: salesChart.dataset.data ? JSON.parse(salesChart.dataset.data) : [],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Évolution des ventes'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Graphique des catégories (si l'élément existe)
    const categoryChart = document.getElementById('categoryChart');
    if (categoryChart) {
        const ctx = categoryChart.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: categoryChart.dataset.labels ? JSON.parse(categoryChart.dataset.labels) : [],
                datasets: [{
                    data: categoryChart.dataset.data ? JSON.parse(categoryChart.dataset.data) : [],
                    backgroundColor: [
                        '#0d6efd',
                        '#198754',
                        '#ffc107',
                        '#dc3545',
                        '#6c757d',
                        '#0dcaf0'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Répartition par catégorie'
                    }
                }
            }
        });
    }
}

// Fonction pour rafraîchir les statistiques
function refreshStats() {
    fetch('/api/stats/')
        .then(response => response.json())
        .then(data => {
            // Mettre à jour les statistiques affichées
            const statsElements = document.querySelectorAll('[data-stat]');
            statsElements.forEach(element => {
                const statName = element.dataset.stat;
                if (data[statName] !== undefined) {
                    element.textContent = data[statName];
                }
            });
        })
        .catch(error => console.error('Error refreshing stats:', error));
}

// Fonction pour exporter les données
function exportData(format = 'csv') {
    const table = document.querySelector('.exportable-table');
    if (!table) return;

    let csv = '';
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(col => {
            rowData.push('"' + col.textContent.replace(/"/g, '""') + '"');
        });
        csv += rowData.join(',') + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'export_' + new Date().toISOString().split('T')[0] + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Fonction pour imprimer une page
function printPage() {
    window.print();
}

// Fonction pour basculer l'affichage des colonnes
function toggleColumn(columnIndex) {
    const table = document.querySelector('.table');
    const cells = table.querySelectorAll(`td:nth-child(${columnIndex + 1}), th:nth-child(${columnIndex + 1})`);

    cells.forEach(cell => {
        cell.style.display = cell.style.display === 'none' ? '' : 'none';
    });
} 
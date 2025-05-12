document.addEventListener('DOMContentLoaded', function () {
    // Cache tous les graphiques au départ
    document.getElementById('graphBar').style.display = 'none';
    document.getElementById('graphLine').style.display = 'none';
    document.getElementById('graphPie').style.display = 'none';

    // Ajoute l'écouteur à chaque checkbox pour les graphiques
    const checkboxes = document.querySelectorAll('input[name="chartType"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleChangeBox);
    });

    // Charger le fichier config.json et peupler le sélecteur de fermes
    fetch('/static/config/config.json')
        .then(response => response.json())
        .then(data => {
            populateFarmSelector(data);
        })
        .catch(error => {
            console.error('Erreur lors du chargement du fichier config.json :', error);
        });
});

// Fonction pour remplir le sélecteur de ferme
function populateFarmSelector(data) {
    const farmSelect = document.getElementById('farmSelect');
    for (const farm in data) {
        const option = document.createElement('option');
        option.value = farm;
        option.textContent = farm.charAt(0).toUpperCase() + farm.slice(1); // Capitaliser le nom de la ferme
        farmSelect.appendChild(option);
    }

    // Ajout d'un écouteur d'événements pour quand l'utilisateur choisit une ferme
    farmSelect.addEventListener('change', function () {
        const selectedFarm = farmSelect.value;
        if (selectedFarm) {
            displayShieldList(data[selectedFarm]);
        }
    });
}

// Fonction pour gérer l'affichage des graphiques en fonction des cases cochées
function handleChangeBox() {
    // Récupération de l'état des cases à cocher
    const barChart = document.getElementById('barChart').checked;
    const lineChart = document.getElementById('lineChart').checked;
    const pieChart = document.getElementById('pieChart').checked;

    // Affiche ou masque chaque graphique selon l'état de la case à cocher
    document.getElementById('graphBar').style.display = barChart ? 'block' : 'none';
    document.getElementById('graphLine').style.display = lineChart ? 'block' : 'none';
    document.getElementById('graphPie').style.display = pieChart ? 'block' : 'none';
}

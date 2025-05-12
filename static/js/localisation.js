let map = null;
        let marker = null;

        // Charger les fermes dynamiquement
        document.addEventListener('DOMContentLoaded', function () {
            fetch('/static/config/config.json')
                .then(response => response.json())
                .then(data => {
                    populateFarmSelector(data);
                })
                .catch(error => console.error('Erreur lors du chargement du fichier config.json :', error));
        });

        // Remplir le sélecteur de fermes
        function populateFarmSelector(data) {
            const shieldSelect = document.getElementById('shieldSelect');
            for (const farm in data) {
                const option = document.createElement('option');
                option.value = farm;
                option.textContent = farm.charAt(0).toUpperCase() + farm.slice(1); // Capitalisation du nom de la ferme
                shieldSelect.appendChild(option);
            }
            loadSensors(); // Charger les capteurs pour la première ferme sélectionnée
        }

        // Charger les capteurs en fonction de la ferme sélectionnée
        async function loadSensors() {
            const shieldGroup = document.getElementById('shieldSelect').value;
            const response = await fetch(`/get_sensors/${shieldGroup}`);
            const sensors = await response.json();
            
            const sensorSelect = document.getElementById('sensorSelect');
            sensorSelect.innerHTML = ''; // Réinitialise la liste des capteurs

            // Ajouter les capteurs au menu déroulant
            sensors.forEach(sensor => {
                const option = document.createElement('option');
                option.value = sensor.id;
                option.textContent = sensor.id;
                sensorSelect.appendChild(option);
            });

            if (sensors.length > 0) {
                loadSensorData(); // Charge le 1er capteur automatiquement
            }
        }

        // Charger les données du capteur sélectionné
        async function loadSensorData() {
            const sensorId = document.getElementById('sensorSelect').value;
            const response = await fetch(`/get_data/${sensorId}`);
            const data = await response.json();

            // Affichage des coordonnées dans les spans
            document.getElementById('longitude').textContent = data.longitude;
            document.getElementById('latitude').textContent = data.latitude;

            const lat = data.latitude;
            const lon = data.longitude;

            // Initialiser ou mettre à jour la carte
            if (!map) {
                map = L.map('map').setView([lat, lon], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap'
                }).addTo(map);

                marker = L.marker([lat, lon]).addTo(map)
                    .bindPopup(`Capteur : ${sensorId}<br>`)
                    .openPopup();
            } else {
                map.setView([lat, lon], 13);
                marker.setLatLng([lat, lon])
                    .setPopupContent(`Capteur : ${sensorId}<br>`)
                    .openPopup();
            }
        }

        // Appeler loadSensors au chargement de la page
        window.onload = loadSensors;
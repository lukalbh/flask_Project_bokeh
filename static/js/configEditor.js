let previousConfig = null;

async function configEditor() {
    const response = await fetch('/get-config');
    const json = await response.json();

    if (json.error) {
        document.getElementById('json-editor').value = json.error;
        return;
    }

    const formatted = JSON.stringify(json, null, 2);
    document.getElementById('json-editor').value = formatted;

    // Stocker la configuration précédente pour la comparaison
    previousConfig = json;
}

async function saveRawConfig() {
    const rawText = document.getElementById('json-editor').value;

    try {
        const parsed = JSON.parse(rawText); // Vérifie si c’est bien du JSON

        // Comparaison pour détecter les suppressions
        const deletedKeys = Object.keys(previousConfig).filter(key => !(key in parsed));

        // Si des clés ont été supprimées, on les envoie pour les retirer du serveur
        if (deletedKeys.length > 0) {
            await fetch('/remove-keys', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ keys: deletedKeys })
            });
        }

        // Sauvegarde de la nouvelle configuration
        const response = await fetch('/save-config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(parsed)
        });

        if (response.ok) {
            alert('Configuration sauvegardée !');
            // Mettre à jour previousConfig après la sauvegarde
            previousConfig = parsed;
        } else {
            alert('Erreur lors de la sauvegarde.');
        }
    } catch (e) {
        alert("Erreur JSON : " + e.message);
    }
}

window.addEventListener('DOMContentLoaded', configEditor);

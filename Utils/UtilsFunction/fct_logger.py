import logging

# Étape 1 : Définir le niveau de journalisation personnalisé
TRACK = 25  # Une valeur entre INFO (20) et WARNING (30)

# Étape 2 : Ajouter le niveau de journalisation personnalisé
logging.addLevelName(TRACK, "TRACK")

# Étape 3 : Créer une méthode de journalisation pour ce niveau
def track(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACK):
        self._log(TRACK, message, args, **kwargs)

# Étape 4 : Ajouter la méthode de journalisation à la classe Logger
logging.Logger.track = track

# Étape 5 : Créer un gestionnaire de journalisation personnalisé avec le format souhaité
class CustomFormatter(logging.Formatter):
    format_track = '%(asctime)s - %(levelname)s - %(message)s'

    def format(self, record):
        if record.levelno == TRACK:
            self._style = logging.PercentStyle(self.format_track)
        return super().format(record)

# Étape 6 : Créer un logger et configurer un gestionnaire avec le format personnalisé
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

# # Exemple d'utilisation du niveau de journalisation personnalisé "TRACK"
# logger.track("Ceci est un message de niveau TRACK")
#
# # Exemple d'utilisation des autres niveaux de journalisation
# logger.info("Ceci est un message INFO")
# logger.warning("Ceci est un message WARNING")

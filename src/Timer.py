import time


class Timer:
    """ Classe permettant d'être utilisée pour délayer une tâche
    """
    def __init__(self, delayInMs):
        self.delay = delayInMs   # in milliseconds
        self.startTime = None
        self.lastCheck = None

    def start(self):
        self.startTime = time.time()
        self.lastCheck = time.time()

    def isDone(self):
        """ Retourne si oui ou non le délais requis à été complété
        :return: True si le délais est terminé sinon False
        """
        try:
            return time.time() - self.lastCheck >= self.delay / 1000
        except TypeError:   # Le timer n'a pas été explicitement démarré
            raise TimerException("Le timer n'a pas été lancer, appeler la fonction start() explicitement")

    def getRunningTime(self):
        """ Retourne le temps en seconde depuis le début que le timer fonctionne
        :return: int temps en secondes
        """
        return int(time.time() - self.startTime)

    def reset(self):
        self.lastCheck = time.time()


class TimerException(Exception):
    def __init__(self, msg):
        self.message = msg
        Exception.__init__(self, self.message)


# EXEMPLE UTILISATION
t = Timer(1000)
t.start()
while 1:
    if t.isDone():
        print("Running time: %ssec" % t.getRunningTime())
        t.reset()

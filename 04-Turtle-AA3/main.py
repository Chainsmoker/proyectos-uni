from utilidades import Config
from utilidades import Partes

config = Config()
partes = Partes()

config.cuerpo()

partes.ojo1(-85, 90)
partes.ojo2(50, 110)

partes.cachete1(-126, 32)
partes.cachete2(107, 63)


partes.boca(-5, 25)

partes.oreja_derecha(-250, 100)
partes.oreja_izquierda(140, 270)

config.loop()
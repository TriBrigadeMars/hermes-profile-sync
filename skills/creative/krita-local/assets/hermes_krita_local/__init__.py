from .plugin import HermesLocalExtension
from krita import Krita
Krita.instance().addExtension(HermesLocalExtension(Krita.instance()))

from qgis.core import Qgis
from qgis.core import QgsApplication
if __name__ == '__main__':
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    qgs.initQgis()
    version = Qgis.version()
    print(QgsApplication.prefixPath())
    print("Hello qgis,  version is {} ".format( version))
    qgs.exitQgis()
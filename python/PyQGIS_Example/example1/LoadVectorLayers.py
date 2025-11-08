import os
import sys

from qgis._core import QgsRasterLayer
from qgis.core import QgsProject, QgsVectorLayer, QgsPointXY, QgsFeature, QgsGeometry, QgsField
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction
from PyQt5.QtCore import QVariant, Qt

current_path = os.path.abspath(__file__)
data_path = os.path.dirname(os.path.dirname(current_path))+"/data/"

class QGISMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = None
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('QGIS 主界面')
        self.setGeometry(100, 100, 1200, 800)

        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.enableAntiAliasing(True)
        self.setCentralWidget(self.canvas)
        self.createToolbar()

    def createToolbar(self):
        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)
        refresh_action = QAction("加载所有矢量图层", self)
        refresh_action.triggered.connect(self.loadAllVectorLayers)
        toolbar.addAction(refresh_action)

    def loadAllVectorLayers(self):
        QgsProject.instance().removeAllMapLayers()

        geojson_layer = self.loadGeojsonLayer(data_path + "test_points.geojson", "GeoJSON点图层")
        shp_layer = self.load_shapefile(data_path + "test_lines.shp", "SHP线图层")
        spatialite_layer = self.load_spatialite(data_path + "test_ploygons.sqlite", "new_layer")
        raster_layer = self.load_tif(data_path + "random_china_raster.tif", "raster_layer")
        QgsProject.instance().addMapLayer(geojson_layer)
        QgsProject.instance().addMapLayer(shp_layer)
        QgsProject.instance().addMapLayer(spatialite_layer)
        QgsProject.instance().addMapLayer(raster_layer)

        # 设置画布图层
        self.canvas.setLayers([geojson_layer,shp_layer,spatialite_layer,raster_layer])
        self.canvas.zoomToFullExtent()


    def loadGeojsonLayer(self, geojson_path, layer_name):
        layer = QgsVectorLayer(geojson_path, layer_name, "ogr")
        # 检查图层是否有效加载
        if not layer.isValid():
            print(f"图层 {layer_name} 加载失败!")
            return None
        return layer

    def load_shapefile(self, path, layer_name):
        layer_name = "SHP图层"
        layer = QgsVectorLayer(path, layer_name, "ogr")
        if not layer.isValid():
            print(f"图层 {layer_name} 加载失败!")
            return None
        return layer

    def load_spatialite(self, path, layer_name):
        layer = QgsVectorLayer(path.replace("\\", "/"), layer_name, "ogr")
        # 检查图层是否有效加载
        if not layer.isValid():
            print(f"图层 {layer_name} 加载失败!")
            return None
        return  layer
    def load_tif(self, path, layer_name):
        layer = QgsRasterLayer(path, layer_name)
        if not layer.isValid():
            print(f"图层 {layer_name} 加载失败!")
            return None
        return  layer
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("PyQGIS 加载图层示例")
    main_window = QGISMainWindow()
    main_window.show()
    sys.exit(app.exec_())
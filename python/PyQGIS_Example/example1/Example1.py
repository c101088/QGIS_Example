import sys
import random

from qgis.core import QgsProject, QgsVectorLayer, QgsPointXY, QgsFeature, QgsGeometry, QgsField
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction
from PyQt5.QtCore import QVariant, Qt


class QGISMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('QGIS 主界面 - 随机点图层')
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 创建QGIS地图画布
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.enableAntiAliasing(True)

        # 将画布添加到布局中
        layout.addWidget(self.canvas)

        # 创建工具栏
        self.createToolbar()

        # 生成随机点图层
        self.createRandomPointLayer()

        # 设置画布范围
        self.zoomToLayer()

    def createToolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)

        # 刷新按钮
        refresh_action = QAction("刷新点图层", self)
        refresh_action.triggered.connect(self.refreshPoints)
        toolbar.addAction(refresh_action)

        # 缩放至图层按钮
        zoom_action = QAction("缩放至图层", self)
        zoom_action.triggered.connect(self.zoomToLayer)
        toolbar.addAction(zoom_action)

    def createRandomPointLayer(self):
        # 创建内存图层
        self.point_layer = QgsVectorLayer("Point?crs=EPSG:4326", "随机点", "memory")
        provider = self.point_layer.dataProvider()

        # 添加属性字段
        provider.addAttributes([QgsField("id", QVariant.Int),
                                QgsField("x", QVariant.Double),
                                QgsField("y", QVariant.Double)])
        self.point_layer.updateFields()

        # 生成随机点
        features = []
        for i in range(50):  # 生成50个随机点
            # 在经纬度范围内生成随机点
            x = random.uniform(116.0, 117.0)  # 经度范围
            y = random.uniform(39.0, 40.0)  # 纬度范围

            # 创建点几何
            point = QgsPointXY(x, y)
            geometry = QgsGeometry.fromPointXY(point)

            # 创建要素
            feature = QgsFeature()
            feature.setGeometry(geometry)
            feature.setAttributes([i, x, y])
            features.append(feature)

        # 添加要素到图层
        provider.addFeatures(features)
        self.point_layer.updateExtents()

        # 将图层添加到项目
        QgsProject.instance().addMapLayer(self.point_layer)

        # 设置画布图层
        self.canvas.setLayers([self.point_layer])

    def refreshPoints(self):
        """刷新随机点"""
        # 移除旧图层
        QgsProject.instance().removeMapLayer(self.point_layer.id())

        # 生成新图层
        self.createRandomPointLayer()

    def zoomToLayer(self):
        """缩放至图层范围"""
        if self.point_layer:
            self.canvas.setExtent(self.point_layer.extent())
            self.canvas.refresh()



if __name__ == '__main__':
    # 创建QApplication实例
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("QGIS随机点示例")

    # 创建并显示主窗口
    main_window = QGISMainWindow()
    main_window.show()

    # 运行应用
    sys.exit(app.exec_())
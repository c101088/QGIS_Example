from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsGeometry, QgsPointXY,
    QgsFeature, QgsField, QgsFields, QgsWkbTypes
)
import random
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolIdentify
from qgis.PyQt.QtGui import QCursor

def create_random_layers():
    # 创建多边形图层
    polygon_layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "随机多边形", "memory")
    polygon_provider = polygon_layer.dataProvider()

    # 添加字段
    polygon_provider.addAttributes([QgsField("id", QVariant.Int)])
    polygon_layer.updateFields()

    # 创建5个随机多边形
    features = []
    for i in range(5):
        # 随机生成多边形的中心点和大小
        center_x = 116.3 + random.uniform(-0.5, 0.5)
        center_y = 39.9 + random.uniform(-0.5, 0.5)

        # 创建矩形多边形
        points = []
        for dx, dy in [(-0.1, -0.1), (0.1, -0.1), (0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1)]:
            points.append(QgsPointXY(center_x + dx, center_y + dy))

        poly = QgsGeometry.fromPolygonXY([points])
        feat = QgsFeature()
        feat.setGeometry(poly)
        feat.setAttributes([i])
        features.append(feat)

    polygon_provider.addFeatures(features)
    polygon_layer.updateExtents()

    # 创建点图层
    point_layer = QgsVectorLayer("Point?crs=EPSG:4326", "随机点", "memory")
    point_provider = point_layer.dataProvider()

    # 添加字段
    point_provider.addAttributes([
        QgsField("id", QVariant.Int),
        QgsField("value", QVariant.Double)
    ])
    point_layer.updateFields()

    # 创建100个随机点
    point_features = []
    for i in range(100):
        x = 116.0 + random.uniform(0, 1)
        y = 39.5 + random.uniform(0, 1)

        point = QgsGeometry.fromPointXY(QgsPointXY(x, y))
        feat = QgsFeature()
        feat.setGeometry(point)
        feat.setAttributes([i, random.uniform(0, 100)])
        point_features.append(feat)

    point_provider.addFeatures(point_features)
    point_layer.updateExtents()

    # 添加到项目
    QgsProject.instance().addMapLayer(polygon_layer)
    QgsProject.instance().addMapLayer(point_layer)

    return polygon_layer, point_layer

# 执行创建图层
polygon_layer, point_layer = create_random_layers()


class PolygonPointSelectionTool(QgsMapToolIdentify):
    def __init__(self, canvas, polygon_layer, point_layer):
        super().__init__(canvas)
        self.canvas = canvas
        self.polygon_layer = polygon_layer
        self.point_layer = point_layer
        self.setCursor(QCursor(Qt.CrossCursor))

    def canvasReleaseEvent(self, event):
        # 识别点击的多边形
        results = self.identify(event.x(), event.y(), [self.polygon_layer],
                                QgsMapToolIdentify.TopDownStopAtFirst)

        if results:
            # 清除之前的选中状态
            self.polygon_layer.removeSelection()
            self.point_layer.removeSelection()

            # 选中被点击的多边形
            polygon_feature = results[0].mFeature
            self.polygon_layer.select(polygon_feature.id())

            # 选择多边形内的点
            self.select_points_in_polygon(polygon_feature.geometry())

    def select_points_in_polygon(self, polygon_geometry):
        """选择多边形内的所有点"""
        selected_point_ids = []

        # 遍历点图层中的所有要素
        for point_feature in self.point_layer.getFeatures():
            point_geometry = point_feature.geometry()

            # 检查点是否在多边形内
            if point_geometry.within(polygon_geometry):
                selected_point_ids.append(point_feature.id())

        # 选中这些点
        if selected_point_ids:
            self.point_layer.select(selected_point_ids)

        # 刷新画布显示选中状态
        self.canvas.refresh()

        # 显示选中结果
        iface.messageBar().pushMessage(
            "选择完成",
            f"选中了 {len(selected_point_ids)} 个点",
            level=0,
            duration=3
        )

canvas = iface.mapCanvas()

# 创建选择工具实例
selection_tool = PolygonPointSelectionTool(canvas, polygon_layer, point_layer)

# 激活工具
canvas.setMapTool(selection_tool)

# 显示提示信息
iface.messageBar().pushMessage(
    "提示",
    "点击多边形来选择其内部的点",
    level=0,
    duration=5
)
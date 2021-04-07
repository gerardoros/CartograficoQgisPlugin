from qgis.utils import iface
from qgis.core import *
from qgis.utils import *
from osgeo import ogr, osr
import os, json, requests, jwt, datetime
from PyQt5.QtCore import QFileInfo, QSettings, QCoreApplication, QTimer
from PyQt5.QtGui import *


def run():
    
    mem_layer = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&field=cveCat:string(15)&field=id:int(15)&field=nombre:string(200)&index=yes', 'municipio.geom', 'memory')
    QgsProject.instance().addMapLayers([mem_layer], True)
    render = mem_layer.renderer()
    symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#3579b1', 'width_border':'0.5'})
    render.setSymbol(symbol)
    etiquetaField = 'clave'
    colorCapa = QColor(53,121,177)

    settings = QgsPalLayerSettings()
    settings.placement = QgsPalLayerSettings.AroundPoint
    settings.fieldName = etiquetaField
    settings.enabled = True
    settings.isExpression = False
        
    settings.centroidWhole = True

    textFormat = QgsTextFormat()
    textFormat.setSize(8)
    textFormat.setNamedStyle('Bold')
    textFormat.setColor(colorCapa)
    settings.setFormat(textFormat)

    labeling = QgsVectorLayerSimpleLabeling(settings)

    mem_layer.setLabeling(labeling)
    mem_layer.setLabelsEnabled(True)

    mem_layer.triggerRepaint()
    
    
    
    #servidorIP = 'https://worknest.cianet.mx/jeather/cartografico/'
    servidorIP = 'http://192.168.0.25:8080'
    srid = QSettings().value("srid")
    url = servidorIP + "/busquedasimplewkn/consulta/get-municipio/" + str(srid)
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers = headers)

    except requests.exceptions.RequestException:
        print("Error de consulta")
        return
            

    data = response.json()
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(int(srid))
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(int(srid))
    coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    if not bool(data):
        print('ERROR: CAP000')
        return

    #Obtenemos todos los atributos del JSON
    if data['features'] == []:
        return True

    varKeys = data['features'][0]['properties']

    keys = list(varKeys.keys())
    properties = []
    geoms = []

    for feature in data['features']:
        geom = feature['geometry']

        property = feature['properties']
        geom = json.dumps(geom)
        geometry = ogr.CreateGeometryFromJson(geom)
        geometry.Transform(coordTrans)
        geoms.append(geometry.ExportToWkt())
        l = []
        for i in range(0, len(keys)):
            l.append(property[keys[i]])
        properties.append(l)

    prov = mem_layer.dataProvider()
    feats = [ QgsFeature() for i in range(len(geoms)) ]

    for i, feat in enumerate(feats):
        feat.setAttributes(properties[i])
        feat.setGeometry(QgsGeometry.fromWkt(geoms[i]))
        bbox = QgsGeometry.fromWkt(geoms[i]).boundingBox()

    prov.addFeatures(feats)

    mem_layer.triggerRepaint()

    iface.mapCanvas().setExtent(bbox)
    iface.mapCanvas().refresh()
    return True
    
    

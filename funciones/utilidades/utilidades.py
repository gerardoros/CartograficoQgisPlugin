
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QAction, QFileDialog, QTableWidgetItem, QListView, QHeaderView
import os, json, requests, jwt, datetime
from datetime import datetime as dt
from osgeo import ogr, osr
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from qgis.core import *
from qgis.utils import *

class Utilidad:

	def __init__(self):
		self.tablas = {'sectores':'e_sector',
					   'municipio': 'e_municipio',
					   'manzana': 'e_manzana',
					   'predios.geom': 'e_predio',
					   'construcciones': 'e_construccion',
					   'horizontales.geom':'e_condominio_horizontal',
					   'verticales':'e_condominio_vertical',
					   'cves_verticales':'e_condominio_vert_clave'}
		self.rot13 = str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

		#Cursor Redondo
		self.cursorRedondo = QCursor(QPixmap(["16 16 3 1",
										"      c None",
										".     c #FF0000",
										"+     c #FFFFFF",
										"                ",
										"       +.+      ",
										"      ++.++     ",
										"     +.....+    ",
										"    +.     .+   ",
										"   +.   .   .+  ",
										"  +.    .    .+ ",
										" ++.    .    .++",
										" ... ...+... ...",
										" ++.    .    .++",
										"  +.    .    .+ ",
										"   +.   .   .+  ",
										"   ++.     .+   ",
										"    ++.....+    ",
										"      ++.++     ",
										"       +.+      "]))

		#Cursor Cruz
		self.cursorCruz = QCursor(QPixmap(["16 16 3 1",
										"      c None",
										".     c #FF0000",
										"+     c #FFFFFF",
										"                ",
										"       +++       ",
										"       +.+      ",
										"       +.+      ",
										"       +.+     ",
										"       +.+     ",
										"       +.+      ",
										"++++++++.+++++++",
										"+..............+",
										"++++++++.+++++++",
										"       +.+      ",
										"       +.+      ",
										"       +.+      ",
										"       +.+      ",
										"       +.+      ",
										"       +++      "]))

		#Cursor Cruz
		self.cursorCuadro = QCursor(QPixmap(["16 16 3 1",
										"      c None",
										".     c #FF0000",
										"+     c #FFFFFF",
										"                ",
										"+++++++++++++++",
										"+..............+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+++++++++++++++",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.+++++++++++.+",
										"+.............+",
										"+++++++++++++++",
										"       +++      "]))

	#---------------------------------------------------------------------------------

	def mostrarAlerta(self, mensaje, icono, titulo):

		msg = QMessageBox()
		msg.setText(mensaje)
		msg.setIcon(icono)
		msg.setWindowTitle(titulo)
		msg.setFixedSize(500, 500)
		msg.show()
		msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		result = msg.exec_()

	#------------------------------------------------------------------------------------------------

	def obtenerToken(self):

		url = self.CFG.urlAutenticacion

		# validar la caducidad del token
		# se obtiene el token almacenado
		var = QSettings()
		token = var.value('token')

		# se decodifica el token (JWT)
		decode = jwt.decode(token, verify=False)

		# se obtiene la fecha de expiracion (timestamp)
		ttFromJWT = decode['exp']

		# se convierte a fecha legible para compararse con la fecha actual
		exp = dt.fromtimestamp(ttFromJWT).strftime('%Y-%m-%d %H:%M:%S')
		exp = dt.strptime(exp,'%Y-%m-%d %H:%M:%S')

		# se obtiene la fecha actual
		currentDate = datetime.datetime.now()

		# se compara para verificar que se haya caducado el token
		if currentDate > exp:

			payload = {"username" : self.decodeRot13(var.value('usuario')), "password" : self.decodeRot13(var.value('clave'))}
			payload = json.dumps(payload)
			headers = {'Content-Type': 'application/json'}

			response = requests.post(url, headers = headers, data = payload)
			if response.status_code == 200:
				data = response.content
			else:
				self.mostrarAlerta('No se ha conseguido token', QMessageBox().Critical, 'Autenticacion')
				return

			var.setValue('token', json.loads(data)['access_token'])

			t = json.loads(data)['access_token']
			d = jwt.decode(t, verify=False)
			t1 = d['exp']
			e = dt.fromtimestamp(t1).strftime('%Y-%m-%d %H:%M:%S')
			e = dt.strptime(e,'%Y-%m-%d %H:%M:%S')

			#print('nuevoooooooooooo', e, currentDate)
			return 'bearer ' + json.loads(data.decode('utf-8'))['access_token']

		else:
			#print('el mismo', exp, currentDate)
			return 'bearer ' + token

	#-----------------------------------------------------------------------------------------------------

	def decodeRot13(self, cadena):
		return str.translate(cadena, self.rot13)
	
	#-----------------------------------------------------------------------------------------------------

	def esEntero(self, num): #Funcion para checar si una variable es un entero numerico
		try: 
			int(num)
			return True
		except ValueError:
			return False

	#--------------------------------------------------------------------------------

	def esFloat(self, num): #Funcion para checar si una variable es un entero numerico
		try: 
			float(num)
			return True
		except ValueError:
			return False
	
	#---------------------------------------------------------------------------------

	def limpiarCanvas(self):
		grupoLayers =  QgsProject.instance().layerTreeRoot().findGroup('consulta')
		layers = grupoLayers.findLayers()
		for layer in layers:
			layer.layer().startEditing()
			for f in layer.layer().getFeatures():
				layer.layer().dataProvider().deleteFeatures([f.id()])
			layer.layer().triggerRepaint()
			layer.layer().commitChanges()

	#----------------------------------------------------------------------------------

	def guardarCambios(self):
		
		root = QgsProject.instance().layerTreeRoot()

		group = root.findGroup('ERRORES DE TOPOLOGIA')
		if not group is None:
			for child in group.children():
				dump = child.dump()
				id = dump.split("=")[-1].strip()
				QgsProject.instance().removeMapLayer(id)
			root.removeChildNode(group)

		for layer in iface.mapCanvas().layers():
			layer.triggerRepaint()

		if QSettings().value('posibleGuardar') == 'True' or True:
			print('fue posible guardar')
			self.listaAGuardar = []

			self.agregarALista('manzana')
			self.agregarALista('predios.geom')
			self.agregarALista('construcciones')
			self.agregarALista('horizontales.geom')
			self.agregarALista('verticales')
			self.agregarALista('cves_verticales')
			self.agregarAListaEliminados()

			
			#Formato para solicitar la peticion
			m = {}
			m['features'] = self.listaAGuardar
			m['claves'] = QSettings().value('clavesEstatus')
			print(m['claves'])
			#jsonParaGuardarAtributos = json.dumps(self.listaAGuardar)
			jsonParaGuardarAtributos = json.dumps(m)

			print(jsonParaGuardarAtributos)
			
			url = self.CFG.urlGuardadoConClaves
			print(url)
			payload = jsonParaGuardarAtributos
			headers = {'Content-Type': 'application/json', 'Authorization' : self.obtenerToken()}
			try:
				response = requests.post(url, headers = headers, data = payload)
				print(response)
			except requests.exceptions.RequestException:
				self.mostrarAlerta("No se ha podido conectar al servidor v1", QMessageBox.Critical, "Guardar Cambios v1")#Error en la peticion de consulta

			if response.status_code == 200:
				self.mostrarAlerta("Cambios guardados con exito", QMessageBox.Information, "Guardar Cambios")
				QSettings().setValue('listaEliminada', [])
				#Guardado de datos correcto
			elif response.status_code == 202:
				root.insertGroup(0, 'ERRORES DE TOPOLOGIA')

				capa = QgsVectorLayer('Point?crs=epsg:' + str(QSettings().value('srid')) +'&field=mensaje:string(80)', 'ERRORES PUNTO', 'memory')

				QgsProject.instance().addMapLayers([capa], False)

				props = capa.renderer().symbol().symbolLayer(0).properties()
				props['color'] = '#FF0000'
				capa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))

				self.etiquetarCapa(capa.name(), capa)

				QgsProject.instance().addMapLayer(capa, False)
				grupoErrores = root.findGroup('ERRORES DE TOPOLOGIA')
				capaError = QgsLayerTreeLayer(capa)
				capa.startEditing()

				puntosMalos = response.json()
				#print (type(puntosMalos))

				for malo in puntosMalos:
					
					#print(type(malo))
					geom = QgsGeometry.fromWkt(malo["wkt"])
					feat = QgsFeature()
					feat.setGeometry(geom)
					feat.setAttributes([malo['mensaje']])
					capa.dataProvider().addFeatures([feat])
					capa.updateFeature(feat)

				capa.triggerRepaint()
				capa.commitChanges()
				grupoErrores.insertChildNode(0, capaError)

			else:
				self.mostrarAlerta("No se ha podido conectar al servidor v2\n" + str(response.json()), QMessageBox.Critical, "Guardar Cambios v2")
				#Error al guardar datos
			
			#except ValueError:
				#self.mostrarAlerta("No se ha podido conectar al servidor v3", QMessageBox.Critical, "Guardar Cambios v3")
			print(response.status_code)
		else:
			self.mostrarAlerta("Se debe validar la topologia antes de guardar", QMessageBox.Critical, "Guardar Cambios v4")
		

		QSettings().setValue('posibleGuardar', 'False')
		QSettings().setValue('clavesEstatus', [])

	#-------------------------------------------------------------------------------------------------------------

	def agregarALista(self, idCapa):

		# armar la clave catastral del predio (e_predio)
		# consulta la manzana, se toma la clave de ella y se concatena con la clave del predio
		clave = ''
		if idCapa == 'predios.geom' or idCapa == 'construcciones':
			manzana = QgsProject.instance().mapLayer( self.ACA.obtenerIdCapa('manzana'))
			feat = manzana.getFeatures()
			
			for f in feat:
				clave = f['cve_cat']

		capa = QgsProject.instance().mapLayer( self.ACA.obtenerIdCapa( idCapa))
		listaTemp = []

		for feat in capa.getFeatures():
			campos = {}
			campos['wkt'] = feat.geometry().asWkt()
			campos['srid'] = QSettings().value('srid')
			campos['tabla'] = self.tablas[capa.name()]
			atributos = {}
			nombresAtrbutos = capa.fields()   

			nombres = [campo.name() for campo in nombresAtrbutos]

			for x in range(0, len(nombres)):
				atributo = feat.attributes()[x]
				if str(feat.attributes()[x]) == "NULL":
					atributo = None
				atributos[str(nombres[x])] = atributo
				
				if capa.id() == self.ACA.obtenerIdCapa('predios.geom'):
					punto = self.exteriorPredio(feat.geometry())
					if punto != None:
						atributos['num_ext'] = punto['numExt']
						atributos['geom_num'] = punto.geometry().asWkt()

				elif capa.id() == self.ACA.obtenerIdCapa('horizontales.geom'):
					punto = self.exteriorCondom(feat.geometry())
					if punto != None:
						atributos['num_ofi'] = punto['num_ofi']
						atributos['geom_num'] = punto.geometry().asWkt()


			campos['attr'] = atributos
			if campos['attr']['id'] == None or campos['attr']['id'] == '':
				campos['nuevo'] = True
				campos['eliminado'] = False
			else:
				campos['nuevo'] = False
				campos['eliminado'] = False
			self.listaAGuardar.append(campos)

	############################################################################################

	def agregarAListaEliminados(self):

		listaTemp = QSettings().value('listaEliminada')

		if listaTemp == None:
			return

		for elemento in listaTemp:
			self.listaAGuardar.append(elemento)
			print(self.listaAGuardar.append(elemento))
	#####################################################################################################################

	def exteriorPredio(self, predio):

		puntos = QgsProject.instance().mapLayer(self.ACA.obtenerIdCapa('predios.num')).getFeatures()

		for punto in puntos:
			if punto.geometry().intersects(predio):
				return punto

	def exteriorCondom(self, condominio):

		puntos = QgsProject.instance().mapLayer(self.ACA.obtenerIdCapa('horizontales.num')).getFeatures()

		for punto in puntos:
			if punto.geometry().intersects(condominio):
				return punto

	####################################################################################################################

	def extenderCombo(self, combo, signal, modelo):

		combo.setFocusPolicy( Qt.StrongFocus )
		combo.setEditable( True )
		combo.completer = QCompleter(combo )

		# always show all completions
		combo.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
		combo.pFilterModel = QSortFilterProxyModel( combo)
		combo.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )
		combo.completer.setPopup( combo.completer.popup() )
		combo.setCompleter( combo.completer )
		combo.lineEdit().textEdited.connect( combo.pFilterModel.setFilterFixedString )
		combo.lineEdit().setCursorPosition(0);
		combo.completer.activated.connect(signal)

		combo.setModel( modelo )
		combo.pFilterModel.setSourceModel( modelo )
		combo.completer.setModel(combo.pFilterModel)
		combo.completer.setCompletionColumn( 0 )
		combo.pFilterModel.setFilterKeyColumn( 0 )
		combo.setModelColumn( 0 )

	def extenderCombo_actualizado(self, combo, modelo, listaIds):

		combo.setFocusPolicy( Qt.StrongFocus )
		combo.setEditable( True )
		combo.completer = QCompleter(combo )

		# always show all completions
		combo.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
		combo.pFilterModel = QSortFilterProxyModel( combo)
		combo.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )
		combo.completer.setPopup( combo.completer.popup() )
		combo.setCompleter( combo.completer )
		combo.lineEdit().textEdited.connect( combo.pFilterModel.setFilterFixedString )
		combo.lineEdit().setCursorPosition(0);

		combo.setModel( modelo )
		combo.pFilterModel.setSourceModel( modelo )
		combo.completer.setModel(combo.pFilterModel)
		combo.completer.setCompletionColumn( 0 )
		combo.pFilterModel.setFilterKeyColumn( 0 )
		combo.setModelColumn( 0 )
		combo.setInsertPolicy(0)

		for i, temp in enumerate( listaIds ): 
			combo.setItemData(i, temp)

	################################################################################################################
	def strechtTabla(self, tabla):
		header = tabla.horizontalHeader()
		
		for x in range(0, tabla.columnCount()):
			header.setSectionResizeMode(x, QHeaderView.Stretch)
			header.setStretchLastSection(True)

	def formatoCapa(self, capaParam, nuevaCapa):

		'''
		elif capaParam == 'areas_inscritas':
			QSettings().setValue('xAreasInscritas', nuevaCapa.id())
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#F646F3', 'width_border':'0.5'})
			render.setSymbol(symbol)
		'''

		# C A P A S   D E   C O N S U L T A 
		if capaParam == 'manzana':
			QSettings().setValue('xManzana', nuevaCapa.id())
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#F5A9F2', 'width_border':'0.5'})
			render.setSymbol(symbol)
		
		elif capaParam == 'predios.geom':
			QSettings().setValue('xPredGeom', nuevaCapa.id())
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00ff00', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'predios.num':
			QSettings().setValue('xPredNum', nuevaCapa.id())
			props = nuevaCapa.renderer().symbol().symbolLayer(0).properties()
			props['color'] = '#00FF00'
			nuevaCapa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))

		elif capaParam.lower() == 'construcciones':
			if capaParam != 'Construcciones':
				QSettings().setValue('xConst', nuevaCapa.id())
			
			road_rules = (
				('Const_Esp',  'NOT "cve_const_esp" is NULL '),
				('Construccion', ' "cve_const_esp" is NULL '),
			)

			symbolConst = QgsSymbol.defaultSymbol(nuevaCapa.geometryType())
			rendererConst = QgsRuleBasedRenderer(symbolConst)
			fillConst = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#000000', 'width_border':'0.5'})
			fillEsp = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00FFFF', 'width_border':'0.5'})

			# get the "root" rule
			root_rule = rendererConst.rootRule()
			for label, expression in road_rules:
				# create a clone (i.e. a copy) of the default rule
				rule = root_rule.children()[0].clone()
				# set the label, expression and color
				rule.setLabel(label)
				rule.setFilterExpression(expression)

				if label == "Const_Esp":
					rule.setSymbol(fillEsp)
				else:
					rule.setSymbol(fillConst)

				root_rule.appendChild(rule)
			root_rule.removeChildAt(0)
			#apply the renderer to the layer
			nuevaCapa.setRenderer(rendererConst)

		elif capaParam == 'horizontales.geom':
			QSettings().setValue('xHoriGeom', nuevaCapa.id())
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#C68C21', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'horizontales.num':
			QSettings().setValue('xHoriNum', nuevaCapa.id())
			props = nuevaCapa.renderer().symbol().symbolLayer(0).properties()
			props['color'] = '#C68C21'
			nuevaCapa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))

		elif capaParam == 'verticales':
			QSettings().setValue('xVert', nuevaCapa.id())
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#ff9900', 'width_border':'0.5'})
			render.setSymbol(symbol)
			
		elif capaParam == 'cves_verticales':
			QSettings().setValue('xCvesVert', nuevaCapa.id())
			props = nuevaCapa.renderer().symbol().symbolLayer(0).properties()
			props['color'] = '#ff9900'
			nuevaCapa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))

		# C A P A S   D E   R E F E R E N C I A 
		elif capaParam == 'Estado':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#a0e000', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Region Catastral':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00b4b4', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Municipios':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#3579b1', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Secciones':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#d20000', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Localidades':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00ffff', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Sectores':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#83C7FF', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Manzanas':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#C15ABC', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Predios':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#09DE66', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Calles':
			render = nuevaCapa.renderer()
			symbol = QgsLineSymbol.createSimple({'line_style':'SimpleLine', 'color':'#ff00ff', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Colonias':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#0000b4', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Codigo Postal':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#ff7f00', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Zona Uno':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#C383FF', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Zona Dos':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#7800E8', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Area de Valor':
			render = nuevaCapa.renderer()
			symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00ADAD', 'width_border':'0.5'})
			render.setSymbol(symbol)

		elif capaParam == 'Corredor de Valor':
			render = nuevaCapa.renderer()
			symbol = QgsLineSymbol.createSimple({'line_style':'SimpleLine', 'color':'#0e0bff', 'width_border':'0.5'})
			render.setSymbol(symbol)

	def etiquetarCapa(self, nombreCapa, capa):

		if capa == None:
			capa = QgsProject.instance().mapLayersByName(nombreCapa)[0]
		
		etiquetaField = ""
		colorCapa = ""
		esExpresion = False
		if nombreCapa == "manzana":
			etiquetaField = "clave"
			colorCapa = QColor(255,0,0)
		elif nombreCapa == "predios.geom":
			etiquetaField = "clave"
			colorCapa = QColor(0,255,0)
		elif nombreCapa == "predios.num":
			etiquetaField = "numExt"
			colorCapa = QColor(0,255,0)
		elif nombreCapa.lower() == "construcciones":
			etiquetaField = " if( cve_const_esp is null, concat(nom_volumen, '\n', num_niveles), concat(nom_volumen, '\n', cve_const_esp))"
			esExpresion = True
			colorCapa = QColor(0,0,255)
		elif nombreCapa == "horizontales.geom":
			etiquetaField = "clave"
			colorCapa = QColor(198,140,33)
		elif nombreCapa == "horizontales.num":
			etiquetaField = "num_ofi"
			colorCapa = QColor(198,140,33)
		elif nombreCapa == "verticales":
			etiquetaField = "clave"
			colorCapa = QColor(255,153,0)
		elif nombreCapa == "cves_verticales":
			etiquetaField = "clave"
			colorCapa = QColor(255,153,0)
		else:
			etiquetaField = "mensaje"
			colorCapa = QColor(255,153,0)
		'''
		elif nombreCapa == "areas_inscritas":
			etiquetaField = "clave"
			colorCapa = QColor(255,153,0)
		'''

		settings = QgsPalLayerSettings()
		settings.fieldName = etiquetaField
		settings.enabled = True
		settings.isExpression = esExpresion
		
		settings.centroidWhole = True
		settings.centroidInside = True

		textFormat = QgsTextFormat()
		textFormat.setColor(colorCapa)
		textFormat.setSize(8)
		textFormat.setNamedStyle('Bold')

		settings.setFormat(textFormat)

		#settings.placement= QgsPalLayerSettings.OverPoint
		labeling = QgsVectorLayerSimpleLabeling(settings)

		capa.setLabeling(labeling)
		capa.setLabelsEnabled(True)
		capa.triggerRepaint()

	def cargarCapaVacio(self):

		# valida si ya se ha agregado el grupo
		root = QgsProject.instance().layerTreeRoot()
		group = root.findGroup('consulta')
		if group is None:

			root = QgsProject.instance().layerTreeRoot() 
			root.addGroup('consulta')
			root.addGroup('referencia')
			


		# Se crea una lista de vectores a partir de una fuente de datos
		# ejemplo. 'point?crs=epsg:4326&field=id:integer'
		listNC = []
		'''
		if QgsProject.instance().mapLayer(QSettings().value('xAreasInscritas')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sAreasInscritas'), 'areas_inscritas', 'memory'))
		'''
		if QgsProject.instance().mapLayer(QSettings().value('xCvesVert')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sCvesVert'), 'cves_verticales', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xVert')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sVert'), 'verticales', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xHoriNum')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sHoriNum'), 'horizontales.num', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xHoriGeom')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sHoriGeom'), 'horizontales.geom', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xConst')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sConst'), 'construcciones', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xPredNum')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sPredNum'), 'predios.num', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xPredGeom')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sPredGeom'), 'predios.geom', 'memory'))

		if QgsProject.instance().mapLayer(QSettings().value('xManzana')) is None:
			listNC.append(QgsVectorLayer(QSettings().value('sManzana'), 'manzana', 'memory'))

		root = QgsProject.instance().layerTreeRoot()
		group = root.findGroup('consulta')
		
		for capa in listNC:

			# valida si la capa ya se tiene agregada
			
			self.formatoCapa(capa.name(), capa)

			self.etiquetarCapa(capa.name(), capa)

			QgsProject.instance().addMapLayers([capa], False)

			capaArbol = QgsLayerTreeLayer(capa)
			group.insertChildNode(0, capaArbol)

#------------------------------------------------------------------------------------------------------------------------
	
	# regresa una lista de puntos de tipo QgsPointXY
	def obtenerVerticesLinea(self, geom):

		return geom.asPolyline()

	# regresa una lista de puntos de tipo QgsPointXY
	def obtenerVerticesPoligono(self, geom):
		polygon = geom.asPolygon()
		listaVertices = []

		n = len(polygon[0])

		for i in range(n):
			listaVertices.append(polygon[0][i])

		return listaVertices

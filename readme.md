# Proceso de traducción
1. Tratamiento del original en inglés:
	```vim
		source ../ass_prepare
	```
	* Eliminado de OP y ED (*descartado*)
	* Considerar comentarios como diálogos
	* Marcar traducciones de carteles con #
	* Marcar pensamientos con *
	* Pasaje de XX.ass a XX-eng.srt
1. Obtener XX-spa.srt
	apertium o simplemente cp (parte de ass_prepare)
1. Traducción del archivo XX-spa.srt
	```vim
		source ../commands
	```
	vertical split, scrollbind, colorcolumns 25,50
	traducción manual
1. Pasaje de XX-spa.srt a XX-spa.ass
	```vim
		source spa_ass
	```
	1. Arreglo formato .ass
		* Establece el tipo de fuente
		* Elimina espacios en blanco al final de la línea
		* Elimina saltos de línea consecutivos
		* Elimina líneas vacías
		* Inserta el header
		* Crea enlace duro al directorio donde está el video

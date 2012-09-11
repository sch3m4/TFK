all : gui.ui
	rm -fv *.pyc
	pyuic4 gui.ui -o tfk_gui.py
	pyuic4 about.ui -o tfk_about.py
	pyuic4 loghistory.ui -o tfk_log.py
	pyrcc4 resources.qrc -o resources_rc.py

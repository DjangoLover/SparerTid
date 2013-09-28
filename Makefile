PRJPATH := $(shell pwd)


run:
	python manage.py runserver

css:
	mkdir -p $(PRJPATH)/sparertid/media/css
	lessc $(PRJPATH)/sparertid/media/less/main.less $(PRJPATH)/sparertid/media/css/main.css

js:
	mkdir -p $(PRJPATH)/sparertid/media/js/bootstrap
	cp $(PRJPATH)/sparertid/media/less/bootstrap/js/*.js $(PRJPATH)/sparertid/media/js/bootstrap/

font:
	mkdir -p $(PRJPATH)/sparertid/media/fonts
	cp $(PRJPATH)/sparertid/media/less/bootstrap/fonts/* $(PRJPATH)/sparertid/media/fonts/

static: css js
	python manage.py collectstatic

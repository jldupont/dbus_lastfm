#
# @author Jean-Lou Dupont
#
#
PRJ=dbus_lastfm

PYTHON=`which python`
BASE=/usr/lib/dlastfm

all:
	@echo "make install"
	@echo "make clean"
	@echo "make buildsrc"

clean:
	@rm -f -r $(DESTDIR)$(BASE)/dbus_lastfm/*.pyc
	@rm -f -r $(DESTDIR)$(BASE)/dbus_lastfm_service/*.pyc
		
install:
	@install -d $(DESTDIR)$(BASE)
	@install -d $(DESTDIR)$(BASE)/dbus_lastfm
	@install -d $(DESTDIR)$(BASE)/dbus_lastfm_service
	@install -d $(DESTDIR)$(BASE)/dbus_lastfm_service/api
	@install -d $(DESTDIR)/usr/share/applications
	@install -d $(DESTDIR)/usr/share/icons
	@install -d $(DESTDIR)/usr/bin
	@install -d $(DESTDIR)/usr/lib
	
	@install -D $(CURDIR)/dbus_lastfm/*.py                 $(DESTDIR)$(BASE)/dbus_lastfm/
	@install -D $(CURDIR)/dbus_lastfm/*.glade              $(DESTDIR)$(BASE)/dbus_lastfm/
	
	@install -D $(CURDIR)/dbus_lastfm_service/*.py        $(DESTDIR)$(BASE)/dbus_lastfm_service/
	@install -D $(CURDIR)/dbus_lastfm_service/api/*.py    $(DESTDIR)$(BASE)/dbus_lastfm_service/api/
	
	@install -D $(CURDIR)/dlastfm.desktop                 $(DESTDIR)/usr/share/applications/
	@install -D $(CURDIR)/dlastfm.png                     $(DESTDIR)/usr/share/icons/ 

	@install $(CURDIR)/dlastfmservice                     $(DESTDIR)/usr/bin/
	@install $(CURDIR)/dlastfm.tap                        $(DESTDIR)/usr/bin/

	@python -m compileall ${DESTDIR}$(BASE)/dbus_lastfm
	@python -m compileall ${DESTDIR}$(BASE)/dbus_lastfm_service
	
buildsrc:
	debuild -S
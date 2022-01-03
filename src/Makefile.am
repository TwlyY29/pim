SUBDIRS = pim_mailhelper pim_modules
bin_SCRIPTS = mainreceiver sendreminder
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = mainreceiver.in sendreminder.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
		-e 's,[@]PYTHON[@],$(PYTHON),g' \
		-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
		-e 's,[@]RCV_BASE_PATH[@],$(RCV_BASE_PATH),g' \
		-e 's,[@]pimconfdir[@],$(PIM_CONFDIR),g' \
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'

mainreceiver: mainreceiver.in Makefile
	$(do_substitution) < $(srcdir)/mainreceiver.in > mainreceiver
	chmod +x mainreceiver

sendreminder: sendreminder.in Makefile
	$(do_substitution) < $(srcdir)/sendreminder.in > sendreminder
	chmod +x sendreminder

dist-hook:
	rm -f $(distdir)/mainreceiver $(distdir)/sendreminder

install-exec-hook:
	mkdir -p "$(RCV_BASE_PATH)"
	touch "$(RCV_BASE_PATH)/pim.log"
	chgrp $(MAIL_USER) "$(RCV_BASE_PATH)/pim.log"
	chmod g+w "$(RCV_BASE_PATH)/pim.log"

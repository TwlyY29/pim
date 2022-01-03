crondir = $(sysconfdir)/cron.d/

bin_SCRIPTS = pim_receive
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = pim_receive.in

do_substitution = sed -e 's,[@]CRONPATTERN[@],$(CRONPATTERN),g' \
		-e 's,[@]EXEC_RECEIVER_PATH[@],$(bindir),g' \
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'

pim_receive: pim_receive.in Makefile
	$(do_substitution) < $(srcdir)/pim_receive.in > pim_receive
	chmod +x pim_receive

uninstall-hook:
	rm -rf $(crondir)/$(bin_SCRIPTS)

install-exec-hook:
	mkdir -p $(crondir)
	mv $(DESTDIR)$(bindir)/$(bin_SCRIPTS) $(crondir)/$(bin_SCRIPTS)

SUBDIRS = src config cron

install-exec-hook:
	touch $(sysconfdir)/aliases
	sed -i '\@$(MAILALIAS)\:\t"\| $(DESTDIR)$(bindir)/mainreceiver"$\@d' $(sysconfdir)/aliases
	echo -e "$(MAILALIAS):\t\"| "$(DESTDIR)$(bindir)"/mainreceiver\"" >> $(sysconfdir)/aliases
	newaliases
	postalias $(sysconfdir)/aliases

uninstall-hook:
	sed -i '\@$(MAILALIAS)\:\t"\| $(DESTDIR)$(bindir)/mainreceiver"$\@d' $(sysconfdir)/aliases
	newaliases
	postalias $(sysconfdir)/aliases

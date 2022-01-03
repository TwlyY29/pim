expenses_PYTHON = receive.py __init__.py
expensesdir = $(pythondir)/pim_modules/expenses

EXTRA_DIST = __init__.py.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
		-e 's,[@]PYTHON[@],$(PYTHON),g' \
		-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
		-e 's,[@]pimconfdir[@],$(PIM_CONFDIR),g' \
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'


__init__.py: __init__.py.in Makefile
	$(do_substitution) < $(srcdir)/__init__.py.in > __init__.py

dist-hook:
	rm -f $(distdir)/__init__.py

install-exec-hook:
	mkdir -p "$(EXPENSES_BASE_PATH)"
	printf "date\tpm\tamount\twhat\tcategory" > "$(EXPENSES_BASE_PATH)/expenses.tsv"
	printf "date\tpm\tamount\twhat\tcategory" > "$(EXPENSES_BASE_PATH)/taxes.tsv"
	chgrp $(MAIL_USER) "$(EXPENSES_BASE_PATH)" "$(EXPENSES_BASE_PATH)/expenses.tsv" "$(EXPENSES_BASE_PATH)/taxes.tsv"
	chmod g+w "$(EXPENSES_BASE_PATH)/expenses.tsv" "$(EXPENSES_BASE_PATH)/taxes.tsv"

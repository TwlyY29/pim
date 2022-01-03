AC_INIT([Personal Information Manager],
        0.1.3,
        TWlyY29@gmail.com,
        pim,
        http://www.mircoschoenfeld.de)
AM_INIT_AUTOMAKE([foreign])
AM_PATH_PYTHON([3.5])

AC_CONFIG_FILES([Makefile src/Makefile src/pim_mailhelper/Makefile src/pim_modules/Makefile config/Makefile cron/Makefile])
AC_CONFIG_FILES([src/pim_modules/daily/Makefile src/pim_modules/expenses/Makefile])

AC_SUBST(RCV_BASE_PATH,"$localstatedir/log/")
AC_ARG_VAR(RCV_BASE_PATH, 'set location of log output dir')
AC_SUBST(DAILY_BASE_PATH,"$localstatedir/mail/")
AC_ARG_VAR(DAILY_BASE_PATH, 'set location of reminders file')
AC_SUBST(EXPENSES_BASE_PATH,"$localstatedir/expenses/")
AC_ARG_VAR(EXPENSES_BASE_PATH, 'set location of expense databases')
AC_SUBST(STD_REMINDER_FILE,"$DAILY_BASE_PATH/pim_daily_reminder")
AC_SUBST(CRONPATTERN,'0 5 * * *')
AC_ARG_VAR(CRONPATTERN, 'set cron pattern to configure sending of reminder')
AC_SUBST(MAILALIAS,'reminder')
AC_ARG_VAR(MAILALIAS, 'set mailalias for receiving mails')
AC_SUBST(PIM_CONFDIR,"$sysconfdir/pim")
AC_ARG_VAR(PIM_CONFDIR, 'set directory for config file')
AC_SUBST(MAIL_USER,"mail")
AC_ARG_VAR(MAIL_USER, 'username of mailserver')

AC_CONFIG_MACRO_DIRS([m4])

AX_PYTHON_MODULE(dateparser, "", python3)
AX_PYTHON_MODULE([requests], "", python3)
AX_PYTHON_MODULE(configparser, "", python3)

AC_ARG_ENABLE([daily],
[AS_HELP_STRING([--disable-daily],[Turn off daily. Default is enabled.])],
[enable_daily="$enableval"],[enable_daily="yes"])
AM_CONDITIONAL([INSTALL_DAILY], [test "x$enable_daily" = "xyes" ])

AC_ARG_ENABLE([expenses],
[AS_HELP_STRING([--disable-expenses],[Turn off expenses. Default is enabled.])],
[enable_expenses="$enableval"],[enable_expenses="yes"])
AM_CONDITIONAL([INSTALL_EXPENSES], [test "x$enable_expenses" = "xyes" ])

AC_ARG_ENABLE([dailyexpenses],
[AS_HELP_STRING([--enable-dailyexpenses],[Turn on daily expense report. Default is disabled.])],
[enable_dailyexpenses="$enableval"],[enable_dailyexpenses="no" ])
AM_CONDITIONAL([INSTALL_DAILY_EXPENSES], [test "x$enable_dailyexpenses" = "xyes" ])
AM_CONDITIONAL([INSTALL_EXPENSES_CONFIG], [test "x$enable_expenses" = "xyes" -o "x$enable_dailyexpenses" = "xyes" ])

AC_ARG_ENABLE([dailyweather],
[AS_HELP_STRING([--enable-dailyweather],[Turn on daily weather report. Default is disabled.])],
[enable_dailyweather="$enableval"],[enable_dailyweather="no"])
AM_CONDITIONAL([INSTALL_DAILY_WEATHER], [test "x$enable_dailyweather" = "xyes"])

AC_ARG_ENABLE([dailyattachments],
[AS_HELP_STRING([--enable-dailyattachments],[Turn on attachments to daily report. Default is disabled.])],
[enable_dailyattachments="$enableval"],[enable_dailyattachments="no"])
AM_CONDITIONAL([INSTALL_DAILY_ATTACHMENTS], [test "x$enable_dailyattachments" = "xyes"])

AS_IF([test "x$enable_daily" = "xyes"],
      [
      AX_PROG_PERL_MODULES( iCal::Parser, , [AC_MSG_ERROR([perl module iCal::Parser required, but not found.])])
      
      AC_CHECK_PROG(sendmail_exists,sendmail,yes)
      AS_IF([test "x$sendmail_exists" != "xyes"], [AC_MSG_ERROR([sendmail required, but not found.])])
      
      AC_CHECK_PROG(postfix_exists,postfix,yes)
      AS_IF([test "x$postfix_exists" != "xyes"], [AC_MSG_ERROR([postfix required, but not found.])])
      
      AC_CHECK_PROG(remind_exists,remind,yes)
      AS_IF([test "x$remind_exists" != "xyes"], [AC_MSG_ERROR([remind required, but not found.])])
      ])

AS_IF([test "x$enable_dailyweather" = "xyes"],
      [
      AS_IF([test "x$HAVE_PYMOD_REQUESTS" = x"no"], [AC_MSG_ERROR([missing python module: requests])])
      AS_IF([test "x$enable_daily" = "xno"], [AC_MSG_ERROR([turned on daily weather report but disabled daily])])
      ])

AS_IF([test "x$enable_dailyexpenses" = "xyes"],
      [
      AS_IF([test "x$enable_daily" = "xno"], [AC_MSG_ERROR([turned on daily expense report but disabled daily])])
      ])

AS_IF([test "x$enable_dailyattachments" = "xyes"],
      [
      AS_IF([test "x$enable_daily" = "xno"], [AC_MSG_ERROR([turned on daily attachments but disabled daily])])
      ])

AC_SUBST(VERSION)
AC_SUBST(PACKAGE_NAME)
AC_SUBST(PACKAGE_BUGREPORT)

AC_OUTPUT

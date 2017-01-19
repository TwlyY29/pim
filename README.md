Don't we all like braindumping important stuff with the relaxing certainty of not losing track of it?

Sending yourself an email is a possibility. But your email program doesn't remind you of that approaching deadline, automatically. Also, that email with that brilliant idea for a birthday gift doesn't pop up by itself. And finally, the link to that interesting article you could not finish reading in the subway will most likely get lost in the daily flood tide of mails we all love so much.

But still, the idea of sending a short email is charming. So, why not adding a little intelligence? It would be cool to just send a link and receive a copy of that interesting article via email. Also, a daily summary of all approaching deadlines and ideas for birthday gifts would be really helpful. That is what this collection of scripts is for.

The whole idea is to send an email to this program which then creates a reminder, stores that idea of a birthday gift, or downloads the web-article. 

## Functionalities
This part describes the modules in (./modules)-subfolder. Currently, there are three of them:

1. `remarkable`: Notes to yourself
2. `daily`: Reminders of important dates
3. `epub`: Saving webpages as ePubs for reading them later

Programmatically, these functionalities are seperated into modules that are easily de-/activatable and extendable. Deactivating a module only requires to delete the subfolder. 

### Module: `remarkable`
This modules enables you to send yourself a note -- a link, a poem, or a code-snippet. On request, these notes are e-mailed back to you.

Inside this module's folder you will find a `__init__.py`, a `receive.py` and a `summarizenotes.py`. `receive.py` takes an email and saves all of it's content to a specified file. Specification of that file is done in the `__init__.py` via the `OUTFILE`-variable. There, you will also find a variable `MODULE_OUTPUT` that points to `summarizenotes`. That is not only the name of the source-file but also the name of the method inside that source-file that produces the summary of your notes. In this case, the summary is basically the content of the `OUTFILE`.

### Module: `daily`
This module manages a [remind](https://linux.die.net/man/1/remind)-compatible file with all reminders for important (and not-so-important) deadlines coming up. It also puts together a summary of all reminders `remind` reminds you of.

#### What is `remind`? 
From [this presentation of remind](https://www.roaringpenguin.com/files/download/remind-oclug.pdf) we learn:

> * UNIX command-line tool that reads a text file for its database.
> * Sophisticated tool for date calculation.
> * Scripting-language interpreter

A remind-file may look like this:
```
    REM 26 Mar MSG David's birthday
    REM 19 Jan 2017 +3 MSG README finally finished? %x days left!
    REM 6 Jan 2017 *14 MSG Go have a beer!
```
With those reminders you are notified about David's birthday on every 26th of March every year. Also, you are notified on that upcoming deadline for finishing this README. The deadline was set to 19th of January 2017 and notification starts 3 days in advance. On 16th of January 2017 the reminder-message will interpret to "README finally finished? 3 days left!". And finally, starting on January 6 in 2017, you will be notified to go have a beer on every second Friday (if you really need a reminder for that...). 

#### What does this module do?
This module takes your email and creates a `remind`-compatible line. Also, it puts together a summary of all your reminders (based on the output of `remind`).

Inside this module's folder you will find a `__init__.py`, a `receive.py` and a `getreminders.py`. Again, the `receive.py` takes an email as an argument, fetches the message text from it and creates one or more reminders. Especially when sending in several reminders at once from your mobile, typing "REM" and "MSG" every time can be cumbersome. Therefore, this script expects your mail to contain an **even number of lines**. The first line of every pair of lines will be prefixed with "REM" and glued together with the second line seperated by that "MSG"-tag. 

All those reminders will then be appended to `OUTFILE` wich is, again, specified inside the `__init__.py`. There, the `MODULE_OUTPUT` points to `getreminders`. So, the summary of your reminders is put together by the function `getreminders` inside `getreminders.py`.

The summary originates from a sys-call to `remind`, of course. So, maybe, you have to adjust the path to `remind` inside the `getreminders.py` in `REMINDCMD`.

But wait, there is more!

You can specify a URL to a iCal-file inside the `getreminders.py` which is then downloaded, translated into another `remind`-compatible file, and processed via `remind`, separately. The summary of those events are appended to the summary above. Download and translation are also sys-calls -- in this case to `wget` and the nifty script `ical2rem.pl` I found at [dsoulayrol's github](https://github.com/dsoulayrol/config/blob/master/scripts/ical2rem.pl). An example for this usecase can be found inside `getreminders.py` in the `CMDS`-array. You might need to adjust the path to the Perl-Script, there...

### Module: `epub`
This module provides an "email-frontend" to my script from [my other repo](https://github.com/TwlyY29/websiteasepub): You can send yourself a link to a webpage which is then downloaded, converted into an epub-file and sent back to you, immediately. 

To prevent the epub from containing any non-article-parts of the website, only the content of a certain HTML-element with a certain CSS-`class` or -`id` is taken. To help you select the element and CSS-token the script first sends you a DOM-tree of the relevant HTML elements with their corresponding CSS identifiers. You can reply to that message providing only the relevant CSS-`class` or -`id` the content should be taken from. Of course, the URL and the selected CSS-identifier are saved for later reuse. The next time you want to save an article from that URL the known CSS-identifier will be used. 

The conversion from HTML to epub is based on [pandoc](http://pandoc.org/). Again, this is a sys-call to `pandoc`. You may have to specify the exact path. But that is documented at [TwlyY29/websiteasepub](https://github.com/TwlyY29/websiteasepub) in more detail. 

Here, it is worth noting that the module does not provide any summary. Therefore, the `MODULE_OUTPUT` inside `__init__.py` is set to `False`. But, at the same place, the `HANDLER_ACCEPTS_REPLY`-switch is activated. This means that this module can react on an email-reply. That is elaborated in the next section in more detail. 

## Storing and receiving information via eMail
As stated above, this whole program is based upon email-communication. Therefore, this program has two main entry-points: the `mainreceiver` and `sendreminder`.

The `mainreceiver` processes emails. At this point, it takes an email from `stdin`, decides which module is responsible for further processing, activates that module, and passes on the email. The decision on which module to choose is based on the **subject of the email**. Precisely, the subject has to be the name of the submodule. That is, to save a webpage, you would send an email with the subject `epub`. Saving a reminder would require an email with the subject `daily`, and, finally, to save a note, the mail would have the subject `remarkable`.

The second entry-point of the program is the `sendreminder`. This script doesn't take any input but puts together an email with the summary of the `remarkable`- and `daily`-module and sends it via a sys-call to sendmail. The call to `sendreminder` is best to be outsourced to `cron`. For me, I receive this summary every morning, automatically.

## Requirements

* mailserver accepting mails
* `sendmail`
* [pandoc](http://pandoc.org/) for `epub`-module
* [TwlyY29/websiteasepub](https://github.com/TwlyY29/websiteasepub) for `epub`-module
* [remind](https://linux.die.net/man/1/remind) for `daily`-module

To configure your mailserver to pipe an incoming mail to `mainreceiver` simply add 
    name-part-of-email-address: "| /etc/mail/smrsh/mainreceiver"
to `/etc/aliases/`. Be careful to set correct permissions and ownership since `sendmail` is a little touchy with those. 

## Installation

coming soon :)

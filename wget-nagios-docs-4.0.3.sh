#!/bin/sh

VER=4.0.3
D=13-04-2014

if [ -d  /tmp/nagios-docs-$VER }; then
rm -rf  /tmp/nagios-docs-$VER
else
mkdir /tmp/nagios-docs-$VER
fi

cd /tmp/nagios-docs-$VER
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/index.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/toc.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/about.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/beginners.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/upgrading.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/monitoring-windows.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/monitoring-linux.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/monitoring-netware.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/monitoring-printers.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/monitoring -r -l 2outers.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/monitoring-publicservices.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/config.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/configmain.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/startstop.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/plugins.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/macros.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/macrolist.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/hostchecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/servicechecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/activechecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/passivechecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/passivechecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/statetypes.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/timeperiods.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/networkreachability.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/notifications.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/cgis.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/extcommands.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/eventhandlers.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/volatileservices.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/freshness.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/distributed.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/redundancy.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/flapping.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/escalations.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/oncallrotation.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/clusters.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/dependencies.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/stalking.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/perfdata.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/downtime.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/adaptive.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/dependencychecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/cachedchecks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/passivestatetranslation.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/checkscheduling.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/cgiincludes.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/objectinheritance.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/objecttricks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/security.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/cgisecurity.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/tuning.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/faststartup.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/largeinstalltweaks.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/nagiostats.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/mrtggraphs.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/integration.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/int-snmptrap.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/int-tcpwrappers.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/addons.html
wget  -r -l 2 http://nagios.sourceforge.net/docs/nagioscore/4/en/pluginapi.html

cd /tmp
 tar cpfz nagios-docs-$VER.tar.gz nagios-docs-VER
cp nagios-docs-$VER-$D.tar.gz /usr/src/packages/SOURCES/


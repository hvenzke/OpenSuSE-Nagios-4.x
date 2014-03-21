#!/bin/sh


URL=http://download.opensuse.org/repositories/server:/monitoring/openSUSE_13.1/src/
LIST=" nagios-business-process-addon-0.9.6-5.1.src.rpm
nagios-eventhandlers-send_messages-0.1.3-2.1.src.rpm
nagios-plugins-1.5-11.1.src.rpm
nagios-plugins-1.5-108.1.src.rpm
nagios-plugins-aacraid-0.3-3.1.src.rpm
nagios-plugins-apache-1.4-1.1.src.rpm
nagios-plugins-apcupsd-1.3-1.1.src.rpm
nagios-plugins-arcconf-0.3-3.1.src.rpm
nagios-plugins-asterisk-0.1-2.1.src.rpm
nagios-plugins-bind-1.3-8.1.src.rpm
nagios-plugins-bl-1.0-2.1.src.rpm
nagios-plugins-bonding-0.002-11.1.src.rpm
nagios-plugins-clamav-1.2-12.1.src.rpm
nagios-plugins-contentage-0.6-11.1.src.rpm
nagios-plugins-count_file-232-1.1.src.rpm
nagios-plugins-diskio-3.2.4-7.1.src.rpm
nagios-plugins-dothill-0.1.0-1.1.src.rpm
nagios-plugins-drbd-0.5.3-4.1.src.rpm
nagios-plugins-equallogic-20121228-1.1.src.rpm
nagios-plugins-hpasm-4.6.3-8.1.src.rpm
nagios-plugins-infortrend-1.1-1.1.src.rpm
nagios-plugins-ipmi-sensor1-1.3-17.1.src.rpm
nagios-plugins-ipmi-sensor2-2.3-2.1.src.rpm
nagios-plugins-logfiles-3.5.3.2-1.1.src.rpm
nagios-plugins-maintenance-1.7-11.1.src.rpm
nagios-plugins-md_raid-0.7.2-4.1.src.rpm
nagios-plugins-megaraid_sas-12-1.1.src.rpm
nagios-plugins-mem-20120618-13.1.src.rpm
nagios-plugins-multipath-1.12-1.1.src.rpm
nagios-plugins-mysql_health-2.1.8.2-12.1.src.rpm
nagios-plugins-nfsmounts-1.0-12.1.src.rpm
nagios-plugins-nis-1.2-33.1.src.rpm
nagios-plugins-obs-1.1-1.1.src.rpm
nagios-plugins-openmanage-3.7.9-1.1.src.rpm
nagios-plugins-openvpn-1.1-2.1.src.rpm
nagios-plugins-printer-0.15-1.1.src.rpm
nagios-plugins-printer_details-20121023-1.1.src.rpm
nagios-plugins-ps-1.0-2.1.src.rpm
nagios-plugins-puppet_agent-1-1.1.src.rpm
nagios-plugins-qlogic_sanbox-1.3-9.1.src.rpm
nagios-plugins-repomd-2.0-1.1.src.rpm
nagios-plugins-rsync-1.02-15.1.src.rpm
nagios-plugins-sar-perf-0.1-10.1.src.rpm
nagios-plugins-sign-0.92-2.1.src.rpm
nagios-plugins-sip-1.3-5.1.src.rpm
nagios-plugins-smart-1.0.1-2.1.src.rpm
nagios-plugins-smb-1.0-2.1.src.rpm
nagios-plugins-snmp-1.1.1-10.1.src.rpm
nagios-plugins-snmp-C-0.6.0-5.1.src.rpm
nagios-plugins-source-service-0.1-3.1.src.rpm
nagios-plugins-spool_page-1.0-1.1.src.rpm
nagios-plugins-symlinks-1.0-3.1.src.rpm
nagios-plugins-tftp-0.11-2.1.src.rpm
nagios-plugins-traffic_limit-0.3-4.1.src.rpm
nagios-plugins-transtec-1.2-2.1.src.rpm
nagios-plugins-tw_cli-0.3.1-7.1.src.rpm
nagios-plugins-ups_alarm-1.0-8.1.src.rpm
nagios-plugins-zypper-1.50-1.1.src.rpm
nagios-rpm-macros-0.08-35.1.src.rpm
nagios-theme-nuvola-1.0.3-9.2.src.rpm
nagios-theme-switcher-1.2-6.1.src.rpm
nagiosgraph-1.4.4-1.1.src.rpm
nagiosgraph-1.4.4-1.5.src.rpm
nagiosgrapher-1.7.1-5.2.src.rpm
nagiosql-3.2.0-8.1.src.rpm
nagircbot-0.0.33-3.1.src.rpm
nagserv-0.0.26-2.1.src.rpm
nagstamon-0.9.11-29.1.src.rpm
nagtrap-1.5.0-2.1.src.rpm
nagvis-1.7.10-1.1.src.rpm
nconf-1.3.0-9.1.src.rpm
ndoutils-2.0.0-30.1.src.rpm
nmon-14i-2.1.src.rpm
nrpe-2.15-29.1.src.rpm
nsca-2.9.1-9.1.src.rpm
nsca-2.9.1-9.3.src.rpm
"
nagios1:/data/oss13.1-srpms # cat ../aa1 | sort >monitoring-srpms
nagios1:/data/oss13.1-srpms # cat monitoring-srpms | awk -F " " '{ print $3 }' >monitoring-srpms-short


for i in $LIST
> do
> wget http://download.opensuse.org/repositories/server:/monitoring/openSUSE_13.1/src/$i
> done

#  Remsnet Spec file for package nagios-plugins v 2.x
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2014 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf

# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via  https://github.com/remsnet/OpenSuSE-Nagios-4.x


Name: nagios-plugins
Summary: The Nagios Plug-Ins
License: GPL-2.0+ and GPL-3.0
Group: System/Monitoring
Version: 2.0
Release: 1.3
Url: http://nagiosplugins.org/
PreReq: permissions
Source0: nagios-plugins-%{version}.tar.gz
Source1: wget-nagios-docs-4.0.3.sh

Source11: nagios-plugins-permissions
Source12: nagios-plugins-README.SuSE
Source13: nagios-plugins-README.SuSE-check_dhcp
Source14: nagios-plugins-README.SuSE-check_icmp
Source15: nagios-plugins-README.SuSE-check_ide_smart
Source16: usr.lib.nagios.plugins.check_dhcp
Source17: usr.lib.nagios.plugins.check_ntp_time
Source18: nagios-plugins.check_cups.sh
Source19: pkg-nagios-plugins-contrib-master-13032014.tar.bz2
Source20: contrib-misc-tarball-1.4.16.tar.gz
Source21: check_radius.pl.tar.gz
Source22: check_xenvm.sh.tar.gz

Patch1:   nagios-plugins-2.0-freeradius.patch
#
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: bind-utils
BuildRequires: dhcp-devel
BuildRequires: fping
%if 0%{?suse_version} > 1210
BuildRequires: libgnutls-devel
%else
BuildRequires: gnutls-devel
%endif
BuildRequires: iputils
BuildRequires: libsmbclient-devel
BuildRequires: mysql-devel
BuildRequires: nagios-devel
BuildRequires: nagios-rpm-macros
BuildRequires: net-snmp-devel
BuildRequires: openldap2-devel
BuildRequires: openssh
BuildRequires: openssl-devel
BuildRequires: perl-Net-SNMP
BuildRequires: postgresql-devel
BuildRequires: procps
BuildRequires: python-devel
BuildRequires: samba-client
BuildRequires: perl-Test-Base
BuildRequires: perl-Test-Unit
BuildRequires: gnutls
BuildRequires: freeradius-client
BuildRequires: freeradius-client-devel
BuildRequires: automake autoconf make gcc flex bison gettext

%if 0%{?suse_version} > 910
BuildRequires: krb5-devel
BuildRequires: rsyslog
%else
BuildRequires: heimdal-devel
%endif
# recommend the old, included checks to allow an easy update - but
# also allow users to deselect some of the new sub-packages
Recommends: %{name}-bgpstate
Recommends: %{name}-breeze
Recommends: %{name}-by_ssh
Recommends: %{name}-cluster
Recommends: %{name}-dhcp
Recommends: %{name}-dig
Recommends: %{name}-disk
Recommends: %{name}-disk_smb
Recommends: %{name}-dns
Recommends: %{name}-dummy
Recommends: %{name}-file_age
Recommends: %{name}-flexlm
Recommends: %{name}-http
Recommends: %{name}-icmp
Recommends: %{name}-ide_smart
Recommends: %{name}-ifoperstatus
Recommends: %{name}-ifstatus
Recommends: %{name}-ircd
Recommends: %{name}-linux_raid
Recommends: %{name}-load
Recommends: %{name}-log
Recommends: %{name}-mailq
Recommends: %{name}-mrtg
Recommends: %{name}-mrtgtraf
Suggests: %{name}-nagios
Recommends: %{name}-netapp
Recommends: %{name}-nt
Recommends: %{name}-ntp_peer
Recommends: %{name}-ntp_time
Recommends: %{name}-nwstat
Recommends: %{name}-oracle
Recommends: %{name}-overcr
Recommends: %{name}-ping
Recommends: %{name}-procs
Recommends: %{name}-real
Recommends: %{name}-rpc
%ifnarch ppc ppc64 sparc sparc64 s390 s390x
Recommends: %{name}-sensors
%endif
Recommends: %{name}-smtp
Recommends: %{name}-ssh
Recommends: %{name}-swap
Recommends: %{name}-tcp
Recommends: %{name}-time
Recommends: %{name}-ups
Recommends: %{name}-users
Recommends: %{name}-wave
Suggests: %{name}-xenvm
Suggests: %{name}-cups


%define apt_get_command %{_bindir}/apt-get
%define qstat_command %{_bindir}/qstat
##%define nagios_plugindir %{_libdir}/nagios/plugins

%description
Nagios is a program that will monitor hosts and services on your
network, and to email or page you when a problem arises or is resolved.
Nagios runs on a unix server as a background or daemon process,
intermittently running checks on various services that you specify.

The actual service checks are performed by separate "plugin" programs
which return the status of the checks to Nagios.

This package contains those plugins.

%package extras
Summary: Plug-Ins which depend on additional packages
Group: System/Monitoring
Suggests: %{name}-apt
Recommends: %{name}-fping
Suggests: %{name}-game
Requires: %{name}-common = %{version}
Recommends: %{name}-hpjd
Recommends: %{name}-ldap
Recommends: %{name}-mysql
Recommends: %{name}-pgsql
Recommends: %{name}-snmp

%description extras
These are additional monitoring plug-ins for Nagios or Icinga.

They depend on other packages which have to be installed.

%package all
Summary: All Nagios-Plugin checks
Group: System/Monitoring
Recommends: %{name}-apt
Recommends: %{name}-bgpstate
Recommends: %{name}-bind
Recommends: %{name}-bonding
Recommends: %{name}-breeze
Recommends: %{name}-by_ssh
Recommends: %{name}-clamav
Recommends: %{name}-cluster
Recommends: %{name}-contentage
Recommends: %{name}-cups
Recommends: %{name}-dhcp
Recommends: %{name}-dig
Recommends: %{name}-disk
Recommends: %{name}-diskio
Recommends: %{name}-disk_smb
Recommends: %{name}-dns
Recommends: %{name}-dummy
Recommends: %{name}-file_age
Recommends: %{name}-flexlm
Recommends: %{name}-fping
Recommends: %{name}-game
Recommends: %{name}-hpasm
Recommends: %{name}-hpjd
Recommends: %{name}-http
Recommends: %{name}-icmp
Recommends: %{name}-ide_smart
Recommends: %{name}-ifoperstatus
Recommends: %{name}-ifstatus
Recommends: %{name}-ipmi-sensor1
Recommends: %{name}-ircd
Recommends: %{name}-ldap
Recommends: %{name}-linux_raid
Recommends: %{name}-load
Recommends: %{name}-log
Recommends: %{name}-maintenance
Recommends: %{name}-mem
Recommends: %{name}-mailq
Recommends: %{name}-mrtg
Recommends: %{name}-mrtgtraf
Recommends: %{name}-mysql
Recommends: %{name}-mysql_health
Recommends: %{name}-nagios
Recommends: %{name}-netapp
Recommends: %{name}-nfsmounts
Recommends: %{name}-nis
Recommends: %{name}-nt
Recommends: %{name}-ntp_peer
Recommends: %{name}-ntp_time
Recommends: %{name}-nwstat
Recommends: %{name}-oracle
Recommends: %{name}-overcr
Recommends: %{name}-pgsql
Recommends: %{name}-ping
Recommends: %{name}-procs
Recommends: %{name}-qlogic_sanbox
Recommends: %{name}-radius
Recommends: %{name}-real
Recommends: %{name}-rpc
Recommends: %{name}-rsync
%ifnarch ppc ppc64 sparc sparc64 s390 s390x
Recommends: %{name}-sensors
%endif
Recommends: %{name}-smtp
Recommends: %{name}-snmp
Recommends: %{name}-ssh
Recommends: %{name}-swap
Recommends: %{name}-tcp
Recommends: %{name}-time
Recommends: %{name}-ups
Recommends: %{name}-ups_alarm
Recommends: %{name}-users
Recommends: %{name}-wave
Recommends: %{name}-xenvm
Recommends: %{name}-zypper

%description all
This virtual package recommends all currently available, official
Nagios plugins.

%package perlmods
Summary: perl modules for Nagios Perl Plugins
Group: System/Monitoring
Requires: perl

%description perlmods
CPAN perl modules for Nagios Perl Plugins
Class-Accessor-0.34
Config-Tiny-2.14
Math-Calc-Units-1.07
Module-Build-0.4007
Module-Implementation-0.07
Module-Metadata-1.000014
Module-Runtime-0.013
Nagios-Plugin-0.36
Params-Validate-1.08
Perl-OSType-1.003
Test-Simple-0.98
Try-Tiny-0.18
parent-0.226
version-0.9903


%package apt
Summary: Check for software updates via apt-get
Group: System/Monitoring
Requires: perl-Alien-SDL perl-Alien-Tidyp

%description apt
This plugin checks for software updates on systems that use package management
systems based on the apt-get command found in Debian GNU/Linux


%package bgpstate
Summary: Monitor BGP sessions
Group: System/Monitoring
Requires: whois

%description bgpstate
Perl bgpstate plugin monitors all BGP sessions.



%package ajp
Summary: Monitor  sessions
Group: System/Monitoring
Requires: java

%description ajp

Nagios plugin for JBoss monitoring  - check_ajp
see http://www.joedog.org/pub/AJP/check_ajp.txt
see http://blog.devnu11.net/2010/11/nagios-plugin-for-jboss-monitoring-check_ajp/


%package dbi
Summary: Monitor DBI database sessions
Group: System/Monitoring
Requires: libdbi1 libdbi-drivers libdbi-drivers-dbd-mysql libdbi-drivers-dbd-pgsql

%description dbi
check_dbi
see http://exchange.nagios.org/directory/Plugins/Databases/Oracle/check_db/details

%package misc
Summary: Nagios MISC Plugin package
Group: System/Monitoring
Requires: perl coreutils bash tar gzip bzip2 python

%description misc
Re-packaged nagios 1.4.16 contrib plugins


%package haproxy
Summary: Monitor haproxy
Group: System/Monitoring
Requires: haproxy

%description haproxy
HAProxy is an open source TCP/HTTP load balancer, commonly used to improve the performance of web sites and services by spreading requests across multiple servers
https://github.com/polymorf/check_haproxy

%package clamav
Summary: Monitor clamav
Group: System/Monitoring
Requires: clamav

%description clamav
check_clamav see http://exchange.nagios.org/directory/Plugins/Anti-2DVirus/ClamAV/ClamAV-check-plugin/details

%package smstools
Summary: Monitor smstools
Group: System/Monitoring
Requires: smstools

%description smstools
check_smstools see http://exchange.nagios.org/directory/Plugins/Hardware/Mobile-Devices/check_smstools/details

%package uptime
Summary: Monitor system uptime
Group: System/Monitoring
Requires: coreutils

%description uptime
see http://exchange.nagios.org/directory/Plugins/Operating-Systems/Linux/check_uptime/details

%package checksums
Summary: Monitor checksums
Group: System/Monitoring
Requires: coreutils

%description checksums
check_checksums
update_checksums



%package breeze
Summary: Monitor Breezecom wireless equipment
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: net-snmp
Requires: perl

%description breeze
This plugin reports the signal strength of a Breezecom wireless equipment.


%package by_ssh
Summary: Execute checks via SSH
Group: System/Monitoring
Requires: openssh

%description by_ssh
This plugin uses SSH to execute commands on a remote host.

The most common mode of use is to refer to a local identity file with
the '-i' option. In this mode, the identity pair should have a null
passphrase and the public key should be listed in the authorized_keys
file of the remote host. Usually the key will be restricted to running
only one command on the remote server. If the remote SSH server tracks
invocation arguments, the one remote program may be an agent that can
execute additional commands as proxy.


%package cluster
Summary: Host/Service Cluster Plugin
Group: System/Monitoring

%description cluster
Provides the check_cluster plugin to check Services and/or Hosts running
as a cluster.

Example:
  check_cluster -s -d 2,0,2,0 -c @3:
Will alert critical if there are 3 or more service data points in a non-OK
state.


%package common
Summary: Libraries for Nagios plugins
Group: System/Monitoring
Provides: nagios-plugins-libs = %{version}-%{release}
Obsoletes: nagios-plugins-libs < %{version}

%description common
This package includes the libraries (scripts) that are included by many
of the standard checks.


%package dhcp
Summary: Check DHCP servers
Group: System/Monitoring
%if 0%{?suse_version}
Recommends: apparmor-parser
%else
Requires: apparmor-parser
%endif

%description dhcp
This plugin tests the availability of DHCP servers on a network.

Please read
/usr/share/doc/packages/nagios-plugins-dhcp/README.SuSE-check_dhcp
for details how to setup this check.


%package dig
Summary: Test DNS service via dig
Group: System/Monitoring
Requires: %{_bindir}/dig

%description dig
This plugin test the DNS service on the specified host using dig.


%package disk
Summary: Check disk space
Group: System/Monitoring

%description disk
This plugin checks the amount of used disk space on a mounted file system and
generates an alert if free space is less than one of the threshold values.


%package disk_smb
Summary: Check SMB Disk
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl

%description disk_smb
Check the amount of used disk space on a remote Samba or Windows share and
generate an alert if free space is less than one of the threshold values.


%package dns
Summary: Obtain the IP address for a given host/domain
Group: System/Monitoring
Requires: %{_bindir}/nslookup

%description dns
This plugin uses the nslookup program to obtain the IP address for the given
host/domain query.

An optional DNS server to use may be specified. If no DNS server is specified,
the default server(s) specified in /etc/resolv.conf will be used.


%package dummy
Summary: Dummy check
Group: System/Monitoring

%description dummy
This plugin will simply return the state corresponding to the numeric value of
the <state> argument with optional text.


%package file_age
Summary: Check the age/size of files
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl

%description file_age
This plugin will check either the age of files or their size.


%package flexlm
Summary: Check flexlm license managers
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl

%description flexlm
Flexlm license managers usually run as a single server or three servers and a
quorum is needed. The plugin return OK if 1 (single) or 3 (triple) servers
are running, CRITICAL if 1(single) or 3 (triple) servers are down, and WARNING
if 1 or 2 of 3 servers are running.


%package fping
Summary: Fast ping check
Group: System/Monitoring
Requires: fping

%description fping
This plugin will use the fping command to ping the specified host for
a fast check. Note that it is necessary to set the suid flag on fping.


%package game
Summary: Gameserver check
Group: System/Monitoring
Requires: %{qstat_command}

%description game
Check connections to game servers. This plugin uses the 'qstat' command, the
popular game server status query tool.


%package hpjd
Summary: Check status of an HP printer
Group: System/Monitoring
Requires: net-snmp

%description hpjd
This plugin tests the STATUS of an HP printer with a JetDirect card.


%package http
Summary: Test the HTTP service on the specified host
Group: System/Monitoring

%description http
This plugin tests the HTTP service on the specified host. It can test
normal (http) and secure (https) servers, follow redirects, search for
strings and regular expressions, check connection times, and report on
certificate expiration times.


%package icmp
Summary: Send ICMP packets to the specified host
Group: System/Monitoring

%description icmp
This plugin sends ICMP (ping) packets to the specified host. You can
specify different RTA factors and acceptable packet loss.

Please read
/usr/share/doc/packages/nagios-plugins-icmp/README.SuSE-check_icmp
for details how to setup this check.


%package ide_smart
Summary: Check local hard drive
Group: System/Monitoring

%description ide_smart
This plugin checks a local hard drive with the (Linux specific) SMART
interface.

Please read
/usr/share/doc/packages/nagios-plugins-ide_smart/README.SuSE-check_ide_smart
for details how to setup this check.


%package ifoperstatus
Summary: Monitor network interfaces
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl-Net-SNMP

%description ifoperstatus
This plugin monitors operational status of a particular network interface on
the target host.


%package ifstatus
Summary: Monitor operational status network interfaces
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl-Net-SNMP

%description ifstatus
This plugin monitors operational status of each network interface on the target
host.


%package ircd
Summary: Check an IRCd server
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl

%description ircd
Monitor the status of an Internet Relay Chat daemon (IRCd) with this check.


%package ldap
Summary: Test a LDAP server
Group: System/Monitoring

%description ldap
Monitor access to a Lightweight Directory Access Protocol (LDAP) server.

This package includes the 'check_ldap' and 'check_ldaps' plugins.


%package linux_raid
Summary: Check Linux software RAIDs
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl

%description linux_raid
This plugin checks the status of a local Linux software RAID via the
/proc/mdstat interface.


%package load
Summary: Test the current system load average
Group: System/Monitoring

%description load
This plugin tests the current system load average.


%package log
Summary: Log file pattern detector
Group: System/Monitoring
Requires: %{name}-common = %{version}

%description log
This plugin provides a log file pattern detector - excluding old
logfile entries and searching for the given query.


%package mailq
Summary: Check mail queues
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl
%if 0%{?suse_version}
Requires: smtp_daemon
%endif

%description mailq
This plugin checks the number of messages in the mail queue (supports multiple
sendmail queues, qmail).


%package mrtg
Summary: Check average or maximum value in an MRTG logfile
Group: System/Monitoring
Recommends: mrtg

%description mrtg
This plugin will check either the average or maximum value of one of the
two variables recorded in an MRTG log file.


%package mrtgtraf
Summary: Check incoming/outgoing transfer rates of a router
Group: System/Monitoring
Recommends: mrtg

%description mrtgtraf
This plugin will check the incoming/outgoing transfer rates of a router,
switch, etc recorded in an MRTG log. If the newest log entry is older
than <expire_minutes>, a WARNING status is returned. If either the
incoming or outgoing rates exceed the <icl> or <ocl> thresholds (in
Bytes/sec), a CRITICAL status results. If either of the rates exceed
the <iwl> or <owl> thresholds (in Bytes/sec), a WARNING status results.


%package mysql
Summary: Test a MySQL DBMS
Group: System/Monitoring

%description mysql
This plugin tests a MySQL DBMS to determine whether it is active and
accepting queries. It provides the two checks: 'check_mysql' and
'check_mysql_query'.


%package nagios
Summary: Check nagios server
Group: System/Monitoring
Requires: monitoring_daemon

%description nagios
This plugin checks the status of the Nagios process on the local machine. The
plugin will check to make sure the Nagios status log is no older than the
number of minutes specified by the expires option.

It also checks the process table for a process matching the command argument.


%package netapp
Summary: Check NetApp filer
Group: System/Monitoring
Requires: perl-Net-SNMP

%description netapp
Check the the status of a NetApp filer via SNMP.


%package nt
Summary: Collect data from NSClient service
Group: System/Monitoring

%description nt
This plugin collects data from the NSClient service running on a
Windows NT/2000/XP/2003 server.


%package ntp_peer
Summary: Check health of an NTP server
Group: System/Monitoring

%description ntp_peer
Use this plugin to check the health of an NTP server. It supports
checking the offset with the sync peer, the jitter and stratum.

This plugin will not check the clock offset between the local host and NTP
server; please use check_ntp_time for that purpose.


%package ntp_time
Summary: Check clock offset with the ntp server
Group: System/Monitoring
Provides: %{name}-ntp = %{version}-%{release}
%if 0%{?suse_version}
Recommends: apparmor-parser
%else
Requires: apparmor-parser
%endif

%description ntp_time
This plugin checks the clock offset between the local host and a remote NTP
server. It is independent of any commandline programs or external libraries.


%package nwstat
Summary: Check MRTGEXT NLM running
Group: System/Monitoring

%description nwstat
This plugin attempts to contact the MRTGEXT NLM running on a Novell server to
gather the requested system information.


%package oracle
Summary: Check Oracle status
Group: System/Monitoring
Requires: %{name}-common = %{version}

%description oracle
Check Oracle database health status.


%package overcr
Summary: Check Over-CR collector daemon
Group: System/Monitoring

%description overcr
This plugin attempts to contact the Over-CR collector daemon running on the
remote UNIX server in order to gather the requested system information.


%package pgsql
Summary: Test a PostgreSQL DBMS
Group: System/Monitoring

%description pgsql
This plugin tests a PostgreSQL DBMS to determine whether it is active and
accepting queries. It provides the check 'check_pgsql'.


%package ping
Summary: Check connection statistics
Group: System/Monitoring
Requires: iputils

%description ping
Use ping to check connection statistics for a remote host.

This plugin uses the ping command to probe the specified host for packet loss
(percentage) and round trip average (milliseconds).

%package procs
Summary: Check processes
Group: System/Monitoring

%description procs
This plugin checks the number of currently running processes and generates
WARNING or CRITICAL states if the process count is outside the specified
threshold ranges.

The process count can be filtered by process owner, parent process PID, current
state (e.g., 'Z'), or may be the total number of running processes.


%package radius
Summary: Test RADIUS server
Group: System/Monitoring
Requires: freeradius-client

%description radius
This plugin tests a RADIUS server to see if it is accepting connections. The
server to test must be specified in the invocation, as well as a user name and
password. A configuration file may also be present. The format of the
configuration file is described in the radiusclient library sources. The
password option presents a substantial security issue because the password can
possibly be determined by careful watching of the command line in a process
listing. This risk is exacerbated because nagios will run the plugin at regular
predictable intervals. Please be sure that the password used does not allow
access to sensitive system resources.

%package real
Summary: Test REAL service
Group: System/Monitoring

%description real
This plugin will attempt to open an RTSP connection with the host. Successul
connects return STATE_OK, refusals and timeouts return STATE_CRITICAL, other
errors return STATE_UNKNOWN. Successful connects, but incorrect reponse
messages from the host result in STATE_WARNING return values.


%package rpc
Summary: Check RPC service
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: perl
Requires: rpcbind

%description rpc
Check if a rpc service is registered and running using rpcinfo.


%ifnarch ppc ppc64 sparc sparc64 s390 s390x
%package sensors
Summary: Check hardware status using lm_sensors
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: grep
Requires: sensors

%description sensors
This plugin checks hardware status using the lm_sensors package.
%endif

%package smtp
Summary: Check SMTP connections
Group: System/Monitoring

%description smtp
This plugin will attempt to open an SMTP connection with the given host.

%package snmp
Summary: SNMP monitoring
Group: System/Monitoring
Requires: net-snmp

%description snmp
The Simple Network Management Protocol (SNMP) can be used to monitor
network-attached devices for conditions that warrant administrative attention.

This package includes the 'check_snmp' plugin for Nagios or Icinga.


%package ssh
Summary: Check SSH service
Group: System/Monitoring

%description ssh
Try to connect to an SSH server at specified server and port.


%package swap
Summary: Check swap space
Group: System/Monitoring

%description swap
Check swap space on local machine.


%package tcp
Summary: Tests TCP and UDP connections
Group: System/Monitoring
Provides: %{name}-clamd = %{version}-%{release}
Provides: %{name}-ftp = %{version}-%{release}
Provides: %{name}-imap = %{version}-%{release}
Provides: %{name}-jabber = %{version}-%{release}
Provides: %{name}-nntp = %{version}-%{release}
Provides: %{name}-nntps = %{version}-%{release}
Provides: %{name}-pop = %{version}-%{release}
Provides: %{name}-simap = %{version}-%{release}
Provides: %{name}-spop = %{version}-%{release}
Provides: %{name}-ssmtp = %{version}-%{release}
Provides: %{name}-udp = %{version}-%{release}

%description tcp
This plugin tests TCP connections with the specified host (or unix socket).

This package contains the following checks:
* check_clamd
* check_ftp
* check_imap
* check_jabber
* check_nntp
* check_nntps
* check_pop
* check_simap
* check_spop
* check_ssmtp
* check_tcp
* check_udp


%package time
Summary: Check the time on the specified host
Group: System/Monitoring

%description time
This plugin will check the time on the specified host.


%package ups
Summary: Test UPS service on the specified host
Group: System/Monitoring

%description ups
This plugin tests the UPS service on the specified host.

Network UPS Tools from www.networkupstools.org must be running for this plugin
to work.


%package users
Summary: Check number of users currently logged in
Group: System/Monitoring

%description users
This plugin checks the number of users currently logged in on the local system
and generates an error if the number exceeds the thresholds specified.

%package wave
Summary: Check wave signal strength
Group: System/Monitoring
Requires: %{name}-common = %{version}
Requires: net-snmp
Requires: perl

%description wave
Check the wave signal strength via SNMP.


%package xenvm
Summary: Check available XEN VMs
Group: System/Monitoring
Requires: xen

%description xenvm
Checks the number of Xen VMs running on a machine and returns a warning
or a critical message if the number exceeds the thresholds specified.

%package cups
Summary: Check cups service
Group: System/Monitoring
Requires: cups-client

%description cups
Check the status of a remote CUPS server, all printers there
or one selected. It can also check queue there:
it will provide the size of the queue of age of queue.


%package contrib
Summary: Legacy 1.4.16 nagios contrib plugins
Group: System/Monitoring
Requires: cups-client

%description contrib
repackaged Legacy 1.4.16 nagios contrib plugins


%prep
%setup -q -n %{name}-%{version}

# check_radius patch , but incomplete
##%patch1 -p0

%{__mkdir_p} example/permissions.d
%{__cp} %{S:11} example/permissions.d/%{name}
%{__cp} %{S:12} ./README.SuSE
%{__cp} %{S:13} ./README.SuSE-check_dhcp
%{__cp} %{S:14} ./README.SuSE-check_icmp
%{__cp} %{S:15} ./README.SuSE-check_ide_smart

# https://github.com/bzed/pkg-nagios-plugins-contrib
mkdir contrib
cd contrib
%{__tar} xpfj %{S:19}
%{__mv} pkg-nagios-plugins-contrib-master/* .
%{__rm} -rf README common.mk pkg-nagios-plugins-contrib-master

# nagios-plugins tarball contrib v 1.4.19
%{__tar} xpfz %{S:20}
%{__tar} xpfz %{S:21} -C misc
%{__tar} xpfz %{S:22} -C misc
#
%{__cp} %{S:1}  misc/wget-nagios-docs-4.0.3.sh
#
cd ..

echo "" >README.contrib
echo " re-patching nagios plugins 2.x with contrib from " >README.contrib
echo " managed contrib SOURCE URL : https://github.com/bzed/pkg-nagios-plugins-contrib " >>README.contrib
echo " and from nagios-plugins tarball contrib v 1.4.19 " >>README.contrib
echo " Please File Bugs to the orign Plugin contributors" >README.contrib
echo "" >README.contrib




%build
export CFLAGS="%optflags -fno-strict-aliasing -DLDAP_DEPRECATED"
%configure \
        --enable-static=no \
        --enable-extra-opts \
        --libexecdir=%{nagios_plugindir} \
        --sysconfdir=%{nagios_sysconfdir} \
        --with-apt-get-command=%{apt_get_command} \
        --with-cgiurl=/nagios/cgi-bin \
        --with-fping-command=%{_sbindir}/fping \
        --with-ipv6 \
        --with-openssl=%{_prefix} \
        --with-perl=%{_bindir}/perl \
        --with-pgsql=%{_prefix} \
        --with-ping6-command='/bin/ping6 -n -U -w %d -c %d %s' \
        --with-ps-command="/bin/ps axwo 'stat uid pid ppid vsz rss pcpu etime comm args'" \
        --with-ps-format='%s %d %d %d %d %d %f %s %s %n' \
        --with-ps-cols=10 \
        --with-ps-varlist='procstat,&procuid,&procpid,&procppid,&procvsz,&procrss,&procpcpu,procetime,procprog,&pos' \
        --with-rpcinfo-command=%{_sbindir}/rpcinfo \
        --with-qstat-command=%{qstat_command} \
        --with-mysql=%{_prefix} \
        --enable-threads=pth \
        --enable-extra-opts \
        --enable-perl-modules \
         --with-gnutls \
        --disable-rpath \
        --without-radius
make all %{?jobs:-j%jobs}

%install
sed -i 's,^MKINSTALLDIRS.*,MKINSTALLDIRS = ../mkinstalldirs,' po/Makefile

%makeinstall install-root
%{__mkdir_p} -m 0755 $RPM_BUILD_ROOT/etc
%{__mkdir_p} -m 0755 $RPM_BUILD_ROOT/etc/nagios
%{__mkdir_p} -m 0755 $RPM_BUILD_ROOT/var

#########################

%{__install} -m 0755 %{S:18} $RPM_BUILD_ROOT%{nagios_plugindir}/check_cups
# provide check_host and check_rta_multi as on Debian
if [ -x %{buildroot}/%{nagios-plugindir}/check_icmp ] ; then
        test -f %{buildroot}/%{nagios-plugindir}/check_host && rm -f %{buildroot}/%{nagios-plugindir}/check_host
        test -f %{buildroot}/%{nagios-plugindir}/check_rta_multi && rm -f %{buildroot}/%{nagios-plugindir}/check_rta_multi
        ln -s %{nagios-plugindir}/check_icmp %{buildroot}/%{nagios-plugindir}/check_host ;
        ln -s %{nagios-plugindir}/check_icmp %{buildroot}/%{nagios-plugindir}/check_rta_multi ;
fi

# contrib patching in

%{__install} -m 0755 contrib/check_bgpstate/check_bgpstate %{buildroot}/%{nagios_plugindir}/check_bgpstate
%{__install} -m 0755 contrib/check_ajp/check_ajp %{buildroot}/%{nagios_plugindir}/check_ajp
%{__install} -m 0755 contrib/check_clamav/check_clamav %{buildroot}/%{nagios_plugindir}/check_clamav
%{__install} -m 0755 contrib/check_checksums/check_checksums %{buildroot}/%{nagios_plugindir}/check_checksums
%{__install} -m 0755 contrib/check_checksums/update_checksums %{buildroot}/%{nagios_plugindir}/update_checksums
%{__install} -m 0755 contrib/check_raid/check_raid %{buildroot}/%{nagios_plugindir}/check_linux_raid
%{__install} -m 0755 contrib/misc/check_netapp.pl %{buildroot}/%{nagios_plugindir}/check_netapp
%{__install} -m 0755 contrib/misc/check_radius.pl %{buildroot}/%{nagios_plugindir}/check_radius1
%{__install} -m 0755 contrib/misc/check_xenvm.sh %{buildroot}/%{nagios_plugindir}/check_xenvm

%{__install} -m 0755 contrib/check_haproxy/check_haproxy %{buildroot}/%{nagios_plugindir}/check_haproxy
%{__install} -m 0755 contrib/check_smstools/bin/check_smstools %{buildroot}/%{nagios_plugindir}/check_smstools


%{__mkdir_p} -m 0755 %{buildroot}/etc/nagios/contrib
%{__install} -m 0755 contrib/check_bgpstate/bgpstate.cfg %{buildroot}/etc/nagios/contrib/bgpstate.cfg
%{__install} -m 0755 contrib/check_ajp/ajp.cfg %{buildroot}/etc/nagios/contrib/ajp.cfg
%{__install} -m 0755 contrib/check_haproxy/haproxy.cfg /%{buildroot}/etc/nagios/contrib/haproxy.cfg
%{__install} -m 0644 contrib/check_smstools/README.check_smstools /%{buildroot}/etc/nagios/contrib/README.check_smstools

# repack old MISC plugins as subpkg contrib
%{__mkdir_p} -m 0755 %{buildroot}/usr/lib/nagios/contrib
%{__install} -m 0755 contrib/misc/*.pl %{buildroot}/usr/lib/nagios/contrib
%{__install} -m 0755 contrib/misc/*.sh %{buildroot}/usr/lib/nagios/contrib
%{__install} -m 0755 contrib/misc/*.py %{buildroot}/usr/lib/nagios/contrib
%{__install} -m 0755 contrib/misc/check_*_* %{buildroot}/usr/lib/nagios/contrib

%{__mkdir_p} -m 0755 %{buildroot}/usr/share/doc/packages/nagios-plugins/contrib
%{__install} -m 644  contrib/misc/tarballs/*  %{buildroot}//usr/share/doc/packages/nagios-plugins/contrib
%{__install} -m 0644 contrib/misc/README.TXT  %{buildroot}/usr/share/doc/packages/nagios-plugins/contrib

# fix "use lib" on installed perl checks
pushd $RPM_BUILD_ROOT%{nagios_plugindir}
for file in $(find -maxdepth 1 -type f); do
    sed -i 's|use lib "nagios/plugins".*;|use lib "%{nagios_plugindir}";|g;
            s|use lib "/usr/local/nagios/libexec".*;|use lib "%{nagios_plugindir}";|g' $file
done

# provide *.pl files for backwards compatibility
for i in check_linux_raid check_netapp check_radius1 check_haproxy ; do
        ln -s $i ${i}.pl
done
popd


# check_sensors makes no sense on some archs
%ifarch ppc ppc64 sparc sparc64 s390 s390x
%{__rm} -f %{buildroot}%{nagios_plugindir}/check_sensors
%endif
# install Apparmor profiles
mkdir -p %{buildroot}/%{_sysconfdir}/apparmor.d/
install -m 644 %{SOURCE16} %{buildroot}/%{_sysconfdir}/apparmor.d/
install -m 644 %{SOURCE17} %{buildroot}/%{_sysconfdir}/apparmor.d/

# inform the users about the deprecated nagios-plugins-extras package
cat >> README.SuSE-deprecated << EOF
The nagios-plugins-extras package is deprecated.

The checks formerly packaged here are now packaged separately.

For example, to install check_fping just install nagios-plugins-fping.
EOF

cat >> README.SuSE-all << EOF
This virtual package recommends all currently available, official
Nagios plugins.

It does not require the subpackages as you might not have all needed
dependend packages available.
EOF

# find locale files
%find_lang %{name}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre contrib

if [ ! -x /usr/local/bin/perl ] && [  -x /usr/bin/perl ] ; then
        ln -s /usr/bin/perl /usr/local/bin/perl
fi


%post dhcp
# in case somebody uses the permissions file we provide
# in docdir, run permission here
if [ -f %{_sysconfdir}/permissions.d/nagios-plugins ]; then
%if 0%{?suse_version} < 1210
%run_permissions
%else
        %set_permissions nagios-plugins
%endif
fi

%post icmp
if [ -f %{_sysconfdir}/permissions.d/nagios-plugins ]; then
# in case somebody uses the permissions file we provide
# in docdir, run permission here
%if 0%{?suse_version} < 1210
%run_permissions
%else
%set_permissions nagios-plugins
%endif
fi

%post ide_smart
if [ -f %{_sysconfdir}/permissions.d/nagios-plugins ]; then
# in case somebody uses the permissions file we provide
# in docdir, run permission here
%if 0%{?suse_version} < 1210
%run_permissions
%else
%set_permissions nagios-plugins
%endif
fi

%files
%defattr(-,root,root)
%doc README*
%doc contrib/misc/wget-nagios-docs-4.0.3.sh

%files all
%defattr(-,root,root)
%doc README.SuSE-all

%files apt
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_apt

%files bgpstate
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_bgpstate
%{nagios_sysconfdir}/contrib/bgpstate.cfg

%files breeze
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_breeze

%files by_ssh
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_by_ssh

%files cluster
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_cluster

%files common -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS ACKNOWLEDGEMENTS AUTHORS INSTALL SUPPORT ChangeLog CODING COPYING FAQ LEGAL
%doc NEWS README REQUIREMENTS SUPPORT THANKS README.SuSE config.log
%doc example
%dir %{nagios_libdir}
%dir %{nagios_plugindir}
%defattr(0755,root,root)
%{nagios_plugindir}/negate
%{nagios_plugindir}/urlize
%{nagios_plugindir}/utils.sh
%attr(0644,root,root) %{nagios_plugindir}/utils.pm

%files dhcp
%defattr(-,root,root)
%doc README.SuSE-check_dhcp
%dir %{nagios_plugindir}
%dir %{_sysconfdir}/apparmor.d
%attr(0755,root,root) %{nagios_plugindir}/check_dhcp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/apparmor.d/usr.lib.nagios.plugins.check_dhcp

%files dig
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_dig

%files disk
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_disk

%files disk_smb
%defattr(0755,root,root)
%{nagios_plugindir}/check_disk_smb

%files dns
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_dns

%files dummy
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_dummy

%files extras
%defattr(0644,root,root,0755)
%doc README.SuSE-deprecated

%files file_age
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_file_age

%files flexlm
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_flexlm

%files fping
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_fping

%files game
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_game

%files hpjd
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_hpjd

%files http
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_http

%files icmp
%defattr(-,root,root)
%doc README.SuSE-check_icmp
%dir %{nagios_plugindir}
%attr(0755,root,root) %{nagios_plugindir}/check_icmp

%files ifoperstatus
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ifoperstatus

%files ifstatus
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ifstatus

%files ide_smart
%defattr(-,root,root)
%doc README.SuSE-check_ide_smart
%dir %{nagios_plugindir}
%attr(0755,root,root) %{nagios_plugindir}/check_ide_smart

%files ircd
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ircd

%files ldap
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ldap
%{nagios_plugindir}/check_ldaps

%files linux_raid
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_linux_raid
%{nagios_plugindir}/check_linux_raid.pl

%files load
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_load

%files log
%defattr(0755,root,root)
%{nagios_plugindir}/check_log

%files mailq
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_mailq

%files mrtg
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_mrtg

%files mrtgtraf
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_mrtgtraf

%files mysql
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_mysql
%{nagios_plugindir}/check_mysql_query

%files nagios
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_nagios

%files netapp
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_netapp
%{nagios_plugindir}/check_netapp.pl

%files nt
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_nt


%files ajp
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ajp
%{nagios_sysconfdir}/contrib/ajp.cfg

%files dbi
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_dbi

%files haproxy
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_haproxy
%{nagios_plugindir}/check_haproxy.pl
%{nagios_sysconfdir}/contrib/haproxy.cfg

%files clamav
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_clamav

%files smstools
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_smstools
%{nagios_sysconfdir}/contrib/README.check_smstools

%files uptime
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_uptime

%files checksums
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_checksums
%{nagios_plugindir}/update_checksums

%files ntp_peer
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ntp_peer

%files ntp_time
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ntp
%{nagios_plugindir}/check_ntp_time
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/apparmor.d/usr.lib.nagios.plugins.check_ntp_time

%files nwstat
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_nwstat

%files oracle
%defattr(0755,root,root)
%{nagios_plugindir}/check_oracle

%files overcr
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_overcr

%files pgsql
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_pgsql

%files ping
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ping

%files procs
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_procs

%files radius
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_radius1
%{nagios_plugindir}/check_radius1.pl

%files real
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_real

%files rpc
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_rpc

%ifnarch ppc ppc64 sparc sparc64 s390 s390x
%files sensors
%defattr(0755,root,root)
%{nagios_plugindir}/check_sensors
%endif

%files smtp
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_smtp

%files snmp
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_snmp

%files ssh
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ssh

%files swap
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_swap

%files tcp
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_clamd
%{nagios_plugindir}/check_ftp
%{nagios_plugindir}/check_imap
%{nagios_plugindir}/check_jabber
%{nagios_plugindir}/check_nntp
%{nagios_plugindir}/check_nntps
%{nagios_plugindir}/check_pop
%{nagios_plugindir}/check_simap
%{nagios_plugindir}/check_spop
%{nagios_plugindir}/check_ssmtp
%{nagios_plugindir}/check_tcp
%{nagios_plugindir}/check_udp

%files time
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_time

%files ups
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_ups

%files users
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_users

%files wave
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_wave

%files xenvm
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_xenvm

%files cups
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_cups

%files contrib
%defattr(0755,root,root)
%dir %{nagios_plugindir}
%dir %{_libdir}/nagios/contrib
%{_libdir}/nagios/contrib/*

%dir %{_docdir}/nagios-plugins/contrib
%{_docdir}/nagios-plugins/contrib/README.TXT
%{_docdir}/nagios-plugins/contrib/*.gz

%files perlmods
%defattr(0755,root,root)
%dir %{nagios_plugindir}
/usr/perl/bin/ucalc
%dir  /usr/perl/lib/Class
/usr/perl/bin/ucalc
/usr/perl/lib/Class/Accessor.pm
/usr/perl/lib/Class/Accessor/Fast.pm
/usr/perl/lib/Class/Accessor/Faster.pm
/usr/perl/lib/Config/Tiny.pm
/usr/perl/lib/Math/Calc/Units.pm
/usr/perl/lib/Math/Calc/Units/Compute.pm
/usr/perl/lib/Math/Calc/Units/Convert.pm
/usr/perl/lib/Math/Calc/Units/Convert/Base.pm
/usr/perl/lib/Math/Calc/Units/Convert/Base2Metric.pm
/usr/perl/lib/Math/Calc/Units/Convert/Byte.pm
/usr/perl/lib/Math/Calc/Units/Convert/Combo.pm
/usr/perl/lib/Math/Calc/Units/Convert/Date.pm
/usr/perl/lib/Math/Calc/Units/Convert/Distance.pm
/usr/perl/lib/Math/Calc/Units/Convert/Metric.pm
/usr/perl/lib/Math/Calc/Units/Convert/Multi.pm
/usr/perl/lib/Math/Calc/Units/Convert/Time.pm
/usr/perl/lib/Math/Calc/Units/Grammar.pm
/usr/perl/lib/Math/Calc/Units/Grammar.y
/usr/perl/lib/Math/Calc/Units/Rank.pm
/usr/perl/lib/Module/Implementation.pm
/usr/perl/lib/Module/Metadata.pm
/usr/perl/lib/Nagios/Plugin.pm
/usr/perl/lib/Nagios/Plugin/Config.pm
/usr/perl/lib/Nagios/Plugin/ExitResult.pm
/usr/perl/lib/Nagios/Plugin/Functions.pm
/usr/perl/lib/Nagios/Plugin/Getopt.pm
/usr/perl/lib/Nagios/Plugin/Performance.pm
/usr/perl/lib/Nagios/Plugin/Range.pm
/usr/perl/lib/Nagios/Plugin/Threshold.pm
/usr/perl/lib/Perl/OSType.pm
/usr/perl/lib/Test/Builder.pm
/usr/perl/lib/Test/Builder/IO/Scalar.pm
/usr/perl/lib/Test/Builder/Module.pm
/usr/perl/lib/Test/Builder/Tester.pm
/usr/perl/lib/Test/Builder/Tester/Color.pm
/usr/perl/lib/Test/More.pm
/usr/perl/lib/Test/Simple.pm
/usr/perl/lib/Test/Tutorial.pod
/usr/perl/lib/Try/Tiny.pm
/usr/perl/lib/armv7l-linux-thread-multi/auto/Class/Accessor/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Config/Tiny/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Math/Calc/Units/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Module/Implementation/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Module/Metadata/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Nagios/Plugin/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Perl/OSType/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Test/Simple/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/Try/Tiny/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/parent/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/version/.packlist
/usr/perl/lib/armv7l-linux-thread-multi/auto/version/vxs/vxs.bs
/usr/perl/lib/armv7l-linux-thread-multi/auto/version/vxs/vxs.so
/usr/perl/lib/armv7l-linux-thread-multi/version.pm
/usr/perl/lib/armv7l-linux-thread-multi/version.pod
/usr/perl/lib/armv7l-linux-thread-multi/version/Internals.pod
/usr/perl/lib/armv7l-linux-thread-multi/version/vpp.pm
/usr/perl/lib/armv7l-linux-thread-multi/version/vxs.pm
/usr/perl/lib/parent.pm
/usr/perl/lib/perl5/armv7l-linux-thread-multi/perllocal.pod
/usr/perl/man/man3/Class::Accessor.3pm
/usr/perl/man/man3/Class::Accessor::Fast.3pm
/usr/perl/man/man3/Class::Accessor::Faster.3pm
/usr/perl/man/man3/Config::Tiny.3pm
/usr/perl/man/man3/Math::Calc::Units.3pm
/usr/perl/man/man3/Module::Implementation.3pm
/usr/perl/man/man3/Module::Metadata.3pm
/usr/perl/man/man3/Nagios::Plugin.3pm
/usr/perl/man/man3/Nagios::Plugin::Config.3pm
/usr/perl/man/man3/Nagios::Plugin::ExitResult.3pm
/usr/perl/man/man3/Nagios::Plugin::Functions.3pm
/usr/perl/man/man3/Nagios::Plugin::Getopt.3pm
/usr/perl/man/man3/Nagios::Plugin::Performance.3pm
/usr/perl/man/man3/Nagios::Plugin::Range.3pm
/usr/perl/man/man3/Nagios::Plugin::Threshold.3pm
/usr/perl/man/man3/Perl::OSType.3pm
/usr/perl/man/man3/Test::Builder.3pm
/usr/perl/man/man3/Test::Builder::IO::Scalar.3pm
/usr/perl/man/man3/Test::Builder::Module.3pm
/usr/perl/man/man3/Test::Builder::Tester.3pm
/usr/perl/man/man3/Test::Builder::Tester::Color.3pm
/usr/perl/man/man3/Test::More.3pm
/usr/perl/man/man3/Test::Simple.3pm
/usr/perl/man/man3/Test::Tutorial.3pm
/usr/perl/man/man3/Try::Tiny.3pm
/usr/perl/man/man3/parent.3pm
/usr/perl/man/man3/version.3pm
/usr/perl/man/man3/version::Internals.3pm



%changelog
* Sat Mar 15  2014 support@remsnet.de
- added perl symlink /usr/local/bin/perl for contrib plugins
- changed Reqire xen-tools to xen
- changed BuildRequire / Require to libdbi1
- added/FIX pkg ajp dbi haproxy clamav smstools uptime checksums
- tested nagios-plugins-2.0-freeradius.patch - dont copile yet, added temprorarly --without-radius
- removed oss release check for radius due freeradius usage
- added  to %configure   --with-gnutls  --enable-threads=pth --enable-extra-opts --enable-perl-modules
- added BuildRequires gnutls -> configure needs it for --with-gnutls
- packaged nagios-plugins 1.4.16 to %{nagios_plugindir}/contrib as pkg contrib
* Fri Mar 14 2014 support@remsnet.de
- added managed contribs from https://github.com/bzed/pkg-nagios-plugins-contrib as $BUILD/contrib
- RE-added unmaged contrib from oss-12.3 nagios-plugins 1.4.16 $BUILD/contrib/misc
  ... I wanted simply to hold the OLD SINGEL nagios-plugin RPM PKG BUILD structure...
   updating makes then it more simple on older SuSE / RHEL / CENTOS / FC then ...
- added wget-nagios-docu-4.0.3.sh for automated create an nagios docu tarball from http://nagios.sourceforge.net/docs/nagioscore/4/en/toc.html
* Wed Mar 12 2014 support@remsnet.de
- release2.0 for 13.1 in Arm RPI
  Pkg upgrade from old remsnet suse 9.x / 10.x i386 ..
  Cleanup 1.x ChangeLog

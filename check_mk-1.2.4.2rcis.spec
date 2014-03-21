#
# spec file for package check_mk
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
%define         nagios_command_group    nagcmd
%define         nagios_user             nagios



Name:           check_mk
Version:        1.2.4
Release:        3.2rcis
Summary:        Nagios-plugin for retrieving data
License:        GPL-2.0+
Group:          System/Monitoring
Url:            http://mathias-kettner.de/checkmk_index.html
Source0:        http://mathias-kettner.de/download/%{name}-%{version}.tar.gz
Source1:        check_mk-rpmlintrc
Source2:        check_mk-logwatch.cfg
Source3:        check_mk-README.SuSE
Source4:        zzz_check_mk.conf
Source5:        permissions.check_mk
Source6:        permissions.mkeventd
Source7:        check_mk-mysql.cfg
#Source8:        permissions.mk-livestatus
# PATCH-MISSING-TAG -- See http://wiki.opensuse.org/openSUSE:Packaging_Patches_guidelines
#Patch0:         check_mk-no_chgrp.patch
Patch1:         setup.sh.patch
BuildRequires:  gcc-c++
BuildRequires:  nagios-rpm-macros
%if 0%{?suse_version}
BuildRequires:  apache2-devel
# unzip is needed for /usr/lib/rpm/brp-check-bytecode-version
BuildRequires:  unzip
PreReq:         permissions
%endif
%if 0%{?fedora_version} ||  0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  httpd-devel
%endif
%if 0%{?mandriva_version}
BuildRequires:  apache-devel
%endif
Requires(pre):  /bin/logger
Requires(pre):  coreutils
Requires(pre):  sed
Requires(pre):  xinetd
Requires(pre):  permissions
Requires:       mk-livestatus
%if 0%{?suse_version} > 1030
BuildRequires:  fdupes
%endif
%if 0%{?sles_version}
BuildRequires:  unzip
%endif
# systemd
%if 0%{?suse_version} >= 1210
BuildRequires: systemd
%{?systemd_requires}
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    no
%define         nnmmsg logger -t %{name}/rpm
%define         __debug_install_post   %{nil}

%description
Check_mk adopts a new a approach for collecting data
from operating systems and network components. It
obsoletes NRPE, check_by_ssh, NSClient and
check_snmp. It has many benefits, the most important
of which are:

* Significant reduction of CPU usage on the Nagios
* host.
* Automatic inventory of items to be checked on
* hosts.

%package agent
Summary:        Agent for check_mk
Group:          System/Monitoring
%if 0%{?suse_version}
Requires(pre):  %insserv_prereq
%endif
Requires(pre):  xinetd

%description agent
Check_mk adopts a new a approach for collecting data
from operating systems and network components. It
obsoletes NRPE, check_by_ssh, NSClient and
check_snmp. It has many benefits, the most important
of which are:

* Significant reduction of CPU usage on the Nagios
* host.
* Automatic inventory of items to be checked on
* hosts.

%package agent-logwatch
Summary:        Logwatch-Plugin for check_mk agent
Group:          System/Monitoring
Requires:       check_mk-agent = %{version}
Requires:       python
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description agent-logwatch
The logwatch plugin for the check_mk agent allows you to monitor
logfiles on Linux and UNIX. In one or more configuration files you
specify patters for log messages that should raise a warning or
critical state. For each logfile the current position is remembered.
This way only new messages are being sent.

%package agent-mysql
Summary:        MySQL-Plugin for check_mk agent
Group:          System/Monitoring
Requires:       check_mk-agent = %{version}
Requires:       mysql-community-server-client
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description agent-mysql
The MySQL plugin for the check_mk agent allows you to monitor
several aspects of MySQL databases. You need to adapt the
config /etc/check_mk/mysql.cfg to your needs.

%package agent-oracle
Summary:        Oracle-Plugin for check_mk agent
Group:          System/Monitoring
Requires:       check_mk-agent = %{version}
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description agent-oracle
The ORACLE plugin for the check_mk agent allows you to monitor
several aspects of ORACLE databases. You need to adapt the
script /etc/check_mk/sqlplus.sh to your needs.

%package agent-smart
Summary:        SMART-Plugin for check_mk agent
Group:          System/Monitoring
Requires:       check_mk-agent = %{version}
Requires:       smartmontools
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description agent-smart
The SMART plugin for the check_mk agent allows you to monitor
several SMART values of harddisks.

%package agent-jolokia
Summary:    Jolokia-Plugin for check_mk agent
Group:      System/Monitoring
Requires:       check_mk-agent = %{version}
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description agent-jolokia
The Jolokia plugin for the check_mk agent allows you to monitor
several aspect of Java application servers. You need to adapt the
config /etc/check_mk/jolokia.cfg  to your needs.

%package agent-apache_status
Summary:    Apache Status Plugin for check_mk agent
Group:      System/Monitoring
Requires:       check_mk-agent = %{version}
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description agent-apache_status
The apache_status plugin for the check_mk agent allows you to monitor
and parses the information provided by the Apache status module. You
may need to adapt the config /etc/check_mk/apache_status,cfg to your
needs. It requires that Apache mod_status be loaded.

%package multisite
Summary:        Web GUI for displaying monitoring status information
Group:          System/Monitoring
Requires:       %{name} >= %{version}
Requires:       apache2
Requires:       apache2-mod_python
Requires:       pnp4nagios
Requires:       python
Requires(pre):  permissions
Provides:       %{name}-web = %{version}
Obsoletes:      %{name}-web < %{version}
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description multisite
This package contains the Check_mk webpages. They allow you to
search for services and apply Nagios commands to the search results.

%package vsphere
Summary:    Check state of VMWare ESX via vSphere
Group:          System/Monitoring
Requires:       %{name} >= %{version}
Requires:       python-pysphere
%if 0%{?suse_version} > 1130
BuildArch:      noarch
%endif

%description vsphere
This package handles dependencies for the server-side vsphere agent.
See http://mathias-kettner.de/checkmk_vsphere.html for details.

%package -n mk-livestatus
Summary:        Accessing status and historic Nagios data
Group:          System/Monitoring
%if 0%{?mandriva_version}
Recommends:     nagios
%endif
%if 0%{?suse_version}
Recommends:     monitoring_daemon
%endif

%description -n mk-livestatus
Just as NDO, Livestatus make use of the Nagios Event Broker API and loads a
binary module into your Nagios process. But other then NDO, Livestatus does not
actively write out data. Instead, it opens a socket by which data can be
retrieved on demand.

The socket allows you to send a request for hosts, services or other pieces of
data and get an immediate answer. The data is directly read from Nagios'
internal data structures. Livestatus does not create its own copy of that data.
Beginning from version 1.1.2 you are also be able retrieve historic data from
the Nagios log files via Livestatus.

%package -n mkeventd
Summary:    The Check_MK Event Console
Group:      System/Monitoring

%description -n mkeventd
The Check_MK Event Console is a full featured event processing
module that integrates with Multisite. It has an own daemon and
several methods for retrieving events. It even has an integrated
syslog daemon.


%prep
%setup -q
#%patch0 -p1

# explicit kill prebuild - setup.sh will just copy a statical linked binary, so we do it on our own
test -d livestatus.src && rm -rf livestatus.src ;mkdir livestatus.src; tar xfz livestatus.tar.gz -C livestatus.src
test -d mkeventd.src &&  rm -rf mkeventd.src ;mkdir mkeventd.src;  tar xfz mkeventd.tar.gz -C mkeventd.src
test -d agents.src &&  rm -rf agents.src ; mkdir agents.src; tar xpfz agents.tar.gz -C agents.src
test -d modules.src && rm -rf modules.src ; mkdir modules.src ; tar xpfz modules.tar.gz -C modules.src
test -d doc.src && rm -rf doc.src ; mkdir doc.src ; tar xpfz doc.tar.gz -C doc.src
test -d checkman.src && rm -rf checkman.src ; mkdir checkman.src ; tar xpfz checkman.tar.gz -C checkman.src
test -d checks.src && rm -rf checks.src ; mkdir checks.src ; tar xpfz checks.tar.gz -C checks.src
test -d notifications.src && rm -rf notifications.src ; mkdir notifications.src ; tar xpfz notifications.tar.gz -C notifications.src
test -d web.src && rm -rf web.src ; mkdir web.src ; tar xpfz web.tar.gz -C web.src
test -d conf.src && rm -rf conf.src ; mkdir conf.src ; tar xpfz conf.tar.gz -C conf.src
test -d share.src && rm -rf share.src ; mkdir share.src ; tar xpfz share.tar.gz -C share.src
test -d pnp-templates.src && rm -rf pnp-templates.src ; mkdir pnp-templates.src ; tar xpfz pnp-templates.tar.gz -C pnp-templates.src



%patch1
install -m 0644 %{SOURCE6} permissions.mkeventd
touch debugsources.list
touch debugfiles.list

%build
export bindir='%{_bindir}'
export confdir='%{livestatus_sysconfdir}'
export check_mk_configdir='%{livestatus_check_mk_configdir}'
export checksdir='%{livestatus_checksdir}'
export modulesdir='%{livestatus_modulesdir}'
export web_dir='%{livestatus_webdir}'
export mibsdir='%{_datadir}/snmp/mibs'
export docdir='%{_defaultdocdir}/%{name}'
export checkmandir='%{_defaultdocdir}/%{name}/checks'
export vardir='%{livestatus_vardir}'
export agentsdir='%{livestatus_agentsdir}'
export agentslibdir='%{livestatus_agentslibdir}'
export agentsconfdir='%{livestatus_agentsconfdir}'
export htdocsdir='%{livestatus_htdocsdir}'
export nagiosuser='%{nagios_user}'
export wwwuser='wwwrun'
export wwwgroup='%{nagios_command_group}'
export nagios_binary='%{_sbindir}/nagios'
export nagios_config_file='%{nagios_sysconfdir}/nagios.cfg'
export nagconfdir='%{livestatus_nagconfdir}'
export nagios_startscript='%{_sysconfdir}/init.d/nagios'
export nagpipe='%{nagios_command_file}'
export nagiosurl='/nagios'
export cgiurl='/nagios/cgi-bin'
export nagios_status_file='%{nagios_status_file}'
export check_icmp_path='%{nagios_plugindir}/check_icmp'
export checkmk_web_uri='/%{name}'
export apache_config_dir='%{_sysconfdir}/apache2/conf.d'
export htpasswd_file='%{nagios_sysconfdir}/htpasswd.users'
export nagios_auth_name='Nagios Access'
export pnpconfdir='%{pnp4nagios_sysconfdir}'
export pnprraconf='%{pnp4nagios_sysconfdir}'
export pnp_url='%{pnp4nagios_baseurl}'
export pnp_prefix='%{pnp4nagios_baseurl}/'
export rrddir='%{livestatus_rrddir}'
export pnptemplates='%{pnp4nagios_templatedir}'
export enable_livestatus='yes'
export libdir='%{livestatus_libdir}'
export livesock='%{livestatus_socket_file}'
export livebackendsdir='%{livestatus_livebackendsdir}'
export check_result_path='%{nagios_spooldir}'
export wwwuser='%{nagios_command_user}'
export DESTDIR=%{buildroot}
export enable_mkeventd='yes'
export mkeventdstatedir='/var/lib/mkeventd'
R=%{buildroot}

# build agents
# setup.sh will just copy a statical (i386) linked binary,  this way not fit for arm, sparc and others
cd agents.src
test -x waitmax && rm -f waitmax
gcc -s %{optflags} -o waitmax waitmax.c
cd ..

# Build livestatus
cd livestatus.src
./configure --prefix=%{_prefix} --with-nagios4
make
cd ..

# build mkeventd
cd mkeventd.src/src
make
cd ..
cd lib
make
cd ..



%install
%if 0%{?suse_version} && 0%{?suse_version} < 1120
export NO_BRP_CHECK_BYTECODE_VERSION=true
%endif

export bindir='%{_bindir}'
export confdir='%{livestatus_sysconfdir}'
export check_mk_configdir='%{livestatus_check_mk_configdir}'
export checksdir='%{livestatus_checksdir}'
export modulesdir='%{livestatus_modulesdir}'
export web_dir='%{livestatus_webdir}'
export mibsdir='%{_datadir}/snmp/mibs'
export docdir='%{_defaultdocdir}/%{name}'
export checkmandir='%{_defaultdocdir}/%{name}/checks'
export vardir='%{livestatus_vardir}'
export agentsdir='%{livestatus_agentsdir}'
export agentslibdir='%{livestatus_agentslibdir}'
export agentsconfdir='%{livestatus_agentsconfdir}'
export htdocsdir='%{livestatus_htdocsdir}'
export nagiosuser='%{nagios_user}'
export wwwuser='wwwrun'
export wwwgroup='%{nagios_command_group}'
export nagios_binary='%{_sbindir}/nagios'
export nagios_config_file='%{nagios_sysconfdir}/nagios.cfg'
export nagconfdir='%{livestatus_nagconfdir}'
export nagios_startscript='%{_sysconfdir}/init.d/nagios'
export nagpipe='%{nagios_command_file}'
export nagiosurl='/nagios'
export cgiurl='/nagios/cgi-bin'
export nagios_status_file='%{nagios_status_file}'
export check_icmp_path='%{nagios_plugindir}/check_icmp'
export checkmk_web_uri='/%{name}'
export apache_config_dir='%{_sysconfdir}/apache2/conf.d'
export htpasswd_file='%{nagios_sysconfdir}/htpasswd.users'
export nagios_auth_name='Nagios Access'
export pnpconfdir='%{pnp4nagios_sysconfdir}'
export pnprraconf='%{pnp4nagios_sysconfdir}'
export pnp_url='%{pnp4nagios_baseurl}'
export pnp_prefix='%{pnp4nagios_baseurl}/'
export rrddir='%{livestatus_rrddir}'
export pnptemplates='%{pnp4nagios_templatedir}'
export enable_livestatus='yes'
export libdir='%{livestatus_libdir}'
export livesock='%{livestatus_socket_file}'
export livebackendsdir='%{livestatus_livebackendsdir}'
export check_result_path='%{nagios_spooldir}'
export wwwuser='%{nagios_command_user}'
export DESTDIR=%{buildroot}
export enable_mkeventd='yes'
export mkeventdstatedir='/var/lib/mkeventd'
R=%{buildroot}

# fix setup.sh to not use abuild for sudo call
sed -i 's/sudo -u $(id -un)/sudo -u root/' ./setup.sh
# fix serials_file location in setup, which causes mkeventd to not build
#sed -i 's%serials_file=%serials_file=%{buildroot}%' ./setup.sh

DESTDIR=%{buildroot} bash ./setup.sh --yes

# install directories
install -d -m 755 %{buildroot}/$agentslibdir/{local,plugins}
install -d -m 755 %{buildroot}/${docdir}_agent
install -d -m 755 %{buildroot}/%{livestatus_rrddir}
install -d -m 755 %{buildroot}/%{livestatus_socketdir}
install -d -m 755 %{buildroot}/%{livestatus_vardir}/rrd
install -d -m 755 %{buildroot}/%{livestatus_vardir}/wato
install -d -m 755 %{buildroot}/%{livestatus_vardir}/wato/{log,snapshots}
install -d -m 755 %{buildroot}/%{livestatus_check_mk_configdir}/wato

# auth.serials require for WATO/multisite
install -d -m 755 %{buildroot}/%{nagios_sysconfdir}
touch -m 0600 %{buildroot}/%{nagios_sysconfdir}/auth.serials

# documentation
install -m 644 COPYING %{buildroot}/${docdir}_agent/
install -m 644 COPYING ChangeLog AUTHORS %{buildroot}/${docdir}/
install -m 644 %{SOURCE3} %{buildroot}/${docdir}/README.SuSE

# move files to the right place
install -m755 %{buildroot}%{livestatus_agentsdir}/check_mk_agent.linux %{buildroot}%{_bindir}/check_mk_agent
install -m755 %{buildroot}%{livestatus_agentsdir}/plugins/mk_logwatch %{buildroot}%{livestatus_agentslibdir}/plugins

# mysql plugin
install -m755 %{buildroot}%{livestatus_agentsdir}/plugins/mk_mysql %{buildroot}%{livestatus_agentslibdir}/plugins

# oracle plugin
install -m755 %{buildroot}%{livestatus_agentsdir}/plugins/mk_oracle %{buildroot}%{livestatus_agentslibdir}/plugins
install -m755 %{buildroot}%{livestatus_agentsdir}/sqlplus.sh %{buildroot}%{livestatus_agentsconfdir}/

# smart plugin
install -m755 %{buildroot}%{livestatus_agentsdir}/plugins/smart %{buildroot}%{livestatus_agentslibdir}/plugins

# jolokia plugin
install -m755 %{buildroot}%{livestatus_agentsdir}/plugins/mk_jolokia %{buildroot}%{livestatus_agentslibdir}/plugins
install -m755 %{buildroot}%{livestatus_agentsdir}/jolokia.cfg %{buildroot}%{livestatus_agentsconfdir}/

# apache_status plugin
install -m755 %{buildroot}%{livestatus_agentsdir}/plugins/apache_status %{buildroot}%{livestatus_agentslibdir}/plugins
install -m755 %{buildroot}%{livestatus_agentsdir}/apache_status.cfg %{buildroot}%{livestatus_agentsconfdir}/

install -m 755 agents.src/waitmax %{buildroot}%{_bindir}
test -f %{buildroot}%{livestatus_agentsdir}/waitmax && rm -rf %{buildroot}%{livestatus_agentsdir}/waitmax*
ln -s %{_bindir}/waitmax %{buildroot}%{livestatus_agentsdir}/waitmax

# remove unneeded files
rm %{buildroot}%{livestatus_agentsdir}/windows/check_mk_agent.cc
rm %{buildroot}%{livestatus_agentsdir}/windows/Makefile

# install configuration for logwatch agent
install -m 644 %{SOURCE2} %{buildroot}/%{livestatus_agentsconfdir}/logwatch.cfg

# install configuration for mysql agent
install -m 644 %{SOURCE7} %{buildroot}/%{livestatus_agentsconfdir}/mysql.cfg

# install xinetd configuration
install -Dm 644 %{buildroot}/$agentsdir/xinetd.conf %{buildroot}%{_sysconfdir}/xinetd.d/%{name}

# remove softlink and install check_mk_templates.cfg
if [ -L "%{buildroot}/%{livestatus_nagconfdir}/check_mk_templates.cfg" ]; then
        rm %{buildroot}/%{livestatus_nagconfdir}/check_mk_templates.cfg
        install -Dm 644 %{buildroot}/%{_datadir}/check_mk/check_mk_templates.cfg %{buildroot}%{livestatus_nagconfdir}/check_mk_templates.cfg
fi

# install permissions file to allow people running Icinga with mk-livestatus
#install -Dm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/permissions.d/mk-livestatus
install -Dm644 %{SOURCE5} %{buildroot}%{_sysconfdir}/permissions.d/check_mk

# fix permissions
chmod +x %{buildroot}%{livestatus_checksdir}/*
chmod +x %{buildroot}%{livestatus_modulesdir}/*.py
for file in $(find %{buildroot}%{livestatus_webdir} -name "*.py"); do
        chmod +x $file
done
find %{buildroot}/${docdir}/ -type f -exec chmod -x {} \;
chmod -x %{buildroot}%{livestatus_webdir}/htdocs/defaults.py

# make rpmlint happy
%if 0%{?suse_version} > 1030
%fdupes -s %{buildroot}/%{pnp4nagios_templatedir}
%fdupes -s %{buildroot}/%{livestatus_webdir}
%endif
strip %{buildroot}/%{_bindir}/unixcat

# apache config
install -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/apache2/conf.d/

%pre
# Create user and group on the system if necessary
%{nagios_user_group_add}
%{nagios_command_user_group_add}

%post
%if 0%{?suse_version} < 01210
%run_permissions
%else
%set_permissions  %{_sysconfdir}/permissions.d/check_mk
%endif

%post agent
# ensure xinetd is enabled if the package is installed for the first time
%if 0%{?suse_version} >= 1210
%service_add_post xinetd.service
%else
%{fillup_and_insserv -y xinetd}
%endif

%postun agent
%restart_on_update xinetd

%post -n mk-livestatus
%if 0%{?suse_version} < 01210
%run_permissions
%else
%set_permissions %{_sysconfdir}/permissions.d/mk-livestatus
%endif

%post multisite
%if 0%{?suse_version} > 1140
%set_permissions %{_sysconfdir}/permissions.d/check_mk
%else
%run_permissions
%endif

%post -n mkeventd
echo "mkeventd_open514 permissions are not set, i.e not setuid. See
/usr/share/doc/packages/mkeventd/permissions.mkeventd for details
on resolving this on SuSE systems"

%files
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}
%dir %{livestatus_sysconfdir}
%dir %attr(0775,%{nagios_user},%{nagios_command_group})
%dir %{livestatus_check_mk_configdir}
%dir %attr(0775,%{nagios_user},%{nagios_command_group})
%dir %{livestatus_datadir}
%dir %{livestatus_datadir}/notifications
%{livestatus_datadir}/notifications/*
%dir %{livestatus_agentsdir}
%dir %{livestatus_agentsdir}/plugins
%dir %{livestatus_agentslibdir}
%dir %{livestatus_checksdir}
%dir %{livestatus_modulesdir}
%dir %{livestatus_notificationsdir}
%dir %{livestatus_nagconfdir}
%dir %{livestatus_rrddir}
%dir %{livestatus_libdir}
%dir %{pnp4nagios_datadir}
%dir %{pnp4nagios_templatedir}
%dir %{nagios_sysconfdir}
%dir %{livestatus_vardir}
%dir %{livestatus_vardir}/packages
%verify(not mode) %dir %{livestatus_vardir}
%verify(not mode) %dir %{livestatus_vardir}/packages
%dir %attr(-,%{nagios_user},root)
%dir %attr(-,%{nagios_user},root)
%dir %attr(-,%{nagios_user},root)
%dir %attr(-,%{nagios_user},root)
%dir %attr(0775,%{nagios_user},%{nagios_command_group})
%dir %attr(0775,%{nagios_user},%{nagios_command_group})
%dir %attr(0775,%{nagios_user},%{nagios_command_group})
%dir %attr(0775,%{nagios_user},%{nagios_command_group})
%config(noreplace) %{livestatus_sysconfdir}/*.mk*
%config %{livestatus_check_mk_configdir}/README
%config(noreplace) %{_sysconfdir}/permissions.d/check_mk
%config(noreplace) %{livestatus_nagconfdir}/check_mk_templates.cfg
%{_datadir}/check_mk/check_mk_templates.cfg
%{livestatus_agentsdir}/*
%{livestatus_checksdir}/*
%{livestatus_modulesdir}/*
%{livestatus_notificationsdir}/*
%{pnp4nagios_templatedir}/*
%{_bindir}/check_mk
%{_bindir}/cmk
%{_bindir}/mkp
%{livestatus_libdir}/livestatus.o
%{livestatus_vardir}/packages/check_mk
%verify(not mode) %{livestatus_vardir}/packages/check_mk
%exclude %{livestatus_sysconfdir}/logwatch.cfg
%exclude %{livestatus_datadir}/web
%exclude %{livestatus_agentsdir}/plugins/mk_logwatch
%exclude %{livestatus_libdir}/livestatus.o
%exclude %{livestatus_vardir}/packages/check_mk

%files -n mk-livestatus
%defattr(-,root,root)
%dir %attr(-,%{nagios_user},%{nagios_command_group})
%{_bindir}/unixcat
%{livestatus_libdir}/livestatus.o
%{livestatus_vardir}/packages/check_mk
%verify(not mode) %{livestatus_vardir}/packages/check_mk
%dir %attr(-,%{nagios_user},%{nagios_command_group}) %{livestatus_socketdir}
%dir %verify(not mode) %attr(-,%{nagios_user},%{nagios_command_group}) %{livestatus_socketdir}
#%config(noreplace) %{_sysconfdir}/permissions.d/mk-livestatus

%files agent
%defattr(-,root,root)
%doc %{_defaultdocdir}/check_mk_agent
%{_bindir}/check_mk_agent
%{_bindir}/waitmax
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%dir %{livestatus_agentslibdir}
%dir %{livestatus_agentslibdir}/local
%dir %{livestatus_agentslibdir}/plugins

%files agent-logwatch
%defattr(-,root,root,-)
%{livestatus_agentslibdir}/plugins/mk_logwatch
%config(noreplace) %{livestatus_sysconfdir}/logwatch.cfg

%files agent-mysql
%defattr(-,root,root,-)
%{livestatus_agentslibdir}/plugins/mk_mysql
%config(noreplace) %attr(0400,%{nagios_command_user},%{nagios_command_group}) %{livestatus_sysconfdir}/mysql.cfg

%files agent-oracle
%defattr(-,root,root,-)
%{livestatus_agentslibdir}/plugins/mk_oracle
%config(noreplace) %{livestatus_sysconfdir}/sqlplus.sh

%files agent-smart
%defattr(-,root,root,-)
%{livestatus_agentslibdir}/plugins/smart

%files agent-jolokia
%defattr(-,root,root,-)
%{livestatus_agentslibdir}/plugins/mk_jolokia
%config(noreplace) %{livestatus_sysconfdir}/jolokia.cfg

%files agent-apache_status
%defattr(-,root,root,-)
%{livestatus_agentslibdir}/plugins/apache_status
%config(noreplace) %{livestatus_sysconfdir}/apache_status.cfg

%files multisite
%defattr(-,root,root,-)
%{livestatus_datadir}/web
%config(noreplace) %{_sysconfdir}/apache2/conf.d/*.conf
%config(noreplace) %attr(0660,%{nagios_command_user},%{nagios_command_group}) %{nagios_sysconfdir}/auth.serials

%files vsphere
%defattr(-,root,root,-)
%dir %{livestatus_datadir}/agents/special

%files -n mkeventd
%defattr(-,root,root,-)
%doc permissions.mkeventd
%{_bindir}/mkevent
%{_bindir}/mkeventd
%attr(0754,root,root)%{_bindir}/mkeventd_open514

%changelog
* Fri Mar 21 2014 support@remsnet.de
- cleanup old changelog
- updated %build and %install to fit --with-nagios4
- bugreport mailed to lars an michael
- added wwwuser & nagios user / nagioscmd & wwwgroup defines
- fixed some more %build tarball & dir setup stuff

* Wed Mar 12 2014 darin@darins.net
- Add packaging for apache_status plugin
- set require version for agent plugins

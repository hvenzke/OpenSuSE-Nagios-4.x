#
# spec file for package pnp4nagios
#
# Copyright (c) 2012-2013 Lars Vogdt <lars@linux-schulserver.de>
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

Name:           pnp4nagios
Version:        0.6.21
Release:        10.2
License:        GPL-2.0+
Summary:        Tool for producing graphs from Nagios perfdata
Url:            http://www.pnp4nagios.org/
Group:          System/Monitoring
BuildRequires:  apache2-devel
BuildRequires:  kohana2
BuildRequires:  nagios-rpm-macros
BuildRequires:  nagios-www
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Time::HiRes)
PreReq:         permissions
Requires:       kohana2
Requires:       perl
Requires:       rrdtool
Requires:       syslog
Requires:       %{name}-directories == %{version}
Recommends:     dejavu
Recommends:     nagios-plugins-pnp_rrds >= %{version}
# disabled as pnp4nagios can also be used together with icinga
# but the recommends triggers the installation of nagios
# Recommends:     nagios-www
%if 0%{?suse_version}
Requires:       php-gd
Requires:       php-zlib
%endif
%if 0%{?suse_version} > 1020
BuildRequires:  fdupes
BuildRequires:  rrdtool-devel
%else
BuildRequires:  rrdtool
%endif
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-httpd.conf
Source2:        %{name}.quick-start.txt
Source3:        %{name}-init
Source4:        %{name}-rpmlintrc
Source5:        %{name}-%{name}.cfg
Source6:        %{name}-check_nrpe.cfg
Source7:        %{name}-xinetd.sample.conf
Source8:        %{name}-lighttpd.conf
Source9:        %{name}-nagios-permissions
Source10:       %{name}-icinga-permissions
Source11:       %{name}-README.SuSE-Icinga
Patch1:         %{name}-fix-pathnames-in-scripts.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define         apxs2 /usr/sbin/apxs2-prefork
%define         apache2_sysconfdir %(%{apxs2} -q SYSCONFDIR || echo "/etc/apache2")

%description
PNP is an addon for the Nagios or Icinga Network Monitoring System.

PNP provides easy to use, easy to configure RRDTools based performance charts
feeded by the performance data output of the Nagios or Icinga plugins.


%package icinga
Summary:        Icinga specific files for pnp4nagios
Group:          System/Monitoring
Recommends:     logrotate
PreReq:         permissions
Provides:       %{name}-directories = %{version}-%{release}
Supplements:    icinga-www
Supplements:    icinga-web
Provides:       %{name}-directories = %{version}-%{release}
Conflicts:      %{name}-nagios

%description icinga
PNP is an addon for the Nagios or Icinga Network Monitoring System.

This package provides the directories with the correct permissions for
Icinga.


%package nagios
Summary:        Nagios specific files for pnp4nagios
Group:          System/Monitoring
Recommends:     logrotate
PreReq:         permissions
Provides:       %{name}-directories = %{version}-%{release}
Supplements:    nagios-www
Provides:       %{name}-directories = %{version}-%{release}
Conflicts:      %{name}-icinga

%description nagios
PNP is an addon for the Nagios or Icinga Network Monitoring System.

This package provides the directories with the correct permissions for
Nagios.


%package -n nagios-plugins-pnp_rrds
Summary:        Check freshness and state of your RRD files
Group:          System/Monitoring
Requires:       nagios-plugins-common

%description -n nagios-plugins-pnp_rrds
Use this plugin to check the freshness of your host and service RRD files
that are used by pnp4nagios.


%pre nagios
getent group %{nagios_group} >/dev/null || groupadd -r %{nagios_group}
getent passwd %{nagios_user} >/dev/null || useradd -r -g %{nagios_group} -d /var/lib/nagios -s /bin/bash -c "User for %{name}-nagios" %{nagios_user}

%pre icinga
getent group %{icinga_group} >/dev/null || groupadd -r %{icinga_group}
getent passwd %{icinga_user} >/dev/null || useradd -r -g %{icinga_group} -d /var/lib/icinga -s /bin/bash -c "User for %{name}-icinga" %{icinga_user}


%prep
%setup -q
%patch1 -p0

%build
%configure \
    --datadir="%{pnp4nagios_datadir}" \
    --localstatedir="%{pnp4nagios_logdir}" \
    --sysconfdir="%{pnp4nagios_sysconfdir}" \
    --libexecdir="%{nagios_plugindir}" \
    --datarootdir="%{pnp4nagios_datarootdir}" \
    --with-perfdata-logfile="%{pnp4nagios_perfdata_logfile}" \
    --with-perfdata-dir="%{pnp4nagios_perfdata_dir}" \
    --with-perfdata-spool-dir="%{pnp4nagios_perfdata_spooldir}" \
    --with-init-dir="%{_sysconfdir}/init.d" \
    --with-nagios-user="%{nagios_user}" \
    --with-nagios-group="%{nagios_group}" \
    --with-nagios_cmd_file="%{nagios_command_file}" \
    --with-base-url="%{pnp4nagios_baseurl}" \
    --without-kohana \
    --with-kohana_system="%{_datadir}/kohana2/system"

make %{?_smp_mflags} all

%install
LOGDIR=$(dirname %{pnp4nagios_perfdata_logfile})
mkdir -p %{buildroot}/%{pnp4nagios_perfdata_dir} %{buildroot}/$LOGDIR
make install install-config \
    DESTDIR=%{buildroot} \
    LIBEXEC_DIR="%{nagios_plugindir}" \
    MANDIR=%{_mandir} \
    INSTALL_OPTS=""
# move samples to the docdir
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}/sample-config
find sample-config/ -name "*-sample*" -exec cp -v {} %{buildroot}/%{_defaultdocdir}/%{name}/sample-config/ \;
# install config files
mv %{buildroot}/%{_sysconfdir}/%{name}/rra.cfg-sample %{buildroot}/%{pnp4nagios_sysconfdir}/rra.cfg
sed -e 's@\^hna0@localhost@' \
    -e 's@\^traffic@traffic@' \
    %{buildroot}/%{pnp4nagios_sysconfdir}/pages/web_traffic.cfg-sample > %{buildroot}/%{pnp4nagios_sysconfdir}/pages/web_traffic.cfg
mv %{buildroot}/%{pnp4nagios_sysconfdir}/check_commands/check_nwstat.cfg-sample %{buildroot}/%{pnp4nagios_sysconfdir}/check_commands/check_nwstat.cfg
install -m644 %{SOURCE6} %{buildroot}/%{pnp4nagios_sysconfdir}/check_commands/check_nrpe.cfg
find %{buildroot}/%{pnp4nagios_sysconfdir} -name "*-sample" -exec rm {} \;
install -Dm644 %{SOURCE7} %{buildroot}/%{_sysconfdir}/xinetd.d/%{name}
# fix pathname to the kohana files
sed -i "s|^\$kohana_modules.*|\$kohana_modules = '%{_datadir}/kohana2/modules';|" %{buildroot}/%{pnp4nagios_datarootdir}/index.php
rm %{buildroot}/%{pnp4nagios_datarootdir}/install.php
# install own nagios command file
install -m644 %{SOURCE5}  %{buildroot}/%{pnp4nagios_sysconfdir}/%{name}.cfg
# install the documentation
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}
install -m0644 AUTHORS ChangeLog COPYING README* THANKS %{buildroot}/%{_defaultdocdir}/%{name}/
install -m0644 %{SOURCE2} %{buildroot}/%{_defaultdocdir}/%{name}/README.SuSE
install -m0644 %{SOURCE11} %{buildroot}/%{_defaultdocdir}/%{name}/README.SuSE-Icinga
# install contrib scripts into docdir
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}/example
cp -r contrib/* %{buildroot}/%{_defaultdocdir}/%{name}/example/
# install template placeholder
mkdir -p %{buildroot}/%{pnp4nagios_datadir}/templates/
touch %{buildroot}/%{pnp4nagios_datadir}/templates/PUT-YOUR-TEMPLATES-HERE
# install directories
install -d -m0775 %{buildroot}/%{pnp4nagios_perfdata_spooldir}
install -d -m0775 %{buildroot}%{pnp4nagios_logdir}/stats
# install apache configuration
install -Dm0644 %{SOURCE1} %{buildroot}/%{apache2_sysconfdir}/conf.d/%{name}.conf
# lighttpd config goes as example to /etc/pnp4nagios
install -m0644 %{SOURCE8} %buildroot/etc/pnp4nagios/pnp4nagios-lighttpd.conf
# install init-script
install -Dm0755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/init.d/npcd
mkdir -p %{buildroot}/%{_sbindir}
ln -s %{_sysconfdir}/init.d/npcd %{buildroot}/%{_sbindir}/rcnpcd
test -d %{buildroot}%{pnp4nagios_datadir}/application/logs || mkdir -p %{buildroot}%{pnp4nagios_datadir}/application/logs
test -d %{buildroot}%{pnp4nagios_datadir}/application/cache || mkdir -p %{buildroot}%{pnp4nagios_datadir}/application/cache
test -d %{buildroot}%{pnp4nagios_perfdata_dir} || mkdir -p %{buildroot}%{pnp4nagios_perfdata_dir}
# install ssi files in datadir
install -Dm644 contrib/ssi/status-header.ssi %{buildroot}%{pnp4nagios_datadir}/media/ssi/status-header.ssi
# install permissions file for nagios users
install -Dm644 %{SOURCE9} %{buildroot}/%{_sysconfdir}/permissions.d/%{name}-nagios
# install permissions file for icinga users
install -Dm644 %{SOURCE10} %{buildroot}/%{_sysconfdir}/permissions.d/%{name}-icinga
# install logrotate snipplet
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
cat >> %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}-nagios << EOF
%{pnp4nagios_logdir}/perfdata.log {
        missingok
        notifempty
        dateext
        copytruncate
        compress
        size +4096k
        rotate 99
        maxage 365
        su %{nagios_user} %{nagios_group}
}
EOF

cat >> %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}-icinga << EOF
%{pnp4nagios_logdir}/perfdata.log {
        missingok
        notifempty
        dateext
        copytruncate
        compress
        size +4096k
        rotate 99
        maxage 365
        su %{icinga_user} %{icinga_group}
}
EOF
# fix path to livestatus socket
sed -i "s|/usr/local/nagios/var/rw/live|%{livestatus_socketdir}/livestatus.cmd|g" %{buildroot}/%{pnp4nagios_sysconfdir}/config*.php
# save discspace, create links
%if 0%{?suse_version} > 1020
%fdupes -s %{buildroot}/%{_datadir}/%{name}
%endif

%clean
rm -rf %{buildroot}

%post
if [ x"$1" == x"1" ]; then
    # this is the initial installation: enable pnp4nagios
    test -x %{_sbindir}/a2enflag && %{_sbindir}/a2enflag PNP4NAGIOS >/dev/null
else
  if [ -d etc/nagios/pnp ]; then
    echo "WARNING:" >&2
    echo "The directory locations of %{name} have changed." >&2
    echo "Please adapt your NEW configuration in %{pnp4nagios_sysconfdir}" >&2
    echo >&2
  fi
  if [ -f %apache2_sysconfdir/conf.d/nagios-pnp.conf ]; then
        echo "WARNING:" >&2
        echo "The file %apache2_sysconfdir/conf.d/nagios-pnp.conf has been renamed to" >&2
        echo "%apache2_sysconfdir/conf.d/%{name}.conf - please check and adapt the" >&2
        echo "new configuration and remove your the old file afterward." >&2
        echo >&2
  fi
fi


%post nagios
%if 0%{?suse_version} < 01140
%run_permissions
%else
%set_permissions %{_sysconfdir}/permissions.d/%{name}-nagios
%endif

%post icinga
%if 0%{?suse_version} < 01140
%run_permissions
%else
%set_permissions %{_sysconfdir}/permissions.d/%{name}-icinga
%endif


%preun
%stop_on_removal npcd

%postun
%{insserv_cleanup npcd}
if [ x"$1" == x"0" ]; then
    # deinstallation of the package - remove the apache flag
    test -x %{_sbindir}/a2disflag && %{_sbindir}/a2disflag PNP4NAGIOS >/dev/null
    %restart_on_update apache2
fi


%files
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}/
%dir %{pnp4nagios_datadir}
%dir %{pnp4nagios_sysconfdir}
#%%dir %%{pnp4nagios_sysconfdir}/check_commands
#%%dir %%{pnp4nagios_sysconfdir}/config.d
#%%dir %%{pnp4nagios_sysconfdir}/pages
%dir %{pnp4nagios_libdir}
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%config(noreplace) %{pnp4nagios_sysconfdir}/*
# user should use config_local.php, so noreplace is missing by intention here
#%%config            %%{pnp4nagios_sysconfdir}/config.php
%config(noreplace) %apache2_sysconfdir/conf.d/%{name}.conf
%{pnp4nagios_templatedir}/*
%{_libdir}/npcdmod.o
%{_bindir}/*
%{_sbindir}/rcnpcd
%{_sysconfdir}/init.d/npcd
%{pnp4nagios_datadir}/*
%{nagios_plugindir}/*
%exclude %{nagios_plugindir}/check_pnp_rrds.pl
%attr(0644,root,root) %{_mandir}/man8/*
%defattr(775,wwwrun,www)
%{pnp4nagios_datadir}/application/cache
%{pnp4nagios_datadir}/application/logs

%files nagios
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/permissions.d/%{name}-nagios
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-nagios
%dir %{pnp4nagios_perfdata_spooldir}
%dir %{pnp4nagios_perfdata_dir}
%dir %{pnp4nagios_logdir}
%dir %{pnp4nagios_logdir}/stats

%files icinga
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/permissions.d/%{name}-icinga
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-icinga
%dir %{pnp4nagios_perfdata_spooldir}
%dir %{pnp4nagios_perfdata_dir}
%dir %{pnp4nagios_logdir}
%dir %{pnp4nagios_logdir}/stats

%files -n nagios-plugins-pnp_rrds
%defattr(-,root,root)
%dir %{nagios_libdir}
%dir %{nagios_plugindir}
%{nagios_plugindir}/check_pnp_rrds.pl

%changelog
* Tue Feb 11 2014 ecsos@schirra.net
- fix build errors by running 09-check-packaged-twice
* Thu Aug 22 2013 lars@linux-schulserver.de
- create two new subpackages for Icinga and Nagios users:
  pnp4nagios-icinga and pnp4nagios-nagios contain the directories
  (and files) that are different as result of different users and
  groups of those two main monitoring packages
- remove logrotate source file and create it inside the spec file
  instead
* Sun Jul 14 2013 lars@linux-schulserver.de
- added permissions file for Icinga users
  (/var/lib/pnp4nagios* should be owned by icinga in this case)
- added logrotate snipplet for perfdata.log (which is disabled
  by default)
- added README.SuSE-Icinga
- fix path to livestatus socket in config*.php
* Mon Mar 25 2013 lars@linux-schulserver.de
- update to 0.6.21:
  + Feature: Helper functions rrd::alerter and rrd:alerter_gr both
    supports treshold detection
  + Update:  jQuery Mobile update to 1.3.0
* Sun Mar  3 2013 lars@linux-schulserver.de
- update to 0.6.20:
  + Feature: Support check_mk Multisite Cookie Auth (Lars Michelsen)
  + Feature: Allow RRD unknown values (Simon Meggle)
  + feature: Interactive delete mode added to check_rrds.pl (Simon Meggle)
  + Bugfix:  Allow multiple gearman servers (Craig Barraclough)
  + Bugfix:  Fixed Graph Search (Stefan Triep)
  + Update:  jQuery update to 1.8.1
  + Update:  jQueryUI update to 1.8.23
* Sun Dec 30 2012 lars@linux-schulserver.de
- fix the apache configuration to work as include also with enabled
  SSL
- fix wrong rewrite base PKG_NAME in apache config
* Sun Dec  2 2012 lars@linux-schulserver.de
- update to 0.6.19:
  + Bugfix:  socketDOMAIN changed to AF_INET while using livstatus
    tcp socket ( Rene Koch )
  + Fix:     simplify/improve apache rules (Christoph Anton Mitterer)
  + Fix:     Check for missing PHP GD functions
  + Feature: Parameter "width" added to popup controller (Andreas Doehler)
* Sun Jul 22 2012 lars@linux-schulserver.de
- only place check_pnp_rrds.pl in nagios-plugins-pnp_rrds
* Thu Jul 12 2012 lars@linux-schulserver.de
- update to 0.6.18:
  * Bugfix:  Fixed STORAGE_TYPE and CUSTOM_TEMPLATE vars used in
    custom templates
  * Bugfix:  Blank screen on PHP 5.4 fixed
  * Feature: Allow multiple gearman job servers
  * Feature: New helper function rrd::debug()
  * Feature: New templates check_jmx4perl_*.php
* Thu Jun 14 2012 schneemann@b1-systems.de
- update to 0.6.17:
  * Bugfix: Fixed rrd_convert.pl while running with âdry-run
  * Bugfix: logging.c include missing header files ( Lars Vogdt )
  * Bugfix: Check if pnp4nagios/etc/rra.cfg is readable
  * Bugfix: rrd_convert.pl use XML tag TEMPLATE instead of
    CHECKCOMMAND to selects RRDs ( Sven Velt )
  * Feature: npcdmod.o increase perfdata buffer and log discarded
    perfdata ( Birger Schmidt )
  * Feature: rrd_modify.pl to change number of data sources of an
    RRD file
  * Feature: New template check_apachestatus_auto.php
  * Feature: Implement etc/config.d to place config snippets
    ( Lars Michelsen )
* Wed Jan 18 2012 lars@linux-schulserver.de
- disabled recommendation of nagios-www as pnp4nagios can also be
  installed with icinga. But the recommends triggers the installation
  of nagios even in this case.
  We might think about a virtual "Provides: monitoring" later, but
  first fix the current problem.
* Tue Nov 29 2011 lars@linux-schulserver.de
- print a warning, if old /etc/nagios/pnp directory is still there
- update to 0.6.16:
  * Bugfix:  Fixed single quoted check_multi labels
    (Reported by Matthias Flacke)
  * Bugfix:  Append missing slash to perfdata_spool_dir
    (Reported by Juergen-Michael Radtke)
  * Bugfix:  Fixed jQuery-ui multisite theme
  * Feature: PDF margins are now adjustable via config.php
    (Thomas Witzenrath)
  * Feature: Support for PDF size 'letter' added ( Robert Becht )
* Sat Nov  5 2011 lars@linux-schulserver.de
- use nagios-rpm-macros to export some internal directories and
  filenames used/defined during build, so other applications can
  make use of them
* Sun Oct  9 2011 lars@linux-schulserver.de
- just recommend nagios-www to allow clean icinga installation
- use macros from nagios-rpm-macros package
- added xinetd file
- rework patches
* Sat Sep 24 2011 lars@linux-schulserver.de
- update to 0.6.15:
  + new Webinterface for mobile devices based on jQuery Mobile
  + Zoom based on jQuery plugin imgAreaSelect
  + New template check_mssql_health.php
  + "Clear basket" button added
  + New helper function "rrd::alerter_gr()"
  + Helper rrd::vdef() fixed
  + Fixed Overview link
  + Fixed zoom popup
  + Fixed double urlencode()
* Sun May 22 2011 lars@linux-schulserver.de
- rewrite of the package:
  + use /etc/pnp4nagios as config directory
  + webui is now located in /usr/share/pnp4nagios
  + use own logdir /var/log/pnp4nagios
  + use own spooldir /var/spool/pnp4nagios
  + use own dir for rrds /var/lib/pnp4nagios
- update to 0.6.13:
  + New option --ignore-hosts added to check_pnp_rrds.pl
  + New options zgraph_width and zgraph_height in config.php
  + rrd_convert.pl: parse_xml_filename() regex fix
  + mod_gearman support added
  + rrd_convert.pl is now able to convert all RRDs from
    RRD_STORAGE_TYPE=SINGLE to RRD_STORAGE_TYPE=MULTIPLE
  + New template check_gearman.php
  + rrd_convert.pl is now able to parse xml dumps created
    by rrdtool 1.4.x
  + process_perfdata.pl default timeout value set to 15 seconds
* Sat Feb 26 2011 lars@linux-schulserver.de
- remove duplicated Alias definition from apache config
- enable pnp4nagios in apache during first install
* Tue Jun 29 2010 lars@linux-schulserver.de
- update to 0.6.4:
  + Update: jQuery Update to 1.4.2
  + Update: jQuery-ui Update to 1.8
  + Feature: New configure Option --with-base-url
  + Template: New template check_ntp_time.php (Mathias Kettner)
  + Feature: New i18n files for fr_FR (Yannig Parre)
  + Feature: New jQuery Theme 'multisite'
- rebased patches
- added Should-Stop to init script
* Tue Mar 23 2010 lars@linux-schulserver.de
- update to 0.6.3:
  + Feature: New helper script libexec/rrd_convert.pl
  + Feature: XML_WRITE_DELAY option added to process_perfdata.cfg
    as suggested by Mathias Kettner
  + Feature: New template integer.php
  + Feature: PNP will now work with lighttpd and php-cgi
  + Feature: PNP will now work without mod_rewrite
  + Update: FPDI update to 1.3.1
  + Template: check_mk-ps.perf.php added ( by Mathias Kettner )
  * Template: New template check_hpasm.php
  * Template: Updates for check_openmanage.php, check_hp_bladecenter.php
    and check_dell_baldecenter.php
  * Workaround: Allow "trailing unfilled semicolons".
    Workaround for nsclient++
  * Bugfix: Installer now checks for json_decode()
  * Bugfix: Ignore old XML files while building the service list
  + Bugfix: Wrong pdf link used on site 'pages' and 'basket'
  + Bugfix: Incorrect group permissions on spool directory
* Tue Dec 15 2009 lars@linux-schulserver.de
- update to 0.6.1
  + Webfrontend based on http://www.kohanaphp.com (separate package)
  + Javascript-functions using jQuery plugins
  + process_perfdata.pl will be able to use one RRD database
    per datasource
  + RRDtool errors are now displayed as images. no more missing images
  + PNP templates cannot overwrite internal variables anymore
  + PNP templates of version 0.4.x can still be used
  + PDF functions recoded
  + Template default.php optimized
  + Export from RRD databases into XML, CSV and JSON format using the
    RRDtool "xport" function
  + Page functions recoded
  + Error pages links to online FAQ
  + Mouseover Popup in Nagios frontend via jQuery.clueTip plugin
  + Full support of rrdcached
  + RRD heartbeat per check_command -> tpl_custom
  + New config.php option pdf_graph_opt
  + Recognize the 'background_pdf' option in page definitions
  + Recognize the 'source' option in page definitions
  + Array $TIMERANGE now available for templates
  + Store internal runtime statistics on a per minute base
  + Added two widgets views/widget_menu.php and views/widget_graph.php
- improved apache include config
- pnp4nagios requires kohana now
* Thu Jul 23 2009 lars@linux-schulserver.de
- update to 0.4.14:
  + Use Nagios TIMET Macro while creating new RRD Databases.
  + New config option enable_recursive_template_search.
  + Better signal handling in process_perfdata.pl
  + FIX: Optimized check_multi detection.
  + FIX: Popups are now working with IE.
  + RRA config per check_command.
- recommend dejavu
* Tue Mar 17 2009 lars@linux-schulserver.de
- enhance the command template for users using NPCD to process
  their performance data.
* Fri Feb 20 2009 lars@linux-schulserver.de
- update to 0.4.13:
  + Overlib 4.21 included http://www.bosrup.com/web/overlib/
  + Prototype Ajax Framework 1.6.0.3 included http://www.prototypejs.org/
  + Script.aculo.us Update to 1.8.1
  + FIX: Function rrd_fetch renamed to rrdtool_fetch to avoid
    naming conflict
  + Experimental: New npcd Event Broker Module - handle with care
  + Experimental: New special templates stored in templates.special
  + FIX: autoconf detection for getloadavg() - ignore
    loadthreshold if not available
  + FIX: Host OS Detection for mod_cflags/mod_ldflags
* Tue Oct 28 2008 lars@linux-schulserver.de
- update to 0.4.12:
  + Remove Call-time pass-by-reference
  + FIX: Fixed wrong check_multi service description
  + FIX: Fixed page config parser
* Fri Aug 29 2008 lars@linux-schulserver.de
- add <IfDefine PNP4NAGIOS> to the apache configuration to
  avoid startup problems if SSL is enabled and no SSLKey is
  available for this config.
* Wed Jul 16 2008 lars@linux-schulserver.de
- update to 0.4.10:
  + BUGFIX: Fixed wrong link to avail.cgi used on pages.
  + BUGFIX: DonÂ´t exit process_perfdata.pl when process_perfdata.cfg
    is missig.
  + Report missing RRDs Perl Modules.
* Fri May 16 2008 lars@linux-schulserver.de
- update to 0.4.9:
  + process_perfdata.pl results in timeouts and broken XML files
    caused by missing RRDs Perl Modules
- removed pnp-0.4.7-buffer_overflow.patch
* Thu May  1 2008 lars@linux-schulserver.de
- update to 0.4.8:
  + New process_perfdata.pl option -c [âconfig] to specify an
    alternate config file.
  + France Translation added by Jean-Marie Le Borgne
  + XML Encoding can now be changed by using XML_ENC in
    process_perfdata.cfg
  + Set SetAutoPageBreak() in doPDF function.
  + New Option background_pdf can be used in page definitions to
    override the defaults.
  + process_perfdata.cfg: Option RRD_HEARTBEAT added.
  + New NPCD Option: sleep_time
  + Fixed process_perfdata.pl race condition: config file timeout
    now won't be ignored
  + Backslashes used in service descriptions are now substituted
    to underscores.
* Sat Apr 12 2008 lars@linux-schulserver.de
- fix directory ownership
- fix execute bits for process_perfdata.pl
- safe_mode must currently be off to keep it easily running
- added nagios-pnp.cfg containing command definitions
* Thu Mar 13 2008 lars@linux-schulserver.de
- update to 0.4.7:
  + Fixed compiler errors on Solaris
  + Switched to autoconf 2.61
  + Fixed is_file() on older SuSE releases
* Mon Feb 11 2008 lars@linux-schulserver.de
- update to 0.4.6:
  + XML Tag <RRD> reflects the last rrdtool returncode and text.
  + parse_xml() cleanup.
  + Improved check_multi support.
  + Calendar added to all views.
  + New Icons based on KDE Theme nuvoX.
  + Fixed libpng write errors.
  + Added suport for threshold range format
  + New Template check_snmp_int-bits.php.
    Output is displayed in Bits/s
  + NPCD now takes care about the exit status
    of the executed command
  + No more PID File creation without Daemon Mode
  + Load thresholding through config file (experimental)
  + No try to write PID File after a HUP Signal
  + File Log is now ready for testing
  + Rotation of logfile
  + New configure option: âwith-perfdata-spool-dir
  + Stay in the current timerange when switching between pages
  + New Configure Option âwith-init-dir
* Tue Dec 18 2007 lars@linux-schulserver.de
- initial release 0.4.3

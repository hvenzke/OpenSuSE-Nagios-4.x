
# spec file for package nrpe
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


#       default
%define nagios3only 0
# Macro that print mesages to syslog at package (un)install time
%define nnmmsg logger -t %{name}/rpm
%define nrpeport 5666

Name:           nrpe
Version:        2.15
Release:        1.1
Summary:        Nagios Remote Plug-In Executor
License:        GPL-2.0+
Group:          System/Monitoring
Url:            http://www.nagios.org/
Source0:        nrpe-%{version}.tar.bz2
Source1:        nrpe.init
Source2:        nagios-nrpe-rpmlintrc
Source3:        nagios-nrpe-SuSEfirewall2
Source4:        nrpe.8
Source10:       README.SuSE
# PATCH-FIX-openSUSE place the service disabled in the directory
Patch1:         nrpe-xinetd.patch
# PATCH-FIX-openSUSE adapts NRPE to support the standard buffersize of Nagios 3.x
Patch2:         nagios-nrpe-buffersize.patch
# PATCH-FIX-UPSTREAM produce more randomness and do not reduce entropy on Linux kernels
Patch3:         nrpe-more_random.patch
# PATCH-FIX-UPSTREAM improve help output of nrpe and check_nrpe
Patch4:         nrpe-improved_help.patch
# PATCH-FIX-UPSTREAM null buffer before using it
Patch5:         nrpe-weird_output.patch
# PATCH-FIX-UPSTREAM drop privileges before writing the pidfile for more safety
Patch6:         nrpe-drop_privileges_before_writing_pidfile.patch
# PATCH-FIX-openSUSE fix pathnames for nrpe_check_control command
Patch10:        nrpe_check_control.patch
# PATCH-FIX-UPSTREAM using implicit definitions of functions
Patch11:        nrpe-implicit_declaration.patch
PreReq:         %fillup_prereq
PreReq:         %insserv_prereq
PreReq:         /bin/logger
PreReq:         coreutils
PreReq:         grep
PreReq:         netcfg
PreReq:         pwdutils
PreReq:         sed
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} > 1130
PreReq:         sysvinit(network)
PreReq:         sysvinit(syslog)
%endif
#
BuildRequires:  nagios-plugins-common
BuildRequires:  nagios-rpm-macros
BuildRequires:  tcpd-devel
#
%if 0%{?suse_version} > 1000
BuildRequires:  krb5-devel
%else
BuildRequires:  heimdal-devel
%endif
#
%if 0%{?suse_version} > 1020
BuildRequires:  libopenssl-devel
BuildRequires:  openssl
%else
BuildRequires:  openssl-devel
%endif
#
%if 0%{?suse_version} > 1020
Recommends:     inet-daemon
Recommends:     nagios-plugins-users
Recommends:     nagios-plugins-load
Recommends:     nagios-plugins-disk
Recommends:     nagios-plugins-procs
%else
Requires:       inet-daemon
Requires:       nagios-plugins
%endif
#
Provides:       nagios-nrpe = %{version}
Obsoletes:      nagios-nrpe < 2.14
Provides:       nagios-nrpe-client = %{version}
Obsoletes:      nagios-nrpe-client < 2.14

%description
NRPE can be used to run nagios plug-ins on a remote machine for
executing local checks.
This package contains the software for NRPE server.
It could be run by inet-daemon or as stand-alone daemon

%package doc
Summary:        Nagios Remote Plug-In Executor documentation
Group:          Documentation/Other
Provides:       nagios-nrpe-doc = %{version}
Obsoletes:      nagios-nrpe-doc < 2.14

%description doc
This package contains the README files, OpenOffice and PDF
documentation for the remote plugin executor (NRPE) for nagios.

%package -n nagios-plugins-nrpe
Summary:        Nagios NRPE plugin
Group:          System/Monitoring
%if 0%{?suse_version} > 1020
Recommends:     monitoring_daemon
%endif
Provides:       nagios-nrpe-server = %{version}
Obsoletes:      nagios-nrpe-server < 2.14

%description -n nagios-plugins-nrpe
This package contains the plug-in for the host runing the Nagios
daemon.

It is used to contact the NRPE process on remote hosts. The plugin
requests that a plugin be executed on the remote host and wait for the
NRPE process to execute the plugin and return the result.

The plugin then uses the output and return code from the plugin
execution on the remote host for its own output and return code.

%prep
%setup -q
%patch1 -p0
%if %{nagios3only}
%patch2 -p0
%endif
%patch3 -p0
%patch4 -p1
%patch5 -p0
%patch6 -p0
%patch10 -p0
%patch11 -p0
cp -a %{SOURCE10} .
chmod -x contrib/README.nrpe_check_control
%if 0%{?suse_version} > 01110
# increase the number of 'allowed' processes on newer systems:
sed -i "s|check_procs -w 150 -c 200|check_procs -w 250 -c 300|g" sample-config/nrpe.cfg.in
%endif
# add the new include directory
sed -i "s|#include_dir=<someotherdirectory>|#include_dir=<someotherdirectory>\ninclude_dir=/etc/nrpe.d|g" sample-config/nrpe.cfg.in

%build
%configure \
        --sbindir=%{nagios_cgidir} \
        --libexecdir=%{nagios_plugindir} \
        --datadir=%{nagios_datadir} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{nagios_logdir} \
        --exec-prefix=%{_sbindir} \
        --bindir=%{_sbindir} \
        --with-log_facility=daemon \
        --with-kerberos-inc=%{_includedir} \
        --with-nagios-user=%{nagios_user} \
        --with-nagios-group=%{nagios_group} \
        --with-nrpe-user=%{nagios_user} \
        --with-nrpe-group=%{nagios_group} \
        --with-nrpe-port=%nrpeport \
        --enable-command-args \
        --enable-bash-command-substitution \
        --enable-ssl
make %{?_smp_mflags} all

gcc %{optflags} -o contrib/nrpe_check_control contrib/nrpe_check_control.c

%install
%nagios_command_user_group_add
install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_localstatedir}/run/%{name}
install -d %{buildroot}%{_sysconfdir}/nrpe.d
make install install-daemon install-daemon-config install-xinetd \
    DESTDIR=%{buildroot} \
    INSTALL_OPTS="" \
    COMMAND_OPTS="" \
    CGICFGDIR="%{_sysconfdir}" \
    NAGIOS_INSTALL_OPTS="" \
    NRPE_INSTALL_OPTS="" \
    INIT_OPTS=""

install -Dm 644 %{SOURCE4} %{buildroot}%{_mandir}/man8/nrpe.8
install -Dm 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/nrpe
ln -s -f ../../etc/init.d/nrpe %{buildroot}%{_sbindir}/rcnrpe

# install SuSEfirewall2 script
%if 0%{?suse_version} > 1020
install -Dm644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/nrpe
%endif

# fix pid_file in nrpe.cfg
sed -i -e "s,^\(pid_file=\).*,\1/var/run/%{name}/nrpe.pid," %{buildroot}/%{_sysconfdir}/nrpe.cfg

# create directory and pidfile (package them as ghost)
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
touch %{buildroot}%{_localstatedir}/run/%{name}/nrpe.pid

# create home directory of nagios user
mkdir -p %{buildroot}%{nagios_localstatedir}

# create contrib plugin
install -m0755 contrib/nrpe_check_control %{buildroot}%{nagios_plugindir}/nrpe_check_control
cat > nrpe_check_control.cfg <<'EOF'
define command {
    command_name    nrpe_check_control
    command_line    %{nagios_plugindir}/nrpe_check_control $SERVICESTATE$ $SERVICESTATETYPE$ $SERVICEATTEMPT$ "$HOSTNAME$"
}
EOF
install -Dm0644 nrpe_check_control.cfg %{buildroot}%{nagios_sysconfdir}/objects/nrpe_check_control.cfg

%pre
# Create user and group on the system if necessary
%nagios_user_group_add
%nagios_command_user_group_add
# check if the port for nrpe is already defined in /etc/services
if grep -q %nrpeport /etc/services ; then
    : OK - port already defined
else
    %nnmmsg "Adding port %nrpeport to /etc/services"
        echo "nrpe            %nrpeport/tcp # Nagios nrpe" >> etc/services
fi

%preun
%stop_on_removal %{name}

%post
%{fillup_and_insserv -fy %{name}}

%triggerun -- nagios-nrpe < 2.14
STATUS='/var/adm/update-scripts/nrpe'
if [ -x %{_sysconfdir}/init.d/nrpe ]; then
    %{_sysconfdir}/init.d/nrpe status >/dev/null
    if test $? = 0; then
        echo "%{_sysconfdir}/init.d/nrpe restart" >> "$STATUS"
    else
        touch "$STATUS"
    fi
    chmod +x "$STATUS"
fi
if [ -x %{_sysconfdir}/init.d/xinetd ]; then
    %{_sysconfdir}/init.d/xinetd status >/dev/null
    if test $? = 0; then
        echo "%{_sysconfdir}/init.d/xinetd try-restart" >> "$STATUS"
    else
        touch "$STATUS"
    fi
    chmod +x "$STATUS"
fi

%triggerpostun -- nagios-nrpe < 2.14
# Move /etc/nagios/nrpe.cfg to /etc/nrpe.cfg when updating from an old version
# and inform the admin about the rename.
if test -e %{nagios_sysconfdir}/nrpe.cfg.rpmsave -a ! -e %{_sysconfdir}/nrpe.cfg.rpmnew; then
    mv %{_sysconfdir}/nrpe.cfg %{_sysconfdir}/nrpe.cfg.rpmnew
    mv %{nagios_sysconfdir}/nrpe.cfg.rpmsave %{_sysconfdir}/nrpe.cfg
    echo "# %{nagios_sysconfdir}/nrpe.cfg has been moved to %{_sysconfdir}/nrpe.cfg" > %{nagios_sysconfdir}/nrpe.cfg
    echo "# This file can be removed." >> %{nagios_sysconfdir}/nrpe.cfg
    echo "include=%{_sysconfdir}/nrpe.cfg" >> %{nagios_sysconfdir}/nrpe.cfg
fi
sed -i "s|%{nagios_sysconfdir}/nrpe.cfg|%{_sysconfdir}/nrpe.cfg|g" %{_sysconfdir}/xinetd.d/nrpe || :
sed -i "s|nrpe-service|%{name}|g" %{_sysconfdir}/sysconfig/SuSEfirewall2 || :
if [ -e /var/adm/update-scripts/nrpe ]; then
    /bin/sh /var/adm/update-scripts/nrpe
    rm /var/adm/update-scripts/nrpe
fi

%postun
%restart_on_update nrpe
%insserv_cleanup

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.SuSE README.SSL SECURITY
%{_mandir}/man8/nrpe.8*
%dir %{_sysconfdir}/nrpe.d
%config(noreplace) %{_sysconfdir}/nrpe.cfg
%config(noreplace) %{_sysconfdir}/xinetd.d/nrpe
%if 0%{?suse_version} > 1020
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/nrpe
%endif
%{_sysconfdir}/init.d/nrpe
%{_sbindir}/nrpe
%{_sbindir}/rcnrpe
%ghost %dir %{_localstatedir}/run/%{name}
%ghost %{_localstatedir}/run/%{name}/nrpe.pid

%files doc
%defattr(0644,root,root,0755)
%doc Changelog LEGAL README README.SSL README.SuSE SECURITY docs/*.pdf

%files -n nagios-plugins-nrpe
%defattr(-,root,root)
%doc contrib/README.nrpe_check_control
%dir %{nagios_libdir}
%attr(0755,root,%{nagios_command_group})           %dir %{nagios_sysconfdir}
%attr(0755,root,%{nagios_command_group})           %dir %{nagios_sysconfdir}/objects
%config(noreplace) %{nagios_sysconfdir}/objects/nrpe_check_control.cfg
%{nagios_plugindir}/check_nrpe
%{nagios_plugindir}/nrpe_check_control

%changelog
* Thu Sep 26 2013 lars@linux-schulserver.de
- adapt directory ownership of /etc/nagios directories
* Thu Sep 19 2013 lars@linux-schulserver.de
- update to 2.15:
  + Added support for IPv6 (Leo Baltus, Eric Stanley)
- removed nrpe-uninitialized_variable.patch (fixed upstream)
- rebased other patches
* Mon Aug 12 2013 lars@linux-schulserver.de
- fix directory permissions for nagios sysconfdir
* Mon Aug  5 2013 ro@suse.de
- adapt owner and permissions for sysconfdir/nagios to
  main nagios package
* Sun Jan 20 2013 lars@linux-schulserver.de
- reduce runtime dependencies: just recommend the plugins that are
  configured in the default configuration, not the whole Nagios
  plugins
* Tue Jan 15 2013 lars@linux-schulserver.de
- also fix old xinetd config and SuSEFirewall2
- save the status of the old nagios-nrpe daemon via %%%%triggerun in
  /var/adm/update-scripts/nrpe and restart the service, if needed,
  after the renamed package has been installed (same, if the
  service is started via xinetd)
* Sat Dec 22 2012 lars@linux-schulserver.de
- update to 2.14:
  + Added configure option to allow bash command substitutions,
    disabled by default [bug #400] (Eric Stanley)
  + Patched to shutdown SSL connection completely (Jari Takkala)
- enable bash command substitution in binary (disabled by config)
- renamed the main package to nrpe to follow upstream
  (Provide/Obsolete the old package name)
- placed nrpe.cfg in /etc now to allow running with Icinga only
- add include directory /etc/nrpe.d to make future updates easier
- increase check_procs warning (250) and critical (300) levels
- use new rpm macro nagios_user_group_add for user-/groupadd
- refreshed patches
* Tue Nov 20 2012 dimstar@opensuse.org
- Fix useradd invocation: -o is useless without -u and newer
  versions of pwdutils/shadowutils fail on this now.
* Thu Oct 11 2012 lars@linux-schulserver.de
- the plugin can also be used with icinga
  - > recommend monitoring_daemon instead
* Sun Feb 26 2012 lars@linux-schulserver.de
- update to 2.13:
  + Applied Kaspersky Labs supplied patch for extending
    allowed_hosts (Konstantin Malov)
  + Fixed bug in allowed_hosts parsing (Eric Stanley)
- rebased patches
- simplify (and disable) nrpe-more_random.patch
- added nrpe-implicit_declaration.patch
- use macros from nagios-rpm-macros
* Mon May 30 2011 lrupp@suse.de
- specfile cleanup using spec-cleaner (add comments to patches)
* Thu Feb 10 2011 ro@suse.de
- add directory to filelist to fix build
* Mon Feb  7 2011 lars@linux-schulserver.de
- also package nrpe_check_control from contrib
* Tue Dec  7 2010 coolo@novell.com
- prereq init scripts syslog and network
* Wed Sep 22 2010 lars@linux-schulserver.de
- use /var/lib/nagios as home directory (same as nagios package)
* Sat Jul 10 2010 lars@linux-schulserver.de
- fix missing operand for dirname in init script
* Mon May 24 2010 lars@linux-schulserver.de
- add netcfg to PreReq to have /etc/services installed
  (fixes bnc #608164 )
* Wed May  5 2010 lars@linux-schulserver.de
- set default values in init script
* Mon May  3 2010 lars@linux-schulserver.de
- fix file ownership in /etc
- added nrpe manpage from debian
- added adapted patches from Debian:
  + nrpe-more_random.patch (overwrite the buffer with better
    randomness)
  + nrpe-improved_help.patch (list additional commandline options)
  + nrpe-weird_output.patch (null the buffer before using it)
  + nrpe-drop_privileges_before_writing_pidfile.patch (name says all)
- added the following patches to fix compilation warnings:
  + nrpe-return_value.patch
  + nrpe-uninitialized_variable.patch
  + nrpe-unused_variable.patch
* Thu Apr 29 2010 lars@linux-schulserver.de
- use /var/run/nrpe/nrpe.pid for pidfile; nagios can be run as
  different user/group which might cause conflicts
- clean up the init skript and implement automatic movement/
  creation of the pid directory
- package /var/run/nrpe/nrpe.pid as ghost
* Sat Mar  6 2010 chris@computersalat.de
- cleanup subpackages
  o nagios-nrpe is default package and provides NRPE daemon
    obsoletes: client
  o nagios-plugins-nrpe provides the check plugin to be installed
    with the nagios host
    obsoletes: server
- cleanup spec
  o sort TAGS
  o removed/added define
  - nsusr == nrpeusr
  - nsgrp == nrpegrp
  - added cmdgrp
  - redefine _libexecdir
  o added PreReq
  o fix pre{,un}/post{,un} sections
  - no restart_on_update x{,inetd}, cause xinet file is
    installed 'disabled' by default
  - service port is needed with server, not with plugin
  - no restart_on_update nagios when nrpe plugin is update
    there is also no restart_on_update when nagios_plugins
    are updated
  o fix nrpe.cfg
    o PID_File => /var/run/nagios/nrpe.pid
- SOURCE mods
  o reworked patches (Makefile,xinetd)
  o replaced rcnrpe with nrpe.init
  o added README.SuSE
* Wed Dec 23 2009 aj@suse.de
- Use -fno-strict-aliasing to CFLAGS since the code is not clean.
- Own /etc/nagios directory.
- Add _GNU_SOURCE to CFLAGS to get prototype of asprintf.
* Mon Dec  1 2008 lrupp@suse.de
- disable buffersize patch per default: breaks compatibility
- run try-restart only if the service is installed
* Thu Nov 27 2008 lrupp@suse.de
- Added nagios-nrpe-buffersize.patch: support long check output
  of plugins, which is possible since Nagios 3.0
* Mon Oct 13 2008 lrupp@suse.de
- added cron to Should-Start/Should-Stop, so nrpe starts even on
  curious systems
- added nagios-nrpe-SuSEfirewall2
- use --with-log_facility=daemon
* Wed Sep 10 2008 lars@linux-schulserver.de
- disable nrpe in xinetd per default
- use a more stupid way to get the port in etc/services
* Mon Jul 28 2008 lars@linux-schulserver.de
- move the Requires from the main- into the subpackage
* Tue Mar 11 2008 lars@linux-schulserver.de
- update to 2.12:
  + Fix for unterminated multiline plugin (garbage) output
    (Krzysztof Oledzki). Needed for nagios 3.0
- own the docu directory
- added rpmlintrc
* Tue Jan 29 2008 lars@linux-schulserver.de
- Update to 2.11:
  + Added lib64 library paths to configure script for
    64-bit systems (John Maag)
  + Added --with-ssl-lib configure script option
  + Added --with-log-facility option to control syslog logging
    (Ryan Ordway and Brian Seklecki)
* Mon Jan 21 2008 lars@linux-schulserver.de
- start the client automatically
* Wed Jan  9 2008 lars@linux-schulserver.de
- split out the documenation to an extra package
* Thu Dec 27 2007 lars@linux-schulserver.de
- use user nagios and group nagios to run as daemon (client)
- try to add the nrpeport to /etc/services if not done already
* Wed Dec 26 2007 lars@linux-schulserver.de
- back to nagios* again as all pathnames are now identical
* Tue Nov 27 2007 lars@linux-schulserver.de
- rename to nagios3*
- use new libexecdir
* Fri Nov 23 2007 lars@linux-schulserver.de
- require krb5 for suse_version < 1000; otherwise heimdal
* Thu Oct 25 2007 tsieden@suse.de
- Moved PDF docs to docs/ subdirectory, added OpenOffice source document
- A critical result is now returned for child processed that die due to a signal (Klas Lindfors)
- Fixed bug with --with-nrpe-group configure script option (Graham Collinson)
- Fixed bug with check_disk thresholds in sample config file (Patric Wust)
- Added NRPE_PROGRAMVERSION and NRPE_MULTILINESUPPORT environment variables
  for scripts that need to detect NRPE version and capabilities (Gerhard Lausser)
- Added asprintf() support for systems that are missing it (Samba team)
* Mon May 21 2007 tsieden@suse.de
- fix build (Requires libopenssl and openssl for 10.3 and beyond)
* Wed May 16 2007 tsieden@suse.de
- update to version 2.8.1
  * Fixed configure script error with user-specified NRPE group
  * Added support for multiline plugin output (limited to 1KB at the moment) (Matthias Flacke)
  * Changes to sample config files
  * Added ';' as an additional prohibited metachar for command arguments
  * Updated documentation and added easier installation commands
* Mon Mar 12 2007 tsieden@suse.de
- update to version 2.7.1
  * Changed C++ style comment to C style to fix compilation errors on AIX
    (Ryan McGarry)
  * Patches for detection SSL header and library locations
    (Andrew Boyce-Lewis)
  * NRPE daemon will now partially ignore non-fatal configuration file
    errors and attempt to startup (Andrew Boyce-Lewis)
* Tue Jan 30 2007 tsieden@suse.de
- update to version 2.6
  * Added -u option to check_nrpe to return UNKNOWN states on socket
    timeouts (Bjoern Beutel)
  * Added connection_timeout variable to NRPE daemon to catch dead
    client connections (Ton Voon)
  * Added graceful timeout to check_nrpe to ensure connection to
    NRPE daemon is properly closed (Mark Plaksin)
* Sat Jul  1 2006 stark@suse.de
- update to version 2.5.2
  * number of bugfixes
  * Added optional command line prefix
  * Added ability to reload config file with SIGHUP
* Fri Jan 27 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 24 2006 stark@suse.de
- added patch to fix config parser regression
* Mon Jan 23 2006 stark@suse.de
- update to version 2.2
- enabled TCP wrapper support
* Wed Jan 18 2006 stark@suse.de
- added -fstack-protector
- added service handling for update and removal
* Tue Jan 17 2006 stark@suse.de
- added init script (#143288)
- fixed xinet configuration (#143288)
* Tue Nov 18 2003 stark@suse.de
- update to 2.0 final
- don't build as root
* Mon Sep 15 2003 stark@suse.de
- require inet-daemon (#30752)
- use port number in xinet config (#30754)
* Thu Jul 24 2003 stark@suse.de
- update to 2.0b5
* Mon Jul 21 2003 stark@suse.de
- update to 2.0b4
  * minor fixes
* Thu Jun 19 2003 stark@suse.de
- added nagios-plugins to neededforbuild (fixing directory
  ownerships)
* Tue May 20 2003 stark@suse.de
- update to 2.0b3
  * Added support for passing arguments to command
  * NRPE daemon can no longer be run as root user/group
  * Added native SSL support (Derrick Bennett)
* Wed Feb  5 2003 stark@suse.de
- update to 1.8
  * Daemon now closes stdio/out/err properly
  * Makefile changes
  * Mode command line option bug fix in daemon
  * Fixed incorrect command line options in check_nrpe plugin
* Thu Jan 16 2003 stark@suse.de
- added /etc/xinetd.d/nagios-nrpe
- moved nrpe to /usr/bin
* Mon Jan 13 2003 stark@suse.de
- update to 1.7
  * Syntax changes (-H option specifies host name in check_nrpe,
  - c option specifies config file in nrpe)
  * Added command_timeout directive to config file to allow user
    to specify timeout for executing plugins
* Thu Sep 26 2002 stark@suse.de
- initial package

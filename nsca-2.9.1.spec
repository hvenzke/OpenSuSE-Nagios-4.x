#
# spec file for package nsca
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


Name:           nsca
Version:        2.9.1
Release:        2.1.2
Summary:        The Nagios Service Check Acceptor
License:        GPL-2.0+
Group:          System/Monitoring
Url:            http://www.nagios.org/
Source0:        %{name}-%{version}.tar.bz2
Source1:        rcnsca
Source2:        nsca-rpmlintrc
Source3:        nsca-SuSEfirewall2
Source4:        send_nsca.1
Source5:        nsca.1
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch1:         nsca.abuild.patch
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch2:         nsca.xinetd.patch
# PATCH-MISSING-TAG -- See http://en.opensuse.org/Packaging/Patches
Patch3:         nsca.spooldir.patch
BuildRequires:  libmcrypt-devel
BuildRequires:  nagios-rpm-macros
BuildRequires:  tcpd-devel
Recommends:     monitoring_daemon
Provides:       nagios-nsca = %{version}
Obsoletes:      nagios-nsca < 2.9.2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The purpose of this add-on is to allow the execution of NetSaint and
Nagios plug-ins on a remote host in a manner that is as transparent as
possible. This is the server part including the daemon without the
client program.

%package client
Summary:        The Nagios Service Check Acceptor Client
Group:          System/Monitoring
Provides:       nagios-nsca-client = %{version}
Obsoletes:      nagios-nsca-client < 2.9.2

%description client
The purpose of this add-on is to allow the execution of NetSaint and
Nagios plug-ins on a remote host in a manner that is as transparent as
possible. This package includes only the client program.

%prep
%setup -q
%patch1
%patch2
%patch3

%build
export CFLAGS="%{optflags}"
%if %suse_version > 1000
export CFLAGS="$CFLAGS -fstack-protector"
%endif
%configure \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{nagios_spooldir} \
        --with-nsca-user=%{nagios_user} \
        --with-nsca-grp=%{nagios_group} \
        --with-nsca-port=5667
make all

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_initddir}/
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d/
install -m 755 src/nsca %{buildroot}%{_bindir}/
install -m 755 src/send_nsca %{buildroot}%{_bindir}/
install -m 644 sample-config/nsca.cfg %{buildroot}%{_sysconfdir}/
install -m 644 sample-config/send_nsca.cfg %{buildroot}%{_sysconfdir}/
install -m 644 sample-config/nsca.xinetd %{buildroot}%{_sysconfdir}/xinetd.d/nsca
install -m 755 %{SOURCE1}    %{buildroot}%{_sysconfdir}/init.d/nsca
ln -sf ../../%{_sysconfdir}/init.d/nsca %{buildroot}%{_sbindir}/rcnsca
chmod 644 README
# install SuSEfirewall2 script
%if 0%{?suse_version} > 1020
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/%{name}
%endif
# install man pages
install -Dm644 %{SOURCE4} %{buildroot}%{_mandir}/man1/send_nsca.1
install -m644  %{SOURCE5} %{buildroot}%{_mandir}/man1/nsca.1

%preun
%stop_on_removal nsca

%postun
%restart_on_update nsca
%insserv_cleanup

%triggerpostun -- nagios-nrpe < 2.9.2
STATUS='/var/adm/update-scripts/%{name}'
if [ -x %{_sysconfdir}/init.d/nsca ]; then
        %{_sysconfdir}/init.d/nsca status >/dev/null
        if test $? = 0; then
                echo "%{_sysconfdir}/init.d/nsca restart" >> "$STATUS"
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

%triggerpostun -- nagios-nsca < 2.9.2
# Move /etc/nagios/nsca.conf to /etc/nsca.conf when updating from an old version
# and inform the admin about the move.
pushd %{_sysconfdir}
if test -e nagios/nsca.conf.rpmsave -a ! -e nsca.conf.rpmnew; then
    mv nsca/nsca.conf nsca.conf.rpmnew
    mv nagios/nsca.conf.rpmsave nsca.conf
    test -L %{nagios_sysconfdir}/nsca.conf || ln -s %{_sysconfdir}/nsca.conf %{nagios_sysconfdir}/nsca.conf
        %restart_on_update nsca
fi
sed -i "s|%{nagios_sysconfdir}/nsca.cfg|%{_sysconfdir}/nsca.cfg|g" %{_sysconfdir}/xinetd.d/nsca || :
if [ -e /var/adm/update-scripts/%{name} ]; then
    /bin/sh /var/adm/update-scripts/%{name}
    rm /var/adm/update-scripts/%{name}
fi

%triggerpostun -- nagios-nsca-client < 2.9.2
# Move /etc/nagios/send_nsca.cfg to /etc/send_nsca.cfg when updating from an old version
# and inform the admin about the move.
pushd %{_sysconfdir}
if test -e nagios/send_nsca.cfg.rpmsave -a ! -e send_nsca.cfg.rpmnew; then
        mv nsca/send_nsca.cfg send_nsca.cfg.rpmnew
        mv nagios/send_nsca.cfg send_nsca.cfg
    test -L %{nagios_sysconfdir}/send_nsca.cfg || ln -s %{_sysconfdir}/send_nsca.cfg %{nagios_sysconfdir}/send_nsca.cfg
fi

%clean
rm -rf %{buildroot};

%files
%defattr(-,root,root)
%{_bindir}/nsca
%{_sysconfdir}/init.d/nsca
%{_sbindir}/rcnsca
%config(noreplace) %{_sysconfdir}/nsca.cfg
%config(noreplace) %{_sysconfdir}/xinetd.d/nsca
%config(noreplace) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/%{name}
%{_mandir}/man1/nsca.1*
%doc Changelog README SECURITY LEGAL

%files client
%defattr(-,root,root)
%{_bindir}/send_nsca
%{_mandir}/man1/send_nsca.1*
%config(noreplace) %{_sysconfdir}/send_nsca.cfg

%changelog
* Thu Feb 14 2013 lars@linux-schulserver.de
- rename the package from nagios-nsca to nsca (following upstream
  name)
- require 'monitoring_daemon' in init script as nsca also runs
  together with icinga
- add man pages for send_nsca and nsca from Debian
* Thu Oct 11 2012 lars@linux-schulserver.de
- recommend 'monitoring_daemon' to allow nsca to run with
  compatible monitoring solutions
* Fri Feb  3 2012 lars@linux-schulserver.de
- update to 2.9.1:
  + Applied patch to allow packets arriving with a future time stamp
    (Daniel Wittenberg)
  + Updated server (nsca) to allow packets with older, smaller
    packet size (Eric Stanley)
- use macros from nagios-rpm-macros package
- added rpmlintrc
* Wed Dec 21 2011 coolo@suse.com
- remove call to suse_update_config (very old work around)
* Thu Nov 10 2011 schneemann@b1-systems.de
- update to version 2.9
  * Add config directive to submit directly to checkresults directory (Mike Lindsey)
  * Support multi-line check output with 4000 character limit (Mike Lindsey)
- fixes in skipped version 2.8
  * Added --with-log-facility option to control syslog logging (Ryan Ordway and Brian Seklecki)
  * Fixed bug where daemon would segfault if mcrypt library was not initialized before timeout (Holger Weiss)
  * Fixed bug with switching from dump file to command file when running under single mode (Ton Voon)
  * Fix for small memory leak with running as a single process daemon (Daniel)
* Fri Aug 31 2007 tsieden@suse.de
- cleanup spec file (removed unneeded %%dir entry)
* Mon Aug 13 2007 tsieden@suse.de
- update to version 2.7.2
  * fixed bug with NSCA daemon eating CPU if child process
  couldn't accept a connection in multi-process mode (Chris Wilson)
* Fri Feb  9 2007 tsieden@suse.de
- update to version 2.7.1
  * Fixed bug that prevented single mode daemon from working properly
  * Added sample scripts for testing functionality to nsca_tests/
    (Ton Voon/Altinity)
* Mon Jan 29 2007 tsieden@suse.de
- update to version 2.7
  * Fixed crash from malformed command line
    (therefore removed removed nagios-nsca.send_nsca.formatstring.patch)
  * Updated to config.sub and config.guess to latest from GNU Savannah
  * changed default user and group to nagios nagios (#236135)
* Thu Dec  7 2006 tsieden@suse.de
- package split: nagios-nsca for the server and
  nagios-nsca-client for the remote host
- removed unneeded BuildRequires (nagios)
* Fri Dec  1 2006 tsieden@suse.de
- update to version 2.6
  * spec file fix
  * segfault fix in encryption library cleanup
  * daemon now exits with an error if it can't drop privileges
  * added chroot support (Sean Finney)
  * added support for writing a PID file
  * added support for reloading config files with SIGHUP
  * removed obsolete patches which are included in upstream now
- fix NscaBin location in init script
* Tue Oct 10 2006 olh@suse.de
- fix send_nsca  segfault with -c and -d options
* Thu Feb  2 2006 stark@suse.de
- fixed crash while encrypt_cleanup()
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Sun Jan 22 2006 stark@suse.de
- update to version 2.5
- added init-script
- added xinetd configuration
- use -fstack-protector
- use tcp-wrapper
* Wed Oct 12 2005 stark@suse.de
- fixed uninitialized variable and missing return-codes
* Sun Jan 11 2004 adrian@suse.de
- add %%defattr
* Thu Jul 24 2003 stark@suse.de
- update to 2.4
  * Better support for u_int32_t detection
  * Minor bug fixes
* Thu Jun 19 2003 stark@suse.de
- added nagios to neededforbuild (fixing directory ownership)
* Wed Feb  5 2003 stark@suse.de
- update to 2.3
  * Minor changes to daemon init code
  * Minor Makefile fixes
* Wed Jan 29 2003 ro@suse.de
- fix compile for gcc-3.3 (wrong code ...)
* Mon Jan 13 2003 stark@suse.de
- update to 2.2
  * Syntax changes for command line arguments
  * Added support for passive host checks (supported
    only in Nagios 2.x and later)
  * Added sample xinetd config file (nsca.xinetd)
  * Minor mods and bug fixes
* Fri Aug 16 2002 kukuk@suse.de
- Remove libmcrypt-devel from requires, libmcrypt.la is now in
  main libmcrypt package.
* Wed Jun 12 2002 stark@suse.de
- update to 2.1
* Tue May 28 2002 stark@suse.de
- changed conf-dir to /etc/nagios
* Mon Apr 29 2002 stark@suse.de
- switch to Nagios NSCA (which is only another name)
  * update to version 2.0
* Thu Mar 21 2002 stark@suse.de
- finally updated to 1.2.0
* Thu Feb 14 2002 stark@suse.de
- modified patch to write to an alternative "command" file
  if the NetSaint command-file doesn't exist
  (backport from 1.2.0)
* Mon Feb  4 2002 stark@suse.de
- update to 1.2.0b8
- added a patch to NOT create the commandfile as regular file
  if it doesn't exist
* Mon Jul 16 2001 stark@suse.de
- added libmcrypt-devel to requires
* Mon Jul 16 2001 stark@suse.de
- update to 1.1.1 (configure-fixes for mcrypt)
* Tue Apr 24 2001 stark@suse.de
- initial package (linked against mcrypt)

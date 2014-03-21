#
# spec file for package ndoutils
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           ndoutils
Summary:        Nagios v3.x Data Output Utilities
License:        GPL-2.0+
Group:          System/Monitoring
Version:        2.0.0
Release:        30.1
Url:            http://www.nagios.org/
Source0:        %{name}-%{version}.tar.bz2

Source1:        %{name}-init
Source2:        ndoutils-README.SUSE
Source3:        ndoutils-rpmlintrc
# PATCH-MISSING-TAG -- See http://wiki.opensuse.org/openSUSE:Packaging_Patches_guidelines
Patch0:         ndoutils-2.0.0-libpq-fe-include.patch
Patch1:         ndoutils-2.0.0-return-non-void-queue.patch
Requires(pre):  %insserv_prereq
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  nagios-rpm-macros
%if 0%{?suse_version} > 1020
BuildRequires:  libmysqlclient-devel
%else
BuildRequires:  mysql-devel
%endif
BuildRequires:  nagios-devel >= 3.0
# postgresql is currently not supported but will likely be added in the future
BuildRequires:  postgresql-devel
BuildRequires:  tcpd
%if 0%{?suse_version} > 1030 || 0%{?fedora_version} > 8
BuildRequires:  fdupes
%endif
Requires:       nagios >= 3.0
%if 0%{?suse_version} < 1120
Requires:       mysql-shared
%endif

%description
NDOUtils is an Nagios addon allowing you to store Nagios data (current status
information, state history, notification history, etc.) in a MySQL database.

This addon consists of an event broker module and a daemon.

Consider this addon to be experimental for the moment, although it will likely
play a central role in the a new Nagios web interface in the future.


%package doc
Summary:        Main documentation for ndoutils
Group:          Documentation/Other
%if 0%{?suse_version} >= 1010
Recommends:     %{name} = %{version}
%else
Requires:       %{name} = %{version}
%endif

%description doc
This package includes the main documentation for ndoutils.


%prep
%setup -q
%patch0 -p1
%patch1
install -m644 %{SOURCE2} README.SUSE
## rpmlint
# wrong-file-end-of-line-encoding
pushd docs/docbook/en-en
%{__perl} -p -i -e 's|\r\n|\n|' Makefile.in ent/documents.ent ent/version.ent
popd

# fix permissions of documentation to prevent false duplicates issued by rpmlint (bnc#784670)
find docs -type f -exec chmod 0644 {} +

%build
%configure \
    --enable-mysql \
    --with-mysql-lib=%{_libdir}/mysql \
    --with-mysql-inc=%{_includedir}/mysql \
    --localstatedir=%{_localstatedir}/lib/ndo \
    --enable-pgsql \
    --with-pgsql-lib=%{_libdir} \
    --with-pgsql-inc=%{_includedir}/pgsql \
    --with-ndo2db-user=%{nagios_user} \
    --with-ndo2db-group=%{nagios_group}
# do not use jobs here, makefile dependencies are unsafe
make

%install
install -d %{buildroot}%{_sysconfdir}/init.d
install -d %{buildroot}%{nagios_sysconfdir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_prefix}/lib/nagios/brokers
install -d %{buildroot}%{_localstatedir}/lib/ndo

install -d %{_builddir}/%{name}-%{version}/examples

install -m0755 src/ndo2db-3x     %{buildroot}%{_sbindir}/ndo2db
install -m0755 src/file2sock     %{buildroot}%{_bindir}/file2sock
install -m0755 src/log2ndo       %{buildroot}%{_bindir}/log2ndo
install -m0755 src/sockdebug     %{buildroot}%{_bindir}/sockdebug
install -m0755 src/ndomod-3x.o   %{buildroot}%{_prefix}/lib/nagios/brokers/ndomod.o
install -m0755 %{SOURCE1}        %{buildroot}%{_sysconfdir}/init.d/ndo2db
ln -s %{_sysconfdir}/init.d/ndo2db %{buildroot}%{_sbindir}/rcndo2db

#
# fix path names in config
#
sed -e "s@^socket_name=.*@socket_name=%{nagios_spooldir}/ndo.sock@g" \
    -e "s@^debug_file=.*@debug_file=%{nagios_logdir}/ndo2db.debug@g" config/ndo2db.cfg-sample > %{buildroot}%{nagios_sysconfdir}/ndo2db.cfg

sed -e "s@^output=.*@output=%{nagios_spooldir}/ndo.sock@g" \
    -e "s@^buffer_file=.*@buffer_file=%{nagios_spooldir}/ndomod.tmp@g" config/ndomod.cfg-sample > %{buildroot}%{nagios_sysconfdir}/ndomod.cfg

cat > %{_builddir}/%{name}-%{version}/config/nagios.cfg << EOF
# SAMPLE NAGIOS CONFIG SNIPPET FOR NDOMOD
#
# In order to have Nagios run the NDOMOD event broker module, you'll need
# to place a statement like the one found below in your main Nagios
# configuration file (nagios.cfg).

# Uncomment the line below if you're running Nagios 3.x
#broker_module=%{_prefix}/lib/nagios/brokers/ndomod.o config_file=%{nagios_sysconfdir}/ndo2db.cfg
EOF

cat > %{_builddir}/%{name}-%{version}/config/misccommands.cfg << EOF
# SAMPLE NDO FILE ROTATION COMMAND
#
# This is an example Nagios command definition that can be used to
# rotate the NDO output file on a regular basis.  Adjust the paths, etc.
# to suit your needs.  This definition will need to be included in your
# Nagios config files if you want to use it.

define command {
        command_name    rotate_ndo_log
        command_line    /bin/mv %{nagios_spooldir}/ndo.dat %{nagios_spooldir}/ndo.\`date +%s\`
}
EOF
# install docu
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}/
cp -r db docs Changelog README* REQUIREMENTS TODO UPGRADING config/misccommands.cfg config/nagios.cfg %{buildroot}/%{_defaultdocdir}/%{name}/

# some rpmlint stuff
## files-duplicate
%if 0%{?suse_version} > 1030
%fdupes -s %{buildroot}
%endif
%if 0%{?fedora_version} > 8
fdupes -q -n -r %{buildroot}
%endif

%preun
%stop_on_removal ndo2db

%postun
%insserv_cleanup ndo2db
%restart_on_update

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%exclude %{_defaultdocdir}/%{name}/docs
%config(noreplace) %attr(664,%{nagios_user},%{nagios_command_group}) %{nagios_sysconfdir}/ndomod.cfg
%config(noreplace) %attr(660,%{nagios_user},%{nagios_command_group}) %{nagios_sysconfdir}/ndo2db.cfg
%attr(0755,%{nagios_user},%{nagios_group}) %dir %{_localstatedir}/lib/ndo
%{_sysconfdir}/init.d/ndo2db
%{_bindir}/file2sock
%{_bindir}/log2ndo
%{_bindir}/sockdebug
%{_sbindir}/ndo2db
%{_sbindir}/rcndo2db
%dir %{_prefix}/lib/nagios/brokers
%{_prefix}/lib/nagios/brokers/ndomod.o

# change defattr
%defattr(0644,root,root,0755)
%doc  %{_defaultdocdir}/%{name}

%files doc
%defattr(0644,root,root,0755)
%doc %{_defaultdocdir}/%{name}/docs

%changelog
* Sun Mar  2 2014 lars@linux-schulserver.de
- update to 2.0.0:
  + Updated database schema upgrade script to support multiple
    updates (Eric Stanley, Scott Wilkerson)
  + Added data serialization functions (Eric Stanley)
  + Added new Nagios Core 4 attributes: importance values,
    service parents (Eric Stanley)
  + Resolved tracker items #374 and #118 by adding auto-trimming
    options (Mike Guthrie)
  + Replaced ndomod.cfg data_processing_options variable with
    single options (Mike Guthrie)
  + Updated to work with Nagios Core 4 (Eric Stanley)
  + Replaced ndomod.cfg data_processing_options variable with single
    options for easier customization (See README) (Mike Guthrie)
  + Added missing maintenance options for table trimming (Mike Guthrie)
- refreshed patches
* Mon Aug 12 2013 lars@linux-schulserver.de
- Update to 1.5.2:
  + Added Linux kernel tuning instructions (Eric Stanley)
  + Added code to limit retries when system resources are too low
    (Eric Stanley)
  + Added code to retry sending messages queue is full (Mike Guthrie)
* Wed Oct 31 2012 mvyskocil@suse.com
- fix permissions of documentation to prevent false duplicates issued by
  rpmlint as fdupes is now permissions sensitive (bnc#784670)
* Tue May 22 2012 lars@linux-schulserver.de
- update to 1.5.1:
  + Fixed off-by-one error packing data in ndomod
* Mon Feb  6 2012 schneemann@b1-systems.de
- fixed no-return-in-nonvoid-function in get_queue_id queue.c:35
* Mon Feb  6 2012 schneemann@b1-systems.de
- update to 1.5
  * Added various performance improvements originally added for
  Nagios XI (Ethan Galstad)
  * Added asynchronous data spooling to increase performance (andree)
  * Fixed to small es array (Michael Friedrich)
  * Fixed wrong type of object_id in ndo2db_save_custom_variables()
  (Michael Friedrich)
* Sun Nov  6 2011 lars@linux-schulserver.de
- use macros defined in nagios-rpm-macros package
- added rpmlintrc for init file name
* Sat Nov  5 2011 chris@computersalat.de
- spec-cleaner
- fix build: directories not owned by a package:
  - /usr/lib/nagios/brokers
- rpmlint: wrong-file-end-of-line-encoding
  docs/docbook/en-en: Makefile.in ent/documents.ent ent/version.ent
* Tue May 18 2010 ro@suse.de
- disable -j for make, makefile deps are not safe
* Sun Dec 20 2009 chris@computersalat.de
- fix build for o:F
  * reworked patch ndoutils-1.4b7-libpq-fe-include.patch
    now with fuzz=0
* Sat Nov  7 2009 chris@computersalat.de
- fix expansion error
  o nothing provides mysql-shared needed by ndoutils
  * do not define explicit libdepency
  * removed Requires: mysql-shared for >= 1120
* Sat Nov  7 2009 chris@computersalat.de
- update to 1.4b9
  + Improved writes from file2sock to ndo2db by matching buffer
    sizes (Opsera Ltd)
  + Add in 4 missing tables from clearout process during
    prelaunch (Opsera Ltd)
  + Fix for Solaris 10 which gets an EINTR on accept for the 2nd
    file2sock call (Opsera Ltd)
  + Fix for not retrying read on 'EAGAIN' and 'EINTR' soft
    errors (Opsera Ltd)
  + Improve error info by showing failed MySQL query in
    syslog (Opsera Ltd)
  + Move database connections/disconnections syslog detail to DEBUG
    from INFO (Opsera Ltd)
  + Allow externalcommands table to be trimmed with a specific time
    limit (Opsera Ltd)
  + Support SSL encryption between the communication partners
  + Support for long performance data
  + Added installation procedure with "make install" or
    "make fullinstall"
  + Fix missing output fields in hostcheck and servicecheck tables
  + Workaround small NDOMOD Buffers to handle more than 4k chars
    (tracker id 21)
  + Fix unescape of strings containing tabstops
  + Fix case insensitive behavior in NDOUtils (tracker id 66)
- specmods
  + fix sed for {ndo2db,ndomod}.cfg
    o files were renamed in SOURCE to {ndo2db,ndomod}.cfg-sample
  + fix build for SLES_9
    o unknown tag Recommends
- rpmlint
  o files-duplicate in docdir
  o spurious-executable-perm in docdir
* Wed Jul 22 2009 lars@linux-schulserver.de
- update to 1.4b8:
  + Added additional error messages during failed startup
  + Better MySQL library detection (Ton Voon, Herbert Straub,
    and Nagios Plugin Team)
  + Compiler flag fix for building on GNU/kFreeBSD systems
    (Hendrik Frenzel)
  + Added lock_file option
  + Fix debug file permission race (Lars Michelsen)
  + More error reporting if debug file can not be opened
  + Fix wait for childs on SIGCHLD
  + Added long_output support
  + Fix missing SIGTERM forwarding to childs
  + Fix fmt specifier in ndo2db_daemonize()
  + Escape custom values in 'customvariablestatus'
    and 'customvariables'
  + Fix ndomod doesn't execute rotate_command propperly
  + Fix several compiler warnings
  + Rewrite ndo2db init script, install it with 'make install-init'
* Sun May 24 2009 chris@computersalat.de
- some spec mods
  o added cmdusr, cmdgrp
  o changed perm, ownership for "centreon" of:
    660,nsusr,cmdgrp ndo2db.cfg
    664,nsusr,cmdgrp ndomod.cfg
* Mon May 18 2009 chris@computersalat.de
- fixed init script
  o su - [user] -c'...' obsolete
- beautify spec
* Fri Apr 24 2009 lars@linux-schulserver.de
- add %%postun and %%preun scripts
- split up doc package
* Sat Jul 26 2008 lars@linux-schulserver.de
- just require mysql-shared, so the database can be on a different
  host (thanks to Ciro Iriarte)
* Sun Jul 20 2008 lars@linux-schulserver.de
- added init patch from Ciro Iriarte
* Sat Jan 12 2008 lars@linux-schulserver.de
- added some tips from Tom Throckmorton in README.SuSE
* Tue Nov 27 2007 lars@linux-schulserver.de
- use new libexecdir
* Mon Nov 19 2007 lars@linux-schulserver.de
- initial version 1.4b7

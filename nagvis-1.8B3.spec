nagios1:/proj/OpenSuSE-Nagios-4.x # cat nagvis-1.8B3.spec
#
# spec file for package nagvis
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



Name:           nagvis
Version:        1.8b3
Release:        1
License:        GPL-2.0
Summary:        Visualization addon for Nagios
Url:            http://www.nagvis.org/
Group:          Productivity/Networking/Web/Utilities
Source:         %name-%version.tar.gz
Source1:        nagvis-rpmlintrc
Source2:        nagvis-include.conf
Source3:        nagvis-update-script.sh
Source4:        nagvis-update-script.1
Source5:        nagvis-README.SuSE
Source6:        nagvis-make-admin.1
Patch1:         nagvis-make-admin.patch
Patch2:         nagvis-config.patch
BuildRequires:  apache2-devel
BuildRequires:  nagios-rpm-macros
PreReq:         %insserv_prereq
BuildArch:      noarch
%if 0%{?suse_version} > 1020
BuildRequires:  fdupes
%endif
# gd mbstring gettext session xml pdo
Requires:       graphviz
Requires:       php5-gd
Requires:       php5-gettext
Requires:       php5-mbstring
Requires:       php5-pdo
Requires:       php5-pear
Requires:       php5-ZendFramework
Requires:       php5-sockets
Requires:       php5-json
Requires:       php5-sqlite
Requires:       graphviz-gd
Recommends:     monitoring_webfrontend
Requires:       mk-livestatus > 1.2.4
Recommends:     php5-mysql
Recommends:     php5-session
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define         wwwusr wwwrun
%define         wwwgrp www
%define         apache2_sysconfdir %(/usr/sbin/apxs2 -q SYSCONFDIR)/conf.d
%define         installdir %{_datadir}/%{name}

%description
NagVis can be used to visualize Nagios Data, e.g. to display IT
processes like a mail system or a network infrastructure.

Key features are:
    * Display of single Hosts and Services
    * Visualize a complete Host- oder Servicegroup with one icon
    * Display the state of a Host dependent on the state of
      its services (.recognize services.)
    * Display only the real problems (.only_hard_states.)
    * Define Sub-Map icons wich represent a complete NagVis
      Map of Hosts/Services/Groups in one icon (drill down)
    * Visualization/Documentation of complete IT Processes
      and Infrastructures using self drawn graphics

%package demos
Summary:        Some demo maps for NagVis
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Utilities

%description demos
This package contains demo maps for NagVis.

%prep
%setup -q
find -name ".gitignore" | xargs rm
sed -i "s|\r||g" LICENCE
chmod -x share/server/core/ext/php-gettext*/*.php
install -m644 %{SOURCE5} README.SuSE
%patch1 -p1
%patch2 -p1

%build

%install
mkdir -p %{buildroot}%{installdir}
cp -r share %{buildroot}%{installdir}
cp -r docs %{buildroot}%{installdir}/share/

# configurations belong to /etc (FHS)
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/{automaps,profiles}
cp -r etc/maps %{buildroot}%{_sysconfdir}/%{name}
cp -r etc/geomap %{buildroot}%{_sysconfdir}/%{name}
cp -r etc/conf.d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/nagvis.ini.php-sample \
    %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php
pushd %{buildroot}%{installdir}
rm -rf etc
ln -s ../../..%{_sysconfdir}/%{name} etc
pushd share
mv userfiles %{buildroot}%{_sysconfdir}/%{name}/
ln -s ../../../../%{_sysconfdir}/%{name}/userfiles .
popd
popd

# install directories needed during runtime
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_var}/cache/%{name}
install -d -m 755 %{buildroot}%{_var}/cache/%{name}/tmpl
install -d -m 755 %{buildroot}%{_var}/cache/%{name}/tmpl/cache
install -d -m 755 %{buildroot}%{_var}/cache/%{name}/tmpl/compile
pushd %{buildroot}%{installdir}/
rm -rf var
ln -s ../../../%{_var}/cache/%{name} var
ln -s ../../../../%{_var}/cache/%{name} %{buildroot}%{installdir}/share/var
popd

# fix nagvis config
sed "s|;base=.*|base=\"%{installdir}/\"|; \
     s|;htmlbase=.*|htmlbase=\"/%{name}/\"|; \
         s|var=.*|var=\"%{_var}/cache/nagvis/\"|; \
         s|mapcfg=.*|mapcfg=\"%{_sysconfdir}/%{name}/maps/\"|; \
     s|;socket=\"unix:/usr/local/nagios/var/rw/live\"|socket=\"unix:%{livestatus_socket_file}\"|; \
         s|cfg=.*|cfg=\"%{_sysconfdir}/%{name}/\"|;" \
        %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php > %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php.new
mv %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php.new %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php

# install apache config
install -Dm644 %{SOURCE2} %{buildroot}%{apache2_sysconfdir}/%{name}.conf

# install nagvis-make-admin
sed -e "s@__SYSCONFDIR__@%{_sysconfdir}/%{name}@g" nagvis-make-admin > %{buildroot}%{_bindir}/nagvis-make-admin
chmod +x %{buildroot}%{_bindir}/nagvis-make-admin
install -Dm644 %{SOURCE6} %{buildroot}/%{_mandir}/man1/nagvis-make-admin.1

# install nagvis-update-script.sh
install -Dm755 %{SOURCE3} %{buildroot}%{_bindir}/nagvis-update-script
install -m644  %{SOURCE4} %{buildroot}/%{_mandir}/man1/nagvis-update-script.1

%if 0%{?suse_version} > 1020
# save some space - relink
%fdupes %{buildroot}/%{installdir}
%endif
find %{buildroot}%{installdir} -name "*.orig" -delete

%clean
rm -rf %{buildroot}

%pre
if [ -d %{installdir}/share/userfiles ]; then
        if [ -d %{_sysconfdir}/%{name}/userfiles ]; then
                mv %{installdir}/share/userfiles %{_sysconfdir}/%{name}/userfiles.rpmnew
                echo "Moved %{installdir}/share/userfiles to %{_sysconfdir}/%{name}/userfiles.rpmnew - please compare with %{_sysconfdir}/%{name}/userfiles and remove the .rpmnew directory"
        else
                mv %{installdir}/share/userfiles %{_sysconfdir}/%{name}/
                echo "Moved %{installdir}/share/userfiles to %{_sysconfdir}/%{name}/"
        fi
fi

%post
if [ ${1:-0} -lt 1 ]; then
        if [ -x %{_sbindir}/a2enmod ]; then
                %{_sbindir}/a2enmod php5 >/dev/null
        fi
        if [ -x %{_sbindir}/a2enflag ]; then
                %{_sbindir}/a2enflag NAGVIS
        fi
else
    %{_bindir}/nagvis-update-script -u %wwwusr -g %wwwgrp -f %{_sysconfdir}/%{name}/nagvis.ini.php -p %{_sysconfdir}/%{name} -l %{_sysconfdir}/%{name}/nagvis-update.log
fi
%restart_on_update apache2

%preun
%restart_on_update apache2

%files
%defattr(-,root,root)
%doc ChangeLog LICENCE README README.SuSE
%config(noreplace) %{apache2_sysconfdir}/%{name}.conf
%{_bindir}/*
%{installdir}/
%{_mandir}/man1/nagvis*.1*
%defattr(664,%wwwusr,%wwwgrp,775)
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/maps
%dir %{_sysconfdir}/%{name}/automaps
%dir %{_sysconfdir}/%{name}/geomap
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_sysconfdir}/%{name}/userfiles
%dir %{_sysconfdir}/%{name}/profiles
%dir %{_var}/cache/%{name}
%dir %{_var}/cache/%{name}/tmpl
%dir %{_var}/cache/%{name}/tmpl/cache
%dir %{_var}/cache/%{name}/tmpl/compile
%config(noreplace) %{_sysconfdir}/%{name}/nagvis.ini.php
%config(noreplace) %{_sysconfdir}/%{name}/maps/*.cfg
%config(noreplace) %{_sysconfdir}/%{name}/geomap/*.xml
%config(noreplace) %{_sysconfdir}/%{name}/conf.d/*.php
%config(noreplace) %{_sysconfdir}/%{name}/userfiles/*
%exclude %{_sysconfdir}/%{name}/maps/demo*
%exclude %{_sysconfdir}/%{name}/conf.d/demo.ini.php
%exclude %{_sysconfdir}/%{name}/geomap/demo-locations.csv
%exclude %{_sysconfdir}/%{name}/userfiles/images/shapes/demo*
%exclude %{_sysconfdir}/%{name}/userfiles/images/maps/demo*

%files demos
%defattr(-,root,root)
%config %{_sysconfdir}/%{name}/geomap/demo-locations.csv
%config %{_sysconfdir}/%{name}/maps/demo*
%config %{_sysconfdir}/%{name}/conf.d/demo.ini.php
%config(noreplace) %{_sysconfdir}/%{name}/geomap/demo-locations.csv
%config(noreplace) %{_sysconfdir}/%{name}/userfiles/images/shapes/demo*
%config(noreplace) %{_sysconfdir}/%{name}/userfiles/images/maps/demo*

%changelog




Name:           kohana2
%define         realname Kohana
Summary:        PHP 5 framework that uses the Model View Controller architectural pattern
Version:        2.3.4
Release:        5.1
Url:            http://kohanaphp.com
License:        BSD like, Free Redistribution by Kohana Team
Group:          Productivity/Networking/Web/Utilities
AutoReqProv:    off
Source0:        %{realname}_v%{version}.tar.bz2
Source1:        kohana2-apache_include
Requires(pre):  http_daemon
Requires:       mod_php_any
Requires:       php5-ZendFramework
Recommends:     php5-mcrypt
Provides:       kohana = %{version}
Obsoletes:      kohana <= %{version}
BuildRequires:  apache2-devel
%if 0%{?suse_version} >= 1020
BuildRequires:  fdupes
%endif
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define         apache_serverroot %(/usr/sbin/apxs2 -q DATADIR)
%define         apache_sysconfdir %(/usr/sbin/apxs2 -q SYSCONFDIR)
%define         installpath %{apache_serverroot}/%{name}


%description
Kohana is a PHP 5 framework that uses the Model View Controller architectural
pattern. It aims to be secure, lightweight, and easy to use.


Features

    * Highly secure
    * Extremely lightweight
    * Short learning curve
    * Uses the MVC pattern
    * 100% UTF-8 compatible
    * Loosely coupled architecture
    * Extremely easy to extend


Authors:
--------
    The Kohana Team


%prep
%setup -q -n %{realname}_v%{version}

%build

%install
mkdir -p %{buildroot}/%{installpath}
cp -r * %{buildroot}/%{installpath}/
find %{buildroot}/%{installpath}/ -type d -exec chmod 755 {} \;
find %{buildroot}/%{installpath}/ -type f -exec chmod 644 {} \;
for dir in application/logs application/cache; do
        chmod 775 %{buildroot}/%{installpath}/$dir
done
# install apache config
mkdir -p %{buildroot}/%{apache_sysconfdir}/conf.d/
install -m640 %{SOURCE1} %{buildroot}/%{apache_sysconfdir}/conf.d/%{name}_include.conf
# move system and modules folder out of webroot
mkdir -p %{buildroot}/%{_datadir}/%{name}/
mv %{buildroot}/%{installpath}/{system,modules} %{buildroot}/%{_datadir}/%{name}/
# remove example file
rm %{buildroot}/%{installpath}/example.htaccess
# move the global config files to /etc
for dir in system ; do
        mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/$dir
        mv %{buildroot}/%{_datadir}/%{name}/$dir/config %{buildroot}/%{_sysconfdir}/%{name}/$dir/
        pushd %{buildroot}/%{_datadir}/%{name}/$dir
        ln -s %{_sysconfdir}/%{name}/$dir/config .
        popd
done
# same for the initial application config directory
mkdir %{buildroot}/%{_sysconfdir}/%{name}/application
mv %{buildroot}/%{installpath}/application/config %{buildroot}/%{_sysconfdir}/%{name}/application/
pushd %{buildroot}/%{installpath}/application/
ln -s %{_sysconfdir}/%{name}/application/config .
popd
%if 0%{?suse_version} >= 1020
%fdupes %{buildroot}
%endif

%clean
rm -rf %buildroot

%postun
if [ "$1" = "0" ]; then
    # deinstallation of the package - remove the apache flag
    test -x %{_sbindir}/a2disflag && %{_sbindir}/a2disflag KOHANA2 >/dev/null
    %restart_on_update apache2
fi

%pre
if [ "$1" = "1" ]; then
    # enable php5 in apache config
    test -x %{_sbindir}/a2enmod && %{_sbindir}/a2enmod php5 >/dev/null
    # enable KOHANA in /etc/sysconfig/apache2
    test -x %{_sbindir}/a2enflag && %{_sbindir}/a2enflag KOHANA2 >/dev/null
fi

%post
%restart_on_update apache2

%files
%defattr(-,root,root)
%if 0%{?suse_version} <= 1230
%doc Kohana\ License.html
%else
%doc "Kohana License.html"
%endif
%dir %{installpath}
%{installpath}/
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/application
%dir %{_sysconfdir}/%{name}/application/config
%dir %{_sysconfdir}/%{name}/system
%dir %{_sysconfdir}/%{name}/system/config
%config(noreplace) %{_sysconfdir}/%{name}/*/config/*
%config(noreplace) %{apache_sysconfdir}/conf.d/%{name}_include.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/
%attr(-,wwwrun,www) %{installpath}/application/cache
%attr(-,wwwrun,www) %{installpath}/application/logs

%changelog
* Thu Sep 26 2013 obs@botter.cc
- fix files section for handling filename containing space
  for openSUSE >= 12.3
* Fri Aug 30 2013 obs@botter.cc
- fix typo in  Requires(pre) to build on openSUSE >= 12.2
* Sat Sep 24 2011 lars@linux-schulserver.de
- rename the package to kohana2 to allow an additional kohana3
  package coexisting with this one
- adapted config and other (directory) places to the new name
* Sun Feb 20 2011 lars@linux-schulserver.de
- currently stay at 2.3.4 as 3.x needs more love for packaging
* Mon Feb 14 2011 lars@linux-schulserver.de
- require php5-ZendFramework
- use IfDefine to enable kohana via APACHE_SERVER_FLAGS
* Tue Dec 15 2009 lars@linux-schulserver.de
- initial package 2.3.4

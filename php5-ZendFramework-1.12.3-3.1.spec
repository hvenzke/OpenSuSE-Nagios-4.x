#
# spec file for package php5-ZendFramework
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


%define pkg_name ZendFramework

Version:        1.12.3
Release:        3.1
Name:           php5-ZendFramework
Provides:       php-ZendFramework = %{version}

Summary:        Leading open-source PHP framework
License:        BSD-3-Clause
Group:          Development/Libraries/Other
Source0:        %{pkg_name}-%{version}.tar.gz
Source100:      %{pkg_name}-%{version}-apidoc.tar.gz
Source101:      %{pkg_name}-%{version}-manual-de.tar.gz
Source102:      %{pkg_name}-%{version}-manual-en.tar.gz
Source103:      %{pkg_name}-%{version}-manual-fr.tar.gz
Source104:      %{pkg_name}-%{version}-manual-ja.tar.gz
Source105:      %{pkg_name}-%{version}-manual-ru.tar.gz
Source106:      %{pkg_name}-%{version}-manual-zh.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Patch0:         zf.sh.patch
Url:            http://framework.zend.com/
BuildArch:      noarch

# Satisfy common hard requirements
%if 0%{?suse_version} > 1130
BuildRequires:  php5 >= 5.3
%endif
Requires:       pcre
Requires:       php >= 5.2.4
Requires:       php-ctype
Requires:       php-curl
Requires:       php-dom
Requires:       php-hash
Requires:       php-iconv
Requires:       php-pdo

%if 0%{?suse_version}
Requires:       php-mbstring
# Suggested modules for improved performance/functionality
Suggests:       php-bcmath php-bitset php-json php-posix

# Documentation & dojo requirements
%if 0%{?sles_version} != 10
BuildRequires:  fdupes
%endif
%endif

%if 0%{?suse_version}
%define _phpdir %{_datadir}/php5
%else
%define _phpdir %{_datadir}/php
%endif

%description
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.


%package demos
Summary:        Demos for the Zend Framework
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description demos
This package includes Zend Framework demos for the Feeds, Gdata, Mail, OpenId,
Pdf, Search-Lucene and Services subpackages.


%package tests
Summary:        Unit tests for the Zend Framework
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       php5-pear-phpunit

%description tests
This package includes Zend Framework unit tests for all available subpackages.


%package extras
Summary:        Zend Framework Extras (ZendX)
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-ZendX = %{version}-%{release}

%description extras
This package includes the ZendX libraries.


%package cache-backend-apc
Summary:        Zend Framework APC cache backend
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       php5-APC

%description cache-backend-apc
This package contains the backend for Zend_Cache to store and retrieve data via
APC.


%package cache-backend-memcached
Summary:        Zend Framework memcache cache backend
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       php5-pecl-memcache

%description cache-backend-memcached
This package contains the back end for Zend_Cache to store and retrieve data
via memcache.


%package cache-backend-sqlite
Summary:        Zend Framework sqlite back end
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       php5-sqlite

%description cache-backend-sqlite
This package contains the back end for Zend_Cache to store and retrieve data
via sqlite databases.


%package captcha
Summary:        Zend Framework CAPTCHA component
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       php5-gd

%description captcha
This package contains the Zend Framework CAPTCHA extension.


%package dojo
Summary:        Dojo javascript toolkit
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       unzip

%description dojo
This package contains a full copy of the Dojo Javascript toolkit from
Zend Framework externals. You may wish to install this as a reference or
to build custom Dojo layers for deployment with your site.


# %%package Db-Adapter-Db2
# Summary:  Zend Framework database adapter for DB2
# Group:    Development/Libraries/Other
# Requires: %%{name} = %%{version}-%%{release}
# Requires: php-ibm_db2 # Not available on openSUSE

# %%description Db-Adapter-Db2
# This package contains the files for Zend Framework necessary to connect to an
# IBM DB2 database.


%package Db-Adapter-Firebird
Summary:        Zend Framework database adapter for InterBase/Firebird
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-extras = %{version}-%{release}
Requires:       php5-firebird

%description Db-Adapter-Firebird
This package contains the files for Zend Framework necessary to connect to a
Firebird/InterBase database.


# %%package Db-Adapter-Oracle
# Summary:  Zend Framework database adapter for Oracle
# Group:    Development/Libraries/Other
# Requires: %%{name} = %%{version}-%%{release}
# Requires: php-oci8 # Not available on openSUSE

# %%description Db-Adapter-Oracle
# This package contains the files for Zend Framework necessary to connect to an
# Oracle database.


%package pdf
Summary:        PDF document creation and manipulation
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}
Requires:       php5-gd

%description pdf
Portable Document Format (PDF) from Adobe is the de facto standard for
cross-platform rich documents. Now, PHP applications can create or read PDF
documents on the fly, without the need to call utilities from the shell, depend
on PHP extensions, or pay licensing fees. Zend_Pdf can even modify existing PDF
documents.

* supports Adobe PDF file format
* parses PDF structure and provides access to elements
* creates or modifies PDF documents
* utilizes memory efficiently


%package manual-de
Summary:        Zend Framework German programmers reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description manual-de
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

Programmer's reference guide - German


%package manual-en
Summary:        Zend Framework English programmers reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description manual-en
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

Programmer's reference guide - English


%package manual-fr
Summary:        Zend Framework French programmers reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description manual-fr
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

Programmer's reference guide - French


%package manual-ja
Summary:        Zend Framework Japanese programmers reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description manual-ja
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

Programmer's reference guide - Japanese


%package manual-ru
Summary:        Zend Framework Russian programmers reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description manual-ru
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

Programmer's reference guide - Russian


%package manual-zh
Summary:        Zend Framework simplified Chinese programmers reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description manual-zh
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

Programmer's reference guide - simplified Chinese


%package apidoc
Summary:        Zend Framework API reference guide
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description apidoc
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.

API reference guide


%prep
%setup -qn %{pkg_name}-%{version}
tar zfx %{SOURCE100}
tar zfx %{SOURCE101}
tar zfx %{SOURCE102}
tar zfx %{SOURCE103}
tar zfx %{SOURCE104}
tar zfx %{SOURCE105}
tar zfx %{SOURCE106}
mv %{pkg_name}-%{version}/* ./ && rm -r %{pkg_name}-%{version}
%patch0 -p1

%if 0%{?sles_version} || 0%{?suse_version} == 1120
mv tests/Zend/Tool/Project/_files/.zfproject.xml.orig \
  tests/Zend/Tool/Project/_files/.zfproject.xml
sed -i 's/zfproject.xml.orig/zfproject.xml/g' \
  tests/Zend/Tool/Project/ProfileTest.php
%endif

# Add shebang
sed -i -e '1i#!/usr/bin/sh' externals/dojo/util/doh/robot/compilerobot.sh
sed -i -e '1i#!/usr/bin/sh' tests/runtests.sh
sed -i -e '1i#!/usr/bin/php' bin/zf.php

%build
find . -type f -perm /111 \
  -fprint executables -exec %{__chmod} -x '{}' \; >/dev/null
find . -type f -name \*.sh \
  -fprint valid_executables -exec %{__chmod} +x '{}' \; >/dev/null

%{__cat} executables valid_executables|sort|uniq -u > invalid_executables

%{__chmod} +x externals/dojo/util/migration/dijitCss14to15.sed
%{__chmod} +x externals/dojo/util/buildscripts/zoneinfo/strip_olson_comments.rb
%{__chmod} +x bin/zf.php

%install
# Zend Core
%{__mkdir_p} %{buildroot}/%{_phpdir}
%{__cp} -pr library/Zend %{buildroot}/%{_phpdir}
%{__cp} -pr demos/Zend %{buildroot}/%{_phpdir}/Zend/demos
%{__cp} -pr tests %{buildroot}/%{_phpdir}/Zend
%{__cp} -pr externals %{buildroot}/%{_phpdir}/Zend

# ZendX
%{__cp} -pr extras/library/ZendX %{buildroot}/%{_phpdir}
%{__cp} -pr extras/tests %{buildroot}/%{_phpdir}/ZendX

# Manual
for lang in {de,en,fr,ja,ru,zh}; do
  %{__mkdir_p} %{buildroot}/%{_datadir}/doc/ZendFramework/${lang}
  %{__cp} -pr documentation/manual/core/${lang}/* %{buildroot}/%{_datadir}/doc/ZendFramework/${lang}
done

# API manual
%{__mkdir_p} %{buildroot}/%{_datadir}/doc/ZendFramework/api
%{__cp} -pr documentation/api/core/* %{buildroot}/%{_datadir}/doc/ZendFramework/api

# Zend_Tool
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -pr bin/zf.{php,sh} %{buildroot}%{_bindir}
%{__ln_s} -f /usr/bin/zf.sh %{buildroot}%{_bindir}/zf

# create softlinks
%if 0%{?suse_version} && 0%{?sles_version} != 10
%fdupes -s %{buildroot}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_phpdir}/
%{_phpdir}/Zend
%exclude %{_phpdir}/Zend/demos
%exclude %{_phpdir}/Zend/externals
%exclude %{_phpdir}/Zend/tests
%exclude %{_phpdir}/Zend/Cache/Backend/Apc.php
%exclude %{_phpdir}/Zend/Cache/Backend/Memcached.php
%exclude %{_phpdir}/Zend/Captcha
%exclude %{_phpdir}/Zend/Pdf.php
%exclude %{_phpdir}/Zend/Pdf
%{_bindir}/zf.sh
%{_bindir}/zf.php
%{_bindir}/zf
%doc LICENSE.txt INSTALL.txt README.txt

%files demos
%defattr(-,root,root,-)
%{_phpdir}/Zend/demos
%doc LICENSE.txt

%files tests
%defattr(-,root,root,-)
%{_phpdir}/Zend/tests
%doc LICENSE.txt

%files extras
%defattr(-,root,root,-)
%{_phpdir}/ZendX
%exclude %{_phpdir}/ZendX/Db/Adapter/Firebird*
%exclude %{_phpdir}/ZendX/Db/Statement/Firebird*
%doc LICENSE.txt extras/documentation/manual/extras/en/*

%files cache-backend-apc
%defattr(-,root,root,-)
%{_phpdir}/Zend/Cache/Backend/Apc.php
%doc LICENSE.txt

%files cache-backend-memcached
%defattr(-,root,root,-)
%{_phpdir}/Zend/Cache/Backend/Memcached.php
%doc LICENSE.txt

%files captcha
%defattr(-,root,root,-)
%{_phpdir}/Zend/Captcha
%doc LICENSE.txt

%files dojo
%defattr(-,root,root,-)
%dir %{_phpdir}/Zend/externals/
%{_phpdir}/Zend/externals/dojo
%doc LICENSE.txt

%files Db-Adapter-Firebird
%defattr(-,root,root,-)
%{_phpdir}/ZendX/Db/Adapter/Firebird/
%{_phpdir}/ZendX/Db/Adapter/Firebird.php
%{_phpdir}/ZendX/Db/Statement/Firebird/
%{_phpdir}/ZendX/Db/Statement/Firebird.php
%doc LICENSE.txt

%files pdf
%defattr(-,root,root,-)
%{_phpdir}/Zend/Pdf.php
%{_phpdir}/Zend/Pdf
%doc LICENSE.txt

%files manual-de
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/de/
%{_datadir}/doc/ZendFramework/de/*
%doc LICENSE.txt

%files manual-en
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/en/
%{_datadir}/doc/ZendFramework/en/*
%doc LICENSE.txt

%files manual-fr
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/fr/
%{_datadir}/doc/ZendFramework/fr/*
%doc LICENSE.txt

%files manual-ja
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/ja/
%{_datadir}/doc/ZendFramework/ja/*
%doc LICENSE.txt

%files manual-ru
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/ru/
%{_datadir}/doc/ZendFramework/ru/*
%doc LICENSE.txt

%files manual-zh
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/zh/
%{_datadir}/doc/ZendFramework/zh/*
%doc LICENSE.txt

%files apidoc
%defattr(-,root,root,-)
%dir %{_datadir}/doc/ZendFramework/
%dir %{_datadir}/doc/ZendFramework/api/
%{_datadir}/doc/ZendFramework/api/*
%doc LICENSE.txt

%changelog
* Fri Nov  8 2013 aj@ajaissle.de
- New upstream release 1.12.3
  * http://framework.zend.com/changelog/1.12.3/
  * http://framework.zend.com/changelog/1.12.2/
- Removed build-tools.tar.bz2 and autoconf_manual.tar.gz (not needed)
- Removed rpmlintrc from spec (no need to mention it in spec)
- Enabled Db-Adapter-Firebird package
- Removed (Build)Requires for php5-sqlite and php5-xmlreader
* Tue Jan 29 2013 aj@ajaissle.de
- New upstream release 1.12.1
  * http://framework.zend.com/changelog/1.12.1/
- Added russian manual package
- Added API documentation package
* Tue Sep  6 2011 graham@andtech.eu
- 1.11.10 point Release
- http://framework.zend.com/changelog/1.11.10
- On suse_version > 11.30 (php 5.3 required), Build manual using
  PHD instead of xsltproc, reduces build time by an order of
  magnitude.
* Mon May 30 2011 graham@andtech.eu
- 1.11.6 point Release
- http://framework.zend.com/changelog/1.11.6
* Fri Jan 28 2011 graham@andtech.eu
- 1.11.2 point Release
- http://framework.zend.com/changelog/1.11.2
* Tue Nov  2 2010 graham@andtech.eu
- 1.11.0 Point Release
- http://framework.zend.com/changelog/1.11.0
- Zend_Http_UserAgent performs two responsibilities:
    User-Agent detection
    Device capabilities detection, based on User-Agent
- Zend_Cloud
- Zend_Service_Ebay
- Zend_Config_Yaml
- Zend_Config_Json
- Zend_Service_ShortUrl
- Additional view helpers
* Tue Oct  5 2010 graham@andtech.eu
- Bugfix release (1.10.8)
- http://framework.zend.com/changelog/1.10.8
* Wed Jun 23 2010 graham@andtech.eu
- Bugfix release (1.10.6)
- http://framework.zend.com/changelog/1.10.6
* Wed Jun  2 2010 graham@andtech.eu
- Bugfix release (1.10.5)
- http://framework.zend.com/changelog/1.10.5
* Mon May 17 2010 graham@andtech.eu
- Bugfix release (1.10.4)
- http://framework.zend.com/changelog/1.10.4
* Fri Apr  2 2010 graham@andtech.eu
- Revert document build to xsltproc (Phd has PHP5.3 requirement)
- Bugfix release (1.10.3)
- http://framework.zend.com/changelog/1.10.3
* Sat Feb 27 2010 graham@andtech.eu
- Change document build process, switch from xsltproc to Phd
- Bugfix release (1.10.2)
- http://framework.zend.com/changelog/1.10.2
* Tue Feb 16 2010 graham@andtech.eu
- Bugfix release (1.10.1)
- http://framework.zend.com/changelog/1.10.1
* Fri Jan 29 2010 graham@andtech.eu
- Update to 1.10.0, minor update, new features:
- Zend_Barcode, Zend_Cache_Backend_Static
- Zend_Cache_Backend_Static, Zend_Cache_Manager
- Zend_Exception, Zend_Feed_Pubsubhubbub, Zend_Feed_Writer
- Zend_Filter_Boolean,Zend_Filter_Compress/Decompress
- Zend_Filter_Null, Zend_Log::factory(), Zend_Log_Writer_ZendMonitor
- Zend_Markup, Zend_Oauth, Zend_Serializer
- Zend_Service_DeveloperGarden, Zend_Service_LiveDocx
- Zend_Service_WindowsAzure, Zend_Validate_Barcode
- Zend_Validate_Callback, Zend_Validate_CreditCard,
- Zend_Validate_PostCode
- Many bugfixes: http://framework.zend.com/changelog/1.10.0

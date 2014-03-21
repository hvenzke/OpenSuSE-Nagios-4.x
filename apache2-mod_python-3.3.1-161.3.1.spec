#
# spec file for package apache2-mod_python
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%if 0%{?sles_version} == 9
%define __python /usr/bin/python2.5
%define py_ver    %(%__python -c "import sys; v=sys.version_info[:2]; print '%%d.%%d'%%v" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_prefix %(%__python -c "import sys; print sys.prefix" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_libdir %{py_prefix}/%{_lib}/python%{py_ver}
%define py_incdir %{py_prefix}/include/python%{py_ver}
%endif

Name:           apache2-mod_python
BuildRequires:  apache2-devel
BuildRequires:  pcre-devel
%if 0%{?sles_version} == 9
BuildRequires:  python25
BuildRequires:  python25-devel
PreReq:         python25
%else
BuildRequires:  python-devel
%{py_requires}
%endif
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
%define modname mod_python
%define apxs /usr/sbin/apxs2
%define apache apache2
%define apache_libexecdir %(%{apxs} -q LIBEXECDIR)
%define apache_sysconfdir %(%{apxs} -q SYSCONFDIR)
%define apache_includedir %(%{apxs} -q INCLUDEDIR)
%define apache_serverroot %(%{apxs} -q PREFIX)
%define apache_localstatedir %(%{apxs} -q LOCALSTATEDIR)
%define apache_mmn        %(MMN=$(%{apxs} -q LIBEXECDIR)_MMN; test -x $MMN && $MMN)
Version:        3.5.0
Release:        17.3
Summary:        A Python Module for the Apache 2 Web Server
License:        Apache-2.0
Group:          Productivity/Networking/Web/Servers
Requires:       apache2 %{apache_mmn}
Conflicts:      mod_python
Url:            http://www.modpython.org/
Source:         %{modname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
mod_python allows embedding Python within the Apache HTTP server for a
considerable boost in performance and added flexibility in designing
Web-based applications.

Apache processes requests in stages (for example: read the request,
parse headers, check access, and so on). These stages can be
implemented by functions called handlers. Traditionally, handlers are
written in C and compiled into Apache modules. mod_python provides a
way to extend Apache functionality by writing Apache handlers in
Python. For a detailed description of the Apache request processing
process, see the Apache API notes.

For most programmers, the request and the authentication handlers
provide everything required. To ease migration from CGI and Httpdapy,
two handlers are provided that simulate these environments, allowing a
user to run scripts under mod_python with (for the most part) no
changes to the code.

mod_python originated from a project called Httpdapy. For a long time,
Httpdapy was not called mod_python because Httpdapy was not meant to be
Apache-specific. Httpdapy was designed to be cross-platform and was
initially written for the Netscape server.

Usage Hints:

To load mod_python into Apache, add it to APACHE_MODULES in
/etc/sysconfig/apache2. The configuration is described in
/usr/share/doc/packages/apache2-mod_python/doc-html/index.html.

%prep
%setup -n %{modname}-%{version}
case %_lib in
        lib) ;;
        *) mv lib %_lib;;
esac
%__sed -i 's@lib/python@%{_lib}/python@' configure.in
%__sed -i "
s@setup.py install@setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT@
;
s@/lib@/%{_lib}@
" dist/Makefile.in

sed -i "
s@setup.py install@setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT@
;
s@'lib'@'%{_lib}'@
" dist/setup.py.in
%__sed -i 's@GIT.*$@GIT=none@' dist/version.sh

%build
autoconf
# RPM_OPT_FLAGS come from apxs2
%configure \
        --with-apxs=`which %{apxs}` \
        --libdir="%{_libdir}" \
        --with-python="%__python"

make OPT="$(%{apxs} -q CFLAGS)" %{?_smp_mflags}

%install
%__install -d $RPM_BUILD_ROOT/%{_bindir}
%__make DESTDIR=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root)
%doc COPYRIGHT CREDITS NEWS doc-html
%{apache_libexecdir}/%{modname}.so
%{python_sitearch}/*
%{_bindir}/mod_python

%changelog
* Thu Jan  9 2014 poeml@cmdline.net
- update to 3.5.0
- remove the three obsolete patches
* Thu May 10 2012 cfarrell@suse.com
- license update: Apache-2.0
  Choose the correct license and use SPDX format
  (http://www.spdx.org/licenses)
* Tue Dec 20 2011 coolo@suse.com
- add autoconf as buildrequire to avoid implicit dependency
* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile
- Use %%_smp_mflags for parallel build
* Sat Mar  5 2011 draht@suse.de
- refine last change to apply to python-2.7+ only (11.4+).
* Tue Mar  1 2011 draht@suse.de
- apache2-mod_python-bnc675927.patch fixes bnc#675927:
  python segfaults on openSUSE 11.4 when used with mod_python
* Thu May  6 2010 opensuse@dstoecker.de
- fix md5 deprecation warning
* Tue May 19 2009 pascal.bleser@opensuse.org
- spec file cosmetic fixes
- pass -j
- use in-place sed (sed -i)
- added hacks for building with python2.5 on SLE 9
* Tue Aug 19 2008 poeml@suse.de
- fix build with apr 1.3.2 and later
  mod_python-3.3.1-bucket-brigade.patch
  http://www.mail-archive.com/dev@apr.apache.org/msg20588.html
* Fri Apr 13 2007 poeml@suse.de
- update to 3.3.1
  | New Features
  | - (MODPYTHON-103) New req.add_output_filter(),
  |   req.add_input_filter(), req.register_output_fiter(),
  |   req.register_input_filter() methods. These allows the dynamic
  |   registration of filters and the attaching of filters to the
  |   current request.
  | - (MODPYTHON-104) Support added for using Python in content being
  |   passed through "INCLUDES" output filter, or as more commonly
  |   referred to server side include (SSI) mechanism.
  | - (MODPYTHON-108) Added support to cookies for httponly attribute,
  |   an extension originally created by Microsoft, but now getting
  |   more widespread use in the battle against cross site-scripting
  |   attacks.
  | - (MODPYTHON-118) Now possible using the PythonImport directive to
  |   specify the name of a function contained in the module to be
  |   called once the designated module has been imported.
  | - (MODPYTHON-124) New req.auth_name() and req.auth_type() methods.
  |   These return the values associated with the AuthName and AuthType
  |   directives respectively. The req.ap_auth_type has now also been
  |   made writable so that it can be set by an authentication handler.
  | - (MODPYTHON-130) Added req.set_etag(), req.set_last_modified() and
  |   req.update_mtime() functions as wrappers for similar functions
  |   provided by Apache C API. These are required to effectively use
  |   the req.meets_condition() function.  The documentation for
  |   req.meets_condition() has also been updated as what it previously
  |   described probably wouldn't actually work.
  | - (MODPYTHON-132) New req.construct_url() method. Used to construct
  |   a fully qualified URI string incorporating correct scheme, server
  |   and port.
  | - (MODPYTHON-144) The "apache.interpreter" and "apache.main_server"
  |   attributes have been made publically available. These were
  |   previously private and not part of the public API.
  | - (MODPYTHON-149) Added support for session objects that span
  |   domains.
  | - (MODPYTHON-153) Added req.discard_request_body() function as
  |   wrapper for similar function provided by Apache C API. The
  |   function tests for and reads any message body in the request,
  |   simply discarding whatever it receives.
  | - (MODPYTHON-164) The req.add_handler(),
  |   req.register_input_filter() and req.register_output_filter()
  |   methods can now take a direct reference to a callable object as
  |   well a string which refers to a module or module::function
  |   combination by name.
  | - (MODPYTHON-165) Exported functions from mod_python module to be
  |   used in other third party modules for Apache. The purpose of
  |   these functions is to allow those other modules to access the
  |   mechanics of how mod_python creates interpreters, thereby
  |   allowing other modules to also embed Python and for there not to
  |   be a conflict with mod_python.
  | - (MODPYTHON-170) Added req._request_rec, server._server_rec and
  |   conn._conn_rec semi private members for getting accessing to
  |   underlying Apache struct as a Python CObject. These can be used
  |   for use in implementing SWIG bindings for lower level APIs of
  |   Apache. These members should be regarded as experimental and
  |   there are no guarantees that they will remain present in this
  |   specific form in the future.
  | - (MODPYTHON-193) Added new attribute available as
  |   req.hlist.location. For a handler executed directly as the result
  |   of a handler directive within a Location directive, this will be
  |   set to the value of the Location directive. If LocationMatch, or
  |   wildcards or regular expressions are used with Location, the
  |   value will be the matched value in the URL and not the pattern.
  |
  | Improvements
  | - (MODPYTHON-27) When using mod_python.publisher, the __auth__()
  |   and __access__() functions and the __auth_realm__ string can now
  |   be nested within a class method as a well a normal function.
  | - (MODPYTHON-90) The PythonEnablePdb configuration option will now
  |   be ignored if Apache hasn't been started up in single process
  |   mode.
  | - (MODPYTHON-91) If running Apache in single process mode with PDB
  |   enabled and the "quit" command is used to exit that debug
  |   session, an exception indicating that the PDB session has been
  |   aborted is raised rather than None being returned with a
  |   subsequent error complaining about the handler returning an
  |   invalid value.
  | - (MODPYTHON-93) Improved util.FieldStorage efficiency and made the
  |   interface more dictionary like.
  | - (MODPYTHON-101) Force an exception when handler evaluates to
  |   something other than None but is otherwise not callable.
  |   Previously an exception would not be generated if the handler
  |   evaluated to False.
  | - (MODPYTHON-107) Neither mod_python.publisher nor mod_python.psp
  |   explicitly flush output after writing the content of the response
  |   back to the request object. By not flushing output it is now
  |   possible to use the "CONTENT_LENGTH" output filter to add a
  |   "Content-Length" header.
  | - (MODPYTHON-111) Note made in session documentation that a save is
  |   required to avoid session timeouts.
  | - (MODPYTHON-125) The req.handler attribute is now writable. This
  |   allows a handler executing in a phase prior to the response phase
  |   to specify which Apache module will be responsible for generating
  |   the content.
  | - (MODPYTHON-128) Made the req.canonical_filename attribute
  |   writable. Changed the req.finfo attribute from being a tuple to
  |   an actual object. For backwards compatibility the attributes of
  |   the object can still be accessed as if they were a tuple. New
  |   code however should access the attributes as member data. The
  |   req.finfo attribute is also now writable and can be assigned to
  |   using the result of calling the new function apache.stat(). This
  |   function is a wrapper for apr_stat().
  | - (MODPYTHON-129) When specifying multiple handlers for a phase,
  |   the status returned by each handler is now treated the same as
  |   how Apache would treat the status if the handler was registered
  |   using the low level C API. What this means is that whereas
  |   stacked handlers of any phase would in turn previously be
  |   executed as long as they returned apache.OK, this is no longer
  |   the case and what happens is dependent on the phase.
  |   Specifically, a handler returning apache.DECLINED no longer
  |   causes the execution of subsequent handlers for the phase to be
  |   skipped. Instead, it will move to the next of the stacked
  |   handlers. In the case of PythonTransHandler, PythonAuthenHandler,
  |   PythonAuthzHandler and PythonTypeHandler, as soon as apache.OK is
  |   returned, subsequent handlers for the phase will be skipped, as
  |   the result indicates that any processing pertinent to that phase
  |   has been completed. For other phases, stacked handlers will
  |   continue to be executed if apache.OK is returned as well as when
  |   apache.DECLINED is returned. This new interpretation of the
  |   status returned also applies to stacked content handlers listed
  |   against the PythonHandler directive even though Apache notionally
  |   only ever calls at most one content handler. Where all stacked
  |   content handlers in that phase run, the status returned from the
  |   last handler becomes the overall status from the content phase.
  | - (MODPYTHON-141) The req.proxyreq and req.uri attributes are now
  |   writable. This allows a handler to setup these values and trigger
  |   proxying of the current request to a remote server.
  | - (MODPYTHON-142) The req.no_cache and req.no_local_copy attributes
  |   are now writable.
  | - (MODPYTHON-143) Completely reimplemented the module importer.
  |   This is now used whenever modules are imported corresponding to
  |   any of the Python*Handler, Python*Filter and PythonImport
  |   directives. The module importer is still able to be used directly
  |   using the apache.import_module() function. The new module
  |   importer no longer supports automatic reloading of
  |   packages/modules that appear on the standard Python module search
  |   path as defined by the PythonPath directive or within an
  |   application by direct changes to sys.path. Automatic module
  |   reloading is however still performed on file based modules (not
  |   packages) which are located within the document tree where
  |   handlers are located.  Locations within the document tree are
  |   however no longer added to the standard Python module search path
  |   automatically as they are maintained within a distinct importer
  |   search path. The PythonPath directive MUST not be used to point
  |   at directories within the document tree. To have additional
  |   directories be searched by the module importer, they should be
  |   listed in the mod_python.importer.path option using the
  |   PythonOption directive. This is a path similar to how PythonPath
  |   argument is supplied, but MUST not reference sys.path nor contain
  |   any directories also listed in the standard Python module search
  |   path. If an application does not appear to work under the module
  |   importer, the old module importer can be reenabled by setting the
  |   mod_python.legacy.importer option using the PythonOption
  |   directive to the value '*'. This option must be set in the global
  |   Apache configuration.
  | - (MODPYTHON-152) When in a sub request, when a request is the
  |   result of an internal redirect, or when when returning from such
  |   a request, the req.main, req.prev and req.next members now
  |   correctly return a reference to the original Python request
  |   object wrapper first created for the specific request_rec
  |   instance rather than creating a new distinct Python request
  |   object. This means that any data added explicitly to a request
  |   object can be passed between such requests.
  | - (MODPYTHON-178) When using mod_python.psp, if the PSP file which
  |   is the target of the request doesn't actually exist, an
  |   apache.HTTP_NOT_FOUND server error is now returned to the client
  |   rather than raising a ValueError exception which results in a 500
  |   internal server error. Note that if using SetHandler and the
  |   request is against the directory and no DirectoryIndex directive
  |   is specified which lists a valid PSP index file, then the same
  |   apache.HTTP_NOT_FOUND server error is returned to the client.
  | - (MODPYTHON-196) For completeness, added req.server.log_error()
  |   and req.connection.log_error(). The latter wraps ap_log_cerror()
  |   (when available), allowing client information to be logged along
  |   with message from a connection handler.
  | - (MODPYTHON-206) The attribute req.used_path_info is now
  |   modifiable and can be set from within handlers. This is
  |   equivalent to having used the AcceptPathInfo directive.
  | - (MODPYTHON-207) The attribute req.args is now modifiable and can
  |   be set from within handlers.
  |
  | Bug Fixes
  | - (MODPYTHON-38) Fixed issue when using PSP pages in conjunction
  |   with publisher handler or where a PSP error page was being
  |   triggered, that form parameters coming from content of a POST
  |   request weren't available or only available using a workaround.
  |   Specifically, the PSP page will now use any FieldStorage object
  |   instance cached as req.form left there by preceding code.
  | - (MODPYTHON-43) Nested __auth__() functions in
  |   mod_python.publisher now execute in context of globals from the
  |   file the function is in and not that of mod_python.publisher
  |   itself.
  | - (MODPYTHON-47) Fixed mod_python.publisher so it will not return a
  |   HTTP Bad Request response when mod_auth is being used to provide
  |   Digest authentication.
  | - (MODPYTHON-63) When handler directives are used within Directory
  |   or DirectoryMatch directives where wildcards or regular
  |   expressions are used, the handler directory will be set to the
  |   shortest directory matched by the directory pattern. Handler
  |   directives can now also be used within Files and FilesMatch
  |   directives and the handler directory will correctly resolve to
  |   the directory corresponding to the enclosing Directory or
  |   DirectoryMatch directive, or the directory the .htaccess file is
  |   contained in.
  | - (MODPYTHON-76) The FilterDispatch callback should not flush the
  |   filter if it has already been closed.
  | - (MODPYTHON-84) The original change to fix the symlink issue for
  |   req.sendfile() was causing problems on Win32, plus code needed to
  |   be changed to work with APR 1.2.7.
  | - (MODPYTHON-100) When using stacked handlers and a SERVER_RETURN
  |   exception was used to return an OK status for that handler, any
  |   following handlers weren't being run if appropriate for the
  |   phase.
  | - (MODPYTHON-109) The Py_Finalize() function was being called on
  |   child process shutdown. This was being done though from within
  |   the context of a signal handler, which is generally unsafe and
  |   would cause the process to lock up. This function is no longer
  |   called on child process shutdown.
  | - (MODPYTHON-112) The req.phase attribute is no longer overwritten
  |   by an input or output filter. The filter.is_input member should
  |   be used to determine if a filter is an input or output filter.
  | - (MODPYTHON-113) The PythonImport directive now uses the
  |   apache.import_module() function to import modules to avoid
  |   reloading problems when same module is imported from a handler.
  | - (MODPYTHON-114) Fixed race conditions on setting sys.path when
  |   the PythonPath directive is being used as well as problems with
  |   infinite extension of path.
  | - (MODPYTHON-120) (MODPYTHON-121) Fixes to test suite so it will
  |   work on virtual hosting environments where localhost doesn't
  |   resolve to 127.0.0.1 but the actual IP address of the host.
  | - (MODPYTHON-126) When Python*Handler or Python*Filter directive is
  |   used inside of a Files directive container, the handler/filter
  |   directory value will now correctly resolve to the directory
  |   corresponding to any parent Directory directive or the location
  |   of the .htaccess file the Files directive is contained in.
  | - (MODPYTHON-133) The table object returned by
  |   req.server.get_config() was not being populated correctly to be
  |   the state of directives set at global scope for the server.
  | - (MODPYTHON-134) Setting PythonDebug to Off, wasn't overriding On
  |   setting in parent scope.
  | - (MODPYTHON-140) The util.redirect() function should be returning
  |   server status of apache.DONE and not apache.OK otherwise it will
  |   not give desired result if used in non content handler phase or
  |   where there are stacked content handlers.
  | - (MODPYTHON-147) Stopped directories being added to sys.path
  |   multiple times when PythonImport and PythonPath directive used.
  | - (MODPYTHON-148) Added missing Apache contants
  |   apache.PROXYREQ_RESPONSE and apache.HTTP_UPGRADE_REQUIRED. Also
  |   added new constants for Apache magic mime types and values for
  |   interpreting the req.connection.keepalive and req.read_body
  |   members.
  | - (MODPYTHON-150) In a multithread MPM, the apache.init() function
  |   could be called more than once for a specific interpreter
  |   instance whereas it should only be called once.
  | - (MODPYTHON-151) Debug error page returned to client when an
  |   exception in a handler occurred wasn't escaping special HTML
  |   characters in the traceback or the details of the exception.
  | - (MODPYTHON-157) Wrong interpreter name used for fixup handler
  |   phase and earlier, when PythonInterpPerDirectory was enabled and
  |   request was against a directory but client didn't provide the
  |   trailing slash.
  | - (MODPYTHON-159) Fix FieldStorage class so that it can handle
  |   multiline headers.
  | - (MODPYTHON-160) Using PythonInterpPerDirective when setting
  |   content handler to run dynamically with req.add_handler() would
  |   cause Apache to crash.
  | - (MODPYTHON-161) Directory argument supplied to req.add_handler()
  |   is canonicalized and a trailing slash added automatically. This
  |   is needed to ensure that the directory is always in POSIX path
  |   style as used by Apache and that convention where directories
  |   associated with directives always have trailing slash is adhered
  |   to. If this is not done, a different interpreter can be chosen to
  |   that expected when the PythonInterpPerDirective is used.
  | - (MODPYTHON-166) PythonHandlerModule was not setting up
  |   registration of the PythonFixupHandler or PythonAuthenHandler.
  |   For the latter this meant that using Require directive with
  |   PythonHandlerModule would cause a 500 error and complaint in
  |   error log about "No groups file".
  | - (MODPYTHON-167) When PythonDebug was On and and exception
  |   occurred, the response to the client had a status of 200 when it
  |   really should have been a 500 error status indicating that an
  |   internal error occurred. A 500 error status was correctly being
  |   returned when PythonDebug was Off.
  | - (MODPYTHON-168) Fixed psp_parser error when CR is used as a line
  |   terminator in psp code. This may occur with some older editors
  |   such as GoLive on Mac OS X.
  | - (MODPYTHON-175) Fixed problem whereby a main PSP page and an
  |   error page triggered from that page both accessing the session
  |   object would cause a deadlock.
  | - (MODPYTHON-176) Fixed issue whereby PSP code would unlock session
  |   object which it had inherited from the caller meaning caller
  |   could no longer use it safely. PSP code will now only unlock
  |   session if it created it in the first place.
  | - (MODPYTHON-179) Fixed the behaviour of req.readlines() when a
  |   size hint was provided. Previously, it would always return a
  |   single line when a size hint was provided.
  | - (MODPYTHON-180) Publisher would wrongly output a warning about
  |   nothing to publish if req.write() or req.sendfile() used and data
  |   not flushed, and then published function returned None.
  | - (MODPYTHON-181) Fixed memory leak when mod_python handlers are
  |   defined for more than one phase at the same time.
  | - (MODPYTHON-182) Fixed memory leak in req.readline().
  | - (MODPYTHON-184) Fix memory leak in apache.make_table(). This was
  |   used by util.FieldStorage class so affected all code using forms.
  | - (MODPYTHON-185) Fixed segfault in psp.parsestring(src_string)
  |   when src_string is empty.
  | - (MODPYTHON-187) Table objects could crash in various ways when
  |   the value of an item was NULL. This could occur for
  |   SCRIPT_FILENAME when the req.subprocess_env table was accessed in
  |   the post read request handler phase.
  | - (MODPYTHON-189) Fixed representation returned by calling repr()
  |   on a table object.
  | - (MODPYTHON-191) Session class will no longer accept a normal
  |   cookie if a signed cookie was expected.
  | - (MODPYTHON-194) Fixed potential memory leak due to not clearing
  |   the state of thread state objects before deleting them.
  | - (MODPYTHON-195) Fix potential Win32 resource leaks in parent
  |   Apache process when process restarts occur.
  | - (MODPYTHON-198) Python 2.5 broke nested
  |   __auth__/__access__/__auth_realm__ in mod_python.publisher.
  | - (MODPYTHON-200) Fixed problem whereby signed and marshalled
  |   cookies could not be used at the same time. When expecting
  |   marshalled cookie, any signed, but not marshalled cookies will be
  |   returned as normal cookies.
* Mon Oct 23 2006 poeml@suse.de
- simplify last fix, so it still builds with python < 2.5.
* Sat Sep 23 2006 aj@suse.de
- Fix build with python 2.5.
* Fri Aug 18 2006 poeml@suse.de
- update to 3.2.10
  |- New Features
  |  - (MODPYTHON-78) Added support for Apache 2.2.
  |  - (MODPYTHON-94) New req.is_https() and req.ssl_var_lookup()
  |    methods. These communicate direct with the Apache mod_ssl
  |    module, allowing it to be determined if the connection is
  |    using SSL/TLS and what the values of internal ssl variables
  |    are.
  |  - (MODPYTHON-137) New req.server.get_options() method. This
  |    returns the subset of Python options set at global scope
  |    within the Apache configuration. That is, outside of the
  |    context of any VirtualHost, Location, Directory or Files
  |    directives.
  |  - (MODPYTHON-131) The directory used for mutex locks can now be
  |    specified at at compile time using ./configure
  |    --with-mutex-dir value or at run time with PythonOption
  |    mod_python.mutex_directory value.
  |  - (MODPYTHON-145) The number of mutex locks can now be
  |    specified at run time with PythonOption
  |    mod_python.mutex_locks value.
  |  - (MODPYTHON-172) Fixed three memory leaks that were found in
  |    _apachemodule.parse_qsl, req.readlines and util.cfgtree_walk.
  |- Improvements
  |  - (MODPYTHON-77) Third party C modules that use the simplified
  |    API for the Global Interpreter Lock (GIL), as described in
  |    PEP 311, can now be used. The only requirement is that such
  |    modules can only be used in the context of the
  |    "main_interpreter".
  |  - (MODPYTHON-119) DbmSession unit test no longer uses the
  |    default directory for the dbm file, so the test will not
  |    interfer with the user's current apache instance.
  |  - (MODPYTHON-158) Added additional debugging and logging output
  |    for where mod_python cannot initialise itself properly due to
  |    Python or mod_python version mismatches or missing Python
  |    module code files.
  |- Bug Fixes
  |  - (MODPYTHON-122) Fixed configure problem when using bash 3.1.x.
  |  - (MODPYTHON-173) Fixed DbmSession to create db file with mode 0640.
  |  - (MODPYTHON-84) Fixed request.sendfile() bug for symlinked
  |    files on Win32.
- drop obsolete patches
* Fri Aug 18 2006 poeml@suse.de
- update to 3.2.8
  |- New Features:
  |  - New apache.register_cleanup() method.
  |  - New apache.exists_config_define() method.
  |  - New file-based session manager class.
  |  - Session cookie name can be specified.
  |  - The maximum number of mutexes mod_python uses for session
  |    locking can now be specifed at compile time using configure
  |    --with-max-locks.
  |  - New a version attribute in mod_python module.
  |  - New test handler testhandler.py has been added.
  |- Improvements
  |  - Autoreload of a module using apache.import_module() now works
  |    if modification time for the module is different from the
  |    file.  Previously, the module was only reloaded if the the
  |    modification time of the file was more recent. This allows
  |    for a more graceful reload if a file with an older
  |    modification time needs to be restored from backup.
  |  - Fixed the publisher traversal security issue
  |  - Objects hierarchy a la CherryPy can now be published.
  |  - mod_python.c now logs reason for a 500 error
  |  - Calls to PyErr_Print in mod_python.c are now followed by
  |    fflush()
  |  - Using an empty value with PythonOption will unset a
  |    PythonOption key.
  |  - req.path_info is now a read/write member.
  |  - Improvements to FieldStorage allow uploading of large files.
  |    Uploaded files are now streamed to disk, not to memory.
  |  - Path to flex is now discovered at configuration time or can
  |    be specifed using configure --with-flex=/path/to/flex.
  |  - sys.argv is now initialized to ["mod_python"] so that modules
  |    like numarray and pychart can work properly.
  |- Bug Fixes
  |  - Fixed memory leak which resulted from circular references
  |    starting from the request object.
  |  - Fixed memory leak resulting from multiple PythonOption
  |    directives.
  |  - Fixed Multiple/redundant interpreter creation problem.
  |  - Cookie attributes with attribute names prefixed with $ are
  |    now ignored. See Section 4.7 for more information.
  |  - Bug in setting up of config_dir from Handler directives
  |    fixed.
  |  - mod_python.publisher will now support modules with the same
  |    name but in different directories
  |  - Fixed continual reloading of modules problem
  |  - Fixed big marshalled cookies error.
  |  - Fixed mod_python.publisher extension handling
  |  - mod_python.publisher default index file traversal
  |  - mod_python.publisher loading wrong module and giving no
  |    warning/error
  |  - apply_fs_data() now works with "new style" objects
  |  - File descriptor fd closed after ap_send_fd() in
  |    req_sendfile()
  |  - Bug in mem_cleanup in MemorySession fixed.
  |  - Fixed bug in _apache._global_lock() which could cause a
  |    segfault if the lock index parameter is greater number of
  |    mutexes created at mod_python startup.
  |  - Fixed bug where local_ip and local_host in connection object
  |    were returning remote_ip and remote_host instead
  |  - Fixed install_dso Makefile rule so it only installs the dso,
  |    not the python files
  |  - Potential deadlock in psp cache handling fixed
  |  - Fixed bug where sessions are used outside <Directory>
  |    directive.
  |  - Fixed compile problem on IRIX. ln -s requires both TARGET and
  |    LINK_NAME on IRIX. ie. ln -s TARGET LINK_NAME
  |  - Fixed ./configure problem on SuSE Linux 9.2 (x86-64). Python
  |    libraries are in lib64/ for this platform.
  |  - Fixed req.sendfile() problem where sendfile(filename) sends
  |    the incorrect number of bytes when filename is a symlink.
  |  - Fixed problem where util.FieldStorage was not correctly
  |    checking the mime types of POSTed entities
  |  - Fixed conn.local_addr and conn.remote_addr for a better IPv6
  |    support.
  |  - Fixed psp_parser.l to properly escape backslash-n,
  |    backslash-t and backslash-r character sequences.
  |  - Fixed segfault bug when accessing some request object members
  |    (allowed_methods, allowed_xmethods, content_languages) and
  |    some server object members (names, wild_names).
  |  - Fixed request.add_handler() segfault bug when adding a
  |    handler to an empty handler list.
  |  - Fixed PythonAutoReload directive so that AutoReload can be
  |    turned off.
  |  - Fixed connection object read() bug on FreeBSD.
  |  - Fixed potential buffer corruption bug in connection object
  |    read().
- remove references to obsolete APR_STATUS_IS_SUCCESS and
  apr_sockaddr_port_get() for libapr-1.2.7
- drop obsolete mod_python-3.1.3-publisher.dif
- fix installation into the correct libdir, it didn't work anymore
* Sat Mar  4 2006 aj@suse.de
- updated to reflect python changes due to #149809
* Mon Jan 30 2006 poeml@suse.de
- removed libapr-util1-devel from BuildRequires (apache2-devel does
  require it)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Dec 21 2005 ro@suse.de
- fix quoting problem in configure.in
* Thu Dec  8 2005 poeml@suse.de
- if building with apache 2.2, remove references to
  obsolete APR_STATUS_IS_SUCCESS
* Wed Oct  5 2005 dmueller@suse.de
- add norootforbuild
* Fri Feb 11 2005 poeml@suse.de
- fix CAN-2005-0088 patch [#50324]
* Tue Feb  1 2005 poeml@suse.de
- fix information leak in publisher handler, CAN-2005-0088 [#50324]
* Tue Jan 25 2005 poeml@suse.de
- move usage hints from %%post into package description
* Wed Nov 24 2004 mcihar@suse.de
- use %%{py_sitedir}
* Fri Mar  5 2004 poeml@suse.de
- update to 3.1.3
- package is now licensed under Apache Software License 2.0
* Tue Feb 10 2004 poeml@suse.de
- update to 3.0.4, which fixes a vulnerability whereby a specific
  query string processed by mod_python would cause the httpd rocess
  to crash.
- mod_python-3.0.3-python-2.3b1.dif is no longer needed
* Fri Aug 29 2003 mcihar@suse.cz
- require same python version as it was built with
* Fri Aug 29 2003 poeml@suse.de
- Conflicts: mod_python (the Apache 1 module) [#29637]
* Mon Jul 28 2003 poeml@suse.de
- don't explicitely strip binaries since RPM handles it, and may
  keep the stripped information somewhere
- fix mentioned path to documentation
* Thu Jun  5 2003 poeml@suse.de
- install missing .py files into python's site-packages folder
- fix installation on 64 bit architecture (lib64)
* Fri May 30 2003 poeml@suse.de
- new package
- in python-2.3b1, LONG_LONG is renamed to PY_LONG_LONG

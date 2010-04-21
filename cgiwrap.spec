Summary:	A gateway for more secure user access to CGI scripts
Summary(pl.UTF-8):	Bramka do bezpieczniejszego dostępu użytkowników do skryptów CGI
Name:		cgiwrap
Version:	4.1
Release:	8
License:	GPL
Group:		Utilities
Source0:	http://dl.sourceforge.net/cgiwrap/%{name}-%{version}.tar.gz
# Source0-md5:	14c02c57e4a0c6224951018e2f6b9211
Patch0:		%{name}-mime_magic.patch
Patch1:		%{name}-bs.patch
Patch2:		%{name}-phprc.patch
Patch3:		%{name}-customhtmlerrors.patch
URL:		http://cgiwrap.sourceforge.net/
BuildRequires:	automake
BuildRequires:	libmagic-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cgibindir	/home/services/httpd/cgi-bin

%description
A gateway that allows more secure user access to CGI programs on an
HTTPd server than is provided by the HTTP server itself. The primary
function of CGIwrap is to make certain that any CGI script runs with
the permissions of the user who installed it, and not those of the
server.

%description -l pl.UTF-8
Bramka pozwalająca na bardziej bezpieczny dostęp użytkowników do
programów CGI na serwerze HTTP niż ten udostępniany przez sam serwer
HTTP. Główna funkcja CGIwrap to upewnienie się, że skrypt CGI działa z
uprawnieniami użytkownika, który go zainstalował, a nie serwera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1

%build
install %{_datadir}/automake/config.* .
%{__autoconf}
%configure \
	--with-perl=%{_bindir}/perl \
	--with-php=%{_bindir}/php.cgi \
	--with-local-contact-email=root@localhost \
	--with-httpd-user=http \
	--with-minimum-uid=500 \
	--with-minimum-gid=500 \
	--with-block-svn-paths \
	--with-block-cvs-paths \
	--with-php-interpreter \
	--with-soft-rlimit-only \
	--with-cgi-dir=public_html \
	--without-check-symlink \
	--without-check-group \
	--with-use-script-url \
	--with-quiet-errors \
	--with-custom-html-errors=/etc/cgiwrap

%{__make} \
	LDFLAGS='%{rpmldflags} -lmagic'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_cgibindir},%{_sysconfdir}/cgiwrap}

install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/cgiwrapd
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/nph-cgiwrap
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/nph-cgiwrapd
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/php-cgiwrap
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/php-cgiwrapd

echo "The cgiwrap executable(s) were not made setuid-root. This is required" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/CGIWrapNotSetUID.html
echo "The userid that the web server ran cgiwrap as does not match the userid that was configured into the cgiwrap executable" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/ServerUserMismatch.html
echo "CGIWrap was configured with a server userid that does not exist" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/ServerUserNotFound.html
echo "Execution is not permitted" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/ExecutionNotPermitted.html
echo "CGIWrap access control mechanism denied execution of this script" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/AccessControl.html
echo "CGIWrap encountered a system error" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/SystemError.html
echo "CGIWrap encountered an error while attempting to execute this script" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/ExecFailed.html
echo "CGIWrap was unable to find the user" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/NoSuchUser.html
echo "The specified user does not have a script directory set up" > $RPM_BUILD_ROOT%{_sysconfdir}/cgiwrap/NoScriptDir.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc htdocs/*
%attr(4755,root,root) %{_cgibindir}/*
%dir %{_sysconfdir}/cgiwrap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cgiwrap/*.html

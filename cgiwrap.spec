Summary:	A gateway for more secure user access to CGI scripts
Name:		cgiwrap
Version:	3.9
Release:	1
License:	GPL
Group:		Utilities
Source0:	http://dl.sourceforge.net/cgiwrap/%{name}-%{version}.tar.gz
# Source0-md5:	0f9c88802658f45231ee463c351bd2a7
URL:		http://cgilib.sourceforge.net/
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A gateway that allows more secure user access to CGI programs on an
HTTPd server than is provided by the http server itself. The primary
function of CGIwrap is to make certain that any CGI script runs with
the permissions of the user who installed it, and not those of the
server.

%prep
%setup -q

%build
install %{_datadir}/automake/config.* .
%configure \
	--with-perl=%{_bindir}/perl \
	--with-php=%{_bindir}/php \
	--with-local-contact-email=root@localhost \
	--with-httpd-user=http \
	--with-minimum-uid=500 \
	--with-minimum-gid=500 \
--with-allow-file=%{_sysconfdir}/cgiwrap/cgiwrap.allow \
--with-deny-file=%{_sysconfdir}/cgiwrap/cgiwrap.deny
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/home/services/httpd/cgi-bin

install cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin
ln -s cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/cgiwrapd
ln -s cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/nph-cgiwrap
ln -s cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/nph-cgiwrapd
ln -s cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/php-cgiwrap
ln -s cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/cgiwrapd
ln -s cgiwrap $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/php-cgiwrapd

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc htdocs/*
%attr(4755,root,root) $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/*

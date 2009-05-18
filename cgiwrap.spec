Summary:	A gateway for more secure user access to CGI scripts
Summary(pl.UTF-8):	Bramka do bezpieczniejszego dostępu użytkowników do skryptów CGI
Name:		cgiwrap
Version:	4.1
Release:	2
License:	GPL
Group:		Utilities
Source0:	http://dl.sourceforge.net/cgiwrap/%{name}-%{version}.tar.gz
# Source0-md5:	14c02c57e4a0c6224951018e2f6b9211
Patch0:		%{name}-php.patch
URL:		http://cgiwrap.sourceforge.net/
BuildRequires:	automake
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
%patch0 -p0

%build
install %{_datadir}/automake/config.* .
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
	--with-cgi-dir=./ \
	--without-check-group

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_cgibindir}

install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/cgiwrapd
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/nph-cgiwrap
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/nph-cgiwrapd
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/php-cgiwrap
install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/php-cgiwrapd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc htdocs/*
%attr(4755,root,root) %{_cgibindir}/*

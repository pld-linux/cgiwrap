Summary:	A gateway for more secure user access to CGI scripts
Summary(pl):	Bramka do bezpieczniejszego dostêpu u¿ytkowników do skryptów CGI
Name:		cgiwrap
Version:	3.9
Release:	1
License:	GPL
Group:		Utilities
Source0:	http://dl.sourceforge.net/cgiwrap/%{name}-%{version}.tar.gz
# Source0-md5:	0f9c88802658f45231ee463c351bd2a7
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

%description -l pl
Bramka pozwalaj±ca na bardziej bezpieczny dostêp u¿ytkowników do
programów CGI na serwerze HTTP ni¿ ten udostêpniany przez sam serwer
HTTP. G³ówna funkcja CGIwrap to upewnienie siê, ¿e skrypt CGI dzia³a z
uprawnieniami u¿ytkownika, który go zainstalowa³, a nie serwera.

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
install -d $RPM_BUILD_ROOT%{_cgibindir}

install cgiwrap $RPM_BUILD_ROOT%{_cgibindir}
ln -s cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/cgiwrapd
ln -s cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/nph-cgiwrap
ln -s cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/nph-cgiwrapd
ln -s cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/php-cgiwrap
ln -s cgiwrap $RPM_BUILD_ROOT%{_cgibindir}/php-cgiwrapd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc htdocs/*
%attr(4755,root,root) %{_cgibindir}/*

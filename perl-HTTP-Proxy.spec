#
# Conditional build:
%bcond_without  autodeps	# don't BR packages needed only for resolving deps
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	HTTP
%define		pnam	Proxy
Summary:	A pure Perl HTTP proxy
Summary(pl.UTF-8):	Proxy HTTP zaimplementowany w czystym Perlu
Name:		perl-%{pdir}-%{pnam}
Version:	0.304
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	09ac64c5f67b7d8baff4ea135d74af48
URL:		http://search.cpan.org/dist/HTTP-Proxy/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with autodeps} || %{with tests}
BuildRequires:	perl(HTTP::Daemon) >= 1.25
BuildRequires:	perl(LWP::UserAgent) >= 2
BuildRequires:	perl-libwww >= 1.25
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements a HTTP proxy, using a HTTP::Daemon to accept
client connections, and a LWP::UserAgent to ask for the requested
pages.

The most interesting feature of this proxy object is its ability to
filter the HTTP requests and responses through user-defined filters.

%description -l pl.UTF-8
Ten moduł implementuje proxy HTTP, używając HTTP::Daemon do
przyjmowania połączeń klienckich i LWP::UserAgent do pobierania
żądanych stron.

Najciekawszą opcją tego obiektu proxy jest możliwość filtrowania
zapytań i odpowiedzi HTTP poprzez filtry definiowane przez
użytkownika.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

# disable tests as one is broken: https://github.com/book/HTTP-Proxy/issues/7
#%%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a eg $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/HTTP/Proxy.pm
%{perl_vendorlib}/HTTP/Proxy
%{_mandir}/man3/*.3*
%{_examplesdir}/%{name}-%{version}

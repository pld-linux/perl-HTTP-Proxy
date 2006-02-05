#
# Conditional build:
%bcond_without  autodeps	# don't BR packages needed only for resolving deps
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	HTTP
%define		pnam	Proxy
Summary:	A pure Perl HTTP proxy
Summary(pl):	Proxy HTTP zaimplementowany w czystym Perlu
Name:		perl-%{pdir}-%{pnam}
Version:	0.17
Release:	0.1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5f8dee810951840408092c07faccfa1a
URL:		http://search.cpan.org/dist/HTTP-Proxy/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with autodeps} || %{with tests}
BuildRequires:	perl-libwww
BuildRequires:	perl(HTTP::Daemon) >= 1.25
BuildRequires:	perl(LWP::UserAgent) >= 2
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements a HTTP proxy, using a HTTP::Daemon to accept
client connections, and a LWP::UserAgent to ask for the requested
pages.

The most interesting feature of this proxy object is its ability to
filter the HTTP requests and responses through user-defined filters.
 
%description -l pl
Ten modu³ implementuje proxy HTTP, u¿ywaj±c HTTP::Daemon do
przyjmowania po³±czeñ klienckich i LWP::UserAgent do pobierania
¿±danych stron.

Najciekawsz± opcj± tego obiektu proxy jest mo¿liwo¶æ filtrowania
zapytañ i odpowiedzi HTTP poprzez filtry definiowane przez
u¿ytkownika.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/HTTP/Proxy.pm
%{perl_vendorlib}/HTTP/Proxy
%{_mandir}/man3/*

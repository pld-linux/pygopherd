Summary:	Gopher server
Summary(pl):	Serwer gophera
Name:		pygopherd
Version:	2.0.9
Release:	0.2
License:	GPL
Group:		Networking/Daemons
Vendor:		John Goerzen <jgoerzen@complete.org>
Source0:	http://gopher.quux.org:70/give-me-gopher/%{name}/%{name}_%{version}.tar.gz
# Source0-md5:	98f552fc13edefdd5fd3e70db07eed0b
URL:		gopher://gopher.quux.org/1/Software/Gopher
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
Provides:	gopher-server
Obsoletes:	gopher-server
Obsoletes:	gofish
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gopherd - a gopher server.

%description -l pl
gopherd - serwer gophera.

%prep
%setup -q -n %{name}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{py_sitescriptdir}/%{name}
%dir %{py_sitescriptdir}/%{name}/protocols
%dir %{py_sitescriptdir}/%{name}/handlers
%dir %{py_sitescriptdir}/%{name}/*.py[oc]
%dir %{py_sitescriptdir}/%{name}/handlers/*.py[oc]
%dir %{py_sitescriptdir}/%{name}/protocols/*.py[oc]

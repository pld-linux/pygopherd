Summary:	Gopher server
Summary(pl.UTF-8):	Serwer gophera
Name:		pygopherd
Version:	2.0.9
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://gopher.quux.org:70/give-me-gopher/pygopherd/%{name}_%{version}.tar.gz
# Source0-md5:	98f552fc13edefdd5fd3e70db07eed0b
Source1:	%{name}.init
Patch0:		%{name}-conf.patch
URL:		gopher://gopher.quux.org/1/Software/Gopher
BuildRequires:	rpmbuild(macros) >= 1.202
%pyrequires_eq	python-modules
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	gopher-server
Provides:	group(gopher)
Provides:	user(gopher)
Obsoletes:	gofish
Obsoletes:	gopher-server
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_rootdir	/home/services/gopher

%description
gopherd - a gopher server.

%description -l pl.UTF-8
gopherd - serwer gophera.

%prep
%setup -q -n %{name}
%patch0 -p0

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/{%{name},rc.d/init.d},%{py_sitescriptdir},%{_rootdir}}

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--install-lib=%{py_sitescriptdir} \
	--optimize=2

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pygopherd

find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 30 gopher
%useradd -u 13 -g 30 -d /no/home -s /bin/false -c "gopherd user" gopher

%postun
if [ "$1" = "0" ]; then
	%userremove gopher
	%groupremove gopher
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/pygopherd
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[oc]
%dir %{py_sitescriptdir}/%{name}/handlers
%{py_sitescriptdir}/%{name}/handlers/*.py[oc]
%dir %{py_sitescriptdir}/%{name}/protocols
%{py_sitescriptdir}/%{name}/protocols/*.py[oc]
%dir %{_rootdir}

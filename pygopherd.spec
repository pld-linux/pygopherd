Summary:	Gopher server
Summary(pl):	Serwer gophera
Name:		pygopherd
Version:	2.0.9
Release:	0.4
License:	GPL
Group:		Networking/Daemons
Vendor:		John Goerzen <jgoerzen@complete.org>
Source0:	http://gopher.quux.org:70/give-me-gopher/%{name}/%{name}_%{version}.tar.gz
# Source0-md5:	98f552fc13edefdd5fd3e70db07eed0b
Patch0:		%{name}-conf.patch
URL:		gopher://gopher.quux.org/1/Software/Gopher
%pyrequires_eq  python-modules
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	gopher-server
Obsoletes:	gopher-server
Obsoletes:	gofish
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_rootdir	/home/services/gopher

%description
gopherd - a gopher server.

%description -l pl
gopherd - serwer gophera.

%prep
%setup -q -n %{name}
%patch0 -p0

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/%{name},%{py_sitescriptdir},%{_rootdir}}

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--install-lib=%{py_sitescriptdir} \
	--optimize=2

find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid gopher`" ]; then
       if [ "`getgid gopher`" != "30" ]; then
               echo "Error: group gopher doesn't have gid=30 . Correct this before installing gofish." 1>&2
               exit 1
       fi
else
       echo "Adding group gopher GID=30."
       /usr/sbin/groupadd -g 30 gopher || exit 1
fi
if [ -n "`id -u gopher 2>/dev/null`" ]; then
       if [ "`id -u gopher`" != "13" ]; then
               echo "Error: user gopher doesn't have uid=13. Correct this before installing gofish." 1>&2
               exit 1
       fi
else
       echo "Adding user gopher UID=13."
       /usr/sbin/useradd -u 13 -g 30 -d /no/home -s /bin/false -c "gopherd user" gopher || exit 1
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[oc]
%dir %{py_sitescriptdir}/%{name}/handlers
%{py_sitescriptdir}/%{name}/handlers/*.py[oc]
%dir %{py_sitescriptdir}/%{name}/protocols
%{py_sitescriptdir}/%{name}/protocols/*.py[oc]
%dir %{_rootdir}

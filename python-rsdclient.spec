%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora}
%global with_python3 1
%endif

%global sname rsdclient
%global pyname python_rsdclient

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        OpenStack client plugin for Rack Scale Design

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{name}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n     python2-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-oslotest >= 1.10.0
BuildRequires:  python2-reno >= 1.8.0
BuildRequires:  python2-setuptools
BuildRequires:  python2-testrepository >= 0.0.18
BuildRequires:  python2-testtools >= 1.4.0

Requires:       python2-six >= 1.10.0
Requires:       python2-cliff >= 2.8.0
Requires:       python2-osc-lib >= 1.7.0
Requires:       python2-pbr >= 2.0
Requires:       python2-rsd-lib >= 0.1.1

%description -n python2-%{sname}
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n python2-%{sname}-tests
Summary: python-rsdclient tests
Requires: python2-%{sname} = %{version}-%{release}

%description -n python2-%{sname}-tests
Tests for python-rsdclient

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-reno >= 1.8.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-testrepository >= 0.0.18
BuildRequires:  python3-testtools >= 1.4.0

Requires:       python3-six >= 1.10.0
Requires:       python3-cliff >= 2.8.0
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-pbr >= 2.0
Requires:       python3-rsd-lib >= 0.1.1

%description -n python3-%{sname}
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n python3-%{sname}-tests
Summary: python-rsdclient tests
Requires: python3-%{sname} = %{version}-%{release}

%description -n python3-%{sname}-tests
Tests for python-rsdclient

%endif # with_python3

%package -n python-%{sname}-doc
Summary: python-rsdclient documentation

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx
BuildRequires: python2-openstackdocstheme >= 1.11.0

%description -n python-%{sname}-doc
Documentation for python-rsdclient

%prep
%autosetup -n %{name}-%{upstream_version} -S git

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pyname}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pyname}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pyname}

%files -n python2-%{sname}
%license LICENSE
%doc README.rst doc/source/readme.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/%{pyname}-*.egg-info
%exclude %{python2_sitelib}/%{sname}/tests

%files -n python2-%{sname}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{pyname}-*.egg-info
%exclude %{python3_sitelib}/%{sname}/tests

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests

%endif # with_python3

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst

%changelog

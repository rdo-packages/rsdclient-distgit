%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:           python-rsdclient
Version:        XXX
Release:        XXX
Summary:        OpenStack client plugin for Rack Scale Design

License:        ASL 2.0
URL:            https://github.com/openstack/%{name}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildConflicts: python-coverage = 4.4
BuildRequires:  python-coverage >= 4.0
BuildRequires:  python-hacking >= 0.12.0
BuildRequires:  python-openstackdocstheme >= 1.11.0
BuildRequires:  python-oslotest >= 1.10.0
BuildRequires:  python-reno >= 1.8.0
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx >= 1.6.2
BuildRequires:  python-testrepository >= 0.0.18
BuildRequires:  python-testtools >= 1.4.0
BuildRequires:  python-sphinx

Requires:       python-cliff >= 2.8.0
Requires:       python-osc-lib >= 1.7.0
Requires:       python-pbr >= 2.0
Requires:       python-rsd-lib >= 0.0.1
Requires:       python-setuptools

%description
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n     python2-rsdclient
Summary:        %{summary}
%{?python_provide:%python_provide python2-rsdclient}
Provides:       python-rsdclient = %{upstream_version}

%description -n python2-rsdclient
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%if 0%{?with_python3}
%package -n     python3-rsdclient
Summary:        %{summary}
%{?python_provide:%python_provide python3-rsdclient}

BuildRequires:  python3-devel
BuildConflicts: python3-coverage = 4.4
BuildRequires:  python3-coverage >= 4.0
BuildRequires:  python3-hacking < 0.13
BuildRequires:  python3-hacking >= 0.12.0
BuildRequires:  python3-openstackdocstheme >= 1.11.0
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-reno >= 1.8.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx >= 1.6.2
BuildRequires:  python3-testrepository >= 0.0.18
BuildRequires:  python3-testtools >= 1.4.0
BuildRequires:  python3-sphinx

Requires:       python3-cliff >= 2.8.0
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-pbr >= 2.0
Requires:       python3-rsd-lib >= 0.0.1
Requires:       python3-setuptools

%description -n python3-rsdclient
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%endif # with_python3

%prep
%autosetup -n python-rsdclient
# Remove bundled egg-info
rm -rf python-rsdclient.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build-2 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python-rsdclient
%license LICENSE
%doc README.rst doc/source/readme.rst
%{python2_sitelib}/python-rsdclient
%{python2_sitelib}/python-rsdclient-%{version}-py?.?.egg-info

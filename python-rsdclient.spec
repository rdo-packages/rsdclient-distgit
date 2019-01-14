# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

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

%package -n     python%{pyver}-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-oslotest >= 1.10.0
BuildRequires:  python%{pyver}-reno >= 1.8.0
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-testrepository >= 0.0.18
BuildRequires:  python%{pyver}-testtools >= 1.4.0

Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-cliff >= 2.8.0
Requires:       python%{pyver}-osc-lib >= 1.7.0
Requires:       python%{pyver}-pbr >= 2.0
Requires:       python%{pyver}-rsd-lib >= 0.1.1

%description -n python%{pyver}-%{sname}
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n python%{pyver}-%{sname}-tests
Summary: python-rsdclient tests
Requires: python%{pyver}-%{sname} = %{version}-%{release}

%description -n python%{pyver}-%{sname}-tests
Tests for python-rsdclient

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: python-rsdclient documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-oslo-sphinx
BuildRequires: python%{pyver}-openstackdocstheme >= 1.11.0

%description -n python-%{sname}-doc
Documentation for python-rsdclient
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pyname}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pyname}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pyname}

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst doc/source/readme.rst
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/%{pyname}-*.egg-info
%exclude %{pyver_sitelib}/%{sname}/tests

%files -n python%{pyver}-%{sname}-tests
%license LICENSE
%{pyver_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog

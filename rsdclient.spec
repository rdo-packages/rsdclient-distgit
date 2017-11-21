Name:           python-rsdclient
Version:        XXX
Release:        XXX
Summary:        OpenStack client plugin for Rack Scale Design

License:        ASL 2.0
URL:            https://github.com/openstack/%{name}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildConflicts: python2-coverage = 4.4
BuildRequires:  python2-coverage >= 4.0
BuildRequires:  python2-hacking < 0.13
BuildRequires:  python2-hacking >= 0.12.0
BuildRequires:  python2-openstackdocstheme >= 1.11.0
BuildRequires:  python2-oslotest >= 1.10.0
BuildRequires:  python2-reno >= 1.8.0
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx >= 1.6.2
BuildRequires:  python2-testrepository >= 0.0.18
BuildRequires:  python2-testtools >= 1.4.0
BuildRequires:  python2-sphinx

%description
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n     python-rsdclient
Summary:        %{summary}
 
Requires:       python2-cliff >= 2.8.0
Requires:       python2-osc-lib >= 1.7.0
Requires:       python2-pbr >= 2.0
Requires:       python2-rsd-lib >= 0.0.1
Requires:       python2-setuptools

%prep
%autosetup -n python-rsdclient
# Remove bundled egg-info
rm -rf python-rsdclient.egg-info

%build
%py2_build
# generate html docs 
sphinx-build-2 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

%check
%{__python2} setup.py test

%files -n python-rsdclient
%license LICENSE
%doc README.rst doc/source/readme.rst
%{python2_sitelib}/rsdclient
%{python2_sitelib}/python_rsdclient-%{version}-py?.?.egg-info

%files -n python-%{srcname}-doc
%doc html
%license LICENSE

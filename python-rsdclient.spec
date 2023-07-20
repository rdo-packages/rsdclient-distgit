%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1

%global sname rsdclient
%global pyname python_rsdclient

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        OpenStack client plugin for Rack Scale Design

License:        Apache-2.0
URL:            http://git.openstack.org/cgit/openstack/%{name}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n     python3-%{sname}
Summary:        %{summary}

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{sname}
This is a client for the RSD Pod Manager API, which is based on OpenStack
client framework. It provides a Python API (rsdclient/v1 module) and a RSD
specific plugin for OpenStack client (rsdclient/osc).

%package -n python3-%{sname}-tests
Summary: python-rsdclient tests
Requires: python3-%{sname} = %{version}-%{release}

%description -n python3-%{sname}-tests
Tests for python-rsdclient

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: python-rsdclient documentation

%description -n python-%{sname}-doc
Documentation for python-rsdclient
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pyname}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pyname}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pyname}

%files -n python3-%{sname}
%license LICENSE
%doc README.rst doc/source/readme.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{pyname}-*.dist-info
%exclude %{python3_sitelib}/%{sname}/tests

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog

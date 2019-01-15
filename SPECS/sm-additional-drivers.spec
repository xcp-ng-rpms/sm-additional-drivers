Summary: Additional storage drivers for sm
Name:    sm-additional-drivers
Version: 0.1.0
Release: 1
License: LGPLv2
URL: https://github.com/xcp-ng/sm-additional-drivers
Source0: https://github.com/xcp-ng/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: python
Requires: sm
Requires: xapi-core

%description
This package contains additional storage drivers for sm

%prep
%autosetup -p1

%install
install -d -m 0755 %{buildroot}/opt/xensource/sm
install -m 0755 EXT4SR.py %{buildroot}/opt/xensource/sm
pushd %{buildroot}/opt/xensource/sm
ln -s EXT4SR.py EXT4SR
popd

install -d -m 0755 %{buildroot}/etc/xapi.conf.d
touch %{buildroot}/etc/xapi.conf.d/sm-additional-drivers.conf

%triggerin -- xapi-core
# create configuration file from the whitelist in xapi.conf
WHITELIST_ORIG=$(grep /etc/xapi.conf -e "^sm-plugins=")
cat << EOF > /etc/xapi.conf.d/sm-additional-drivers.conf
# This overrides sm-plugins from xapi.conf to take additional storage drivers into account.
# This file is re-created each time either xapi-core or sm-additional-drivers is updated.
$WHITELIST_ORIG ext4
EOF

%postun
if [ $1 == 0 ]; then
    # remove .rpmsave file that could confuse xapi
    if [ -f /etc/xapi.conf.d/sm-additional-drivers.conf.rpmsave ]; then
        rm /etc/xapi.conf.d/sm-additional-drivers.conf.rpmsave
    fi
fi

%files
%doc LICENSE
/opt/xensource/sm/EXT4SR
/opt/xensource/sm/EXT4SR.py
/opt/xensource/sm/EXT4SR.pyc
/opt/xensource/sm/EXT4SR.pyo
# empty config file because it is written by scripts
# just listing it here to say we own it
%config /etc/xapi.conf.d/sm-additional-drivers.conf

%changelog
* Mon Jan 14 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.1.0-1
- Initial release with EXT4 storage driver

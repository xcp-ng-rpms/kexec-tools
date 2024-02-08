%global package_speccommit d8e6ad7d4fd95d69a463e69bb651ffd8c17029ed
%global usver 2.0.15
%global xsver 18
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v2.0.15

Name: kexec-tools
Summary: kexec/kdump userspace tools
Epoch: 1
Version: 2.0.15
Release: %{?xsrel}.0.xen417.1%{?dist}
License: GPL

Source0: kexec-tools-2.0.15.tar.gz
Source2: xs-kdump
Source3: kdump.sysconfig
Source5: kdump
Source6: kdump.service

BuildRequires: gcc
BuildRequires: xen-dom0-libs-devel, zlib-devel, systemd, autoconf, automake
%{?_cov_buildrequires}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
kexec-tools, built and packaged as part of XenServer.

%prep
%autosetup -p1
%{?_cov_prepare}

%build
./bootstrap
%configure --with-xen --without-gamecube --without-booke
%{?_cov_wrap} make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# Delete kdump
rm %{buildroot}%{_sbindir}/kdump
rm %{buildroot}%{_mandir}/man8/kdump.*

# Delete vmcore-dmesg
rm %{buildroot}%{_sbindir}/vmcore-dmesg
rm %{buildroot}%{_mandir}/man8/vmcore-dmesg.*

# Delete tests
rm %{buildroot}%{_libdir}/kexec-tools/kexec_test

mkdir -p -m755 %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p -m755 %{buildroot}%{_localstatedir}/crash
mkdir -p -m755 %{buildroot}%{_sbindir}
mkdir -p -m755 %{buildroot}%{_unitdir}

install -m 755 %{SOURCE2} %{buildroot}%{_sbindir}/xs-kdump
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/kdump
install -m 755 %{SOURCE5} %{buildroot}%{_sbindir}/kdump
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/kdump.service

%{?_cov_install}

%post
%systemd_post kdump.service

%postun
%systemd_postun kdump.service

%preun
%systemd_preun kdump.service
exit 0

%files
%{_sbindir}/kexec
%{_sbindir}/kdump
%{_mandir}/man8/kexec.*
%{_sbindir}/xs-kdump
%{_unitdir}/kdump.service

%config %{_sysconfdir}/sysconfig/kdump

%dir %{_localstatedir}/crash

%doc

%{?_cov_results_package}

%changelog
* Thu Feb 08 2024 Thierry Escande <thierry.escande@vates.tech> - 2.0.15-18.0.xen417.1
- Rebuild for Xen 4.17 test build

* Mon Feb 21 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.15-18
- CP-38416: Enable static analysis

* Tue Dec 08 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.15-17
- CP-35517: Package for koji

* Mon Jun 29 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.15-16
- CA-340173: Set umask in kdump environment

* Tue Jul 03 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.4-1.1.4
- CA-197715: Override toolchain flags that affect purgatory runtime


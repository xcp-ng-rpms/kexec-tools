%global package_speccommit 4e13e5540deace22f109e59b3c8217c23c99d17c
%global usver 2.0.29
%global xsver 8
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v2.0.29

Name: kexec-tools
Summary: kexec/kdump userspace tools
%if 0%{?xenserver} < 9
Epoch: 1
%else
Epoch: 0
%endif
Version: 2.0.29
Release: %{?xsrel}.1%{?dist}
License: GPL

Source0: kexec-tools-2.0.29.tar.gz
Source2: xs-kdump
Source3: kdump.sysconfig
Source5: kdump
Source6: kdump.service
Patch0: use-x86-64-abi.patch
Patch1: add_kexec_load_v2.patch

# XCP-ng patches
Patch1000: 0001-xen-Fix-int-to-pointer-assignment-in-do_xen_bzImage6.patch

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
* Fri Oct 02 2026 Julian Vetter <julian.vetter@vates.tech> - 2.0.29-8.1
- Sync with 2.0.29-8
- Drop the kernel_version() removal patch, included in 2.0.29
- Fix int-to-pointer assignment in do_xen_bzImage64_load(), which breaks
  the build with GCC 14 and later
- *** Upstream changelog ***
  * Mon Apr 27 2026 Andrew Cooper <andrew.cooper3@citrix.com> - 2.0.29-8
  - Rebuild against Xen 4.21

  * Mon Apr 13 2026 Frediano Ziglio <frediano.ziglio@citrix.com> - 2.0.29-7
  - CP-312109: Avoid to wait indefinitely for initilisation

  * Wed Aug 27 2025 Andrew Cooper <andrew.cooper3@citrix.com> - 2.0.29-6
  - Rebuild against Xen 4.20

  * Thu Apr 10 2025 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.29-5
  - CP-48958: Implement support for new kexec load types

  * Thu Feb 20 2025 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.29-4
  - CA-406361: Use x86-64 ABI for purgatory

  * Fri Dec 20 2024 Lin Liu <Lin.Liu01@cloud.com> - 2.0.29-3
  - CP-50546: Remove dependencies from initscripts

  * Tue Dec 03 2024 AshwinH <ashwin.h@cloud.com> - 2.0.29-2
  - CP-49883: Updated epoch conditionals based on XenServer Version

  * Mon Dec 02 2024 Lin Liu <Lin.Liu01@cloud.com> - 2.0.29-1
  - CA-383513: Switch to using the IOMMU in translated mode
  - CA-394800: upgrade kexec-tools version to fix crashdump failure

* Fri Sep 13 2024 Thierry Escande <thierry.escande@vates.tech> - 2.0.15-20.1
- Backport patch removing kernel_version(), fixing bug for kernel with
  patchlevel greater than 255

* Mon Mar 11 2024 Frediano Ziglio <frediano.ziglio@cloud.com> - 2.0.15-20
- Remove duplicate declaration causing newer toolchain to fail to compile

* Fri Jan 26 2024 Andrew Cooper <andrew.cooper3@citrix.com> - 2.0.15-19
- Rebuild against Xen 4.17

* Mon Feb 21 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.15-18
- CP-38416: Enable static analysis

* Tue Dec 08 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.15-17
- CP-35517: Package for koji

* Mon Jun 29 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.15-16
- CA-340173: Set umask in kdump environment

* Tue Jul 03 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.4-1.1.4
- CA-197715: Override toolchain flags that affect purgatory runtime


Name: kexec-tools
Summary: kexec/kdump userspace tools
Version: 2.0.4
Release: 30
License: GPL

Patch0: build-system-integration.patch
Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/%{name}/archive?at=b2b9891ce6e&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
Source2: xs-kdump
Source3: kdump.sysconfig
Source5: kdump
Source6: kdump.service

BuildRequires: xen-dom0-libs-devel, zlib-devel, systemd, autoconf, automake
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
kexec-tools, built and packaged as part of XenServer.

%prep
%autosetup -p1 -n kexec-tools-2.0.4

%build
./bootstrap
%configure --with-xen --without-gamecube --without-booke
make

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

%changelog

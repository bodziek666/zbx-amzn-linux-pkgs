Name:           fping
Version:        5.0
Release:        1%{?dist}
Summary:        fping 5.0 for Amazon Linux 2

License:        Freely redistributable without restriction
URL:            https://fping.org
Source0:        https://fping.org/dist/fping-5.0.tar.gz

Packager:       bodzioslav <https://github.com/bodzioslav>

%description
fping is a program to send ICMP echo probes to network hosts, similar to ping,
but much better performing when pinging multiple hosts. fping has a very long
history: Roland Schemers did publish a first version of it in 1992 and it has
established itself since then as a standard tool for network diagnostics and
statistics.

%prep
%setup -q

%build

# fping
%configure --enable-ipv4
make

# fping6
%configure --enable-ipv6
make
%{__mv} -f src/fping src/fping6

%install
rm -rf $RPM_BUILD_ROOT
%make_install DESTDIR="${RPM_BUILD_ROOT}"

# fping6
%{__install} -Dp -m4755 src/fping6 %{buildroot}%{_sbindir}/fping6
%{__ln_s} -f fping.8 %{buildroot}%{_mandir}/man8/fping6.8

%files
%defattr(-,root,root,-)
%attr(4755, root, root) /usr/sbin/fping
%attr(4755, root, root) /usr/sbin/fping6
%doc README.md COPYING CHANGELOG.md
/usr/share/man/man8/fping.8.gz
/usr/share/man/man8/fping6.8.gz

%post
if [ -x /usr/sbin/setcap ]; then
    /usr/sbin/setcap cap_net_raw+ep /usr/sbin/fping 
    /usr/sbin/setcap cap_net_raw+ep /usr/sbin/fping6
fi

%changelog

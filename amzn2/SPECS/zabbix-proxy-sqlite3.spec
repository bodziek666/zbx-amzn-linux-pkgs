Name:           zabbix-proxy-sqlite3
Version:        5.0.12
Release:        1%{?dist}
Summary:        Zabbix Proxy 5.0.12 for Amazon Linux 2

License:        GPLv2+
URL:            www.zabbix.com
Source0:        https://cdn.zabbix.com/zabbix/sources/stable/5.0/zabbix-5.0.12.tar.gz
Patch0:         zabbix-proxy-5.0.12-amzn2.patch

Packager:       bodzioslav <https://github.com/bodzioslav>

BuildRequires:  gcc sqlite-devel net-snmp-devel libssh2-devel libevent-devel pcre-devel openssl-devel
Requires:       OpenIPMI OpenIPMI-libs net-snmp net-snmp-libs libevent unixODBC libtool-ltdl sqlite openssl libssh2 pcre fping logrotate systemd util-linux

Requires(pre):  /usr/bin/getent /usr/sbin/useradd
Requires(post): /usr/bin/systemctl /bin/mkdir /bin/chown

Requires(preun): /usr/bin/systemctl
Requires(postun): /usr/bin/systemctl

%description
Zabbix Proxy 5.0.12 build for Amazon Linux 2

%prep
%setup -n zabbix-5.0.12
%patch0 -p1

%build

flags="
   --enable-proxy
   --with-net-snmp 
   --with-sqlite3 
   --with-ssh2 
   --with-openssl
   --sysconfdir=/etc/zabbix
"

%configure $flags 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install DESTDIR="${RPM_BUILD_ROOT}"
mkdir -p ${RPM_BUILD_ROOT}/lib/systemd/system/
install -m 755 zabbix-proxy.service ${RPM_BUILD_ROOT}/lib/systemd/system/zabbix-proxy.service
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 zabbix-proxy.logrotate ${RPM_BUILD_ROOT}/etc/logrotate.d/zabbix-proxy

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zabbix/zabbix_proxy.conf
/usr/bin/zabbix_js
/usr/sbin/zabbix_proxy
/usr/share/man/man8/zabbix_proxy.8.gz
/lib/systemd/system/zabbix-proxy.service
/etc/logrotate.d/zabbix-proxy

%pre
#getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || useradd -r -d /var/lib/zabbix -s /sbin/nologin -c "Zabbix Monitoring System" zabbix

%post
mkdir -p /var/run/zabbix
chown zabbix:zabbix /var/run/zabbix
mkdir -p /var/lib/zabbix
chown zabbix:zabbix /var/lib/zabbix
mkdir -p /var/log/zabbix
chown zabbix:zabbix /var/log/zabbix

%preun
if [ "$1" = 0 ] ; then
  /usr/bin/systemctl stop zabbix-proxy >/dev/null 2>&1
  /usr/bin/systemctl disable zabbix-proxy >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
  /usr/bin/systemctl restart zabbix-proxy >/dev/null 2>&1 || :
fi

%changelog

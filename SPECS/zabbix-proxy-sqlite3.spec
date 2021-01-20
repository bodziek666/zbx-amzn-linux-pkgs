Name:           zabbix-proxy-sqlite3
Version:        5.0.7
Release:        1%{?dist}
Summary:        Zabbix Proxy 5.0.7 for Amazon Linux 1

License:        GPLv2+
URL:            www.zabbix.com
Source0:        https://cdn.zabbix.com/zabbix/sources/stable/5.0/zabbix-5.0.7.tar.gz
Patch0:		zabbix-proxy-5.0.7.patch

Packager:	bodzioslav <https://github.com/bodzioslav>

BuildRequires:  gcc sqlite-devel net-snmp-devel libssh2-devel libevent-devel pcre-devel openssl-devel
Requires:       OpenIPMI OpenIPMI-libs net-snmp net-snmp-libs fping libevent compat-libevent unixODBC libtool-ltdl sqlite openssl logrotate util-linux

Requires(pre):  /usr/bin/getent /usr/sbin/useradd
Requires(post): /sbin/chkconfig /sbin/service /bin/mkdir /bin/chown

Requires(preun):  /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service

%description
Zabbix Proxy 5.0.7 build for Amazon Linux 1 and other systems based on CentOS/RHEL 6.

%prep
%setup -n zabbix-5.0.7
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
mkdir -p ${RPM_BUILD_ROOT}/etc/init.d/
install -m 755 zabbix-proxy.init ${RPM_BUILD_ROOT}/etc/init.d/zabbix-proxy
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
install -m 644 zabbix-proxy.sysconfig ${RPM_BUILD_ROOT}/etc/sysconfig/zabbix-proxy
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 zabbix-proxy.logrotate ${RPM_BUILD_ROOT}/etc/logrotate.d/zabbix-proxy

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zabbix/zabbix_proxy.conf
/usr/bin/zabbix_js
/usr/sbin/zabbix_proxy
/usr/share/man/man8/zabbix_proxy.8.gz
/etc/init.d/zabbix-proxy
/etc/sysconfig/zabbix-proxy
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
  /sbin/service zabbix-proxy stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-proxy >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
  /sbin/service zabbix-proxy try-restart >/dev/null 2>&1 || :
fi

%changelog


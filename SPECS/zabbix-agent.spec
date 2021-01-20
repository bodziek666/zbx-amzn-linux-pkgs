Name:           zabbix-agent
Version:        5.0.7
Release:        1%{?dist}
Summary:        Zabbix Agent 5.0.7 for Amazon Linux 1

License:        GPLv2+
URL:            www.zabbix.com
Source0:        https://cdn.zabbix.com/zabbix/sources/stable/5.0/zabbix-5.0.7.tar.gz
Patch0:		zabbix-agent-5.0.7.patch

Packager:	bodzioslav <https://github.com/bodzioslav>

BuildRequires:  gcc openssl-devel
Requires:       openssl logrotate util-linux

Requires(pre):  /usr/bin/getent /usr/sbin/useradd
Requires(post): /sbin/chkconfig /sbin/service /bin/mkdir /bin/chown

Requires(preun):  /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service

%description
Zabbix Agent 5.0.7 build for Amazon Linux 1

%prep
%setup -n zabbix-5.0.7
%patch0 -p1

%build

flags="
   --enable-agent
   --with-openssl
   --sysconfdir=/etc/zabbix
"

%configure $flags 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install DESTDIR="${RPM_BUILD_ROOT}"
mkdir -p ${RPM_BUILD_ROOT}/etc/init.d/
install -m 755 zabbix-agent.init ${RPM_BUILD_ROOT}/etc/init.d/zabbix-agent
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
install -m 644 zabbix-agent.sysconfig ${RPM_BUILD_ROOT}/etc/sysconfig/zabbix-agent
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 zabbix-agent.logrotate ${RPM_BUILD_ROOT}/etc/logrotate.d/zabbix-agent
mkdir -m 755 -p ${RPM_BUILD_ROOT}/etc/zabbix/zabbix_agentd.d

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zabbix/zabbix_agentd.conf
/etc/zabbix/zabbix_agentd.d
/usr/sbin/zabbix_agentd
/usr/bin/zabbix_get
/usr/bin/zabbix_sender
/usr/share/man/man1/zabbix_get.1.gz
/usr/share/man/man1/zabbix_sender.1.gz
/usr/share/man/man8/zabbix_agentd.8.gz
/etc/init.d/zabbix-agent
/etc/sysconfig/zabbix-agent
/etc/logrotate.d/zabbix-agent

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
  /sbin/service zabbix-agent stop >/dev/null 2>&1
  /sbin/chkconfig zabbix-agent off >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
  /sbin/service zabbix-agent try-restart >/dev/null 2>&1 || :
fi

%changelog


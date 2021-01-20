# zabbix-amzn-linux-packages
Environment and rpm SPECS for building zabbix-agent and zabbix-proxy-sqlite3 for Amazon Linux.

### Environment Preparation
```
docker build -t zbx-amzn-build .
```
### Package Building
```
docker run -v ${PWD}/SOURCES:/root/rpmbuild/SOURCES -v ${PWD}/RPMS:/root/rpmbuild/RPMS -v ${PWD}/SPECS:/root/rpmbuild/SPECS zbx-amzn-build rpmbuild -bb /root/rpmbuild/SPECS/zabbix-proxy-sqlite3.spec
```
### Create Patch
```
mkdir patch
cp zabbix-5.0.7.tar.gz patch/
tar xvzf zabbix-5.0.7.tar.gz
rm zabbix-5.0.7.tar.gz
cp -a zabbix-5.0.7 zabbix-5.0.7-orig
cp -a ../zabbix-proxy.init ../zabbix-proxy.logrotate ../zabbix-proxy.sysconfig zabbix-5.0.7/
diff -urN zabbix-5.0.7-orig zabbix-5.0.7 > ../SOURCES/zabbix-proxy-5.0.7.patch
cd ..
rm -rf patch
```
### Version Update
It requires you to provide a tarball with the new version  and replace every occurence of `zabbix-5.0.7` string with `zabbix-VERSION` in Dockerfile, SPECs and patch files.

After doing so, run package build and try to install the package inside a Docker Container. 
```
docker run -it -v $PWD/RPMS:/opt amazonlinux:2017.09-with-sources bash
rpm -qpi /opt/x86_64/zabbix-proxy-sqlite3-5.0.7-1.amzn1.x86_64.rpm
yum install zabbix-proxy-sqlite3-5.0.7-1.amzn1.x86_64.rpm
```


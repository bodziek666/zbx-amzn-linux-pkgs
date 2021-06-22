### Environment Preparation
Amazon Linux 1:
```
docker build -t amzn1-zbx-pkgs-builder ./amzn1
```
Amazon Linux 2:
```
docker build -t amzn2-zbx-pkgs-builder ./amzn2
```

### Patching Sources
For Zabbix Agent:
```
mkdir patch
cp SOURCES/zabbix-5.0.12.tar.gz patch/
cd patch
tar xvzf zabbix-5.0.12.tar.gz
rm zabbix-5.0.12.tar.gz
cp -a zabbix-5.0.12 zabbix-5.0.12-orig
cp -a ../amzn2/zabbix-agent.* zabbix-5.0.12
cp -a ../amzn2/zabbix_agentd.conf zabbix-5.0.12/conf/
diff -urN zabbix-5.0.12-orig zabbix-5.0.12 > ../SOURCES/zabbix-agent-5.0.12-amzn2.patch
cd ..
rm -rf patch
```
For Zabbix Proxy:
```
mkdir patch
cp SOURCES/zabbix-5.0.12.tar.gz patch/
cd patch
tar xvzf zabbix-5.0.12.tar.gz
rm zabbix-5.0.12.tar.gz
cp -a zabbix-5.0.12 zabbix-5.0.12-orig
cp -a ../amzn2/zabbix-proxy.* zabbix-5.0.12
cp -a ../amzn2/zabbix_proxy.conf zabbix-5.0.12/conf/
diff -urN zabbix-5.0.12-orig zabbix-5.0.12 > ../SOURCES/zabbix-proxy-5.0.12-amzn2.patch
cd ..
rm -rf patch
```

### Package Building
Zabbix Agent for Amazon Linux 2:
```
docker run -v ${PWD}/SOURCES:/root/rpmbuild/SOURCES -v ${PWD}/RPMS:/root/rpmbuild/RPMS -v ${PWD}/amzn2/SPECS:/root/rpmbuild/SPECS amzn2-zbx-pkgs-builder rpmbuild --define "debug_package %{nil}" -bb /root/rpmbuild/SPECS/zabbix-agent.spec
```
Zabbix Proxy for Amazon Linux 2:
```
docker run -v ${PWD}/SOURCES:/root/rpmbuild/SOURCES -v ${PWD}/RPMS:/root/rpmbuild/RPMS -v ${PWD}/amzn2/SPECS:/root/rpmbuild/SPECS amzn2-zbx-pkgs-builder rpmbuild --define "debug_package %{nil}" -bb /root/rpmbuild/SPECS/zabbix-proxy-sqlite3.spec
```
Fping for Amazon Linux 2:
```
docker run -v ${PWD}/SOURCES:/root/rpmbuild/SOURCES -v ${PWD}/RPMS:/root/rpmbuild/RPMS -v ${PWD}/amzn2/SPECS:/root/rpmbuild/SPECS amzn2-zbx-pkgs-builder rpmbuild --define "debug_package %{nil}" -bb /root/rpmbuild/SPECS/fping.spec
```

Zabbix Agent for Amazon Linux 1:
```
docker run -v ${PWD}/SOURCES:/root/rpmbuild/SOURCES -v ${PWD}/RPMS:/root/rpmbuild/RPMS -v ${PWD}/amzn1/SPECS:/root/rpmbuild/SPECS amzn1-zbx-pkgs-builder rpmbuild -bb /root/rpmbuild/SPECS/zabbix-agent.spec
```
Zabbix Proxy for Amazon Linux 1:
```
docker run -v ${PWD}/SOURCES:/root/rpmbuild/SOURCES -v ${PWD}/RPMS:/root/rpmbuild/RPMS -v ${PWD}/amzn1/SPECS:/root/rpmbuild/SPECS amzn1-zbx-pkgs-builder rpmbuild -bb /root/rpmbuild/SPECS/zabbix-proxy-sqlite3.spec
```

### Version Update
It requires you to provide a tarball with the new version  and replace every occurence of `zabbix-5.0.7` string with `zabbix-VERSION` in Dockerfile, SPECs and patch files.

After doing so, run package build and try to install the package inside a Docker Container. 

FROM amazonlinux:2-with-sources

# install build and runtime dependencies
RUN yum install -y OpenIPMI OpenIPMI-libs net-snmp net-snmp-libs fping libevent compat-libevent unixODBC libtool-ltdl sqlite gzip \
  sqlite-devel net-snmp-devel libssh2-devel libevent-devel pcre-devel
# install build tools
RUN yum install -y gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools
# create directory tree for RPMs: https://rpm-packaging-guide.github.io/
RUN rpmdev-setuptree 
# configure volumes, change WORKDIR to build directory tree
VOLUME ["/root/rpmbuild/SPECS", "/root/rpmbuild/RPMS", "/root/rpmbuild/SRPMS", "/root/rpmbuild/SOURCES"]
WORKDIR "/root/rpmbuild"


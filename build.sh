#!/bin/bash -e

if command -v apt-get; then
	sudo apt-get install gcc g++ git-core make libuv1-dev zlib1g-dev pkg-config \
		uuid-dev liblz4-dev libssl-dev autoconf automake
elif command -v yum; then
	sudo yum install gcc gcc-c++ git-core make libuv-devel zlib-devel pkg-config \
		libuuid-devel lz4-devel openssl-devel autoconf automake
fi

[ -d netdata ] || git clone https://github.com/sfan5/netdata-custom --depth=1 -b netdata netdata
pushd netdata

autoreconf -ivf
LDFLAGS="-s" ./configure --prefix=/opt/netdata --with-user=netdata \
	--enable-dbengine
nice make -j4

make DESTDIR="$PWD/_i" install
ver=$(cat packaging/version)
tar -cvzf "../netdata-$ver.tar.gz" -C _i --numeric-owner opt

popd
exit 0

customized Netdata
==================

[Netdata](https://www.netdata.cloud/) is pretty cool but there's one annoying thing about it: telemetry/tracking/cloud bullshit

Unfortunately these only get harder to get rid of.
In 2020 it sufficed to apply a few small tweaks to the `web` folder, but it became a big mess of React that is impossible to untangle after the fact.


This repository provides a ready-to-use version of Netdata v1.37.1 with the following removed:
* any kind of anonymous statistics
* registry / cloud functionality
* update check
* news panel

This means by default neither the Netdata server nor the web frontend will contact any third parties whatsoever.

**Build instructions**: Run `./build.sh`

Install instructions
--------------------

1. `useradd -rM -d /opt/netdata netdata`

2. Extract the build artifact

3. `mkdir -p /opt/netdata/var/{cache,lib,log}/netdata`

4. `chown netdata:netdata -R /opt/netdata/`

5. start the thing, there's a systemd service file somewhere too

Rebasing (developer-only)
-------------------------

1. Check out `dashboard` branch

2. Rebase onto https://github.com/netdata/dashboard/ (last release)

3. `npm install && npm run build`

4. `tar -cvzf dashboard.tgz --numeric-owner build/` and tag & upload to the 'temp' [release](https://github.com/sfan5/netdata-custom/releases)

5. Check out `netdata` branch

6. Rebase onto https://github.com/netdata/netdata/ (last release) *except* "pull new dashboard" commit

7. Run `./web/gui/bundle_dashboard.py` and commit result

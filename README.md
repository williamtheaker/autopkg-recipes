# AutoPkg recipes

This repo contains [AutoPkg](https://github.com/autopkg/autopkg) recipes used to package and deploy software. Unless otherwise noted, these recipes are available under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)

## Recipes

* Asix **.download** and **.munki** recipes grab the latest version of drivers for AX88179 ethernet adapters, such as StarTech USB31000S.
* Cinc **.download** and **.munki** recipes grab the latest version of [Cinc](https://cinc.sh/).
* Gravitational Teleport **.download** and **.munki** recipes grab the latest version of [Teleport](https://gravitational.com/teleport/).
* Krita **.download** and **.munki** recipes grab the latest version of [Krita](https://krita.org).
* Nessus  **.download** and **.munki** recipes to grab the latest version of the macOS Tenable Nessus Agent.
* OBS  **.download** and **.munki** recipes to grab the latest version of [OBS](https://obsproject.com).
* SensibleSideButtons **.download** and **.munki** recipes to grab the latest version of SensibleSideButtons. Requires a Github API token stored at `~/.autopkg_gh_token`.
* Tuple **.download** and **.munki** recipes to grab the latest version of [Tuple](https://tuple.app).
* ZoomIT **.download** and **.munki** adopted from <https://github.com/ChefAustin/chefaustin-recipes/>
* Zscaler **.download**, **.pkg**, and **.munki** recipes download the requested version of Zscaler Client Connector. Ideally it would download the latest version each run, but Zscaler doesn't publish the version number in a public format and scraping the release notes doesn't work since they don't match the build version.

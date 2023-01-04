# Zscaler recipes

Original recipes forked from [rtrouton-recipes](https://github.com/autopkg/rtrouton-recipes/tree/master/Zscaler).

Change the `DESIRED_VERSION` input variable to match the version to download. As long as Zscaler doesn't change the Cloudfront CDN URL this should continue to work. Please open a PR or file an issue if/when it doesn't.

There are two Munki recipes - one which installs the generated package and one which doesn't. The only advantage of installing the Zscaler package is a resulting installs array in the Munki pkginfo. If receipt based install logic is enough in your scenario, use `Zscaler.munki.recipe`, otherwise consider `Zscaler-Install.munki.recipe`. In situations where Autopkg is run ephemerally within CI, this install only adds a trivial amount of time. There may be other considerations when running Autopkg on a static box.

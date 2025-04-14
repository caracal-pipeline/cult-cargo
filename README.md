# cult-cargo
Curated Stimela2 cargo for popular radio astronomy software. See [Image manifest](./bundle-manifest.md) for available images.

## Regular userland install

```
pip install cult-cargo
```

This installs both cult-cargo and the required version of stimela.

## Poweruser install

To work off the repo versions:

```
# activate your virtualenv
$ pip install -U pip
$ gh repo clone caracal-pipeline/stimela
$ gh repo clone caracal-pipeline/cult-cargo
$ pip install -e stimela
$ pip install -e cult-cargo
```

## Sample recipe

```yml
#!/usr/bin/env -S stimela run -l
_include: 
  - (cultcargo)wsclean.yml

dummy-recipe:
  info: a dummy recipe
  steps:
    image:
      cab: wsclean
```

## Overriding image versions

By default, cult-cargo will use the [image versions](./bundle-manifest.md) designated as latest in its [cargo manifest](https://github.com/caracal-pipeline/cult-cargo/blob/master/cultcargo/builder/cargo-manifest.yml). These versions are always called ``ccX.Y.Z``, where X.Y.Z is the cult-cargo release.

You can select a different image version on a per-cab basis as follows:

```yml
#!/usr/bin/env -S stimela run -l
_include: 
  - (cultcargo)wsclean.yml

cabs: 
  wclean:
    image:
      version: 2.10.1-kern7-cc0.2.0

dummy-recipe:
  info: a dummy recipe
  steps:
    image:
      cab: wsclean
```

## Cab developers install

```
$ poetry install --with builder
```

This makes the ``build-cargo.py`` script available. The script is preconfigured to read ``cultcargo/builder/cargo-manifest.yml``, which describes the images that must be built.

``build-cargo.py -a`` will build and push all images, or specify an image name to build a particular one. Use ``-b`` to build but not push, or ``-p`` for push-only. Use ``-l`` to list available images.

The ``cultcargo`` folder contains YaML files with cab definitions.

If you would like to maintain your own image collection, write your own manifest and Dockerfiles following the cult-cargo example, and use the ``build-cargo.py`` script to build your images.

## Using cult-cargo as a standalone image repository

You don't even need to run stimela (or indeed install anything) to take advantage of the images packaged with cult-cargo. The [image manifest](./bundle-manifest.md) will provide a concise version, or else take a look at the image repository on https://quay.io/organization/stimela2. 

For example, if you want to run a wsclean image, just do:

```
$ singularity build wsclean-3.3.sif docker:quay.io/stimela2/wsclean:3.3-cc0.2.0
$ singularity exec wsclean-3.3.sif wsclean 
```

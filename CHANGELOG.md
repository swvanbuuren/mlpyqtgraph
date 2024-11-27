# CHANGELOG

## v0.6.2 (2024-11-27)

### Bug Fixes

* Correct defintion of line colors for 2d axes ([`4df55b6`](https://github.com/swvanbuuren/mlpyqtgraph/commit/4df55b604348f9b90ebf81871b88e956537cecfd))

### Chores

* Add support for python v3.12 ([`2fef80e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/2fef80e640a0546f89783a9ced708f57bab64a86))

### Code Style

* Remove unnecessary linebreaks ([`0ec47d1`](https://github.com/swvanbuuren/mlpyqtgraph/commit/0ec47d1e5f7706af588c832fd11f9c11caec03a6))

* Update ruff linting rules ([`946832b`](https://github.com/swvanbuuren/mlpyqtgraph/commit/946832b21c4ed1903b792ee21d35ce76114918f8))

* Switch to ruff as linter, including rules ([`2669ded`](https://github.com/swvanbuuren/mlpyqtgraph/commit/2669dede05705df6a43980b47f5fe388062e9985))

### Continuous Integration

* Switch to docker container for testing and linting ([`ac2a29c`](https://github.com/swvanbuuren/mlpyqtgraph/commit/ac2a29cc4b20fb945c18a3dc263d6d5569dc9316))

* Include basic testing running and drop python v3.12 support ([`68d9df9`](https://github.com/swvanbuuren/mlpyqtgraph/commit/68d9df9eb3ee102a2361dcd715976d2b789ac70f))

### Documentation

* Update year in license text ([`55329ad`](https://github.com/swvanbuuren/mlpyqtgraph/commit/55329ad3a31c7d72dc53c0adb923c05902fce865))

* Update to align with new config options setup ([`7b8770a`](https://github.com/swvanbuuren/mlpyqtgraph/commit/7b8770ac3a53ad03e42b3caf000b7a6bad029376))

### Refactoring

* Simplify plot3 and surf examples ([`d7d48b0`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d7d48b0f2f01dd265c5a31eece2758027f07110a))

* Line and surface gl options in 3d axis ([`cc9b6c6`](https://github.com/swvanbuuren/mlpyqtgraph/commit/cc9b6c6ced8d73ce171301c87ad76b2d0a0b0ef5))

* Simplified configuration options naming ([`496031a`](https://github.com/swvanbuuren/mlpyqtgraph/commit/496031a3ae8e23223ae641cc6e9aebfeba0d729f))
## v0.6.1 (2024-11-10)

### Bug Fixes

* Add missing required method for 2d plotting ([`f5d2d4e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f5d2d4e4b49a1598cfff77e2c1b9f5a180d9884f))

### Documentation

* Add info and resolution for missing xcb plugin error ([`0ddb6a1`](https://github.com/swvanbuuren/mlpyqtgraph/commit/0ddb6a1224988e669c3a075de713adb32f22f6c9))

### Testing

* Setup basic testing ([`fe61dad`](https://github.com/swvanbuuren/mlpyqtgraph/commit/fe61dadd0059a5dafc652f28a0f0574c404ebdfe))
## v0.6.0 (2024-11-09)

### Features

* Add azimuth and elevation properties for 3d axis ([`13f2631`](https://github.com/swvanbuuren/mlpyqtgraph/commit/13f263142ea342af6bba738ba764b916e8c4cfef))

### Refactoring

* Remove orthographic plot of surface example ([`121b890`](https://github.com/swvanbuuren/mlpyqtgraph/commit/121b8902a6204113e134ff127efcd52881dbe7d2))

* Change view angle of arctan2 example ([`9e53c24`](https://github.com/swvanbuuren/mlpyqtgraph/commit/9e53c24787455a8a4056ab1401d03438bce1b61e))
## v0.5.0 (2024-11-09)

### Features

* Add plot3 functionality including example ([`4fa0510`](https://github.com/swvanbuuren/mlpyqtgraph/commit/4fa0510e8b3f4362333fda9c7c3b7b64ef8ab7af))
## v0.4.0 (2024-11-09)

### Chores

* Update python semantic release version and naming ([`fb72583`](https://github.com/swvanbuuren/mlpyqtgraph/commit/fb72583459761ee413289f1e077277d7a11383b2))

* Make sure commit subjects start with a capital ([`5cc9249`](https://github.com/swvanbuuren/mlpyqtgraph/commit/5cc92491cff83d8a3302984f89071343c9bd7e5e))

### Code Style

* Improve readability of full plot example ([`7ff201a`](https://github.com/swvanbuuren/mlpyqtgraph/commit/7ff201ac631d4185a69b7ec144a09eb0f7672495))

### Features

* Add arctan2 example ([`513589a`](https://github.com/swvanbuuren/mlpyqtgraph/commit/513589a75ff32b44df9c36d5cb9e57f2ae64aeef))
## v0.3.1 (2024-11-08)

### Bug Fixes

* Change signal/slot timeout to 10 seconds ([`375f9d0`](https://github.com/swvanbuuren/mlpyqtgraph/commit/375f9d0e71b238924d6fa7e7b1e2594b67875dfc))

### Chores

* Change template location for semantic release ([`9d320c1`](https://github.com/swvanbuuren/mlpyqtgraph/commit/9d320c1b0ca7acfd4c39433137fef6063e7ea89a))

* Update templates for genearing the changelog and release notes ([`cad4364`](https://github.com/swvanbuuren/mlpyqtgraph/commit/cad43649c37355ed84e7f0c37e9071e7d9d3e06a))

* Add custom templates for changelog and release notes ([`ffe32c8`](https://github.com/swvanbuuren/mlpyqtgraph/commit/ffe32c8d704d719480de011d996922f0ebae07de))

* Ignore venv and uv artifacts ([`724674e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/724674e9d36c43af1a84889355442cdf4a366c2b))

### Documentation

* Mention usage of pqthreads in documentation and readme ([`d276c68`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d276c689311fdcc53cd2fca286f556753f723352))

* Add introduction link and getting started to readme ([`6f40d91`](https://github.com/swvanbuuren/mlpyqtgraph/commit/6f40d91bb356f7aac637e5d627c9ad574a82635e))

* Add copy button to code blocks ([`c99063c`](https://github.com/swvanbuuren/mlpyqtgraph/commit/c99063c1101721043051ccc1c1e88f0fb95df669))
## v0.3.0 (2024-11-03)

### Chores

* Add naming to github actions workflows ([`1fd272c`](https://github.com/swvanbuuren/mlpyqtgraph/commit/1fd272c647f92c539ca020e84e7ea2bcf62e23c6))

### Documentation

* Fix link to installation page ([`6f41c1f`](https://github.com/swvanbuuren/mlpyqtgraph/commit/6f41c1f7f5ca2cf7a2c39bb36e5038f25ae814bc))

* Fix links and typos in documentation ([`517ae15`](https://github.com/swvanbuuren/mlpyqtgraph/commit/517ae154b340cc9ff60cdaeb7be5928e98532609))

### Features

* Add 3d axis grid with automatic tick labels to surf plots ([`ee5a6fb`](https://github.com/swvanbuuren/mlpyqtgraph/commit/ee5a6fbc8423392360c62338c8357ba22f2f9f96))
## v0.2.0 (2024-08-20)

### Documentation

* Include pypi package in installation instructions ([`f514ec1`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f514ec179daa10414a077025876382ab2d03e335))

### Features

* Add more festures to full 2d plot example ([`55c54f4`](https://github.com/swvanbuuren/mlpyqtgraph/commit/55c54f410f34eaf369357edeeb3758301e22efdc))
## v0.1.0 (2024-08-19)

### Bug Fixes

* Align with latest pqthreads version ([`da98f7e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/da98f7e9f18e14cf22f5f0a9369628a02ed6dc3f))

### Chores

* Move to pyproject.toml setup ([`d52221e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d52221ec07ebc6708653baec8d746acbb4cf684e))

### Documentation

* Fix typo on welcome page ([`5069356`](https://github.com/swvanbuuren/mlpyqtgraph/commit/5069356916a23558427732bf8f1dd9beebaedc69))

* Link explicitely to page w/ installation instructions ([`f17b61f`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f17b61f0ccfa95976ea482eea317e09ec2222cf8))

* Change all documentation links to gh pages ([`af48cab`](https://github.com/swvanbuuren/mlpyqtgraph/commit/af48cabdd4bacb58a572a0a1e55eedc5463717fc))

* Move documentation to mkdocstrings hosted on github pages ([`1426d1a`](https://github.com/swvanbuuren/mlpyqtgraph/commit/1426d1a3ae8cf6e1007b102a02199986d9d80a98))

### Features

* Add semantic release management and publishing to pypi ([`5a44c92`](https://github.com/swvanbuuren/mlpyqtgraph/commit/5a44c9231df5848f7092a3c263075ccad197e82b))

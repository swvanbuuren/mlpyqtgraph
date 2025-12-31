# CHANGELOG

## v0.7.0 (2025-12-31)

### Bug Fixes

* Elevation angle range limits ([`86d27eb`](https://github.com/swvanbuuren/mlpyqtgraph/commit/86d27eb05d84cb9d1c925ea69f97c8dc56b70ad5))

### Chores

* Bump python versions for testing and linting ([`a1ca694`](https://github.com/swvanbuuren/mlpyqtgraph/commit/a1ca694157441290eb1c79ebdc13a351cbb06b65))

* Explicitely set pyopengl version ([`c9dd160`](https://github.com/swvanbuuren/mlpyqtgraph/commit/c9dd160a2dfb690ec5f245f3b85dbb784e235cde))

* Bump pqthreads, pyqtgraph and python versions ([`f39ee2b`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f39ee2b5e1ca1728922110cd361451f33801f5fc))

### Features

* Configurable 3d axes aspect ratio ([`38a9843`](https://github.com/swvanbuuren/mlpyqtgraph/commit/38a984369889c48ab1e9b924dad9be15ceae420c))

* Pass other kwargs to glaxis and glgridplane ([`1a91b66`](https://github.com/swvanbuuren/mlpyqtgraph/commit/1a91b666b00950b60a7e20fb726c42793985c03a))

* Support differing tick label and position ([`966c240`](https://github.com/swvanbuuren/mlpyqtgraph/commit/966c2402ece31c6ff085855ad2676932d768a4bd))

* Support dark mode and only create labels when needed ([`714fe99`](https://github.com/swvanbuuren/mlpyqtgraph/commit/714fe99bf3a9142d4cb3bd68e392e55f09c5e307))

### Refactoring

* Improve imports ([`6fd199e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/6fd199e19e711a04a2e0bdfa7d4237a167fd0fac))

* Raise custom error for inconsistent coords ([`45d9ac3`](https://github.com/swvanbuuren/mlpyqtgraph/commit/45d9ac3070568d0e3010dca98e6560ff31e10906))

* Consistent naming of glaxis arguments ([`8b41d74`](https://github.com/swvanbuuren/mlpyqtgraph/commit/8b41d74d852c65170f258b220c1a144317786ced))

* Add docstring and refactor glgridaxis ([`33ec817`](https://github.com/swvanbuuren/mlpyqtgraph/commit/33ec817a53a91a1b64f4e6912a2b7f2e8c0096ed))

* Use indices for axes consistently ([`0efcf70`](https://github.com/swvanbuuren/mlpyqtgraph/commit/0efcf70e8cc3253f5bbede860be8000c24374849))

* Get rid of glaxis axisspecs and config only in glgridaxis ([`abc7f77`](https://github.com/swvanbuuren/mlpyqtgraph/commit/abc7f777fa231fe5ec00da3c642f03f8d6f6329e))

* Extend axisspecs to simplify glaxis code ([`a5aed55`](https://github.com/swvanbuuren/mlpyqtgraph/commit/a5aed55154e3c6f8dfd088ccb6f49e1347705a3e))

* Store alignment in axis_specs ([`a88df51`](https://github.com/swvanbuuren/mlpyqtgraph/commit/a88df5171deea330bde0deaa011d384c9f1501dd))

* Make glaxis more concise using a dataclass ([`d28b012`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d28b0124b98a07227168c8a78a318dba4fc2062d))

* Glaxis refactoring ([`284091a`](https://github.com/swvanbuuren/mlpyqtgraph/commit/284091a60af452d747e0714fc4b074e611370a89))

* Simplify glgridaxis code ([`cb4177e`](https://github.com/swvanbuuren/mlpyqtgraph/commit/cb4177e96fb7664cbdd5655fceeb1830f3293459))

* Simplify grid and axis generators in glgridaxis ([`f109fdd`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f109fdd14aefc23c0a2f1c7749dc0d81794ac684))

* Move plot responsibilities from glgridaxis into child glgraphicsitem's ([`75183f3`](https://github.com/swvanbuuren/mlpyqtgraph/commit/75183f35a3351d26fff9d4260d8325559fc5f920))

* Refactor and simplify grid_axes ([`6945932`](https://github.com/swvanbuuren/mlpyqtgraph/commit/69459325e0505d4cda4b9c8518f5867e0ca2d759))

* Align axes module with upstream changes ([`4cf618b`](https://github.com/swvanbuuren/mlpyqtgraph/commit/4cf618b0be782851fff2f5bba704062c0ce9a235))

* Use upstream glsurfaceplotitem surface plotter ([`555b3f3`](https://github.com/swvanbuuren/mlpyqtgraph/commit/555b3f3d309e94b4bb19b5a1f1e69b45345463d6))

### Testing

* 3d axes aspect ratio and projection in examples ([`9ca1d4c`](https://github.com/swvanbuuren/mlpyqtgraph/commit/9ca1d4ce8d15f44dc44c798ebd8bd4be953f96ef))

* Improve grid_axes test ([`3f84e24`](https://github.com/swvanbuuren/mlpyqtgraph/commit/3f84e2469dc28b4751c8e88b9aa85a2d06be664b))

* Add simplie gridaxis change test ([`ce00044`](https://github.com/swvanbuuren/mlpyqtgraph/commit/ce000441707617094718b159b6056e98b583dca0))
## v0.6.3 (2025-02-26)

### Bug Fixes

* Avoid redrawing 3d grid axes all the time ([`d05e8c5`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d05e8c5266fa153c10a521b5bedd8163dc3f8a6a))

### Chores

* Increase python and pyqtgraph version demands ([`625bed5`](https://github.com/swvanbuuren/mlpyqtgraph/commit/625bed5b1301a8ad45a6c628ae6066256e2039c5))

* Change pre-commit hooks directory ([`6d5a1cf`](https://github.com/swvanbuuren/mlpyqtgraph/commit/6d5a1cfdd95d1e7cf442d8885b24de6eec9531f7))

* Add pre-commit hooks with config instructions ([`d2567cd`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d2567cdd2925f282c8cf682460add9f6e475328e))

* Ignore ruff_cache directory ([`ea659c8`](https://github.com/swvanbuuren/mlpyqtgraph/commit/ea659c85e027b8e99c549dcbf4b4e88d523a79a3))

### Code Style

* Fix ruff linter warning ([`0123ae3`](https://github.com/swvanbuuren/mlpyqtgraph/commit/0123ae3cd1fffe24efdb9f8988dcc8d53edc0b47))

* Add ruff exception for axis2d ([`0add750`](https://github.com/swvanbuuren/mlpyqtgraph/commit/0add750cb47fea31a118b7dacf3fae3553070742))

* Add missing linebreaks ([`12a81da`](https://github.com/swvanbuuren/mlpyqtgraph/commit/12a81da6b7ed6af1325cf3df6759f1bd094cb25c))

### Testing

* Set default pytest arguments ([`cd0bcc8`](https://github.com/swvanbuuren/mlpyqtgraph/commit/cd0bcc8c535c3b0d352527ac20282523f025767f))

* Add test usage of decorator options ([`16f5a7b`](https://github.com/swvanbuuren/mlpyqtgraph/commit/16f5a7b443997e927c91c5535491785beffa56e0))
## v0.6.2 (2024-11-27)

### Bug Fixes

* Correct defintion of line colors for 2d axes ([`3fb95b0`](https://github.com/swvanbuuren/mlpyqtgraph/commit/3fb95b0149b11d38c4caca9ad533ecf9782cda8e))

### Chores

* Add support for python v3.12 ([`2dd1b0f`](https://github.com/swvanbuuren/mlpyqtgraph/commit/2dd1b0f96dbca0e6977801d6fae4a362b399444a))

### Code Style

* Remove unnecessary linebreaks ([`f3f87e7`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f3f87e7078e1f880272fbf3fa7c690b51b6f5683))

* Update ruff linting rules ([`d60bf20`](https://github.com/swvanbuuren/mlpyqtgraph/commit/d60bf20cb6e02ef1099e5fc0e1e58d7c0c221ff4))

* Switch to ruff as linter, including rules ([`afef229`](https://github.com/swvanbuuren/mlpyqtgraph/commit/afef22983ab59225dbfd782d09055bae844f49a1))

### Continuous Integration

* Switch to docker container for testing and linting ([`4e7f55c`](https://github.com/swvanbuuren/mlpyqtgraph/commit/4e7f55c76aea821bb5fe8242a1ac2161aca106cf))

* Include basic testing running and drop python v3.12 support ([`f130c00`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f130c004f24c3db23ccdaf8b4a1041d70a19360b))

### Documentation

* Update year in license text ([`f1217f5`](https://github.com/swvanbuuren/mlpyqtgraph/commit/f1217f5f344cda236fb7a6662a5f10294fea4400))

* Update to align with new config options setup ([`9ca7026`](https://github.com/swvanbuuren/mlpyqtgraph/commit/9ca7026cf09e8c97d4d9543aa52a3ec5fb396ac3))

### Refactoring

* Simplify plot3 and surf examples ([`8ac2863`](https://github.com/swvanbuuren/mlpyqtgraph/commit/8ac2863ea1f809a7a9d8ab0abf7e693fbbd4ae6f))

* Line and surface gl options in 3d axis ([`517c6c5`](https://github.com/swvanbuuren/mlpyqtgraph/commit/517c6c5968ec50bd5042f702d26fe685f2694297))

* Simplified configuration options naming ([`a816a43`](https://github.com/swvanbuuren/mlpyqtgraph/commit/a816a43bf0e3d97a1b0eef896ea6c43bf96970d9))

* Remove unnecessary print statement ([`6ad4643`](https://github.com/swvanbuuren/mlpyqtgraph/commit/6ad46436fa4fd68e146ee9f82999017f8ec65c53))
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

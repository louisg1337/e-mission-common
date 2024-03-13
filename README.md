# e-mission-common library

This library contains code that can be used by multiple e-mission components including [e-mission-server](https://github.com/e-mission/e-mission-server), [e-mission-phone](https://github.com/e-mission/e-mission-phone), [em-public-dashboard](https://github.com/e-mission/em-public-dashboard), and [op-admin-dashboard](https://github.com/e-mission/op-admin-dashboard).

This repository uses the [Transcrypt](https://www.transcrypt.org/) library to compile Python code to JavaScript. This allows us to write and maintain code in 1 language and import it for using in all 4 projects.

## To contribute

1. Make your changes to Python code under the `src` directory.
2. Run `compile_to_js.sh` to build the JavaScript. This will produce output JS files in the `__js__` directory.
3. Commit your changes from both the `src` and `__js__` directories.

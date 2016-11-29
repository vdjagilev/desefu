Changelog
=========

# 0.3

* [Fix]: Output log file fixes
* [CI]: Python 3.4 continuous integration result
* SqliteDatabase module: More verbose output if table information could not be fetched

# 0.2

* Dictionary module fixes. Perform a search in different encoding.
* Title option for each module (useful in export)
* Changed the way result data is saved. Using JSON library `jsonpickle`
* SQLite module full implementation and unit tests
* Other minor bugfixes and improvements

# 0.1

Initial version of application which contains basic search and extract functionality.

* Module chains (list of modules)
* Modules which can have module chain (submodules)
* File filtering
* Data collection
* Export result (JSON format)

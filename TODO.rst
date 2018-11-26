ToDo
=====

Tasks
-----

* Prune the tools dir.

* Imporove error reporting.

  * Log the commands and filenames with rst markup errors.

  * Document or overcome the discrepancies. **Ex:** Function helps could not have headings.

* Take care of sphinx version collision. There might be multiple versions of sphinx which could cause problems like missing themes.

* Adding sphinx.ext.napoleon.

* Handle indentation inside the comments of the tasks properly, so that they tail the existing documentation, rather than being indented as a sub-section.

Check
-----

* Using absolute paths like rst's **include** directive, instead of autodoc styled imports. Beware of module path collisions.

Issues
------

* An error is raised when the doctstrings have a title.

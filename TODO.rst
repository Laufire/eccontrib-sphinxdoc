ToDo
=====

Tasks
-----

* The package isn't installable from PyPI, as it's requirements aren't specified properly in setup.py.

* Take care of sphinx version collision. There might be multiple versions of sphinx which could cause problems like missing themes.

* Adding sphinx.ext.napoleon.

* Log the filenames with rst markup errors.

* Handle indentation inside the comments of the tasks properly, so that they tail the existing documentation, rather than being indented as a sub-section.

Check
-----

* Using absolute paths like rst's **include** directive, instead of autodoc styled imports. Beware of module path collisions.

Issues
------

* An error is raised when the doctstrings have a title.

sphinxdoc
=========
A sphinx extension for documenting ec based scripts.

Installation
------------
At the command line::

    $ pip install eccontrib-sphinxdoc


Or download the source from `github <https://github.com/Laufire/eccontrib-sphinxdoc>`_, extract it and run::

    $ python setup.py install

Usage
-----

#) Like any other sphinx extension, add **sphinxdoc** to the **conf.extensions**. And add the paths of the scripts to **sys.path**.
	In **conf.py** add:

	.. code:: python

		extensions.append('eccontrib.sphinxdoc')

		sys.path.insert(0, os.path.abspath("scripts/examples"))

#) Add the **ec_module** directive to some rst file to document ec based scripts.

	In **tasks.rst** add:

	.. code:: rst

		Nutshell
		--------

		.. ec_module:: nut_shell


	**Note:** There should be a newline or more options after rst directives for them to work

#) Follow these with a regular sphinx build.

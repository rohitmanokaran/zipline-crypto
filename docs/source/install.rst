.. _install:

Installation
============

You can install Zipline either using `pip <https://pip.pypa.io/en/stable/>`_, the Python package installer.

Zipline runs on Python 3.10+. To install and use different Python versions in parallel as well as create
a virtual environment, you may want to use `pyenv <https://github.com/pyenv/pyenv>`_.

Installing with ``pip``
-----------------------

Installing Zipline via ``pip`` is slightly more involved than the average Python package.

There are two reasons for the additional complexity:

1. Zipline ships several C extensions that require access to the CPython C API.
   In order to build these C extensions, ``pip`` needs access to the CPython
   header files for your Python installation.

2. Zipline depends on `NumPy <https://www.numpy.org/>`_, the core library for
   numerical array computing in Python.  NumPy, in turn, depends on the `LAPACK
   <https://www.netlib.org/lapack>`_ linear algebra routines.

Because LAPACK and the CPython headers are non-Python dependencies, the correct
way to install them varies from platform to platform.

Once you've installed the necessary additional dependencies (see below for
your particular platform), you should be able to simply run (preferably inside an activated virtual environment):

.. code-block:: bash

   $ pip install zipline-crypto

If you use Python for anything other than Zipline, we **strongly** recommend
that you install in a `virtualenv
<https://virtualenv.readthedocs.org/en/latest>`_.  The `Hitchhiker's Guide to
Python`_ provides an `excellent tutorial on virtualenv
<https://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

GNU/Linux
~~~~~~~~~

Dependencies
''''''''''''

On `Debian-derived`_ Linux distributions, you can acquire all the necessary
binary dependencies from ``apt`` by running:

.. code-block:: bash

   $ sudo apt install libatlas-base-dev python-dev gfortran pkg-config libfreetype6-dev hdf5-tools

On recent `RHEL-derived`_ derived Linux distributions (e.g. Fedora), the
following should be sufficient to acquire the necessary additional
dependencies:

.. code-block:: bash

   $ sudo dnf install atlas-devel gcc-c++ gcc-gfortran libgfortran python-devel redhat-rpm-config hdf5

On `Arch Linux`_, you can acquire the additional dependencies via ``pacman``:

.. code-block:: bash

   $ pacman -S lapack gcc gcc-fortran pkg-config hdf5

There are also AUR packages available for installing `ta-lib
<https://aur.archlinux.org/packages/ta-lib/>`_.
Python 3 is also installable via:

.. code-block:: bash

   $ pacman -S python3

Compiling TA-Lib
'''''''''''''''''
You will also need to compile the `TA-Lib <https://www.ta-lib.org/>`_ library for technical analysis so its headers become available.

You can accomplish this as follows:

.. code-block:: bash

   $ wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   $ tar -xzf ta-lib-0.4.0-src.tar.gz
   $ cd ta-lib/
   $ sudo ./configure
   $ sudo make
   $ sudo make install

This will allow you to install the Python wrapper with ``pip`` as expected by the binary wheel.

.. _`Debian-derived`: https://www.debian.org/derivatives/
.. _`RHEL-derived`: https://en.wikipedia.org/wiki/Red_Hat_Enterprise_Linux_derivatives
.. _`Arch Linux` : https://www.archlinux.org/
.. _`Hitchhiker's Guide to Python` : https://docs.python-guide.org/en/latest/
.. _`Homebrew` : https://brew.sh

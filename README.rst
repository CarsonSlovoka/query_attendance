==========================================================
Query Attendance
==========================================================

.. sectnum::

This script helps you quickly query your attendance record, but only work for some specific people!

----


:Source Code: https://github.com/CarsonSlovoka/query_attendance/blob/master/query_attendance.py
:Dependencies: `selenium`_ and `chromedriver.exe`_.
:Compatible with: Python >3.6
:Download EXE: `LINK <https://github.com/CarsonSlovoka/query_attendance/raw/master/dist/app.query_attendance.zip>`_
:Platform: Windows
:Browser: Chrome
:License: `Apache 2.0`_
:Author Document: https://carsonslovoka.github.io/CarsonDoc/

----

USAGE
================

Open ``config.ini`` add set your ``username``, ``password`` and ``URL`` on it.

That should be something like this::

    [Required]
    username = 1234
    password = A123456789

    # If you are `specific people` then you will know what value should set
    URL = https://...


For Programmer
================

If you want to modify by yourself, see below:


prepared
---------------

1.  `chromedriver.exe <https://chromedriver.chromium.org/downloads>`_
#. put ``chromedriver.exe`` to {executable}/Scripts/  (or modify source code)

.. _`chromedriver.exe`: https://chromedriver.chromium.org/downloads
.. _`selenium`: https://pypi.org/project/selenium/
.. _`Apache 2.0`: https://github.com/CarsonSlovoka/query_attendance/blob/master/LICENSE
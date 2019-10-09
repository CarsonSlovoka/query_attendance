==========================================================
Query Attendance
==========================================================

.. sectnum::

This script helps you quickly query your attendance record, but only work for some specific people.

----

:Homepage: https://carsonslovoka.github.io/CarsonDoc/
:Code: https://github.com/CarsonSlovoka/query_attendance/blob/master/query_attendance.py
:Dependencies: `selenium`_ and `chromedriver.exe`_.
:Compatible with: Python >3.6
:Download EXE:
:License: `Apache 2.0`_

----

USAGE
================

Open ``config.ini`` add set your username and password on it.

That should be something like this::

    [Required]
    username = 1234
    password = A123456789


For Programmer
================

If you want to modify by yourself, see below:


prepared
---------------

1.  `chromedriver.exe <https://chromedriver.chromium.org/downloads>`_
#. put ``chromedriver.exe`` to {executable}/Scripts/  (or modify source code)

Source code
---------------

1. open query_attendance.py 
#. assign URL path to the variable of DYNA_EMPLOYEE (If you are `specific people` then you will know what value should set)



.. _`chromedriver.exe`: https://chromedriver.chromium.org/downloads
.. _`selenium`: https://pypi.org/project/selenium/
.. _`Apache 2.0`: https://github.com/CarsonSlovoka/query_attendance/blob/master/LICENSE
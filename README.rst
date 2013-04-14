====
abpy
====
-----------------------------------------------------------
Python parser/interpreter for `Adblock Plus filter format`_
-----------------------------------------------------------
.. _Adblock Plus filter format: http://adblockplus.org/en/filters

::

   from abpy import Filter
   f = Filter(file('easylist.txt'))
   f.match(url)



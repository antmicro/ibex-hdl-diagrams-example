.. Ibex HDL Diagrams Example documentation master file, created by
   sphinx-quickstart on Thu Sep 17 16:15:03 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ibex HDL Diagrams Example
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Netlistsvg Diagram
------------------

.. code-block:: rst

   .. hdl-diagram:: generated/ibex.v
      :type: netlistsvg
      :module: ibex_core

.. hdl-diagram:: generated/ibex.v
   :type: netlistsvg
   :module: ibex_core

Yosys BlackBox Diagram
----------------------

.. code-block:: rst

   .. hdl-diagram:: generated/ibex.v
      :type: yosys-blackbox
      :module: ibex_core

.. hdl-diagram:: generated/ibex.v
   :type: yosys-blackbox
   :module: ibex_core

Yosys AIG Diagram
-----------------

.. code-block:: rst

   .. hdl-diagram:: generated/ibex.v
      :type: yosys-aig
      :module: ibex_core

.. hdl-diagram:: generated/ibex.v
   :type: yosys-aig
   :module: ibex_core

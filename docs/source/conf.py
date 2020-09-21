# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Ibex HDL Diagrams Example'
copyright = '2020, Antmicro'
author = 'Antmicro'

# The full version, including alpha/beta/rc tags
release = '0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib_hdl_diagrams'
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# -- Generate ibex sources ----------------------------------------------------

import os
import shutil
import subprocess
from yaml import load, Loader


IBEX_BUILD_DIR = os.path.realpath("../build/ibex")
IBEX_DIR = os.path.realpath("../../third_party/ibex")

DIAGRAM_YOSYS_SCRIPT = os.path.join(IBEX_BUILD_DIR, "diagram.tcl")

GENERATED_DIR = os.path.realpath("./generated")
OUT_VERILOG = os.path.join(GENERATED_DIR, "ibex.v")


def generate_ibex_sources():
    shutil.rmtree(IBEX_BUILD_DIR, ignore_errors=True)
    os.makedirs(IBEX_BUILD_DIR, exist_ok=True)

    generate_cmd = "cd {generate_dir}; \
        fusesoc --cores-root={ibex_dir} run \
            --target=synth \
            --setup \
            lowrisc:ibex:top_artya7 \
                --part xc7a35ticsg324-1L".format(
        generate_dir=IBEX_BUILD_DIR,
        ibex_dir=IBEX_DIR,
    )

    subprocess.run(generate_cmd, shell=True)


def create_input_verilog():
    ibex_srcs = list()
    ibex_inc = list()

    SYNTH_DIR = os.path.join(IBEX_BUILD_DIR, "build/lowrisc_ibex_top_artya7_0.1/synth-vivado")
    EDA_YML_NAME = "lowrisc_ibex_top_artya7_0.1.eda.yml"
    EDA_YML = os.path.join(SYNTH_DIR, EDA_YML_NAME)

    with open(EDA_YML) as f:
        data = load(f, Loader=Loader)
        files = data["files"]

    for src in files:
        if "file_type" not in src.keys():
            continue

        if src["file_type"] in "systemVerilogSource":
            file_path = os.path.realpath(
                os.path.join(os.path.dirname(EDA_YML), src["name"])
            )
            if "is_include_file" not in src.keys():
                ibex_srcs.append(file_path)
            else:
                ibex_inc.append(os.path.dirname(file_path))

    with open(DIAGRAM_YOSYS_SCRIPT, "w") as ys:
        ys.write("verilog_defines -D{key}={val};\n".format(
            key="PRIM_DEFAULT_IMPL",
            val="prim_pkg::ImplGeneric"
        ))

        ibex_inc = list(dict.fromkeys(ibex_inc))
        inc_str = ""
        for inc in ibex_inc:
            inc_str += "-I{} ".format(inc)
            ys.write("verilog_defaults -add {}\n".format(inc_str))

        for src in ibex_srcs:
            ys.write("read_verilog -sv {}\n".format(src))

        ys.write("prep -top ibex_core\n")
        ys.write("write_verilog {}\n".format(OUT_VERILOG))

    os.makedirs(GENERATED_DIR, exist_ok=True)

    cmd = "antmicro-yosys -s {}".format(DIAGRAM_YOSYS_SCRIPT)
    subprocess.run(cmd, shell=True)


generate_ibex_sources()
create_input_verilog()

# -- Sphinxcontrib HDL Diagrams configuration ---------------------------------

hdl_diagram_yosys = shutil.which("antmicro-yosys")

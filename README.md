Blank for working with graphs on competition tasks. Supported: reading, writing, generating, drawing, markers, edge weights, node values, checking structure correctness.

## Requirements

* For generating random graph: networkx, numpy
* For drawing: networkx, numpy, matplotlib, pyqt5
* For drawing in format .dot: pydot

Everything else will work out of the box

## Install editable

This is only a workpiece, which will probably need to be changed for specific tasks. However, it may be convenient to import the original version of the module without copying it into the current directory.

    $ cd `place for permanent keeping this module`
    $ git clone https://github.com/smurphik/graph
    $ cd graph
    $ sudo pip3 install -e .

For test you can just run module. After this you will see text representation of random weighted tree in console and window with visualisation of this tree. After closing this window you will see new window with same marked tree without weights (marked nodes & edges should be red).

    $ ./graph.py

## Examples

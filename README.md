# OpenDSPL Interpreter
OpenDSPL is an open source interpreter (released under the MIT license) for DSPL, written in Python.

The plan is to make this into a proof of concept, to give exposure to the DSPL language (also under MIT license). This interpreter only works on static .wav files and raw binary/text files. In the future, an interactive version should be made. It should also be possible to compile into VST3 or AU plugins for sound processing, AE plugins for video processing, PS or GIMP plugins for images, support live MIDI and DMX processing capabilities and so on.

# Future Developments
After this proof of concept is completed, its source code will remain available for whoever wants to make DSPL-compatible interpreters, compilers, libraries or whatever else. A commercial closed-source compiler will be made if interest and funding are available.

The interpreter can be highly optimized by not using Python. Languages like C, Lisp or Rust are usually much faster.

# About the OpenDSPL language
+ OpenDSPL is a _Digital Signal Processing Language_. A programming language specifically designed for signal processing.

+ Its syntax is heavily influenced by Lisp, Rust and Faust (another DSP language).

+ The interpreter architecture is heavily influenced by Reaktor (an event-based 
visual DSP language).

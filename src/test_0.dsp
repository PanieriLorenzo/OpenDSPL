# === VARIABLES & TYPES =================================================================
# variable are not mutable, under any circumstance
# variables can have one of the following basic types:
a: int;
c: byte;  # 8 -bit raw (unsigned) integer / character
f: float; # 64-bit floating point
h: bool;  # bool

# all of these basic types can be templated by using the "number" type, the exact type
# will be inferred. This allows for re-using functions for different types
x: number;

# complex types
(1, "tree", 2.5);  # tuple
[1, 2, 3];         # list
[[1, 2, 3], [4, 5, 6]];  # matrix
"hello";   # string literals are aliases for lists of bytes

# user-defined types
foo: record = (bar: i32, baz: i32);   # defining the type 'foo'
test: foo = (11, 12);                 # initializing a variable of type foo

# notice that types are themselves variables. This means you can do some strange things
# with them, like passing types around, but be careful, as this can undermine the
# strongly typed system


# === PROCESSES =========================================================================
# processes are the functions of DSPL. A process is similar to a lambda closure, but they
# are able to store states between events, although not within one event.
# a process doesn't return a value by default, instead it returns an expression
# which is only evaluated when the value has to be outputted, this increases performance
# and avoids some floating point errors
# default "plug-in" parameters are the first taken left to right
# last statement is returned
sample_function: process = (x: i32, y: i32) -> (i32, i32){ (+ x y, - x y) }
"""

test_str_2 = """
# === OPERATORS =========================================================================
# most operators are similar to those found in other languages, like +, -, *, /, <<, >>
# here are some more unique operators

# delay operator: accesses previous values of a, offset by b events into the past
#   this is borrowed from the faust language.
a @ b

# "plug" operator: allows for implicit composition of processes in a more readable
#   way. These two lines are equivalent
x -> foo() -> bar();
bar(foo(x));

# callable numbers: positive integers can be called as processes, and they represent
#   their respective church encodings. The following two lines are equivalent
x -> 3(foo())
x -> foo() -> foo() -> foo()

# callable booleans: this is the preferred method of doing structured programming.
#   true takes two parameters and returns the first
#   false takes two parameters and returns the first
#   to implement more complex conditions, boolean expressions can be called:
(x > 5)(1, 2);

# if this syntax seems a bit too contrived, there is a library called "std_imperative"
# which contains more traditional imperative concepts, such as "if_then",
# "if_then_else", "switch", and so on:
if_then(condition, foo)   # returns foo if true, else consumes an event without returning
if_then_else(condition, foo, bar)   # classic if
switch(uint, (1, 2, 3))   # alias for tuple indexing
loop(num, process)        # calls process num times, returning num sub-events
"""

test_str_3 = """
# === EVENT SYSTEM ======================================================================
# DSPL is event based, meaning that every process runs asynchronously from each other
# constantly producing a stream of values called events, each at its own independent
# rate. All variables in DSPL are in reality a way of abstracting a signal, seen as
# an array of values indexed by time.
# All signal originate from some source, which emits events at a set rate, for example
# a wave file might output 44100 values per second.
# any variable in between two samples simply holds whichever value was in the last event.
# certain processes, however, are only triggered when an event arrives.
# DSPL offers a few key features to deal with events:

# sources: sources are entities outside of a DSPL script from which signals are taken
#   these can be audio files, microphones, ...
#   sources can be set up to have a specific event rate, or in real-time scripts they
#   can have an arbitrary event rate.
input: source = (file_path, rate, other_meta_data)

# sources attributes:
source.rate     # the event rate of the source
source.clock    # value-less events at clock-rate
source.path     # string containing file location, note that file might be a macro for
                # STD_IO or device drivers
source.interval # time between current and previous events
source.read     # events (with value) at clock-rate

# instead of sources, one sometimes just needs a clock source
c: clock = (44100)   # clock rate
clock.tick           # emits value-less events at clock rate

# sometimes you might want to change the rate of a specific signal, for this you can
# use reclock():
x -> reclock(c.tick)

# TODO: ...

# Delay operator in depth:
a @ 1   # will make the compiler instantiate an array of lenght 2 to store a
a @ b   # where b is u32, will make the compiler instantiate an array of lenght
        # MAX_U32, as it is not possible to infer how far back in time the expression
        # will try to read. For this reason, try to avoid using variables for the
        # second operand

# simple integral and derivative processes using the delay operator:
integral: proc(x: i32) -> i32{ x + x @ 1 }
diff: proc(x: i32) -> i32{ x - x @ 1 }

# iteration:
# iteration often requires to break the abstraction that variables are immutable
# e.g. in the case we want to sum all members of a list into a single value
# for this reason, we can use the event system to circumvent the limitation, using the
# itr type:
x: i32[] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
i: itr(0, 10)   # will produce sub-events from 0 to 9 when an event arrives
x[i] -> integral()   # will sum all values of x together, as the iteration is completed
                     # within a single event.
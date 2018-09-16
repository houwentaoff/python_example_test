#!/usr/bin/env python
#2.7 and 3.5
from optparse import OptionParser 
import sys
'''
# The list of instance attributes that may be set through
# keyword args to the constructor.
ATTRS = ['action',
         'type',
         'dest',
         'default',
         'nargs',
         'const',
         'choices',
         'callback',
         'callback_args',
         'callback_kwargs',
         'help',
         'metavar']

#action:store,store_true,store_false..,dest->var name,default is default
# The set of known types for option parsers.  Again, listed here for
# constructor argument validation.
    TYPES = ("string", "int", "long", "float", "complex", "choice")

'''
if __name__ == "__main__":
    #parser = OptionParser (option_class=eng_option, conflict_handler="resolve")
    parser = OptionParser (conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-f", "--file", dest="filename",  
                              help="write report to FILE", metavar="FILE")  
    parser.add_option("-v","--verbose", action="store_true", default=False)

    parser.add_option("","--rfreq", type="int",dest="rx_freq", action="store",
                               help="set rx freq ")

    expert_grp.add_option("", "--carrier-threshold", type="float", default=30,
                                        help="set carrier detect threshold (dB) [default=%default]")

      
    (options, args) = parser.parse_args()
    # unknow args
    if len(args) != 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.rx_freq is None:
        sys.stderr.write("You must specify FREQ : --rfreq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)


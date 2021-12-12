from ghidra.app.decompiler import DecompInterface


import __main__ as my_tool


class Decompiler:

    # initialize

    def __init__(self, program=None, timeout=None):


        # DecompInterface object initialization
        self._decompiler = DecompInterface()

        # open the current program
        self._decompiler.openProgram(program or my_tool.currentProgram)

        # specific time for the program to specify the time for the program to run
        self._timeout = timeout

    # This is a decompiler function.
    def decompile_func(self, func):

        # decompiler status flag
        dec_st_flag = self._decompiler.decompileFunction(func, 0, self._timeout)

        # examine the status flag decompiled or not
        if dec_st_flag and dec_st_flag.decompileCompleted():

            # a boolean object to check for the function
            dec_fun = dec_st_flag.getDecompiledFunction()

            # check for the object is true or not
            if dec_fun:

                # This line of code gets the pseodo code in C
                return dec_fun.getC()

# Gather all the decompiled string at one place

    def decompile(self):

        # this joins the psedo code that is returned in the previous function
        # initalize the variable
        dec_cod_c = ''

        # All the function are retreived
        req_functions = my_tool.currentProgram.getListing().getFunctions(True)
        # iterate by taking one function at a time
        for one_function in req_functions:
            decompiled_function = self.decompile_func(one_function)

            #check for a function valid or not
            if decompiled_function:
                # add this function to the string initialised
                dec_cod_c += decompiled_function

        # return the concatenated string
        return dec_cod_c

# run the python script
def run_script():

    # take the arguments
    arguments = my_tool.getScriptArgs()

    # The len of the arguments
    if len(arguments) > 1:


        print('[!] wrong parameters, see following\n\
Usage: ./analyzeHeadless <PATH_TO_GHIDRA_PROJECT> <PROJECT_NAME> \
-process|-import <TARGET_FILE> [-scriptPath <PATH_TO_SCRIPT_DIR>] \
-postScript|-preScript decompile.py <PATH_TO_OUTPUT_FILE>')
        return


    # <CURRENT_PROGRAM>_decompiled.c when no path for saving saving is given will be saved to current location
    if len(arguments) == 0:

        # name of the current program
        N_C_P = my_tool.currentProgram.getName()
        # result of program to split
        res = '{}_decompiled.c'.format(''.join(N_C_P.split('.')[:-1]))
    else:
        # take the initialised of first one
        res = arguments[0]

    # object
    decompiler = Decompiler()
    # decompiled code
    decompiled_code = decompiler.decompile()

    # write to the file and the save
    with open(res, 'w') as res_file:
        # write to the file
        res_file.write(decompiled_code)
        # output the output loaction where the files are saved
        print('This will be saved to the  -> {}'.format(res))


# it will be executed form here
if __name__ == '__main__':
    # run the script
    run_script()
from __future__ import print_function
import __main__ as my_tool
mod_byte_addr = 15
mod_byte_st = 15
output_format = ' {{addr:<{0}}} {{byte:<{1}}} {{inst}}\n'.format(mod_byte_addr , mod_byte_st + mod_byte_addr )

def signature_func(func):
    name = func.getDefaultCallingConventionName()
    params = func.getParameters()
    return '\n{calling_conv} {func_name}({params})\n'.format(calling_name = name, func_name=func.getName(), params=', '.join([str(param).replace('[', '').replace(']', '').split('@')[0] for param in params]))


def instructions_func(func):
    insts = ""
    addr = func.getEntryPoint()
    temp = my_tool.currentProgram.getListing().getInstructions(addr, True)
	# going through each instruction
    for inst in temp : 
        if my_tool.getFunctionContaining(inst.getAddress()) != func :
            break
        insts +=  output_format.format(
            addr=inst.getAddressString(True, True),
            byte=' '.join([hex(b) if b >= 0 else hex((abs(x) ^ 0xff) + 1) for b in inst.getBytes()]),
            inst=inst
    )
    return insts 


def main_disassembling_function(func) :
    '''
	when a function is passed as an argument to disassemble, 
	we are returning as string(signature + instruction)
    '''

    return  signature_func(func) +instructions_func(func)



def disassembling_whole_program(prog):
    '''
    Disassemble the whole program by disassembling each function.
    '''
    disasassemble_result = ""
	# disassemble each function 
    total_funcs = prog.getListing().getFunctions(True)
  	
    for each_func in total_funcs:
       	disasassemble_result += disassembler(each_func)
    return disasassemble_result 

def run():
    arguments  =  my_tool.getScriptArgs()
    if len(arguments) > 1:
        print('For output path, see the following data :: \n\
Usage: ./analyzeHeadless <give_path_to_our_ghidra_project> <include_project_name_here> \
-process|-import <target_file_name> [-scriptPath <path_to_script>] \
-postScript|-preScript disassembling_.py <path_to_OP_file>')
        return

    else :
        print('Please provide proper paths  data')
    
    disassembled =disassembling_whole_program(my_tool.currentProgram)
    with open(output, 'w') as file_w:
        file_w.write(disassembled)
        print('[*] disassembled!!! saved to {}'.format(output))
        
        
if __name__ == '__main__':
    run()

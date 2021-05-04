import re
import os
import sys
import argparse
import semantic_version
from pathlib import Path

from retector.reanalysis import reanalyze
from retector.reanalysis import handle_facts_out
from retector.reanalysis import prints

from retector.securify2.ir import visualizer
from retector.securify2.staticanalysis import static_analysis
from retector.securify2.staticanalysis.factencoder import encode
from retector.securify2.staticanalysis.visualization import visualize
from retector.securify2.solidity.solidity_ast_compiler import  compiler_version
from retector.securify2.solidity import solidity_ast_compiler, solidity_cfg_compiler

def analyze(facts, contract, file_name, file_path, **kw_args_souffle):
    
    facts_out = reanalyze.get_facts_out(facts, file_path, **kw_args_souffle)

    violations = handle_facts_out.extract_reentrancy(facts_out)

    prints.print_violations(violations, contract, file_name, file_path)    

def visualization(compile_output, facts, output_path):
    # Visualize control flow graph.
    visualizer.draw_cfg(
        compile_output.cfg,
        file=output_path + "graph",
        format='pdf',
        only_blocks=True)

    # Visualize Datalog facts.
    visualize(facts).render(
        filename=output_path + "facts",
        format='pdf',
        cleanup=True,
        view=True)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='retector: A simplified-securify2 for reentrancy detection',
        usage="retector contract.sol [opts]")
    parser.add_argument('contract')
    parser.add_argument('--visualize', '-v', help='Visualize AST', action='store_true')

    compilation_group = parser.add_argument_group('Compilation of Datalog code')

    compilation_group.add_argument('--interpreter',
                                   help="Use the souffle interpreter to run the datalog code.\
                                        Particularly useful when experimenting with new patterns.",
                                   action='store_true')

    compilation_group.add_argument('--recompile', help="Force recompilation of the datalog code.",
                                   action='store_true')

    base_path = Path(__file__).parent    
    compilation_group.add_argument('--library-dir', help="Directory of the functors' library.",
                                   default=base_path / 'reanalysis/libfunctors/')
    args = parser.parse_args()
    return args

def prepare_libfunctors(path):
    libfunctors = path / 'libfunctors.so'
    compile_script = './compile_functors.sh'
    if libfunctors.is_file(): return
    print("libfunctors.so not compiled. Compiling it now...")
    os.system("cd " + path.absolute().as_posix() + " && " + compile_script + "&& cd - > /dev/null")

def read_contract(contract_path):
    with open(contract_path, 'r') as f:
        return f.read()

def main():
    # Parse command lines.
    args = parse_arguments()

    # Config and preparation
    souffle_config = dict(use_interpreter=args.interpreter, force_recompilation=args.recompile,
                          library_dir=args.library_dir)
    prepare_libfunctors(args.library_dir)

    # Getting absolute source path and setting output path
    src_name = args.contract
    src_path = os.path.join(os.getcwd(), src_name)
    output_path = src_path + "_out"

    # Compile to ast and convert to cfg
    compile_output = solidity_cfg_compiler.compile_cfg(src_path)
    cfg = compile_output.cfg.contracts[0]
    facts, fact_mapping = encode(cfg)

    # Visulize
    if args.visualize:
        visualization(compile_output, facts, output_path)

    # Get source code
    contract = read_contract(src_path)

    # Static analyze
    analyze(facts, contract, src_name, src_path, **souffle_config)

if __name__ == '__main__':
    main()

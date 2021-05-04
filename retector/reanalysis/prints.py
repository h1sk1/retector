from retector.reanalysis import handle_facts_out

class Colors:
    RED = 31
    BLUE = 34
    GREEN = 32


def get_color(code, color):
    colors = Colors()
    if color == "RED":
        print_color = str(colors.RED)
    elif color == "BLUE":
        print_color = str(colors.BLUE)
    elif color == "GREEN":
        print_color = str(colors.GREEN)

    return "\033[1;" + print_color + "m" + code +"\033[0m"

def print_format(content1, content2, color):
    print('%-30s%-20s' %(get_color(content1, color), get_color(content2, color)))

def print_infos(file_name, file_path):
    print(get_color("A simplified-securify2 for reentrancy detection", "BLUE"))
    print("")
    print(get_color("Contracts Analyzed!", "BLUE"))
    print_format("FileName:", file_name, "BLUE")
    print_format("FilePath:", file_path, "BLUE")

def print_violations(violations, contract, file_name, file_path):
    
    print_infos(file_name, file_path)

    if violations:
        for violation in violations:
            num = violation.getId()
            line = violation.getLine()
            loc = violation.getLoc()
            contract_name = violation.getContract()
            start = int(loc.split(':')[0])
            lens = int(loc.split(':')[1])

            code = contract.split('\n')[int(line) - 1]

            pre_lens = 0
            for i in range(line - 1):
                pre_lens += len(contract.split('\n')[i])

            pre_lens_in_line = start - pre_lens + 1

            wave = " " * pre_lens_in_line + "^" * lens

            print(get_color("\nReentrancy Found!\n", "RED"))
            print_format("Number:", str(num), "RED")
            print_format("Contract:", contract_name, "RED")
            print_format("Line:", str(line), "RED")
            print(get_color("\nSource:", "RED"))
            print(get_color(">" + code, "RED"))
            print(get_color(">" + wave, "RED"))
    else:
        print(get_color("\nNo reentrancy found!", "GREEN"))
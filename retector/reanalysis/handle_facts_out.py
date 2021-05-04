class Violation:
    v_id: int
    line: int
    loc: str
    contract: str

    def addId(self, v_id):
        self.v_id = v_id
    
    def addLine(self, line):
        self.line = line
    
    def addLoc(self, loc):
        self.loc = loc
    
    def addContract(self, contract):
        self.contract = contract

    def getId(self):
        return self.v_id
    
    def getLine(self):
        return self.line

    def getLoc(self):
        return self.loc

    def getContract(self):
        return self.contract

def addIn(violation, v_type, content):
    if v_type == "line":
        violation.addLine(int(content[1 : ]))
    elif v_type == "loc":
        violation.addLoc(content)
    elif v_type == "contract":
        violation.addContract(content)


def extract_reentrancy(facts_out):
    infos = facts_out["info"]
    infos = sorted(infos, key = lambda t: t[0])

    violations = []
    v_id = 0
    id_name = ""
    for info in infos:
        if id_name != info[0]:
            id_name = info[0]
            v_id += 1
            violation = Violation()
            violation.addId(v_id)
            addIn(violation, info[1], info[2])
            violations.append(violation)
        else:
            addIn(violations[v_id - 1], info[1], info[2])
    
    return violations
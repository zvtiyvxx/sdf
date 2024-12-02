from math import log2

class MD(object):

    @staticmethod
    def matrix(m):
        output = []
        for i in m:
                lst = tuple(map(lambda x: str(round(x, 4)), i))
                output.append(" & ".join(lst))
        output = r" \\ ".join(output)
        output = r"\begin{bmatrix} " + output + r" \end{bmatrix}"
        return output

    def u_entropy(self, m: list[list], p: dict) -> str:
        first = self.__u_entropy_first(m, p)
        second = self.__u_entropy_second(m, p)
        third = self.__u_entropy_third(m, p)
        fourth = self.__u_entropy_fourth(m, p)
        solved = " = ".join((first, second, third, fourth))
        return f"H(B|A) = {solved} = "
    
    def a_entropy(self, pbj: list) -> str:
        pbj = tuple(map(lambda i: round(i, 3), pbj))
        first = self.__a_entropy_first(pbj)
        second = self.__a_entropy_second(pbj)
        third = self.__a_entropy_third(pbj)
        solved = " = ".join((first, second, third))
        return f"H(B) = {solved} = "

    
    def __a_entropy_first(self, pbj: list) -> str:
        out = []
        for j in range(len(pbj)):
            out.append(f"{pbj[j]} \\cdot log_2({pbj[j]})")
        return f"-({" + ".join(out)})"
    
    def __a_entropy_second(self, pbj: list) -> str:
        out = []
        for j in range(len(pbj)):
            out.append(f"{round(pbj[j], 3)} \\cdot ({round(log2(pbj[j]), 3)})")
        return f"-({" + ".join(out)})"

    def __a_entropy_third(self, pbj: list) -> str:
        out = []
        for j in range(len(pbj)):
            out.append(f"({round((pbj[j] * log2(pbj[j])), 3)})")
        return f"-({" + ".join(out)})"

    @staticmethod
    def pm(m: list[list], ps: dict, pms: list[list]) -> str:
        out = []
        for i in range(len(m)):
            for j in range(len(m[i])):
                out.append(f"p(a_{i+1}, b_{j+1}) = {round(ps[i+1], 4)} \\cdot {round(m[i][j], 4)} = {round(pms[i][j], 4)};")
        return "$$\\begin{array}{lcl} " + ' \\\\ '.join(out) + "\\end{array}$$"

    @staticmethod
    def pb(m: list[list], p: dict, pbs):
        m = [list(row) for row in zip(*m)]
        pb = []
        pbs = tuple(map(lambda i: round(i, 3), pbs))
        for i in range(len(m)):
            pbj = []
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                pbj.append(f"{p[j+1]}" + r' \cdot ' + str(m[i][j]))
            pb.append(" + ".join(pbj))
        solved = [f"p(b_{i+1}) = {pb[i]} = {pbs[i]}" for i in range(len(pb))]
        out = "$$\\begin{array}{lcl} " + ' \\\\ '.join(solved) + "\\end{array}$$\n\n" 
        out += "$$\\sum_{j=1}^m p(b_j) = " + " + ".join(tuple(map(lambda i: str(i), pbs))) + f" = {sum(pbs)}"
        return out


    def __u_entropy_first(self, m: list[list], p: dict) -> str:
        H = []
        for i in range(len(m)):
            part = []
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                part.append(f"({m[i][j]} \\cdot log_2({m[i][j]}))")
            H.append(f"({p[i+1]} * {" + ".join(part)})")
        return f"-({' + '.join(H)})"
    
    def __u_entropy_second(self, m: list[list], p: dict) -> str:
        H = []
        for i in range(len(m)):
            part = []
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                part.append(f"({m[i][j]} \\cdot {round(log2(m[i][j]), 3)})")
            H.append(f"({p[i+1]} * {" + ".join(part)})")
        return f"-({' + '.join(H)})"
    
    def __u_entropy_third(self, m: list[list], p: dict) -> str:
        H = []
        for i in range(len(m)):
            part = []
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                part.append(f"({round(m[i][j] * log2(m[i][j]), 3)})")
            H.append(f"({p[i+1]} * {" + ".join(part)})")
        return f"-({' + '.join(H)})"
    
    def __u_entropy_fourth(self, m: list[list], p: dict) -> str:
        H = []
        for i in range(len(m)):
            part = []
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                part.append(m[i][j] * log2(m[i][j]))
            H.append(p[i+1] * sum(part))
        H = tuple(map(lambda i: f"({round(i,4)})", H))
        return f"-({' + '.join(H)})"
    
    def __final_entropy_first(self, m: list[list]) -> str:
        H = []
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                H.append((f"{round(m[i][j], 4)} \\cdot log_2({round(m[i][j], 4)})"))
        return f"-({" + ".join(H)})"
    
    def __final_entropy_second(self, m: list[list]) -> str:
        H = []
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                H.append((f"{round(m[i][j], 4)} \\cdot ({round(log2(m[i][j]), 4)})"))
        return f"-({" + ".join(H)})"

    def __final_entropy_third(self, m: list[list]) -> str:
        H = []
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                H.append((f"({round(m[i][j] * log2(m[i][j]), 4)})"))
        return f"-({" + ".join(H)})"

    def final_entropy(self, m: list[list]) -> str:
        first = self.__final_entropy_first(m)
        second = self.__final_entropy_second(m)
        third = self.__final_entropy_third(m)
        solved = " = ".join((first, second, third))
        return f"H(A,B) = {solved} = "



def print_entropy(m, ps):
    md = MD()
    return md.u_entropy(m, ps)

def print_accepted_entropy(pbj):
    md = MD()
    return md.a_entropy(pbj)

def print_final_entropy(m):
    md = MD()
    return md.final_entropy(m)
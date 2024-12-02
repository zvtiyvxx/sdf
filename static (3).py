from math import log2 as log

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
    
    @staticmethod
    def gen_pa(p: dict) -> str:
        keys = p.keys()
        out = tuple(map(lambda key: f"$p(a_{key})={p[key]}$", keys))
        return "; ".join(out)
    
    @staticmethod
    def unified_matrix_ab(matrix: list[list], p: dict, final_matrix: list[list]) -> str:
        matrix = [list(row) for row in zip(*matrix)]
        def first_loop(i, j):
            return f"p(a_{i+1}, b_{j+1}) = p(a_{j+1}) \\cdot p(a_{i+1}|b_{j+1})"
        def second_loop(i, j):
            return f"{p[j+1]} \\cdot {matrix[i][j]}"
        first = []
        second = []
        third = []
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                first.append(first_loop(i,j))
                second.append(second_loop(i,j))
                third.append(round(final_matrix[j][i], 4))
        out = tuple(map(lambda f, s, t: f"{f} = {s} = {t}", first, second, third))
        return "$$\\begin{array}{lcl}" + "\\\\".join(out) + "\\end{array}$$"

    @staticmethod
    def matrix_ab(matrix: list[list], p: dict, final_matrix: list[list]) -> str:
        matrix = [list(row) for row in zip(*matrix)]
        def first_loop(i, j):
            return f"p(a_{i+1}, b_{j+1}) = \\frac{{p(a_{i+1}|b_{j+1})}}{{p(a_{j+1})}}"
        def second_loop(i, j):
            return f"\\frac{{{round(matrix[i][j], 4)}}}{{{round(p[j+1], 4)}}}"
        first = []
        second = []
        third = []
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                first.append(first_loop(i,j))
                second.append(second_loop(i,j))
                third.append(round(final_matrix[j][i], 4))
        out = tuple(map(lambda f, s, t: f"{f} = {s} = {t}", first, second, third))
        return "$$\\begin{array}{lcl}" + "\\\\".join(out) + "\\end{array}$$"
    
    @staticmethod
    def gen_pb(matrix: list[list], result: dict) -> str:
        matrix = [list(row) for row in zip(*matrix)]
        output = []
        for i in range(len(matrix)):
            y = f"p(b_{i+1}) = "
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    continue
                y += f"{round(matrix[i][j], 4)} +"
            output.append(f"{y[:-1]}= {round(result[i+1], 4)}")
        resul_values = tuple(map(lambda i: str(round(i, 4)), tuple(result.values())))
        summ = f"$$\\sum_{{i=1}}^m p(b_i) = {' + '.join(resul_values)} = {sum(tuple(result.values()))}$$"
        return "$$\\begin{array}{lcl}" + "\\\\".join(output) + "\\end{array}$$\n\n" + summ

    @staticmethod
    def absolute_entropy(v: dict, result: float, a: str) -> str:
        values = tuple(map(lambda i: round(i, 4), list(v.values())))
        first = tuple(map(lambda idx: f"p({a}_{idx+1}) \\cdot \\log_2(p({a}_{idx+1}))", range(len(values))))
        second = tuple(map(lambda value: f"{value} \\cdot \\log_2({value})", values))
        third = tuple(map(lambda value: f"{value} \\cdot {round(log(value), 4)}", values))
        fourth = tuple(map(lambda value: f"({round(value * log(value), 4)})", values))
        summ = tuple(map(lambda i: f"-({' + '.join(i)})", (first, second, third, fourth)))
        return f"$$H({a.capitalize()})={' = '.join(summ)} = {round(result, 4)}"

    @staticmethod
    def cond_entropy(m: list[list], v: dict, result: float, a: tuple[str, str]) -> str:
        values = tuple(map(lambda i: round(i, 4), list(v.values())))
        parts = {1: [], 2: [], 3: [], 4: []}
        results = []
        def first_loop(i, j):
            parts[1].append(f"p({a[1]}_{i+1}) \\cdot p({a[0]}_{i+1}|{a[1]}_{j+1}) \\cdot \log(p({a[0]}_{i+1}|{a[1]}_{j+1}))")
        def second_loop(i, j):
            parts[2].append(f"{values[i]} \\cdot {round(m[i][j], 4)} \\cdot \log({round(m[i][j], 4)})")
        def third_loop(i, j):
            parts[3].append(f"{values[i]} \\cdot {round(m[i][j], 4)} \\cdot {round(log(m[i][j]), 4)}")
        def fourth_loop(i, j):
            parts[4].append(f"({round(values[i] * m[i][j] * log(m[i][j]), 4)})")
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == 0:
                    continue
                first_loop(i, j)
                second_loop(i, j)
                third_loop(i, j)
                fourth_loop(i, j)
        for key in tuple(parts.keys()):
            results.append(f"-({' + '.join(tuple(map(lambda i: i, parts[key])))})")
        return f"$$H({a[0].capitalize()}|{a[1].capitalize()})={' = '.join(results)}={round(result, 5)}$$"
    
    @staticmethod
    def bandwitch(absolute: float, cond: float, n: int, result: float, a: tuple[str, str]) -> str:
        first = f"n \\cdot (H({a[0]}) - H({a[0]}|{a[1]}))"
        second = f"{n} \\cdot ({round(absolute, 5)} - {round(cond, 5)})"
        return f"$$C({a[0]}) = {first} = {second} = {round(result, 2)}$$"

class ProcessSensitivity:
    def __init__(self,
                 file_path: str):

        with open(file_path, 'r') as f:
            lines = []
            for row in f:
                lines.append(row)

            self.no_sims = int(lines[0].split('Total Simulations to run: ')[1])
            success_rate = float(lines[-1].split('Success rate = ')[1])

            max_line = len(lines)

            self.outcome = [False] * self.no_sims

            no_variables = int((max_line - 2) / self.no_sims - 1)

            self.variable_names = []
            for v in range(0, no_variables):
                self.variable_names.append(lines[2 + v].split(' = ')[0].split('.')[-1].capitalize())

            self.variables = []

            for i in range(1, self.no_sims + 1):
                start_line = 1
                while start_line < max_line:
                    if 'Simulation No.: ' + str(i) in lines[start_line]:
                        break
                    else:
                        start_line += 1

                # Store simulation outcome
                self.outcome[i - 1] = eval(lines[start_line].split('Outcome: ')[1])

                values = []
                for j in range(0, no_variables):
                    values.append(float(lines[start_line + j + 1].split(' = ')[1]))
                self.variables.append(values)

import collections

# strips whitespace from start of string
def strip_prefix_whitespace(str):
    for idx, char in enumerate(str):
        if char == "<":
            return str[idx:]
    return str

# get string with only numbers
def get_number_only_string(str):
    new_str = [" " if not char.isdigit() else char for char in str]
    return "".join(new_str)

# converts string to tuple of integers
def tuple_from_str(str):
    num_str = get_number_only_string(str)
    return tuple(map(int, num_str.split()))

# gets attribute value starting at certain position
def get_attribute(str):
    first_quotation = False
    first_position = None
    # get what is between quotation marks
    for idx, char in enumerate(str):
        if char == '"':
            if first_quotation:
                return str[first_position+1:idx]
            else:
                first_quotation = True
                first_position = idx
    raise Exceptions("No quotation marks or improperly closed")

# get name of attribute in xml file
def attribute_name(line):
    name_pos = line.find("name")
    return get_attribute(line[name_pos:])

# gets tuple representing location of component
def attribute_loc(line):
    loc_pos = line.find("loc")
    return tuple_from_str(get_attribute(line[loc_pos:]))

# superclass which defines a generic component
class Component:
    def __init__(self):
        self.component_type = ""
        self.location = None
        self.label = ""

# represents wire from coordinates given by start to coordinates given by end
class Wire(Component):
    def __init__(self, line):
        super().__init__()
        from_pos = line.find("from")
        self.start = tuple_from_str(get_attribute(line[from_pos:]))
        to_pos = line.find("to")
        self.end = tuple_from_str(get_attribute(line[to_pos:]))

        self.component_type = "wire"
        self.location = self.start
        self.type = ""

# gets the library in which the current component is
# defined by logisim xml standard
def get_lib(line):
    lib_pos = line.find("lib")
    return int(get_attribute(line[lib_pos:]))

# class which defines an input or output pin
class Pin(Component):
    def __init__(self, line):
        super().__init__()
        self.component_type = "pin"
        self.location = attribute_loc(line)
        self.type = "input"
        self.label = ""

# defines logical operator, such as AND, OR, etc.
class Operator(Component):
    def __init__(self, line):
        super().__init__()
        self.component_type = "operator"
        self.location = attribute_loc(line)
        self.type = attribute_name(line)

# get label from attribute
def get_label(line):
    lib_pos = line.find("val")
    return get_attribute(line[lib_pos:])

# gets label which can be inserted into the code
# e.g. RD0 -> PORTDbits.RD0
def code_label(label):
    port_label = label[1]
    return "PORT" + port_label + "bits." + label

# class which defines logic circuit as graph
# every logic operator and input/output pin represents a node
# operator inputs and wires represent edges
class LogicCircuit:
    # parse xml file into list of components
    def xml_parse(self, xml_file):
        self.component_list = []
        in_pin_specification = False

        for line in xml_file:
            clean_line = strip_prefix_whitespace(line)
            #print(clean_line)
            if clean_line[1:5] == "wire":
                self.component_list.append(Wire(clean_line))
            elif clean_line[1:5] == "comp":
                if get_lib(clean_line) == 0:
                    self.component_list.append(Pin(clean_line))
                    in_pin_specification = True
                else:
                    self.component_list.append(Operator(clean_line))
            elif clean_line[1:6] == "\comp":
                if in_pin_specification:
                    in_pin_specification = False
            # if this line defines an attribute and it sets the output attribute
            if in_pin_specification and clean_line[0:2] == "<a" and attribute_name(clean_line) == "output":
                self.component_list[-1].type = "output"
            # if the attribute has a label read it's label
            if clean_line[0:2] == "<a" and attribute_name(clean_line) == "label":
                self.component_list[-1].label = get_label(clean_line)

        for comp_idx, component in enumerate(self.component_list):
            print(str(comp_idx+1) + ".", end="")
            print(component.component_type)
            print(component.type)
            print(component.label)
            print(component.location)
            print("\n")

    # recursive function for dfs traversal
    def dfs_visit(self, location, directed_graph, is_visited, corresponding_output, output_label):
        is_visited[location] = True
        corresponding_output[location] = output_label
        for neighbor_location in directed_graph[location]:
            if not is_visited[neighbor_location]:
                self.dfs_visit(neighbor_location, directed_graph, is_visited, corresponding_output, output_label)

    # construct directed graph from component list
    # then using dfs traversal gets output labels for locations in circuit diagram
    def get_output_labels(self):
        directed_graph = collections.defaultdict(list)
        corresponding_output = {}  # defines the output connected to a coordinate location
        for idx, component in enumerate(self.component_list):
            if component.component_type == "wire":
                directed_graph[component.start].append(component.end)
                directed_graph[component.end].append(component.start)

        is_visited = collections.defaultdict(bool)
        for (component_idx, component) in enumerate(self.component_list):
            if component.component_type == "operator"\
            or (component.component_type == "pin" and component.type == "input"):
                self.dfs_visit(component.location, directed_graph, is_visited, corresponding_output, component_idx)

        for wire in corresponding_output:
            print(wire, corresponding_output[wire], self.component_list[corresponding_output[wire]].type,\
                  self.component_list[corresponding_output[wire]].location)

        return corresponding_output

    # get graph with non-wire components as nodes
    # from corresponding output dictionary and directed graph
    def form_graph(self, corresponding_output):
        # go through non wire components and form the graph
        self.graph = [[] for component in self.component_list]
        self.reversed_graph = [[] for component in self.component_list]
        print("\n")

        for (component_idx, component) in enumerate(self.component_list):
            if component.type == "wire":
                continue
            # non-wire component
            position = component.location
            input_positions = []

            if component.component_type == "pin" and component.type == "output":
                input_positions = [position]
            elif component.component_type == "operator" and component.type == "Buffer":
                input_positions = [(position[0]-20, position[1])]
            elif component.component_type == "operator" and component.type == "NOT Gate":
                input_positions = [(position[0] - 30, position[1])]
            elif component.component_type == "operator" and (component.type == "OR Gate" or component.type == "AND Gate"):
                for y_pos in range(-2, 3):
                    input_positions.append((position[0] - 50, position[1] + y_pos*10))
            elif component.component_type == "operator" and\
                    (component.type == "NAND Gate" or component.type == "NOR Gate" or component.type == "XOR Gate"):
                for y_pos in range(-2, 3):
                    input_positions.append((position[0] - 60, position[1] + y_pos*10))
            elif component.component_type == "operator" and component.type == "XNOR Gate":
                for y_pos in range(-2, 3):
                    input_positions.append((position[0] - 70, position[1] + y_pos*10))

            for input_position in input_positions:
                # if input is unused skip it
                if input_position not in corresponding_output:
                    continue
                # otherwise add new edge to graph
                output_label = corresponding_output[input_position]
                # output graph edge
                print((self.component_list[output_label].type, self.component_list[output_label].location),\
                      (self.component_list[component_idx].type, self.component_list[component_idx].location))
                self.graph[output_label].append(component_idx)
                self.reversed_graph[component_idx].append(output_label)

    # topological sort the graph
    def topological_sort(self):
        # calculate indegree for all non-wire components in graph
        in_degree = [0] * len(self.component_list)
        queue = collections.deque()

        for component_idx, component in enumerate(self.component_list):
            in_degree[component_idx] = len(self.reversed_graph[component_idx])
            if not in_degree[component_idx] and component.component_type != "wire":
                queue.append(component_idx)

        toposort = []
        while queue:
            cur_node_idx = queue.popleft()
            toposort.append(cur_node_idx)
            for neighbor_idx in self.graph[cur_node_idx]:
                in_degree[neighbor_idx] -= 1
                if not in_degree[neighbor_idx]:
                    queue.append(neighbor_idx)

        # print nodes in toposorted order
        print("")
        for node in toposort:
            print(self.component_list[node].type, self.component_list[node].location)
        print("")

        return toposort

    # gets function name from default name
    def get_function_name(self, preset_type):
        # print(preset_type)
        return (preset_type.split())[0]

    # forms expression from given list of inputs and given operation
    # operators with multiple operands are reduced to 2-port operators
    def form_expression(self, parent_expressions, function_name):
        # special case for single port operators
        if function_name == "NOT" or function_name == "Buffer":
            if len(parent_expressions) > 1:
                raise Exception(function_name + " operator can only take single input")
            return function_name + "(" + parent_expressions[0] + ")"

        # for multiple port operators, generalize them recursively
        # operators are assumed to be left associative, which is a typical assumption
        expression = parent_expressions[0]
        for parent_expression in parent_expressions[1:]:
            expression = function_name + "(" + expression + "," + parent_expression + ")"
        return expression

    # assumes that circuit is valid
    # for example, there is only one corresponding input pin for any location
    def __init__(self, xml_file):
        self.xml_parse(xml_file)
        corresponding_output = self.get_output_labels()
        self.form_graph(corresponding_output)
        toposort = self.topological_sort()

        # form expression in string form from graph form and toposort list
        expr_str = ["" for _ in self.component_list]
        for node_idx in toposort:
            # if it's an input pin
            if self.component_list[node_idx].component_type == "pin" and\
            self.component_list[node_idx].type == "input":
                expr_str[node_idx] = code_label(self.component_list[node_idx].label)
            # else if it's an operator
            elif self.component_list[node_idx].component_type != "pin":
                parent_expressions = []
                for parent_idx in self.reversed_graph[node_idx]:
                    parent_expressions.append(expr_str[parent_idx])
                # get name of operator
                function_name = self.get_function_name(self.component_list[node_idx].type)
                expr_str[node_idx] = self.form_expression(parent_expressions, function_name)
            # if it's output pin
            else:
                # equal to the only in-port
                expr_str[node_idx] = expr_str[self.reversed_graph[node_idx][0]]

        # get code which emmulates given behavior given several preset functions
        self.code_str = ""
        for component_idx, component in enumerate(self.component_list):
            if component.component_type == "pin" and component.type == "output":
                output_pin_name = code_label(component.label)
                new_line = output_pin_name + " = " + expr_str[component_idx] + ";"
                if self.code_str:
                    self.code_str += "\n"
                self.code_str += new_line

# apply tab to all lines in multiline string
def apply_tab(str):
    return ["\t" + line + "\n" for line in str.split("\n")]

# gets code with custom logic implemented
# easy to add additional flexibility with defining individual bits in ports as in/out
# just scan through inputs and outputs in file
# as is, it only supports port B as out, and port D as in

# also doesn't support rotating operators
# this is also a relativelly simple modification
def get_code(circuit):
    preset_code_file = open("default_code.c", "r")
    preset_code = [line for line in preset_code_file]
    logic_location = 38  # constant depending on preset code
    new_code = preset_code[0:logic_location] + apply_tab(circuit.code_str) + preset_code[logic_location+1:]
    return new_code
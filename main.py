import xml_to_circuit

if __name__ == "__main__":
    xml_file = open("logic_circuit.circ", "r")
    circuit = xml_to_circuit.LogicCircuit(xml_file)
    c_code = xml_to_circuit.get_code(circuit)

    c_file = open("main.c", "w+")
    c_file.writelines(c_code)
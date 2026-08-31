#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Este esqueleto ya implementa el contrato de línea de comandos y de salida
requerido por la especificación. Usted debe completar las dos funciones
marcadas con TODO; puede modificar el resto del archivo si lo necesita,
siempre que se preserve el contrato de invocación y la línea "HEX: 0x...".

No es obligatorio usar este esqueleto ni Python: puede implementar su
propia herramienta desde cero, en el lenguaje que prefiera, siempre que
respete el mismo contrato (ver especificación, sección "Modo de operación").
"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]


def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).

    Debe soportar únicamente las instrucciones en SOPORTADAS. Los valores
    de opcode/funct3/funct7 de cada una NO se proveen aquí: deben
    investigarse en el manual oficial de la ISA RISC-V (ver referencia en
    la especificación) y documentarse en el README.
    """
    # TODO: implementar. Sugerencia: parsear el mnemónico y los operandos,
    # despachar según el formato (R/I/S/B), y ensamblar los campos con
    # operaciones de bits.

    opcode = funct3 = funct7 = rs1 = rs2 = rd = cod_32bits = " "

    splitInstruction = instruction.split(" ")
    mnemonic = splitInstruction[0]
    registers = [reg.strip(",") for reg in splitInstruction[1:]]

    #Validar las instrucciones de Tipo R y convertir a binario en un formato de 32 bits
    if mnemonic == "add" or mnemonic == "sub" or mnemonic == "and" or mnemonic == "or":
        format_type = "R"
        opcode = "0110011"

        #Seleccionar el funct7  de cada instrucción
        if mnemonic == "sub":
            funct7 = "0100000"
        else:
            funct7 = "0000000"
        print(f"funct7 Value: {funct7}")

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "add" or mnemonic == "sub":
            funct3 = "000"
        elif mnemonic == "and":
            funct3 = "111"
        elif mnemonic == "or":
            funct3 = "110"
        print(f"funct3 Value: {funct3}")

        #Convertir los registros a binario
        rd = format(int(registers[0][1:]), '05b')
        rs1 = format(int(registers[1][1:]), '05b')
        rs2 = format(int(registers[2][1:]), '05b')
        print(f"rd Value: {rd}")
        print(f"rs1 Value: {rs1}")
        print(f"rs2 Value: {rs2}")  

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = int(f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}", 2)
        print(f"32-bit encoding: {cod_32bits:032b}")  

    #Validar las instrucciones de Tipo I y convertir a binario en un formato de 32 bits
    elif mnemonic == "addi" or mnemonic == "andi" or mnemonic == "lw" or mnemonic == "lb":
        format_type = "I"

        #Seleccionar el opcode de cada instrucción
        if mnemonic == "addi" or mnemonic == "andi":
            opcode = "0010011"
        elif mnemonic == "lw" or mnemonic == "lb":
            opcode = "0000011"

        print(f"opcode Value: {opcode}")

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "addi" or mnemonic == "lb":
            funct3 = "000"
        elif mnemonic == "andi":
            funct3 = "111"
        elif mnemonic == "lw":
            funct3 = "010"
        print(f"funct3 Value: {funct3}")

        #Convertir los registros a binario
        rd = format(int(registers[0][1:]), '05b')
        rs1 = format(int(registers[1][1:]), '05b')
        imm = format(int(registers[2]), '012b')  # Immediate value is 12 bits
        print(f"rd Value: {rd}")
        print(f"rs1 Value: {rs1}")
        print(f"Immediate Value: {imm}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = int(f"{imm}{rs1}{funct3}{rd}{opcode}", 2)
        print(f"32-bit encoding: {cod_32bits:032b}") 

    #Validar las instrucciones de Tipo S y convertir a binario en un formato de 32 bits
    elif mnemonic == "sw" or mnemonic == "sb":
        format_type = "S"  # Load/store instructions use I

    #Validar las instrucciones de Tipo B y convertir a binario en un formato de 32 bits
    elif mnemonic == "beq" or mnemonic == "bne":
        format_type = "B"

    #Validar las instrucciones de Tipo R y convertir a binario en un formato de 32 bits
    else:
        format_type = "Unknown" 

    print(f"Format type: {format_type}")

    print("the mnemonic:")
    print(mnemonic)
    print("the registers:")
    print(registers)

    return cod_32bits

    #raise NotImplementedError("encode_instruction: pendiente de implementar para la instrucción")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    # TODO: implementar.
    #raise NotImplementedError("explain_instruction: pendiente de implementar")

    print("the instruction:")
    print(instruction)
    print("the word:")
    print(f"{word:032b}")  # Print the word in binary format    

    textPrint = f"Instruction: {word}\n"
    return textPrint


def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print("the instruction:")
    print(instruction)
    print("the word:")
    print(f"{word:032b}")  # Print the word in binary format

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()

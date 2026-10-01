#!/usr/bin/env python3
"""
Código de desarrollo del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II
Estudiante : [Heizel Tatiana Chacón Mora]

Esta es una herramienta que traduce una única instrucción del 
subconjunto RISC-V RV32I  a su codificacion binaria de 32 bits, 
mostrando de forma visual el significado de cada campo del 
formato correspondiente (R, I, S o B). 

"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]

def get_instruction_format(instruction: str) -> str:
    """
    Recibe el mnemonico de la instrucción como texto, y debe
    retornar el formato de la instrucción: "R", "I", "S" o "B".

    Debe soportar únicamente las instrucciones en SOPORTADAS.
    """
    if instruction in ["add", "sub", "and", "or"]:
        return "R"
    elif instruction in ["addi", "andi", "lw", "lb"]:
        return "I"
    elif instruction in ["sw", "sb"]:
        return "S"
    elif instruction in ["beq", "bne"]:
        return "B"
    else:
        raise ValueError(f"Instrucción no soportada: {instruction}")


def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).
    """
    #Inicializar variables
    opcode = funct3 = funct7 = rs1 = rs2 = rd = cod_32bits = " "
    out_word = 0  # Initialize out_word to 0

    #Dividir la instrucción en sus componentes: mnemonico y registros
    splitInstruction = instruction.split(" ")
    mnemonic = splitInstruction[0]
    registers = [reg.strip(",") for reg in splitInstruction[1:]]
    format_type = get_instruction_format(mnemonic)

    #Convertir el registro destino rd a binario
    rd = format(int(registers[0][1:]), '05b')

    #Validar las instrucciones de Tipo R y convertir a binario en un formato de 32 bits
    if format_type == "R":
        opcode = "0110011"

        rs1 = format(int(registers[1][1:]), '05b')
        # print(f"rs1 Value: {rs1}")

        rs2 = format(int(registers[2][1:]), '05b')
        # print(f"rs2 Value: {rs2}") 

        #Seleccionar el funct7  de cada instrucción
        if mnemonic == "sub":
            funct7 = "0100000"
        else:
            funct7 = "0000000"
        #print(f"funct7 Value: {funct7}")

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "add" or mnemonic == "sub":
            funct3 = "000"
        elif mnemonic == "and":
            funct3 = "111"
        elif mnemonic == "or":
            funct3 = "110"
        # print(f"funct3 Value: {funct3}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"

    #Validar las instrucciones de Tipo I y convertir a binario en un formato de 32 bits
    elif format_type == "I":
        inm = 0  # Initialize immediate value
        inm_str = " "

        #Seleccionar el opcode de cada instrucción
        if mnemonic == "addi" or mnemonic == "andi":
            opcode = "0010011"
            #Seleccionar el inmediate value de la instrucción
            inm_str = registers[2]
            #print(f"Immediate Value ------------: {inm_str}")
            #print(type(inm_str))
            rs1 = format(int(registers[1][1:]), '05b')

            if inm_str.startswith('-'):
                imm = format(int(inm_str) & 0xFFF, '012b')  # Handle negative immediate values
            else:           
                imm = format(int(inm_str), '012b')  # Immediate value is 12 bits
        elif mnemonic == "lw" or mnemonic == "lb":
            opcode = "0000011"
            #Seleccionar el inmediate value de la instrucción
            inm_str, rs1 = registers[1].split('(')
            rs1 = rs1.rstrip(')')
            rs1 = format(int(rs1[1:]), '05b')  # Update rs1 based on the register in parentheses

            if inm_str.startswith('-'):
                imm = format(int(inm_str) & 0xFFF, '012b')  # Handle negative immediate values
            else:           
                imm = format(int(inm), '012b')  # Immediate value is 12 bits    
        #print(f"rs1 Value: {rs1}")
        #print(f"Immediate Value: {imm}")

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "addi":
            funct3 = "000"
        elif mnemonic == "andi":
            funct3 = "111"
        elif mnemonic == "lb":
            funct3 = "000"
        elif mnemonic == "lw":
            funct3 = "010"
        #print(f"funct3 Value: {funct3}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = f"{imm}{rs1}{funct3}{rd}{opcode}"

    #Validar las instrucciones de Tipo S y convertir a binario en un formato de 32 bits
    elif format_type == "S":
        inm = 0  # Initialize immediate value
        opcode = "0100011"

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "sw":
            funct3 = "010"
        elif mnemonic == "sb":
            funct3 = "000"

        #Seleccionar el inmediate value de la instrucción
        inm, rs1 = registers[1].split('(')
        rs1 = rs1.rstrip(')')
        rs1 = format(int(rs1[1:]), '05b')  # Update rs1 based on the register in parentheses

        # Convertir immediate a entero y obtener representación de 12 bits
        inm = int(inm)
        imm = format(inm & 0xFFF, '012b')

        #print(f"rs1 Value: {rs1}")
        #print(f"Immediate Value: {imm}")
        #print(f"funct3 Value: {funct3}")

        # Separar immediate en los campos de una instrucción S
        inm_high = imm[0:7]   # Bits 11:5
        inm_low = imm[7:12]   # Bits 4:0

        #print(f"Immediate [11:5]: {inm_high}")
        #print(f"Immediate [4:0]: {inm_low}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = f"{inm_high}{rd}{rs1}{funct3}{inm_low}{opcode}"

    #Validar las instrucciones de Tipo B y convertir a binario en un formato de 32 bits
    elif format_type == "B":
        opcode = "1100011"
        
        rs1 = format(int(registers[0][1:]), '05b')
        #print(f"rs1 Value: {rs1}")
        rs2 = format(int(registers[1][1:]), '05b')
        #print(f"rs2 Value: {rs2}") 

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "beq":
            funct3 = "000"
        elif mnemonic == "bne":
            funct3 = "001"
        #print(f"funct3 Value: {funct3}")        

        #Seleccionar el inmediate value de la instrucción y convertir a entero y obtener representación de 12 bits
        inm = int(registers[2])
        imm = format(inm & 0xFFF, '012b')
        #print(f"Immediate Value: {imm}")

        # Separar immediate en los campos de una instrucción S
        inm_high = imm[0:7]   # Bits 11:5
        inm_low = imm[7:12]   # Bits 4:0

        #print(f"Immediate [11:5]: {inm_high}")
        #  print(f"Immediate [4:0]: {inm_low}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = f"{inm_high}{rd}{rs1}{funct3}{inm_low}{opcode}"

    #Validar las instrucciones de Tipo R y convertir a binario en un formato de 32 bits
    else:
        format_type = "Unknown" 

    #print(f"Format type: {format_type}")
    #print(f"opcode Value: {opcode}")

    #print (f"the cod_32bits binary:")
    #print(cod_32bits)

    #print(f"the cod_32bits as integer:")    
    out_word = int(cod_32bits, 2)
    #print(out_word)
    #print(f"the cod_32bits as hex:")
    #print(f"0x{out_word:08x}")  
    #print("--------------------------------------")

    return out_word  # Return the encoded instruction as an integer


def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    splitInstruction = instruction.split(" ")
    mnemonic = splitInstruction[0]
    format_type = get_instruction_format(mnemonic)
    registers = [reg.strip(",") for reg in splitInstruction[1:]]
    
    new_word = format(word, '032b')  # Convert the integer to a 32-bit binary string
    textPrint = " "

    if format_type == "R":
        rd = new_word[20:25]
        funct3 = new_word[17:20]
        rs1 = new_word[12:17]
        rs2 = new_word[7:12]
        funct7 = new_word[0:7]
        opcode = new_word[25:33]

        textPrint = f"""
                ================================================
                The instruction: {instruction}
                mnemonic rd, rs1, rs2
                ================================================
                Formato R
                ================================================
                Bits [31:25] | funct7  | {funct7}
                Bits [24:20] | rs2     | {rs2}
                Bits [19:15] | rs1     | {rs1}
                Bits [14:12] | funct3  | {funct3}
                Bits [11:7]  | rd      | {rd}
                Bits [6:0]   | opcode  | {opcode}
                ================================================
                WORD: {new_word}
        
                mnemonic rd, rs1, rs2
                funct7: determina la operación específica.
                rs2: registro fuente 2.
                rs1: registro fuente 1.
                funct3: especifica la operación.
                rd: registro destino.
                opcode: identifica el tipo de instrucción de tipo R.
                """
        
    elif format_type == "I":
        imm = new_word[0:12]
        rs1 = new_word[12:17]
        funct3 = new_word[17:20]
        rd = new_word[20:25]
        opcode = new_word[25:32]

        inm_str = int(imm, 2)  # Convert binary string to integer
        if inm_str >= 2**11:  # Si el bit de signo es 1
            inm_str -= 2**12

        textPrint = f"""
                ================================================
                The instruction: {instruction}
                mnemonic rd, rs1, inm
                mnemonic rd, inm(rs1)
                ================================================
                Formato I
                ================================================
                Bits [31:20] | imm     | {imm}
                Bits [19:15] | rs1     | {rs1}
                Bits [14:12] | funct3  | {funct3}
                Bits [11:7]  | rd      | {rd}
                Bits [6:0]   | opcode  | {opcode}
                ================================================
                WORD: {new_word}
        
                imm: valor inmediato.
                rs1: registro fuente.
                funct3: especifica la operación.
                rd: registro destino.
                opcode: identifica el tipo de instrucción de tipo I.
                """
        
    elif format_type == "S":
        imm_high = new_word[0:7]
        rs2 = new_word[7:12]
        rs1 = new_word[12:17]
        funct3 = new_word[17:20]
        imm_low = new_word[20:25]
        opcode = new_word[25:32]

        imm = imm_high + imm_low
        inm_str = int(imm, 2)  # Convert binary string to integer
        if inm_str >= 2**11:  # Si el bit de signo es 1
            inm_str -= 2**12

        textPrint = f"""
                ================================================
                The instruction: {instruction}
                mnemonic rs2, inm(rs1)
                ================================================
                Formato S
                ================================================
                Bits [31:25] | imm[11:5] | {imm_high}
                Bits [24:20] | rs2       | {rs2}
                Bits [19:15] | rs1       | {rs1}
                Bits [14:12] | funct3    | {funct3}
                Bits [11:7]  | imm[4:0]  | {imm_low}
                Bits [6:0]   | opcode    | {opcode}
                ================================================
                WORD: {new_word}
        
                imm: desplazamiento/inmediato dividido en dos partes.
                rs2: registro que contiene el valor a almacenar.
                rs1: registro base.
                funct3: especifica el tipo de almacenamiento.
                opcode: identifica la instrucción de tipo store.
                """  
             
    elif format_type == "B":
        imm_high = new_word[0:7]
        rs2 = new_word[7:12]
        rs1 = new_word[12:17]
        funct3 = new_word[17:20]
        imm_low = new_word[20:25]
        opcode = new_word[25:32]

        imm = imm_high + imm_low
        inm_str = int(imm, 2)  # Convert binary string to integer
        if inm_str >= 2**11:  # Si el bit de signo es 1
            inm_str -= 2**12

        textPrint = f"""
                ================================================
                The instruction: {instruction}
                mnemonic rs2, rs1, inm
                ================================================
                Formato B
                ================================================
                Bits [31]    | imm[12]   | {imm_high[0]}
                Bits [30:25] | imm[10:5] | {imm_high[1:7]}
                Bits [24:20] | rs2       | {rs2}
                Bits [19:15] | rs1       | {rs1}
                Bits [14:12] | funct3    | {funct3}
                Bits [11:8]  | imm[4:1]  | {imm_low[0:4]}
                Bits [7]     | imm[11]   | {imm_low[4]}
                Bits [6:0]   | opcode    | {opcode}
                ================================================
                WORD: {new_word}
        
                imm: desplazamiento utilizado para calcular el salto.
                rs2: segundo registro fuente.
                rs1: primer registro fuente.
                funct3: determina la condición de salto.
                opcode: identifica una instrucción de tipo branch.
                 """

       
    else:
        print(f"Unknown instruction format: {format_type}")
        textPrint = "Formato no válido. Use R, I, S o B."
        

    return textPrint

 
def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()

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
import tkinter as tk

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

    print("--------------------------------------")
    print("the mnemonic:")
    print(mnemonic)
    print("the registers:")
    print(registers)

    #Convertir el registro destino rd a binario
    rd = format(int(registers[0][1:]), '05b')
    print(f"rd Value: {rd}")

    #Validar las instrucciones de Tipo R y convertir a binario en un formato de 32 bits
    if format_type == "R":
        opcode = "0110011"

        rs1 = format(int(registers[1][1:]), '05b')
        print(f"rs1 Value: {rs1}")

        rs2 = format(int(registers[2][1:]), '05b')
        print(f"rs2 Value: {rs2}") 

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
            print(f"Immediate Value ------------: {inm_str}")
            print(type(inm_str))
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
        print(f"rs1 Value: {rs1}")
        print(f"Immediate Value: {imm}")

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "addi":
            funct3 = "000"
        elif mnemonic == "andi":
            funct3 = "111"
        elif mnemonic == "lb":
            funct3 = "000"
        elif mnemonic == "lw":
            funct3 = "010"
        print(f"funct3 Value: {funct3}")

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

        print(f"rs1 Value: {rs1}")
        print(f"Immediate Value: {imm}")
        print(f"funct3 Value: {funct3}")

        # Separar immediate en los campos de una instrucción S
        inm_high = imm[0:7]   # Bits 11:5
        inm_low = imm[7:12]   # Bits 4:0

        print(f"Immediate [11:5]: {inm_high}")
        print(f"Immediate [4:0]: {inm_low}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = f"{inm_high}{rd}{rs1}{funct3}{inm_low}{opcode}"

    #Validar las instrucciones de Tipo B y convertir a binario en un formato de 32 bits
    elif format_type == "B":
        opcode = "1100011"
        
        rs1 = format(int(registers[0][1:]), '05b')
        print(f"rs1 Value: {rs1}")
        rs2 = format(int(registers[1][1:]), '05b')
        print(f"rs2 Value: {rs2}") 

        #Seleccionar el funct3 de cada instrucción
        if mnemonic == "beq":
            funct3 = "000"
        elif mnemonic == "bne":
            funct3 = "001"
        print(f"funct3 Value: {funct3}")        

        #Seleccionar el inmediate value de la instrucción y convertir a entero y obtener representación de 12 bits
        inm = int(registers[2])
        imm = format(inm & 0xFFF, '012b')
        print(f"Immediate Value: {imm}")

        # Separar immediate en los campos de una instrucción S
        inm_high = imm[0:7]   # Bits 11:5
        inm_low = imm[7:12]   # Bits 4:0

        print(f"Immediate [11:5]: {inm_high}")
        print(f"Immediate [4:0]: {inm_low}")

        #Combinar los campos en un solo valor de 32 bits
        cod_32bits = f"{inm_high}{rd}{rs1}{funct3}{inm_low}{opcode}"

    #Validar las instrucciones de Tipo R y convertir a binario en un formato de 32 bits
    else:
        format_type = "Unknown" 

    print(f"Format type: {format_type}")
    print(f"opcode Value: {opcode}")

    print (f"the cod_32bits binary:")
    print(cod_32bits)

    print(f"the cod_32bits as integer:")    
    out_word = int(cod_32bits, 2)
    print(out_word)
    print(f"the cod_32bits as hex:")
    print(f"0x{out_word:08x}")  
    print("--------------------------------------")

    return out_word  # Return the encoded instruction as an integer


def create_canvas():
    """
    Crea un lienzo de Tkinter para mostrar la representación visual de los
    campos de la instrucción.
    """
    root = tk.Tk()
    root.title("Visualización de Instrucción RISC-V")
    canvas = tk.Canvas(root, width=800, height=200)
    canvas.pack()
    return root, canvas

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

    # Crear ventana
    ventana = tk.Tk()

    # Título
    ventana.title("Codificador RISC-V")
    # Tamaño de la ventana
    ventana.geometry("930x800")

    # Crear el área de dibujo
    canvas = tk.Canvas(ventana, width=850, height=380, bg="white")
    canvas.place(x=465, y=270, anchor="center")

    # Crear el área de dibujo
    canvas_text = tk.Canvas(ventana, width=850, height=300, bg="white")
    canvas_text.place(x=465, y=620, anchor="center")

    # Texto
    etiqueta = tk.Label(
        ventana,
        text="Codificador de instrucciones RISC-V",
        font=("Times New Roman", 20)
    )
    etiqueta.place(x=465, y=35, anchor="center")
    
    new_word = format(word, '032b')  # Convert the integer to a 32-bit binary string
    if format_type == "R":
        rd = new_word[20:25]
        funct3 = new_word[17:20]
        rs1 = new_word[12:17]
        rs2 = new_word[7:12]
        funct7 = new_word[0:7]
        opcode = new_word[25:33]

        #canvas.create_rectangle(30, 60, 798, 190, fill="lightblue")
        x1, y1 = 30, 40
        canvas.create_rectangle(x1, y1, x1+24.5*7, 190, fill="#76C3CF")
        canvas.create_text((x1 + x1+24.5*7) / 2, y1 + 170, text=f"funct7: {int(funct7, 2)}", font=("Times New Roman", 10))
        canvas.create_text((x1 + x1+24.5*7) / 2, y1 + 195, text=f"{funct7}", font=("Times New Roman", 10))
        canvas.create_text((x1 + x1+24.5*7) / 2, y1 + 220, text="(bits 31-25)", font=("Times New Roman", 10))

        canvas.create_rectangle(x1+24.5*7, y1, x1+25*12, 190, fill="#5252B7")
        canvas.create_text((x1+24.5*7 + x1+25*12) / 2, y1 + 170, text=f"rs2: {int(rs2, 2)}", font=("Times New Roman", 10))
        canvas.create_text((x1+24.5*7 + x1+25*12) / 2, y1 + 195, text=f"{rs2}", font=("Times New Roman", 10))
        canvas.create_text((x1+24.5*7 + x1+25*12) / 2, y1 + 220, text="(bits 24-20)", font=("Times New Roman", 10))

        canvas.create_rectangle(x1+25*12, y1, x1+25*17, 190, fill="#587BE2")
        canvas.create_text((x1+25*12 + x1+25*17) / 2, y1 + 170, text=f"rs1: {int(rs1, 2)}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*12 + x1+25*17) / 2, y1 + 195, text=f"{rs1}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*12 + x1+25*17) / 2, y1 + 220, text="(bits 19-15)", font=("Times New Roman", 10))

        canvas.create_rectangle(x1+25*17, y1, x1+25*20, 190, fill="#36A6C5")
        canvas.create_text((x1+25*17 + x1+25*20) / 2, y1 + 170, text=f"funct3: {int(funct3, 2)}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*17 + x1+25*20) / 2, y1 + 195, text=f"{funct3}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*17 + x1+25*20) / 2, y1 + 220, text="(bits 12-14)", font=("Times New Roman", 10))

        canvas.create_rectangle(x1+25*20, y1, x1+25*25, 190, fill="#8AB9E3")
        canvas.create_text((x1+25*20 + x1+25*25) / 2, y1 + 170, text=f"rd: {int(rd, 2)}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*20 + x1+25*25) / 2, y1 + 195, text=f"{rd}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*20 + x1+25*25) / 2, y1 + 220, text="(bits 11-7)", font=("Times New Roman", 10))

        canvas.create_rectangle(x1+25*25, y1, x1+25*32, 190, fill="#5355E8")
        canvas.create_text((x1+25*25 + x1+25*32) / 2, y1 + 170, text=f"opcode: {int(opcode, 2)}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*25 + x1+25*32) / 2, y1 + 195, text=f"{opcode}", font=("Times New Roman", 10))
        canvas.create_text((x1+25*25 + x1+25*32) / 2, y1 + 220, text="(bits 6-0)", font=("Times New Roman", 10))

        for i in range(1, 33):
            x1_plus = 49*i+i
            canvas.create_text((x1 + x1_plus) / 2, y1 + 65, text=f"{new_word[i-1]}", font=("Times New Roman", 15,"bold"),fill="white")

        canvas.create_text(x1 + 400, y1 + 270, text=instruction, font=("Times New Roman", 22, "italic"))
        canvas.create_text(x1 + 400, y1 + 310, text=f"0x{word:08x}", font=("Times New Roman", 20, "italic"))

        canvas_text.create_text(x1 + 400, y1, text=f"opcode: Identifica la instrucción como operación tipo R", font=("Times New Roman", 12, "italic"),anchor="center")
        canvas_text.create_text(x1 + 400, y1 + 45, text=f"rd: Registro destino {registers[0]}", font=("Times New Roman", 12, "italic"))
        canvas_text.create_text(x1 + 400, y1 + 90, text="funct3: Determina el tipo de operación ", font=("Times New Roman", 12, "italic"))
        canvas_text.create_text(x1 + 400, y1 + 135, text=f"rs1: Registro fuente {registers[1]}", font=("Times New Roman", 12, "italic"))
        canvas_text.create_text(x1 + 400, y1 + 180, text=f"rs2: Registro fuente {registers[2]}", font=("Times New Roman", 12, "italic"))
        canvas_text.create_text(x1 + 400, y1 + 225, text="funct7: Identifica la operación específica", font=("Times New Roman", 12, "italic"))

        print(f"R-type instruction fields:")
        print(f"funct7: {funct7} (bits 31-25)")
        print(f"rs2: {rs2} (bits 24-20)")
        print(f"rs1: {rs1} (bits 19-15)")
        print(f"funct3: {funct3} (bits 14-12)")
        print(f"rd: {rd} (bits 11-7)")
        print(f"opcode: {opcode} (bits 6-0)")
    elif format_type == "I":
        imm = new_word[0:12]
        rs1 = new_word[12:17]
        funct3 = new_word[17:20]
        rd = new_word[20:25]
        opcode = new_word[25:32]

        print(f"I-type instruction fields:")
        print(f"imm: {imm} (bits 31-20)")
        print(f"rs1: {rs1} (bits 19-15)")
        print(f"funct3: {funct3} (bits 14-12)")
        print(f"rd: {rd} (bits 11-7)")
        print(f"opcode: {opcode} (bits 6-0)")
    elif format_type == "S":
        imm_high = new_word[0:7]
        rs2 = new_word[7:12]
        rs1 = new_word[12:17]
        funct3 = new_word[17:20]
        imm_low = new_word[20:25]
        opcode = new_word[25:32]

        print(f"S-type instruction fields:")
        print(f"imm[11:5]: {imm_high} (bits 31-25)")
        print(f"rs2: {rs2} (bits 24-20)")
        print(f"rs1: {rs1} (bits 19-15)")
        print(f"funct3: {funct3} (bits 14-12)")
        print(f"imm[4:0]: {imm_low} (bits 11-7)")
        print(f"opcode: {opcode} (bits 6-0)")
    elif format_type == "B":
        imm_high = new_word[0:7]
        rs2 = new_word[7:12]
        rs1 = new_word[12:17]
        funct3 = new_word[17:20]
        imm_low = new_word[20:25]
        opcode = new_word[25:32]

        print(f"B-type instruction fields:")
        print(f"imm[11:5]: {imm_high} (bits 31-25)")
        print(f"rs2: {rs2} (bits 24-20)")
        print(f"rs1: {rs1} (bits 19-15)")
        print(f"funct3: {funct3} (bits 14-12)")
        print(f"imm[4:0]: {imm_low} (bits 11-7)")
        print(f"opcode: {opcode} (bits 6-0)")
    else:
        print(f"Unknown instruction format: {format_type}")

    print("--------------------------------------")
    print(f"Format type: {format_type}")
    print("the instruction:")
    print(instruction)
    print("the word integer:")  
    print(word) 
    print("the word binary:")
    word = format(word, '032b')  # Convert the integer to a 32-bit binary string
    print(word)
    print("--------------------------------------")

    # Mantener la ventana abierta
    ventana.mainloop()

    textPrint = "Colocar aqui la palabra de entero a binario de 32 bits y explicar los campos de la instrucción"
    return textPrint

 
def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print("the instruction:  (main)")
    print(instruction)
    print("the word:         (main)")
    print(f"{word:032b}")  # Print the word in binary format

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()

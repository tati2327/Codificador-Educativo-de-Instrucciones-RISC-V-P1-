import subprocess
import re

def iniciar_programa():
    # Ejecutar objdump
    resultado = subprocess.run(
        [
            "riscv64-unknown-elf-objdump",
            "-d",
            "-M", "no-aliases,numeric",
            "programa.o"
        ],
        capture_output=True,
        text=True
    )

    salida = resultado.stdout

    # Buscar instrucciones de 32 bits
    for linea in salida.splitlines():

        # Ejemplo:
        # 0: 006a03b3 add x7,x20,x6

        match = re.search(
            r'^\s*[0-9a-f]+:\s+([0-9a-f]{8})\s+(.*)$',
            linea
        )

        if match:

            hexadecimal = match.group(1)
            instruccion = match.group(2)

            # Convertir hexadecimal a entero
            valor = int(hexadecimal, 16)

            # Convertir a binario de exactamente 32 bits
            binario = format(valor, "032b")

            print(f"{instruccion}")
            print(f"Hexadecimal: {hexadecimal}")
            print(f"Binario:     {binario}")
            print()


iniciar_programa()
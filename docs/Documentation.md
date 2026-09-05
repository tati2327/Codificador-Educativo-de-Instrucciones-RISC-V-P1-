# Codificador Educativo de Instrucciones RISC-V. 

*Este proyecto consiste en desarrollar una herramienta que traduce una única instrucción 
del subconjunto RISC-V RV32I a su codificacion binaria de 32 bits, mostrando de 
forma visual el significado de cada campo del formato correspondiente (R, I, S o B).*

## Arquitectura del código y decisiones de diseño

El flujo general del programa consiste en recibir una instrucción en formato ensamblador, identificar su mnemónico y operandos o registros, al extraer estos valores se van seleccionando los demás valores según la instrucción a codificar, de manera que al tener cada campo que forma parte de instrucción en código binario se crea una sola variable con cada campo de bits contatenado en el orden correspondiente

La arquitectura del programa se divide en las siguientes etapas:

### *1. Entrada y análisis de la instrucción:*
Se recibe la instrucción escrita en lenguaje ensamblador y se separa en su mnemónico y operandos o registros.

### *2.Identificación del formato:*
Según el mnemónico, el programa determina si la instrucción corresponde al formato R, I, S o B.

### *Obtención de los campos de codificación:*
Según el formato de la instrucción se obtienen los valores correspondientes a opcode, funct3 y, cuando corresponde, funct7. Además, los registros e inmediatos son convertidos a su representación binaria.

### *Codificación según el formato:*
Cada formato posee una distribución diferente de sus campos dentro de los 32 bits. Por esta razón, la construcción de la instrucción se realiza de acuerdo con las posiciones definidas para cada formato.

### *Generación de la salida:*
El programa muestra el formato identificado, la codificación completa en binario, decimal y hexadecimal, así como una representación visual de los campos que forman la instrucción.

Como decisión de diseño, se separó la codificación de cada formato para facilitar la comprensión, validación y mantenimiento del programa. Esto permite que las reglas específicas de los formatos R, I, S y B se implementen de manera independiente.

## *Funciones utilizadas para desarrollar la herramienta para codificar*

```
def get_instruction_format(instruction: str) -> str:
    """
    Recibe el mnemonico de la instrucción como texto, y debe
    retornar el formato de la instrucción: "R", "I", "S" o "B".

    Debe soportar únicamente las instrucciones en SOPORTADAS.
    """
```

```
def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
```

## Fuente consultada para los campos de codificación de cada instrucción.
Para obtener la informacion acerca de los valores de *funct7, funct y opcode* de cada instrucción se consultó el *Manual del Set de Instrucciones RISC-V, Volumen I* documentado en la parte de la bibliogafia de esta documentsción.

En la página número 16 se describe gráficamente con una tabla las distribuciones de los bits de cada instrucción, a continuación se adjunta 
una imagen con la informacion correspondiente.

![RISC-V base instruction formats](https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-/blob/main/images/Captura%20de%20pantalla%202026-08-31%20083831.png)

Más adelante en el manual en la página número 130 se brindan unas tablas con los valores de *funct7, funct y opcode* de cada instrucción, a continuación se adjunta una imagen con la informacion correspondiente.

![RISC-V base instruction part one](https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-/blob/main/images/Captura%20de%20pantalla%202026-08-31%20084415.png)

![RISC-V base instruction part two](https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-/blob/main/images/Captura%20de%20pantalla%202026-08-31%20084426.png)

### *Evidencia de la validaci´on contra el toolchain oficial.*

![Salida de desemsamblar codigo objdump](https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-/blob/main/images/Captura%20de%20pantalla%202026-09-04%20182106.png)

![Archivo de instrucciones emsambladas]([https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-/blob/main/images/Captura%20de%20pantalla%202026-08-31%20084426.png](https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-/blob/main/images/Captura%20de%20pantalla%202026-09-04%20182249.png))


# Bibliografía 

[ 1 ]   Andrew Waterman and Krste Asanoviç. *The RISC-V Instruction Set Manual, Volume I:
User-Level ISA, Document Version 20191213.* RISC-V Foundation, 2019.

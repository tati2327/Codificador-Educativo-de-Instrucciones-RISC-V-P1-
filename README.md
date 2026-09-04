# Codificador Educativo de Instrucciones RISC-V

Código de desarrollo para una herramienta que traduce una instrucción del subconjunto **RISC-V RV32**  
a su codificacion binaria de 32 bits, mostrando de forma visual el significado de cada campo del 
formato correspondiente (R, I, S o B).

El programa permite recibir instrucciones en lenguaje ensamblador y generar su representación en 
código máquina.


## Inicio rápido
A continuación en esta sección se brindan los pasos mínimos para instalar y ejecutar el proyecto.

* Actualizar la lista de paquetes de Ubuntu e instalar las herramientas necesarias para el proyecto

```
sudo apt update
sudo apt install python3 python3-tk gcc-riscv64-unknown-elf git
```
Las herramientas que se utilizan en el proyecto cumplen las siguientes funciones:

| Paquete | Función |
|---------|---------|
| `python3` | Ejecutar el programa desarrollado en Python |
| `python3-tk` | Permite utilizar la interfaz gráfica Tkinter |
| `gcc-riscv64-unknown-elf` | Proporciona el toolchain para trabajar con RISC-V |
| `git` | Permite descargar el repositorio mediante Git |

El paquete del toolchain proporciona herramientas para ensamblar instrucciones RISC-V como:

```
riscv64-unknown-elf-as
```
 y para desensamblar e inspeccionar el código generado como:

```
riscv64-unknown-elf-objdump
```


* Clonar el repositorio
Este comando `git clone` descarga una copia del repositorio de GitHub a la computadora. Y con el comando
cd que significa change directory (cambiar de directorio) se accedea la carpeta del repositorio
clonado.
```
git clone https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-.git
cd Codificador-Educativo-de-Instrucciones-RISC-V-P1-
```

* Dar permisos de ejecución a `run.sh`
En Linux, un archivo debe tener permiso de ejecución para poder ejecutarse como programa.
Con el comando `chmod` se cambia los permisos de un archivo, con `+x` se agrega permiso de ejecución
y `run.sh` es el archivo al que se le aplican los permisos. Después de la primer línea de este comando,
puedes ejecutar el script con `./run.sh` agregando la instrucción a codificar.
```
chmod +x run.sh
./run.sh "add x7, x20, x6"
```

---

# Requisitos previos

Para tener éxito al ejecutar el proyecto es necesario instalar las siguientes herramientas:

- WSL con Ubuntu
- Python 3
- Tkinter
- Toolchain de RISC-V
- Ensamblador RISC-V
- Objdump
- Git

---

# 1. Instalación de WSL y actualizar Ubuntu

Este proyecto fue desarrollado utilizando **Windows Subsystem for Linux (WSL)** con Ubuntu.

Abra PowerShell como administrador y ejecute:
```
wsl --install       # Para instalar wsl
wsl               # Para ingresar a Ubuntu
```

Una vez dentro de WSL, actualice los paquetes de Ubuntu:
```
sudo apt update
sudo apt upgrade
```

# 2. Instalación de Python
Verifique si Python está instalado:
```
python3 --version
```

Si no está instalado, puede hacerlo con el siguiente comando, además se recomienda instalar pip:
```
sudo apt install python3
sudo apt install python3-pip
```

Verifique la instalación con
```
python3 --version
pip3 --version
```

# 3. Instalación de Tkinter
La interfaz gráfica del proyecto utiliza Tkinter. Desde la terminal de wsl instale la dependencia
con el comando:
```
sudo apt install python3-tk
```
Para verificar que Tkinter funciona correctamente:
```
python3 -m tkinter
```
Si la instalación funciona correctamente, debería aparecer una ventana de prueba.

# 4. Instalación del Toolchain de RISC-V
Para validar la herramienta se utilizará un toolchain de `risc-v` para ensamblar las instrucciones:
```
sudo apt update
sudo apt install gcc-riscv64-unknown-elf
```
Este paquete proporciona herramientas como:
* `riscv64-unknown-elf-gcc`
* `riscv64-unknown-elf-as`
* `riscv64-unknown-elf-objdump`
  
Aunque el proyecto trabaja con instrucciones RV32, se puede utilizar este toolchain especificando la arquitectura RV32.

Para verificar la instalación:
```
riscv64-unknown-elf-gcc --version
riscv64-unknown-elf-as --version
riscv64-unknown-elf-objdump --version
```
# 5. Ensamblar instrucciones RISC-V RV32
Para ensamblar una o m[as instrucciones es necesario un archivo de tipo ensamblador `.s`
Por ejemplo un archivo como:
```
programa.s
```
Con el siguiente contenido:
```
.text

main:
    add x7, x20, x6
    add x14, x26, x31
```
Para ensamblarlo utilizando la arquitectura RV32 es necesaria la siguiente línea de comando:
```
riscv64-unknown-elf-as -march=rv32i -mabi=ilp32 programa.s -o programa.o
```

Esto generará el archivo:
```
programa.o
```

# 6. Desensamblar con objdump
Para visualizar las instrucciones ensambladas en `programa.s` se utiliza objdump de la siguiente manera:
```
riscv64-unknown-elf-objdump -d -M no-aliases programa.o
```

# 7. Clonar el repositorio
Para descargar el proyecto se utiliza Github, si no lo tiene instalado puede hacerlo con el comando:
```
sudo apt install git
```
Una vez instalado Github se puede clonar el repositorio con `git clone` para luego accederlo con 
el comando `cd` nombrado `change directory` y así cambiar de directorio.
```
git clone https://github.com/tati2327/Codificador-Educativo-de-Instrucciones-RISC-V-P1-.git
cd Codificador-Educativo-de-Instrucciones-RISC-V-P1-
```

De esta manera su computador quedará con todas las dependencias necesarias para ejecutar el
programa Codificador Educativo de Instrucciones RISC-V.

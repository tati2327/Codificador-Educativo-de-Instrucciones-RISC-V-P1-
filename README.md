# Codificador Educativo de Instrucciones RISC-V

Proyecto para la codificación y análisis de instrucciones de la arquitectura **RISC-V RV32**.

El programa permite recibir instrucciones en lenguaje ensamblador y generar su representación en código máquina.

## Inicio rápido

sudo apt update
sudo apt install python3 python3-tk gcc-riscv64-unknown-elf git

git clone <URL_DEL_REPOSITORIO>
cd Codificador-Educativo-de-Instrucciones-RISC-V-P1-

chmod +x run.sh

./run.sh "add x7, x20, x6"

---

# Requisitos previos

Antes de ejecutar el proyecto es necesario instalar las siguientes herramientas:

- WSL con Ubuntu
- Python 3
- Tkinter
- Toolchain de RISC-V
- Ensamblador RISC-V
- Objdump
- Git

---

# 1. Instalación de WSL

Este proyecto fue desarrollado utilizando **Windows Subsystem for Linux (WSL)** con Ubuntu.

Abra PowerShell como administrador y ejecute:

```powershell
wsl --install



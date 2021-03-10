# KiKit Script Example

This shows two ways to use [KiKit](https://github.com/yaqwsx/KiKit) to create a panel from a single [KiCAD](https://kicad.org/) PCB example board *temp.kicad_pcb*:
- the Command Line Interface (CLI): see the example *pannellizza.sh* bash script and the resulting *temp_panel_CLI.kicad_pcb*
- the Python library: see the example *panelizeBoard.py* python script and the resulting *temp_panel_SCRIPT.kicad_pcb*

The reason I switched to the library/script method is that I couldn't obtain what I *exactly* desired just by using the CLI; I still think that the CLI method is more than enough for most cases, but when needed the script method gives you more freedom and control.

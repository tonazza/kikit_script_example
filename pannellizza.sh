# comando per pannellizzare con Kikit
# https://github.com/yaqwsx/KiKit
# questo script è da eseguire in Linux o Ubuntu WSL (in windows non funziona)
# dopo aver installato kikit nell'ambiente Python desiderato,
# copiare questo script nella cartella dov'è presente il pcb ed eseguirlo
# per altri esempi, vedere questa pagina
# https://github.com/yaqwsx/KiKit/blob/master/doc/examples.md


# scheda temp.kicad_pcb
# dimensioni: x=43mm y=28mm
# pannello di 5 righe 4 colonne, con spazio fra le schede di 8mm per accomodare antenna
# la dimensione del pannello è calcolata per lasciare 6mm per parte sul bordo lungo


kikit panelize grid --gridsize 5 4 --hspace 8 --vspace 0 --vcuts --htabs 0 --vtabs 0 --tabsfrom Eco1.User 6 --tabsfrom Eco2.User 3 --radius 1 --railsTb 6 --copperfill ./temp.kicad_pcb ./temp_panel_CLI.kicad_pcb


# N.B. ho dovuto modificare l'impronta del modulo ESP32-WROOM-32E
# indicando lo spazio dell'antenna "a sbalzo" mediante un testo "ANTENNA" sul layer
# F.Fab, perché Kikit ignora i componenti i cui feature grafici (linee ecc)
# escono dall'area della scheda. Poi nel PCB ho spostato il testo "ANTENNA"
# sul layer Dwgs.user, in modo da poter ignorare come di consueto il layer F.Fab

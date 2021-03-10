'''
panelizeBoard.py

This script uses KiKit to create a panel of KiCAD pcbnew boards, following certain specific rules
It's a very specific example, thus likely not ready for any other uses.
However I think it can be a starting point for doing your own script

usage:

python3 panelizeBoard.py <boardfile.kicad_pcb> <panelfile.kicad_pcb>

Note: if using windows, you can only run kikit in WSL. Refer to the documentation

'''
__author__      = "Andrea Toninelli"
__copyright__   = "Do whatever you like with this file, as long as you don't consider me responsible for anything :)"


from kikit import panelize
import pcbnew
import sys

####################### CONSTANTS AND VARIABLES ####################################################

#board dimensions
altezzaScheda = 28   # board height
lunghezzaScheda = 43 # board length

# coordinates of panel origin
# NOTE: in pcbnew, Y increases going DOWN
panelOriginX = 15
panelOriginY = 19
panelOrigin = pcbnew.wxPointMM(panelOriginX, panelOriginY)

# panel configuration
righe = 5   #rows
colonne = 4 #columns
spazioOrizzontale = 8 # horizontal space between boards
spazioVerticale = 0 # vertical space between boards
diametroFresa = 2 # milling tool diameter
spessoreBinari = 6 # rails thickness

# in my case, i had to create a "high tab" and "low tab"
# in order to leave space for the WiFi module antenna
# those tabs then "merge" in the junction area of the boards
spessoreTabAlta = 5     #high tab thickness
spessoreTabBassa = 2    #low tab thickness
offsetVerticaleTabBassa = altezzaScheda - spessoreTabBassa #vertical offset of low tab


listaVCutsOrizzontali = []  # list of Y coordinates of horizontal Vcuts
listaVCutsVerticali = []    # list of X coordinates of vertical Vcuts
listaTabs = []  #list of tabs (wxRect objects)

#####################################################################################################


#initialize the panel variable
panel = panelize.Panel()

for c in range(colonne):    # for every column
    for r in range(righe):  # for every row
        #calculate board origin coordinates offsets from panelOrigin
        #NOTE: origin is top left corner
        origineSchedaX = c*(lunghezzaScheda+spazioOrizzontale)
        origineSchedaY = r*(altezzaScheda+spazioVerticale)
        #append the board
        posizione = panel.appendBoard(sys.argv[1], \
         panelOrigin + pcbnew.wxPointMM(origineSchedaX, origineSchedaY), \
         origin=panelize.Origin.TopLeft, \
         tolerance=panelize.fromMm(5))
        
        #in the last column, I add the horizontal Vcuts
        if (c==colonne-1):
            listaVCutsOrizzontali.append(panelOriginY + origineSchedaY) #board upper Vcut
            #since the vertical space between boards is 0, the board's lower Vcut is needed only in the last row
            if (r==righe-1): 
                listaVCutsOrizzontali.append(panelOriginY + origineSchedaY + altezzaScheda)
        
        #in the last row, I add the vertical Vcuts
        if (r==righe-1):
            if (c < colonne - 1): #board rightmost Vcut (not needed in the last column)
                listaVCutsVerticali.append(panelOriginX + origineSchedaX + lunghezzaScheda)
            if (c > 0): #board leftmost Vcut (not needed in the first column)
                listaVCutsVerticali.append(panelOriginX + origineSchedaX)
                

        #tab creation
        if (c > 0): # since tabs are created on the left side of the boards, they are not needed in the first colum
            #higher tab
            tabAlta = pcbnew.wxRectMM(panelOriginX + origineSchedaX - spazioOrizzontale, \
                                panelOriginY + origineSchedaY, \
                                spazioOrizzontale, \
                                spessoreTabAlta)
            listaTabs.append(tabAlta)
            #lower tab
            tabBassa = pcbnew.wxRectMM(panelOriginX + origineSchedaX - spazioOrizzontale, \
                                panelOriginY + origineSchedaY + offsetVerticaleTabBassa, \
                                spazioOrizzontale, \
                                spessoreTabBassa)
            listaTabs.append(tabBassa)
            
        

# tabs are appended to the panel
for t in listaTabs:
    panel.appendSubstrate(t)

# top and bottom rails are added
panel.makeRailsTb(panelize.fromMm(spessoreBinari))

# milling profile is added
# this also merges the areas where the mill cannot fit
# (in my case, high tab and low tab)
panel.addMillFillets(panelize.fromMm(diametroFresa))

#copperfill is added
panel.copperFillNonBoardAreas()

#vertical vcuts are added
for x in listaVCutsVerticali:
    panel.addVCutV(panelize.fromMm(x))

#horizontal vcuts are added
for y in listaVCutsOrizzontali:
    panel.addVCutH(panelize.fromMm(y))

#finally the panel is saved
panel.save(sys.argv[2])
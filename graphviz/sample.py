import graphviz
import datetime
import os

# https://graphviz.readthedocs.io/en/stable/api.html
# https://graphviz.gitlab.io/_pages/pdf/dotguide.pdf
# https://graphviz.gitlab.io/_pages/doc/info/lang.html

def PrintHelper(msg):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + msg )

def Main():
    PrintHelper("Application started.")
    outputDir = '/test-output/'
    CreateIndexPage(outputDir)
    PrintHelper("Application Completed.")
    return

def CreateIndexPage(outputDir):
    outputFileName = 'index'
    htmlFileName = "index.html"
    g = graphviz.Digraph(name='G', engine='dot')
    drawIndexNodes(g)
    GenerateOutput(g, outputDir, outputFileName, htmlFileName)
    return

def drawIndexNodes(g):
    g.node('unh', label='UNH Manchester', URL='https://manchester.unh.edu/', fillcolor='lightyellow',color='lightgreen',style='filled')
    g.node('apply', label='Apply Without\n Transfer', URL='https://admissions.unh.edu/apply', fillcolor='lightyellow',color='lightgreen',style='filled')
    g.node('transfer', label='Transfer')
    g.node('from_nhit', label='Concord Community College', URL='/transfer_college?college=nhit', fillcolor='lightyellow',color='lightgreen',style='filled')
    g.node('from_nashua', label='Nashua Community College', URL='/transfer_college?college=nashua', fillcolor='lightyellow',color='lightgreen',style='filled')
    g.node('from_mcc', label='Manchester Community College', URL='/transfer_college?college=mcc', fillcolor='lightyellow',color='lightgreen',style='filled')


    g.edge('unh', 'apply')
    g.edge('unh', 'transfer')
    g.edge('transfer', 'unh')
    g.edge('transfer', 'from_nhit', label='from')
    g.edge('transfer', 'from_nashua', label='from')
    g.edge('transfer', 'from_mcc', label='from')
    DrawNHITNodes(g, "nhit_",'from_nhit')
    DrawNHITNodes(g, "nashua_",'from_nashua')
    DrawNHITNodes(g, "mcc_",'from_mcc')
    return

def DrawNHITNodes(g, uniqueName, parentEdge):
    g.node(uniqueName+'compare_tuition_cost', label='Compare Tuition Cost', fillcolor='lightyellow', URL='/index.html', color='lightgreen',style='filled')
    g.node(uniqueName+'list_of_unh_programs', label='UNH Programs')
    g.node(uniqueName+'computer_science', label='Computer Science')
    g.node(uniqueName+'information_technology', label='Information Technology')
    g.node(uniqueName+'apply_to_cs', label='Apply',fillcolor='lightyellow', color='lightgreen',style='filled', URL='/index.html')
    g.node(uniqueName+'apply_to_it', label='Apply',fillcolor='lightyellow', color='lightgreen',style='filled', URL='/index.html')


    g.edge(parentEdge,uniqueName+'compare_tuition_cost')
    g.edge(parentEdge,uniqueName+'list_of_unh_programs')
    g.edge(uniqueName+'list_of_unh_programs',uniqueName+'computer_science')
    g.edge(uniqueName+'list_of_unh_programs',uniqueName+'information_technology')
    g.edge(uniqueName+'computer_science',uniqueName+'apply_to_cs', label="review_acceptable_transfer_classes",fillcolor='lightyellow',color='lightgreen',style='filled', URL='/index.html')
    g.edge(uniqueName+'information_technology',uniqueName+'apply_to_it', label="review_acceptable_transfer_classes",fillcolor='lightyellow',color='lightgreen',style='filled', URL='/index.html')
    return

def GenerateOutput(g, outputDir, outputFileName, htmlFileName):
    PrintHelper("Rendering Started.")    
    GraphRenderDot(g, outputDir, outputFileName)
    GraphRender(g, "cmapx", outputDir, outputFileName)
    GraphRender(g, "svg", outputDir, outputFileName)    
    CreateHtml(outputDir, htmlFileName, outputFileName+".svg", outputFileName+".cmapx")
    DeleteSingleFile(outputDir+"/"+outputFileName+".cmapx")
    PrintHelper("Rendering Completed.")
    return
def DeleteSingleFile(filePath):
    os.remove(filePath)
    return
def CreateHtml(outputDir, htmlFileName, imageFileName, cmapFileName):
    with open(outputDir+"/"+htmlFileName,"w")  as outFile:
        outFile.write('<img src="'+imageFileName+'" usemap="#G" alt="graphviz graph" />')   
        outFile.write('\n\n')    
        with open(outputDir+"/"+cmapFileName,"r") as cmapFile:
            for line in cmapFile:
                outFile.write(line)
    return
def GraphRenderDot(g,outputDir, outputFileName):
    g.directory = outputDir
    g.filename = outputFileName+".dot"
    g.save()
    return
def GraphRender(g,formatType, outputDir, outputFileName):    
    g.format = formatType
    g.render(cleanup=True, view=False, directory=outputDir, filename=outputFileName) 
    return

Main()
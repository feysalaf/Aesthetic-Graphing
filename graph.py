import matplotlib.pyplot as plt
import seaborn as sb, numpy as np
from seaborn import lineplot
import pandas as pd


class Graph():
    def __init__(self,*args):
        global graph_counter
        graph_counter = 0
        sb.set_style(style="darkgrid")

        sb.set(font="Gentium")
        sb.color_palette("crest", as_cmap=True)
        for t in args:
            if(t == 'light' or t == 'Light'):
                # scientific light
                textColor:str       = '#252223'
                backgroundColor:str = '#EAEAF2'
                gridColor:str       = '#FFFFFF'
                gridOuter:str       = '#EAEAF2'
            elif(t == 'dark' or t == 'Dark'):
                textColor:str       = '#BFBAB0'
                backgroundColor:str = '#1F2430'
                gridColor:str       = '#6F6F6F'
                gridOuter:str       = '#1F2430'

        sb.set(rc={'axes.facecolor':backgroundColor,
                  'figure.facecolor':backgroundColor,
                  'grid.color':gridColor,
                  'text.color':textColor,
                  'axes.labelcolor':textColor,
                  'axes.edgecolor':gridOuter,
                  'xtick.color':textColor,
                  'ytick.color':textColor})
    #need to pass self for scope context
    def adddata(self,*args):
        global graph_counter
        for g in args:
            if graph_counter == 0:
                graph_counter = graph_counter + 1
                graphname = 'data' + str(graph_counter)
                graphname = pd.DataFrame(g)
                print("Graph # {} initialized".format(graph_counter))
            else:
                #append data after creating
                #first graph
                graph_2 = pd.DataFrame(g)
                graphname['y_'+str(graph_counter)] = pd.Series(graph_2['y'])
                graph_counter = graph_counter + 1
                print("Graph # {} initialized".format(graph_counter))
                print("Final graph is: \n{}".format(graphname))
        #graph them all
        #set color_palette
        palette = sb.color_palette("mako_r", graph_counter)
        graphname = graphname.melt('x',var_name="Values",value_name='values')
        lineplot(x="x", y="values", hue='Values', data=graphname,palette=palette)
        plt.show()

def generate_data(function:str,ranges:dict):
    #declare data container(list)
    datalist = []
    # print(datalist[0])
    for i in range(ranges['start'],ranges['end']):
        #index new data to
        #to ith element in
        #the list + add dict to that entry
        datalist.append({"x":i,"y":function(i)})
    return datalist


#ranges = {"start":-100,"end":101}
#function
def LinearFunction(i):
    return 2 * i ** 2 + 10

def ExponentialFunction(i):
    return 32 * i

def ExponentialFunction1(i):
    return 99 * i

def ExponentialFunction2(i):
    return 3 * i + 23
#datalist = generate_data(LinearFunction,ranges)
#datalist2 = generate_data(ExponentialFunction,ranges)
#datalist3 = generate_data(ExponentialFunction1,ranges)
#datalist4 = generate_data(ExponentialFunction2,ranges)
#myobj = Graph('light')
#myobj.adddata(datalist,datalist2,datalist3)

import matplotlib.pyplot as plt
import seaborn as sb
from seaborn import lineplot
import pandas as pd
import json
import random
#dependency, REFACTOR can be replaced by more efficient plot lib
from drawnow import drawnow
import time
#multiple threads
from multiprocessing import Process

class Graph():
    def __init__(self,*args):
        self.internaldata = []
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
        #show the data if only one dataset was given
        #no. of datasets == graph_counter
        if(graph_counter == 1):
            print("Final graph is: \n{}".format(graphname))
        #graph them all
        #set color_palette
        palette = sb.color_palette("mako_r", graph_counter)
        graphname = graphname.melt('x',var_name="Values",value_name='values')
        lineplot(x="x", y="values", hue='Values', data=graphname,palette=palette)
        plt.show()
        plt.pause(0.0001)
    def make_fig(self):
        #convert to DataFrame
        dataframe = pd.DataFrame(self.internaldata)
        palette = sb.color_palette("mako_r", 1)
        plt.ion()
        lineplot(x="x", y=self.y_label, data=dataframe,palette=palette)
        print(dataframe)
        #plt.plot(x, y)
    def get_json_length(self,jsonfile):
        with open(jsonfile, "r") as read_file:
            in_ = json.load(read_file)
        return len(in_)
    def plotRealtime(self,jsonfile,y_label):
        self.y_label = y_label
        x = []
        y = []
        
        for i in range(self.get_json_length(jsonfile)):
            #read data from json file(get y)
            with open(jsonfile, "r") as read_file:
                datainput = json.load(read_file)
            #get the last value
            self.internaldata.append({"x":i,y_label:datainput[-1][y_label]})
            #y.append(datainput[-1][y_label])
            #x.append(i)
            time.sleep(1)

            drawnow(self.make_fig)

    def plotRealtimeAsync(self,**kwargs):
        var_list = []
        process_list = []
        for k,v in kwargs.items():
            if(k == 'jsonfile'):
                jfile = v
            else:
                var_list.append(v)
        for i in range(len(var_list)):
            process = Process(target=self.plotRealtime,args=(jfile,var_list[i]))
            process_list.append(process)
        for i in process_list:
            i.start()
        print(process_list)

#returns a json dataobject
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


ranges = {"start":-100,"end":101}
#function
def LinearFunction(i):
    return 2 * i ** 2 + 10

def ExponentialFunction(i):
    return 32 * i

def ExponentialFunction1(i):
    return 99 * i

def ExponentialFunction2(i):
    return 3 * i + 23
data = []
# def generateJson():
#
#     d = random.randint(0,100)
#     data.append({"Price":d,"Var":2*d})
#     with open('jsonPriceData', 'w') as fout:
#         json.dump(data, fout)
#
#
# for i in range(50):
#     generateJson()

# with open("jsonPriceData", "r") as read_file:
#     datainput = json.load(read_file)
# print(datainput[49]['Var'])

# datalist = generate_data(LinearFunction,ranges)
# datalist2 = generate_data(ExponentialFunction,ranges)
# datalist3 = generate_data(ExponentialFunction1,ranges)
# datalist4 = generate_data(ExponentialFunction2,ranges)
# print(datalist)
# myobj = Graph('light')
# myobj.adddata(datalist,datalist2,datalist3)
# myobj.adddata(datalist,datalist2,datalist3)

#Realtime testing
myobj = Graph('light')
myobj.plotRealtimeAsync(jsonfile='jsonPriceData'
                        ,var='Var',var1='Price')

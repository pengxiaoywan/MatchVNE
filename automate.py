import os
from DAA import main as DAA
from rethinking import  main as rethinking
from DAA_Random import main as DAA_RAND
import copy
import config
import pickle
import logging
import pandas as pd
from time import sleep
import graph_extraction_uniform
from greedy import main as greedy
from vne_u import create_vne as vne_u

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    # formatter = logging.Formatter('%(asctime)s %(levelname)s  : %(message)s')
    formatter = logging.Formatter('[%(levelname)s] : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler) 

output_dict = {
        "algorithm": [],
        "revenue": [],
        "total_cost" : [],
        "revenuetocostratio":[],
        "accepted" : [],
        "total_request": [],
        "embeddingratio":[],
        "pre_resource": [],
        "post_resource": [],
        "consumed":[],
        "avg_bw": [],
        "avg_crb": [],
        "avg_link": [],
        "avg_node": [],
        "avg_path": [],
        "avg_exec": [],
        "No_of_Links_used": [],
        "No_of_Nodes_used": [],
        "total_nodes": [],
        "total_links": [],
    }

def printToExcel(algorithm='', revenue='', total_cost='', revenuetocostratio='', accepted='', total_request='',
embeddingratio='', pre_resource='', post_resource='',consumed='',avg_bw='',avg_crb='',avg_link='',
avg_node='',avg_path='',avg_exec='' ,total_nodes='', total_links='', No_of_Links_used='', No_of_Nodes_used=''):

    output_dict["algorithm"].append(algorithm)
    output_dict["revenue"].append(revenue)
    output_dict["total_cost"].append(total_cost)
    output_dict["revenuetocostratio"].append(revenuetocostratio)
    output_dict["accepted"].append(accepted)
    output_dict["total_request"].append(total_request)
    output_dict["embeddingratio"].append(embeddingratio)
    output_dict["pre_resource"].append(pre_resource)
    output_dict["post_resource"].append(post_resource)
    output_dict["consumed"].append(consumed)
    output_dict["avg_bw"].append(avg_bw)
    output_dict["avg_crb"].append(avg_crb)
    output_dict["avg_link"].append(avg_link)
    output_dict["avg_node"].append(avg_node)
    output_dict["avg_path"].append(avg_path)
    output_dict["avg_exec"].append(avg_exec)
    output_dict["total_nodes"].append(total_nodes)
    output_dict["total_links"].append(total_links)
    output_dict["No_of_Links_used"].append(No_of_Links_used)
    output_dict["No_of_Nodes_used"].append(No_of_Nodes_used)
    addToExcel()

def exec_greedy(tot=1):#
    gred_out = greedy()
    sleep(tot*1)
    
    printToExcel(
        algorithm='GREEDY',
        revenue=gred_out['revenue'],
        total_cost=gred_out['total_cost'],
        revenuetocostratio=(gred_out['revenue']/gred_out['total_cost'])*100,
        accepted=gred_out['accepted'],
        total_request=gred_out['total_request'],
        embeddingratio=(gred_out['accepted']/gred_out['total_request'])*100,
        pre_resource=gred_out['pre_resource'],
        post_resource=gred_out['post_resource'],
        consumed=gred_out['pre_resource']-gred_out['post_resource'],
        avg_bw=gred_out['avg_bw'],
        avg_crb=gred_out['avg_crb'],
        avg_link=gred_out['avg_link'],
        avg_node=gred_out['avg_node'],
        avg_path=gred_out['avg_path'],
        avg_exec=gred_out['avg_exec'].total_seconds()*1000/gred_out['total_request'],
        total_nodes=gred_out['total_nodes'],
        total_links=gred_out['total_links'],
        No_of_Links_used=gred_out['No_of_Links_used'],
        No_of_Nodes_used=gred_out['No_of_Nodes_used']
    )

def exec_daa(tot=1):
    topsis_out = DAA()
    sleep(tot*1)
    
    printToExcel(
        algorithm='DAA',
        revenue=topsis_out['revenue'],
        total_cost=topsis_out['total_cost'],
        revenuetocostratio=(topsis_out['revenue']/topsis_out['total_cost'])*100,
        accepted=topsis_out['accepted'],
        total_request=topsis_out['total_request'],
        embeddingratio=(topsis_out['accepted']/topsis_out['total_request'])*100,
        pre_resource=topsis_out['pre_resource'],
        post_resource=topsis_out['post_resource'],
        consumed=topsis_out['pre_resource']-topsis_out['post_resource'],
        avg_bw=topsis_out['avg_bw'],
        avg_crb=topsis_out['avg_crb'],
        avg_link=topsis_out['avg_link'],
        avg_node=topsis_out['avg_node'],
        avg_path=topsis_out['avg_path'],
        avg_exec=topsis_out['avg_exec'].total_seconds()*1000/topsis_out['total_request'],
        total_nodes=topsis_out['total_nodes'],
        total_links=topsis_out['total_links'],
        No_of_Links_used=topsis_out['No_of_Links_used'],
        No_of_Nodes_used=topsis_out['No_of_Nodes_used']
    )


def exec_rethinking(tot=1):
    topsis_out = rethinking()
    sleep(tot * 1)

    printToExcel(
        algorithm='Rethinking',
        revenue=topsis_out['revenue'],
        total_cost=topsis_out['total_cost'],
        revenuetocostratio=(topsis_out['revenue'] / topsis_out['total_cost']) * 100,
        accepted=topsis_out['accepted'],
        total_request=topsis_out['total_request'],
        embeddingratio=(topsis_out['accepted'] / topsis_out['total_request']) * 100,
        pre_resource=topsis_out['pre_resource'],
        post_resource=topsis_out['post_resource'],
        consumed=topsis_out['pre_resource'] - topsis_out['post_resource'],
        avg_bw=topsis_out['avg_bw'],
        avg_crb=topsis_out['avg_crb'],
        avg_link=topsis_out['avg_link'],
        avg_node=topsis_out['avg_node'],
        avg_path=topsis_out['avg_path'],
        avg_exec=topsis_out['avg_exec'].total_seconds() * 1000 / topsis_out['total_request'],
        total_nodes=topsis_out['total_nodes'],
        total_links=topsis_out['total_links'],
        No_of_Links_used = topsis_out['No_of_Links_used'],
        No_of_Nodes_used = topsis_out['No_of_Nodes_used']
    )


def exec_daa_rand(tot=1):
    topsis_out = DAA_RAND()
    sleep(tot * 1)

    printToExcel(
        algorithm='DAA_Random',
        revenue=topsis_out['revenue'],
        total_cost=topsis_out['total_cost'],
        revenuetocostratio=(topsis_out['revenue'] / topsis_out['total_cost']) * 100,
        accepted=topsis_out['accepted'],
        total_request=topsis_out['total_request'],
        embeddingratio=(topsis_out['accepted'] / topsis_out['total_request']) * 100,
        pre_resource=topsis_out['pre_resource'],
        post_resource=topsis_out['post_resource'],
        consumed=topsis_out['pre_resource'] - topsis_out['post_resource'],
        avg_bw=topsis_out['avg_bw'],
        avg_crb=topsis_out['avg_crb'],
        avg_link=topsis_out['avg_link'],
        avg_node=topsis_out['avg_node'],
        avg_path=topsis_out['avg_path'],
        avg_exec=topsis_out['avg_exec'].total_seconds() * 1000 / topsis_out['total_request'],
        total_nodes=topsis_out['total_nodes'],
        total_links=topsis_out['total_links'],
        No_of_Links_used=topsis_out['No_of_Links_used'],
        No_of_Nodes_used=topsis_out['No_of_Nodes_used']
    )

def addToExcel():
    geeky_file = open('geekyfile.pickle', 'wb')
    pickle.dump(output_dict, geeky_file)
    geeky_file.close()

def main(substrate, vne):
    ls=[5]
    for l in ls:
        iterations=1
        for _ in range(iterations):
            vne_list = vne(no_requests=l)
            config.substrate = copy.deepcopy(substrate)
            config.vne_list = copy.deepcopy(vne_list)
            exec_greedy()
            # exec_daa()
            # exec_rethinking()
            # exec_daa_rand() # not changed for printing no node and lik=nk used

#######################################################################################
#######################################################################################
##                                                                                   ##
##    IMPORTANT - CLOSE test.xlsx (excel file) IF OPEN BEFORE RUNNING THIS           ##
##                                                                                   ##
##    IMPORTANT - PLEASE CHOOSE THE PICKLE FILE, CRB & BW LIMITS FOR                 ##  
##                ALL(RANDOM, UNIFORM, POISSION) DISTRIBUTIONS BEFORE RUNNING THIS   ##
##                                                                                   ##
#######################################################################################
#######################################################################################

def generateSubstrate(for_automate, pickle_name):
    substrate, _ = for_automate(1)
    geeky_file = open(pickle_name, 'wb')
    pickle.dump(substrate, geeky_file)
    geeky_file.close()


def extractSubstrate(pickle_file):
    filehandler = open(pickle_file, 'rb')
    substrate = pickle.load(filehandler)
    # print("----------------")
    # print(substrate)
    # print("----------------")
    return substrate


def runUniformExtraction(pickle_name):
    substrate = extractSubstrate(pickle_name)
    printToExcel()
    for i in range(3):
        printToExcel(pre_resource='UNIFORM')
    printToExcel()
    print("\nUNIFORM Extraction\n")
    # vne_ext = vne_u()
    main(substrate, vne_u)

if __name__ == "__main__":

    file_exists = os.path.exists('1_random.pickle') or os.path.exists('1_uniform.pickle') or os.path.exists('1_poission.pickle') or os.path.exists('1_normal.pickle')
    print(file_exists)
    # file_exists = False       #Manually set, if want to update a substrate pickle
    if(file_exists==False): # NO Input File in a Path
        #generateSubstrate(graph_extraction_random.for_automate, str(1)+'_random.pickle')        #Random Distribution
        #generateSubstrate(graph_extraction_normal.for_automate, str(1)+'_normal.pickle')    #Normal Distribution
        generateSubstrate(graph_extraction_uniform.for_automate, '1_uniform.pickle')    #Uniform Distribution
        #generateSubstrate(graph_extraction_poisson.for_automate, str(1)+'_poission.pickle')    #Poission Distribution

    #runRandomExtraction('1_random.pickle')
    runUniformExtraction('1_uniform.pickle')
    #runPoissionExtraction('1_poission.pickle')
    #runNormalExtraction('1_normal.pickle')
    
    excel = pd.DataFrame(output_dict)
    excel.to_excel("Results_Greedy.xlsx")

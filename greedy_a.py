import helper
import sys
import copy
from datetime import datetime, date
import logging
import random
import config
# global log2
# log2 = logging.getLogger('log2')


mappingVS = {}

calc_CRB=0
calc_BW=0
set_CRB = set()
set_BW = set()

class temp_map:

    def __init__(self, vne_list,req_no, map=[]) -> None:
        self.node_map = map
        self.node_cost = 0
        self.node_cost += sum(vne_list[req_no].node_weights.values())
        self.edge_cost = 0
        self.total_cost = sys.maxsize
        self.edge_map = dict()

def node_map(substrate, virtual, req_no):
    global calc_CRB
    global set_CRB
    map = [0 for x in range(virtual.nodes)]
    sorder = sorted([a for a in range(substrate.nodes)], key = lambda x: substrate.node_weights[x], reverse=True) # ascending order
    vorder = sorted([a for a in range(virtual.nodes)], key = lambda x: virtual.node_weights[x], reverse=True) 
    assigned_nodes = set()
    for vnode in vorder:
        for snode in sorder:
            if substrate.node_weights[snode] >= virtual.node_weights[vnode] and snode not in assigned_nodes:
                map[vnode] = snode
                mappingVS[vnode] = snode
                calc_CRB += (virtual.node_weights[vnode] / substrate.node_weights[snode])
                set_CRB.add(snode)
                substrate.node_weights[snode] -= virtual.node_weights[vnode]
                assigned_nodes.add(snode)
                break
            if snode == sorder[-1]:
                return None
    # calc_CRB = 0
    # set_CRB = set()

    return map

def edge_map(substrate, virtual, req_no, req_map, vne_list):
    global calc_BW
    global set_BW
    substrate_copy = copy.deepcopy(substrate)
    for edge in virtual.edges:
        if int(edge[0]) < int(edge[1]):
            weight = virtual.edge_weights[edge]
            left_node = req_map.node_map[int(edge[0])]
            right_node = req_map.node_map[int(edge[1])]
            path = substrate_copy.findShortestPath(str(left_node), str(right_node), weight) # modified bfs
            if path != []:
                req_map.edge_map[req_no, edge] = path
                for j in range(1, len(path)):
                    calc_BW += (weight / substrate_copy.edge_weights[(path[j - 1], path[j])])
                    set_BW.add((path[j - 1], path[j]))
                    set_BW.add((path[j], path[j - 1]))
                    substrate_copy.edge_weights[(path[j - 1], path[j])] -= weight
                    substrate_copy.edge_weights[(path[j], path[j - 1])] -= weight
                    req_map.edge_cost += weight
            else:
                return False
    sub_wt = []
    sorder = sorted([a for a in range(substrate.nodes)], key = lambda x: substrate.node_weights[x], reverse=True) # ascending order
    for node in sorder:
        sub_wt.append((node, substrate.node_weights[node]))
    logging.info(f"\t\tSubstrate node before mapping VNR-{req_no} is {sub_wt}")
    sub_wt = []
    for edge in substrate.edges:
        sub_wt.append((edge, substrate.edge_weights[edge]))
    logging.info(f"\t\tSubstrate edge before mapping VNR-{req_no} is {sub_wt}")
    logging.info(f"\t\tNode map of VNR-{req_no} is {req_map.node_map}")
    logging.info(f"\t\tEdge map of VNR-{req_no} is {req_map.edge_map}")
    for edge, path in req_map.edge_map.items():
        edge = edge[1]
        for i in range(1,len(path)):
            substrate.edge_weights[(path[i - 1], path[i])] -= virtual.edge_weights[edge]
            substrate.edge_weights[(path[i], path[i-1])] -= virtual.edge_weights[edge]
    for node in range(vne_list[req_no].nodes):
        substrate.node_weights[req_map.node_map[node]] -= virtual.node_weights[node]
    sub_wt = []
    sorder = sorted([a for a in range(substrate.nodes)], key = lambda x: substrate.node_weights[x], reverse=True) # ascending order
    for node in sorder:
        sub_wt.append((node, substrate.node_weights[node]))
    logging.info(f"\t\tSubstrate after mapping VNR-{req_no} is {sub_wt}")
    sub_wt = []
    for edge in substrate.edges:
        sub_wt.append((edge, substrate.edge_weights[edge]))
    logging.info(f"\t\tSubstrate edge after mapping VNR-{req_no} is {sub_wt}")
    # calc_BW = 0
    # set_BW = set()
    return True

# def findAvgPathLength(vnr, map, graph):
#     cnt=0
#     for node1 in range(vnr.nodes):
#         for node2 in range(vnr.nodes):
#             if(node1 != node2):
#                 path = vnr.findShortestPath(str(node1), str(node2), 0)
#                 cnt += len(path)-1
#     total_nodes = vnr.nodes
#     cnt /= (total_nodes)*(total_nodes-1)
#     return cnt

def findAvgPathLength(vnr, graph):
    cnt=0
    for edg, wg in vnr.edge_weights.items():
        u = mappingVS[int(edg[0])]
        v = mappingVS[int(edg[1])]
        dm = wg
        path = graph.findShortestPath(str(u), str(v), dm)
        cnt += len(path) - 1
    total_ed = len(vnr.edge_weights)
    cnt = cnt / total_ed
    return cnt




def main():
    print(f"\t\t{datetime.now().time()}\tGreedy Started")
    # substrate, vne_list = helper.read_pickle()
    substrate, vne_list = copy.deepcopy(config.substrate), copy.deepcopy(config.vne_list)
    copy_sub = copy.deepcopy(substrate)
    logging.basicConfig(filename="greedy.log",filemode="w", level=logging.INFO)
    logging.info(f"\n\n\t\t\t\t\t\tSUBSTRATE NETWORK (BEFORE MAPPING VNRs for Greedy)")
    logging.info(f"\t\tTotal number of nodes and edges in substrate network is : {substrate.nodes} and {len(substrate.edges)} ")
    temp = []
    for node in range(substrate.nodes):
        temp.append((node, substrate.node_weights[node]))
    logging.info(f"\t\tNodes of the substrate network with weight are : {temp}")
    temp = []
    for edge in substrate.edges:
        temp.append((edge,substrate.edge_weights[edge]))
    logging.info(f"\t\tEdges of the substrate network with weight are : {temp}\n\n\t\t\t\t\t\tVIRTUAL NETWORK")

    total_vnr_nodes = 0
    total_vnr_links = 0
    logging.info(f"\t\tTotal number of Virtual Network Request is : {len(vne_list)}\n")
    for vnr in range(len(vne_list)):
        logging.info(f"\t\tTotal number of nodes and edges in VNR-{vnr} is : {vne_list[vnr].nodes} and {len(vne_list[vnr].edges)}")
        temp = []
        total_vnr_nodes += vne_list[vnr].nodes 
        for node in range(vne_list[vnr].nodes):
            temp.append((node, vne_list[vnr].node_weights[node]))
        logging.info(f"\t\tNodes of the VNR-{vnr} with weight are : {temp}")
        temp = []
        total_vnr_links += len(vne_list[vnr].edges) 
        for edge in vne_list[vnr].edges:
            temp.append((edge, vne_list[vnr].edge_weights[edge]))
        if vnr == len(vne_list)-1:
            logging.info(f"\t\tEdges of the VNR-{vnr} with weight are : {temp}\n\n")
        else:
            logging.info(f"\t\tEdges of the VNR-{vnr} with weight are : {temp}")        
    start_time = datetime.now().time()
    accepted = 0
    revenue = 0
    path_cnt=0
    avg_path_length = 0
    curr_map = dict() # only contains the requests which are successfully mapped
    pre_resource_edgecost = sum(substrate.edge_weights.values())//2 # total available bandwidth of the physical network
    pre_resource_nodecost = sum(substrate.node_weights.values()) # total crb bandwidth of the physical network
    pre_resource = pre_resource_edgecost + pre_resource_nodecost
    
    req_order = list(range(len(vne_list)))
    random.shuffle(req_order)

    for req_no in req_order:
        req_map = node_map(copy.deepcopy(substrate), vne_list[req_no], req_no)
        # revenue += sum(vne_list[req_no].node_weights.values()) + sum(vne_list[req_no].edge_weights.values()) // 2
        if req_map is  None:
            #print(f"Node mapping not possible for req no {req_no}")
            logging.warning(f"\tNode mapping not possible for req no {req_no}\n")
            continue
        req_map = temp_map(vne_list, req_no, req_map)
        if not edge_map(substrate, vne_list[req_no], req_no, req_map, vne_list):
            #print(f"Edge mapping not possible for req no {req_no}")
            logging.warning(f"\tEdge mapping not possible for req no {req_no}\n")
            continue
        revenue += sum(vne_list[req_no].node_weights.values()) + sum(vne_list[req_no].edge_weights.values()) // 2
        accepted += 1
        avg_path_length += findAvgPathLength(vne_list[req_no], substrate)
        for ed in req_map.edge_map:
            path_cnt += len(req_map.edge_map[ed])
        req_map.total_cost = req_map.node_cost + req_map.edge_cost
        #print(f"Mapping for request {req_no} is done successfully!! {req_map.node_map} with total cost {req_map.total_cost}")
        logging.info(f"\t\tMapping for request {req_no} is done successfully!! {req_map.node_map} with revenue {revenue} and total cost {req_map.total_cost}\n")
        curr_map[req_no] = req_map
        # revenue += sum(vne_list[req_no].node_weights.values()) + sum(vne_list[req_no].edge_weights.values())//2

    ed_cost  = 0
    no_cost = 0
    avg_nd = 0
    avg_eg = 0
#---------------------------------------------BW calculations--------------------------------
    for request in curr_map.values():
        avg_eg += request.edge_cost/len(request.edge_map) # total bandwidth for all the mapped requests
        ed_cost += request.edge_cost
        avg_nd += request.node_cost/len(request.node_map) # total crb for all the mapped requests
        no_cost += request.node_cost

    tot_cost = ed_cost + no_cost
#-----------------------------------------------------------------------------------

    post_resource_edgecost =0
    post_resource_nodecost=0
    utilized_nodes=0
    utilized_links=0
    for edge in substrate.edge_weights:
        post_resource_edgecost += substrate.edge_weights[edge]
        if substrate.edge_weights[edge]!=copy_sub.edge_weights[edge]:
            utilized_links += 1
    post_resource_edgecost //= 2
    for node in substrate.node_weights:
        post_resource_nodecost += substrate.node_weights[node]
        if substrate.node_weights[node] != copy_sub.node_weights[node]:
            utilized_nodes += 1

    if (accepted != 0):
        avg_path_length /= accepted
    post_resource = post_resource_edgecost + post_resource_nodecost
    end_time = datetime.now().time()
    duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)    
    
    #print(f"\n\nThe revenue is {revenue} and total cost is {tot_cost}")
    #print(f"Total number of requests embedded is {accepted}")
    #print(f"Embedding ratio is {accepted/len(vne_list)}")
    #print(f"Availabe substrate resources before mapping is {pre_resource}")
    #print(f"Consumed substrate resources after mapping is {pre_resource - post_resource}")
    #print(f"Average link utilization {ed_cost/pre_resource_edgecost}")
    #print(f"Average node utilization {no_cost/pre_resource_nodecost}")
    #print(f"Average execution time {duration/len(vne_list)}")

    logging.info(f"\n\n\t\t\t\t\t\tSUBSTRATE NETWORK AFTER MAPPING VNRs")
    logging.info(f"\t\tTotal number of nodes and edges in substrate network is : {substrate.nodes} and {len(substrate.edges)} ")
    temp = []
    for node in range(substrate.nodes):
        temp.append((node, substrate.node_weights[node]))
    logging.info(f"\t\tNodes of the substrate network with weight are : {temp}")
    temp = []
    for edge in substrate.edges:
        temp.append((edge,substrate.edge_weights[edge]))
    logging.info(f"\t\tEdges of the substrate network with weight are : {temp}\n\n")   
    
    logging.info(f"\t\tThe revenue is {revenue} and total cost is {tot_cost}")
    if tot_cost == 0:
        logging.error(f"\t\tCouldn't embedd any request")
        output_dict = {
            "revenue": -1,
            "total_cost": -1,
            "accepted": -1,
            "total_request": -1,
            "pre_resource": -1,
            "post_resource": -1,
            "avg_bw": -1,
            "avg_crb": -1,
            "avg_link": -1,
            "avg_node": -1,
            "avg_path": -1,
            "avg_exec": (duration),
            # "total_node_used": 0,
            # "total_link_used": 0,
            "total_nodes": total_vnr_nodes,
            "total_links": total_vnr_links,
        }
        print(f"\t\t{datetime.now().time()}\tgreedy completed\n")
        return output_dict
    avg_bw = 0
    if(len(set_BW)!=0):
        avg_bw=(calc_BW/(len(set_BW)//2))*100

    avg_crb = 0
    if (len(set_CRB) != 0):
        avg_crb = (calc_CRB/len(set_CRB))*100

    logging.info(f"\t\tThe revenue is {revenue} and total cost is {tot_cost}")
    logging.info(f"\t\tThe revenue to cost ratio is {(revenue/tot_cost)*100:.4f}%")
    logging.info(f"\t\tTotal number of requests embedded is {accepted} out of {len(vne_list)}")
    logging.info(f"\t\tEmbedding ratio is {(accepted/len(vne_list))*100:.4f}%\n")
    logging.info(f"\t\tTotal {len(set_CRB)} nodes are utilized out of {len(substrate.node_weights)}")
    logging.info(f"\t\tTotal {len(set_BW)//2} links are utilized out of {len(substrate.edge_weights)//2}\n")
    logging.info(f"\t\tAverage node utilization is {(len(set_CRB)/len(substrate.node_weights))*100:0.4f}")
    logging.info(f"\t\tAverage link utilization is {(len(set_BW)/len(substrate.edge_weights)//2)*100:0.4f}\n")
    logging.info(f"\t\tAvailabe substrate before embedding CRB: {pre_resource_nodecost} BW: {pre_resource_edgecost} total: {pre_resource}")
    logging.info(f"\t\tAvailabe substrate after embedding CRB: {post_resource_nodecost} BW: {post_resource_edgecost} total: {post_resource}")
    logging.info(f"\t\tConsumed substrate CRB: {pre_resource_nodecost-post_resource_nodecost} BW: {pre_resource_edgecost-post_resource_edgecost} total: {pre_resource - post_resource}\n")
    logging.info(f"\t\tAverage Path length is {avg_path_length:.4f}\n")
    logging.info(f"\t\tAverage BW utilization {(ed_cost/pre_resource_edgecost)*100:.4f}%")
    logging.info(f"\t\tAverage CRB utilization {(no_cost/pre_resource_nodecost)*100:.4f}%")
    logging.info(f"\t\tAverage execution time {duration/len(vne_list)} (HH:MM:SS)")
    # logging.shutdown()
    output_dict = {
        "revenue": revenue,
        "total_cost" : tot_cost,
        "accepted" : accepted,
        "total_request": len(vne_list),
        "pre_resource": pre_resource,
        "post_resource": post_resource,

        "avg_bw": avg_bw,
        "avg_crb": avg_crb,
        #fine till here

        "avg_link": ((len(set_BW)//2)/(len(substrate.edge_weights)//2))*100,
        "avg_node": (len(set_CRB)/len(substrate.node_weights))*100,

        "avg_path": avg_path_length,
        "avg_exec": (duration/len(vne_list)),
        # "total_node_used": len(set_CRB),
        # "total_link_used": len(set_BW),
        "total_nodes": total_vnr_nodes,
        "total_links": total_vnr_links//2,
    }
    set_BW.clear()
    set_CRB.clear()

    print(f"\t\t{datetime.now().time()}\tGreedy completed\n")
    return output_dict

if __name__ == '__main__':
    '''
    The output can be different as every time we shuffle the
    request order of VNRs.
    '''
    # helper.setup_logger('log2','greedy.log')
    main()
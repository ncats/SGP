# Author: Gergely Zahoranszky-Kohalmi, Phd
#
# Email: gergely.zahoranszky-kohalmi@nih.gov
#
# Organization: National Center for Advancing Translational Sciences (NCATS/NIH)
#
#
# Ref: https://github.com/ncats/sg2cyjs
#
# Ref: https://networkx.org/documentation/stable/tutorial.html
# Ref; https://stackoverflow.com/questions/3810782/most-elegant-way-to-find-nodes-predecessors-with-networkx
# Ref: https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.succ.html
# Ref: https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.DiGraph.out_degree.html
# Ref: https://stackoverflow.com/questions/28488559/networkx-duplicate-edges/51611005
# Ref: https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.nodes.html
# Ref: https://networkx.org/documentation/stable/reference/readwrite/graphml.html
# Ref: https://www.geeksforgeeks.org/python-program-to-convert-list-of-integer-to-list-of-string/

import networkx as nx
import sys
import json
import pandas as pd



def has_item (a = []):
	if len(a) > 0:
		return (True)

	return (False)


def flagNodes (neighbors = {}, target_list = []):
	for neighbor, nattrs in neighbors.items():
		if neighbor not in target_list:
			target_list.append(neighbor)
	
	return (target_list)
	
def markNodeForDeletion (node, nodes_2b_deleted = []):
	if node not in nodes_2b_deleted:
		nodes_2b_deleted.append(node)
	
	return (nodes_2b_deleted)


def filterPaths (G, nosubstances = []):
	instant_nodes_2b_deleted = []
	lazy_nodes_2b_deleted_parent = []
	lazy_nodes_2b_deleted_offspring = []
	deleted_nodes = {}

	#print (G.nodes)

	instant_nodes_2b_deleted.extend (nosubstances)
	#print (G.nodes)
	
	while (has_item(instant_nodes_2b_deleted) or has_item(lazy_nodes_2b_deleted_parent) or has_item(lazy_nodes_2b_deleted_offspring)):
		
		while has_item(instant_nodes_2b_deleted):
			
			n_i = instant_nodes_2b_deleted.pop()
			
			if n_i in G.nodes:

				parent_neighbors = G.pred[n_i]
				offspring_neighbors = G.succ[n_i]
				
			
				if G.nodes[n_i]['node_type'] == 'Substance':
	
					
					instant_nodes_2b_deleted = flagNodes (parent_neighbors, instant_nodes_2b_deleted)
					instant_nodes_2b_deleted = flagNodes (offspring_neighbors, instant_nodes_2b_deleted)

				else:

					lazy_nodes_2b_deleted_parent = flagNodes (parent_neighbors, lazy_nodes_2b_deleted_parent)
					lazy_nodes_2b_deleted_offspring = flagNodes (offspring_neighbors, lazy_nodes_2b_deleted_offspring)
	

	
				G.remove_node(n_i)
			
	
		# lazy cycles comes here
		
		while has_item(lazy_nodes_2b_deleted_parent):
			n_l = lazy_nodes_2b_deleted_parent.pop()


			if G.out_degree(n_l) == 0:
				instant_nodes_2b_deleted = markNodeForDeletion (n_l, instant_nodes_2b_deleted)
	
		while has_item(lazy_nodes_2b_deleted_offspring):
			n_l = lazy_nodes_2b_deleted_offspring.pop()

			if G.in_degree(n_l) == 0 and G.nodes[n_l]['srole'] != 'sm':
				instant_nodes_2b_deleted = markNodeForDeletion (n_l, instant_nodes_2b_deleted)


		
		
			
		#print ("Nr. instant nodes to be deleted: %d" % len(instant_nodes_2b_deleted))
		#print ("Nr. lazy_nodes_2b_deleted_parent to be deleted: %d" % len(lazy_nodes_2b_deleted_parent))
		#print ("Nr. lazy_nodes_2b_deleted_offspring to be deleted: %d" % len(lazy_nodes_2b_deleted_offspring))


	return (G)


def parse_inventory (file_starting_materials):
	df_sm = pd.read_csv(file_starting_materials, sep = '\t')
	df_sm_only = df_sm[df_sm['starting_material'] == 'yes'].copy()


	return (df_sm_only)



print ('\n*CLI Syntax*\n\n')
print ('python SGP_fromGraphML.py <input.graphml> <target molecule InChI-key> <output_filename> <file_annotated_with_starting_materials>\n\n')

file_name = sys.argv[1]
targetmol = sys.argv[2]
file_out = sys.argv[3]
file_starting_materials = sys.argv[4]
file_avoid = sys.argv[5]

df_sub_av = pd.read_csv (file_avoid, sep = '\t')
substances_avoid = list(df_sub_av['uuid'])
substances_avoid = map(str, substances_avoid)

print ('[i] Processing input: %s' % (file_name))



#file_starting_materials = "analysis/output/unique_substances_starting_material_annotated.tsv"


#file_orig_graph = file_out_stem + '_orig_graph.graphml'
#file_pruned_graph = file_out_stem + '_pruned_graph.graphml'

df_sm = pd.read_csv(file_starting_materials, sep = '\t')
df_sm_only = df_sm[df_sm['starting_material'] == 'yes'].copy()

df_sm = parse_inventory (file_starting_materials)

G = nx.read_graphml (file_name)

#nx.write_graphml(G, file_orig_graph)

#print ('[i] Writing input graph in graphml format to file: %s' % (file_orig_graph))


##G = filterPaths(G, ['c4346a04-62cb-11eb-92a0-9ddb6a5f961b_XEKOWRVHYACXOJ-UHFFFAOYSA-N']) # should result in empty graph, OK !!!
##G = filterPaths(G, ['c8d4c19e-62cb-11eb-92a0-9ddb6a5f961b_XLYOFNOQVPJJNP-UHFFFAOYSA-N']) # should result in empty graph, OK !!!
#G = filterPaths(G, ['abfc51e6-62ca-11eb-92a0-9ddb6a5f961b_FLNUOFNGYKMIEC-UHFFFAOYSA-N']) # should result in almst full original retrosynth graph, with 3 substance and 1 reaction node (USPTO_66243 missing, OK!!!)

G = filterPaths(G, substances_avoid) 



nx.write_graphml(G, file_out)

print ('[i] Writing pruned graph in graphml format to file: %s' % (file_out))

print ('\n\n')
print ('[Done.]')

print ('\n\n')




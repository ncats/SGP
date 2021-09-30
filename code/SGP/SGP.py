# Author: Gergely Zahoranszky-Kohalmi, Phd
#
# Email: gergely.zahoranszky-kohalmi@nih.gov
#
# Organization: National Cnter for Advancing Translational Sciences (NCATS/NIH)
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


import networkx as nx
import sys
import json
import pandas as pd


def add_node (G, uuid, node_metadata):
	G.add_node(uuid)

	for key in node_metadata.keys():
		G.nodes[uuid][key] = node_metadata[key]

	return (G)


def process_nodes (G, nodes, targetmol, df_sm, node_type_property = 'node_type'):
	valid_node_types = ['Reaction', 'Substance']


	for n in nodes:

		node_metadata = {}
		
		node_type = n[node_type_property]

		if node_type not in valid_node_types:
			print ("Invalid node type found: %s. Terminating ..." % (node_type))
			sys.exit(-1)

		node_uuid = n['data']['uuid']
		is_in_uspto = n['data']['is_in_uspto']


		node_metadata['uuid'] = node_uuid
		node_metadata['node_type'] = node_type
		node_metadata['is_in_uspto'] = is_in_uspto



		if node_type == 'Reaction':

			rxid = n['data']['rxid']
			rush = n['data']['rush']
			rsha = n['data']['rsha']
			rinchikey = n['data']['rinchikey']
	
			node_metadata['rxid'] = rxid
			node_metadata['rush'] = rush
			node_metadata['rsha'] = rsha
			node_metadata['rinchikey'] = rinchikey
			node_metadata['name'] = rxid




			G = add_node (G, node_uuid, node_metadata)


		else:
			# Then it's a Substance node.

			inchikey = n['data']['inchikey']
			nsinchikey = n['data']['nsinchikey']
			#smiles = n['data']['smiles']

			node_metadata['inchikey'] = inchikey
			node_metadata['nsinchikey'] = nsinchikey
			#node_metadata['smiles'] = smiles
			node_metadata['name'] = nsinchikey


			# placeholder for parsing synthesis planning roles of substances
			# i.e.: starting material, intermedier, target molecule

			G = add_node (G, node_uuid, node_metadata)
			
			# > To be delete start. Temporary solution only until the synthesis roles
			# of nodes are parsed from actual iputs.
			# intermedier and target moecule here are not distuingished, as it is not required
			# by this algorithm, but will be distinguished once this info will be parsed
			# from input JSON.

			indegree = G.in_degree(node_uuid)

			if inchikey == targetmol:
                                srole = 'tm'
			elif indegree == 0 or inchikey in list(df_sm['inchikey_substance']):
				srole = 'sm'
			else:
				srole = 'im'


			
			G.nodes[node_uuid]['srole'] = srole

			# < To be deleted end.



	return (G)



def add_edge (G, start_node, end_node, edge_metadata):
	G.add_edge (start_node, end_node)
	
	for key in edge_metadata.keys():
		G[start_node][end_node][key] = edge_metadata[key]


	return (G)


def process_edges (G, edges, edge_type_property = 'edge_type'):
	valid_edge_types = ['REACTANT_OF', 'REAGENT_OF', 'PRODUCT_OF']


	for e in edges:
		
		edge_metadata ={}

		edge_uuid = e['edge_uuid']
		edge_type = e[edge_type_property]

		if edge_type not in valid_edge_types:
			print ("Invalid edge type found: %s. Terminating ..." % (edge_type))
			sys.exit(-1)


		start_node = e['start_node']
		end_node = e['end_node']

		edge_metadata['edge_type'] = edge_type
		edge_metadata['edge_type'] = edge_type
		edge_metadata['uuid'] = edge_uuid



		G = add_edge (G, start_node, end_node, edge_metadata)

	return (G)



def parse_graph (input_json, targetmol, df_sm):
	with open(input_json) as f:
		data = json.load(f)

	EPT = 'edge_label'

	G = nx.DiGraph()

	all_shortest_paths = data['Shortest Possible Paths']
	for shortest_path in all_shortest_paths:
		p = shortest_path['Shortest Paths']
		nodes = p[0]['nodes']
		edges = p[0]['edges']

		G = process_nodes (G, nodes, targetmol, df_sm)
		G = process_edges (G, edges, EPT)



	return (G)			


"""
G = nx.DiGraph()

G.add_nodes_from ([
	('a', {'node_type': 'substance'}),
	('b', {'node_type': 'substance'}),
	('c', {'node_type': 'substance'}),
	('d', {'node_type': 'substance'}),
	('e', {'node_type': 'substance'}),
	('f', {'node_type': 'substance'}),
	('g', {'node_type': 'substance'}),
	('h', {'node_type': 'substance'}),
	('r1', {'node_type': 'reaction'}),
	('r2', {'node_type': 'reaction'}),
	('r3', {'node_type': 'reaction'}),

])


G.add_edge ('a', 'r1')
G.add_edge ('r1', 'b')
G.add_edge ('c', 'r1')
G.add_edge ('d', 'r2')
G.add_edge ('r2', 'e')
G.add_edge ('f', 'r2')
G.add_edge ('g', 'r3')
G.add_edge ('b', 'r3')
G.add_edge ('r3', 'h')

G['a']['r1']['role'] = 'reactant'
G['r1']['b']['role'] = 'product'
G['c']['r1']['role'] = 'reagent'
G['d']['r2']['role'] = 'reactant'
G['r2']['e']['role'] = 'product'
G['f']['r2']['role'] = 'reactant'
G['g']['r3']['role'] = 'reactant'
G['b']['r3']['role'] = 'reactant'
G['r3']['h']['role'] = 'product'

#print (G.nodes)
#print (G.edges)

#print (G['b']['r3'])
"""



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


	instant_nodes_2b_deleted.extend (nosubstances)

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
print ('python SGP.py <input.json> <target molecule InChI-key> <output_stem> <file_annotated_with_starting_materials>\n\n')

file_name = sys.argv[1]
targetmol = sys.argv[2]
file_out_stem = sys.argv[3]
file_starting_materials = sys.argv[4]
file_avoid = sys.argv[5]

df_sub_av = pd.read_csv (file_avoid, sep = '\t')
substances_avoid = list(df_sub_av['uuid'])

print ('[i] Processing input: %s' % (file_name))

#file_starting_materials = "analysis/output/unique_substances_starting_material_annotated.tsv"


file_orig_graph = file_out_stem + '_orig_graph.graphml'
file_pruned_graph = file_out_stem + '_pruned_graph.graphml'

df_sm = pd.read_csv(file_starting_materials, sep = '\t')
df_sm_only = df_sm[df_sm['starting_material'] == 'yes'].copy()

df_sm = parse_inventory (file_starting_materials)

G = parse_graph (file_name, targetmol, df_sm)

nx.write_graphml(G, file_orig_graph)

print ('[i] Writing input graph in graphml format to file: %s' % (file_orig_graph))


##G = filterPaths(G, ['c4346a04-62cb-11eb-92a0-9ddb6a5f961b_XEKOWRVHYACXOJ-UHFFFAOYSA-N']) # should result in empty graph, OK !!!
##G = filterPaths(G, ['c8d4c19e-62cb-11eb-92a0-9ddb6a5f961b_XLYOFNOQVPJJNP-UHFFFAOYSA-N']) # should result in empty graph, OK !!!
#G = filterPaths(G, ['abfc51e6-62ca-11eb-92a0-9ddb6a5f961b_FLNUOFNGYKMIEC-UHFFFAOYSA-N']) # should result in almst full original retrosynth graph, with 3 substance and 1 reaction node (USPTO_66243 missing, OK!!!)

G = filterPaths(G, substances_avoid) 



nx.write_graphml(G, file_pruned_graph)

print ('[i] Writing pruned graph in graphml format to file: %s' % (file_pruned_graph))

print ('\n\n')
print ('[Done.]')

print ('\n\n')




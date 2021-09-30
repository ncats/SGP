# Author: Gergely Zahoranszky-Kohalmi, Phd
# 
# Email: gergely.zahoranszky-kohalmi@nih.gov
#
# Organization: National Center for Advancing Translational Sciences (NCATS/NIH)
#


# Example 1
python SGP.py ../../data/input/example_1.json QKKPBPMGSMLOPE-UHFFFAOYSA-N ../../data/output/example_1_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_1_substances_avoid



# Example 2 (2a-2d)

python SGP.py ../../data/input/example_2.json DRLLGUSIBMKHRP-UHFFFAOYSA-N ../../data/output/example_2a_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_2a_substances_avoid


python SGP.py ../../data/input/example_2.json DRLLGUSIBMKHRP-UHFFFAOYSA-N ../../data/output/example_2a_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_2a_substances_avoid

python SGP.py ../../data/input/example_2.json DRLLGUSIBMKHRP-UHFFFAOYSA-N ../../data/output/example_2b_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_2b_substances_avoid


python SGP.py ../../data/input/example_2.json DRLLGUSIBMKHRP-UHFFFAOYSA-N ../../data/output/example_2c_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_2c_substances_avoid


python SGP.py ../../data/input/example_2.json DRLLGUSIBMKHRP-UHFFFAOYSA-N ../../data/output/example_2d_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_2d_substances_avoid




python SGP.py ../../data/input/example_3.json JHAOAKJTOFHYLE-YJJYDOSJSA-N ../../data/output/example_3_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_3_substances_avoid





python SGP.py ../../data/input/example_4a.json NWFOHDSVPZKRKC-UHFFFAOYSA-N ../../data/output/example_4a_sgp ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_4a_substances_avoid

python SGP_fromGraphML.py ../../data/output/example_4a_sgp_edited_graph_orig.graphml  NWFOHDSVPZKRKC-UHFFFAOYSA-N ../../data/output/example_4a_edited_sgp_pruned.graphml ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_4a_edited_substances_avoid


python SGP_fromGraphML.py ../../data/output/example_4b_sgp_edited_graph_orig.graphml  NWFOHDSVPZKRKC-UHFFFAOYSA-N ../../data/output/example_4b_edited_sgp_pruned.graphml ../../data/output/unique_substances_starting_material_annotated.tsv ../../data/input/example_4b_edited_substances_avoid

#python SGP.py ../../data/input/example_5.json JURMMYUXJDLGNG-UHFFFAOYSA-N ../../data/output/example_5_sgp ../../data/output/unique_substances_starting_material_annotated.tsv


	

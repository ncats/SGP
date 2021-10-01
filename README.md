# SGP Source Code and Data Repository


This repository is associated with the study disclosed in manuscript:
<BR>
<BR>
*Zahoranszky-Kohalmi et al.*, Algorithm for the Pruning of Synthesis Graphs. 


## Instructions to Reproduce the Workflow 
<BR>


### Prerequisites

The workflow was tested successfully on Python version 3.6.7.

1. Install **Git Large File Support (Git LFS)**


	- Follow instructions to install Git LFS *before* cloning the Git repository, see: https://git-lfs.github.com/




2. Clone repository

	- Create a working directory "**sgp_rep**" which is in the user's home directory 
	(*/home/user/sgp_rep* in linux, */Users/user/sgp_rep on Mac*)

	- Change directory to working directory:

		`cd ~/sgp_rep/`


	- Clone repo:


		`git clone https://github.com/ncats/SGP`

	- Change to source code directory:

		`cd SGP/code/`




3. Setting up Conda environment

	- Follow OS specific instructions to install Conda, see: https://docs.conda.io/en/latest/miniconda.html

	- Once Conda is installed, create a clean conda environment (make sure you're in the `SGP/code/` directory of the repository, in this example this location of this directory is `~/sgp_rep/SGP/code/` ):

		if you have a Linux environment, then:

		`conda env create -f sgp_env_linux.yml`


		if you have a Mac environment, then:

		`conda env create -f sgp_env_mac.yml`



	- Activate the Conda environment

		`conda activate sgp`


### Reproducing the Experiments

1. Change to `~/sgp_rep/SGP/code/SGP/` directory

`cd ~/sgp_rep/SGP/code/SGP`

2. Activate Conda environment

`conda activate sgp`

3. Run workflows


`bash workflow.sh`

`bash si_workflow.sh`


### Remarks


- Creating conda dependencies
<BR>
<BR>
`conda env export --name sgp --file sgp_env_linux.yml`
<BR>
<BR>
`conda env export --name sgp --file sgp_env_mac.yml`






### LICENSE REMARKS


This repository contains source code, and data and results files which are organized into various subdirectories.

Source code subdirectories:

`code/`


Data and results subdirectory:

`data/`


- Source Code License of **SGP** Repository

	The applicable license to source code can be found under filename: `code/LICENSE` . This license is applicable to all files recursively in the Source code subdirectories as defined above. The file `code/NOTES` lists source code modules that were utilized and their respective licenses. These modules have their own licenses which might be different from the Source Code License of this repository, and they need to be respected accordingly.

- Data License of **SGP** Repository

	The applicable license to data and results can be found under filename: `data/LICENSE` . This license is applicable to all files recursively in the Data and results subdirectory as defined above. The file `data/NOTES` lists input files and resources utilized to perform the experiments and are considered as derivative work of those resources. These input files and resources have their own licenses which might be different from the Data License of this repository, and they need to be respected accordingly. In the same file we also list which results files can be considered as derivative works, and we also list the the respective ascendent data source(s).




### References

https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/04-sharing-environments/index.html
<BR>
<BR>
https://git-lfs.github.com/
<BR>
<BR>
https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment
<BR>
<BR>
https://unix.stackexchange.com/questions/1136/batch-renaming-files
<BR>
<BR>
https://unix.stackexchange.com/questions/34549/how-to-rename-multiple-files-by-removing-the-extension


	
	


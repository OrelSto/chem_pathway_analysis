"""
Module Name
read_reaction_system

A brief description of what this module does or provides.

Detailed Description:
- Provide additional details about the module's functionality.
- Mention any key classes, functions, or variables defined in the module.
- Explain the module's role in the larger project or system.

Usage:
- Describe how to import this module.
- Provide examples of how to use the module's features or classes.
- Mention any common use cases.

Dependencies:
- List any external libraries or modules that this module depends on.
- Include version requirements if necessary.

Author:
- Your name or the name of the module's author.

License:
- Specify the module's licensing information if applicable.

Note:
- Include any important notes, warnings, or considerations.
- This module is part of the sub-package i__user_model from CPAP

"""

import json

def read_chemical_system(json_filename:str):
    # Open the JSON file and read its contents
    with open(json_filename, 'r') as json_file:
        # Parse the JSON data and store it in a variable
        json_data = json.load(json_file)
    
    return json_data

def format_first_pathway(reaction:list,index:int):
    pathway_data = {
        "index":index,
        "reactions":[{
            "index":reaction["index"],
            "multiplicity":1}],
        "branching points":[reaction["results"]],
        "rate":reaction["rate"]
    }
    return pathway_data

def init_pathways(json_filename:str):

    # Empty list of active pathways
    active_pathways = []

    # We save the JSON stucture into a dict
    chemical_system = read_chemical_system(json_filename=json_filename)

    # Then, we go through the chemical system and save the initial reactions as pathways
    ind=1
    for reaction in chemical_system:
        active_pathways.append(format_first_pathway(reaction=reaction,index=ind))
        ind += 1
    
    # Write the JSON data to an output file
    with open('active_pathways.json', 'w') as output_file:
        json.dump(active_pathways, output_file, indent=2)
    
    # Write the JSON data to an output file
    with open('deleted_pathways.json', 'w') as output_file:
        json.dump([], output_file, indent=2)

    print("Initialization of Active Pathways saved as active_pathways.json")
    print("Initialization of Deleted Pathways saved as deleted_pathways.json")

    
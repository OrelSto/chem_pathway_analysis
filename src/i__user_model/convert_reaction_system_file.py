"""
Module Name
convert_reaction_system_file

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
- This module is part of the sub-package i__user_model from CPA

"""

import json
import re

# Function to extract the compound and stoichiometry from a term
def extract_compound_and_stoichiometry(term:str):
    """extract_compound_and_stoichiometry _summary_

    _extended_summary_

    Parameters
    ----------
    term : str
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # Define a regular expression pattern to match stoichiometry numbers
    stoichiometry_pattern = re.compile(r'(\d*)\s*(\w+)')

    match = stoichiometry_pattern.match(term)
    if match:
        stoichiometry = int(match.group(1)) if match.group(1) else 1
        compound = match.group(2)
        return {"compound": compound, "stoichiometry": stoichiometry}
    else:
        return None

def format_line(reaction_equation:str):
    """format_line _summary_

    _extended_summary_

    Parameters
    ----------
    reaction_equation : str
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # Split the reaction equation into reactants and products
    reactants, products = reaction_equation.split(' => ')
    products, rate = products.split(' k ',1)

    # Split reactants and products into individual compounds
    reactants = reactants.split(' + ')
    products = products.split(' + ')

    # Create a list to store reactant, product and result data
    reactant_data = []
    product_data = []
    result_data = []

    # Process and merge reactant terms
    for term in reactants:
        compound_data = extract_compound_and_stoichiometry(term.strip())
        if compound_data:
            # Check if the compound already exists in reactant_data
            existing_compound = next((c for c in reactant_data if c["compound"] == compound_data["compound"]), False)
            if existing_compound:
                # If the compound exists, add its stoichiometry
                existing_compound["stoichiometry"] += compound_data["stoichiometry"]
            else:
                # If the compound does not exist, add it to reactant_data
                reactant_data.append(compound_data)
    
    # Process and merge products terms
    for term in products:
        compound_data = extract_compound_and_stoichiometry(term.strip())
        if compound_data:
            # Check if the compound already exists in reactant_data
            existing_compound = next((c for c in product_data if c["compound"] == compound_data["compound"]), False)
            if existing_compound:
                # If the compound exists, add its stoichiometry
                existing_compound["stoichiometry"] += compound_data["stoichiometry"]
            else:
                # If the compound does not exist, add it to product_data
                product_data.append(compound_data)
    
    # Process the results
    # First do the reactants
    for reactant in reactant_data:
        result = {}
        result["compound"] = reactant["compound"]
        # Check if the compound already exists in product_data
        exist_in_products = next((c for c in product_data if c["compound"] == reactant["compound"]), False)
        if exist_in_products:
            # If the compound exists, add its stoichiometry
            result["stoichiometry"] = -reactant["stoichiometry"] + exist_in_products["stoichiometry"]
        else:
            # If the compound does not exist, just the reactant stoichiometry
            result["stoichiometry"] = -reactant["stoichiometry"]
        # Appending to the results
        result_data.append(result)

    # Second do the products
    for product in product_data:
        # Check if the compound already exists in product_data
        exist_in_reactants = next((c for c in reactant_data if c["compound"] == product["compound"]), False)
        if exist_in_reactants:
            # If the compound exists,do nothing
            pass
        else:
            # If it does not exist, appending to the results
            result_data.append(product)

    # Create a JSON structure
    reaction_data = {
        "reactants": reactant_data,
        "products": product_data,
        "rate": float(rate),
        "results": result_data
    }

    return reaction_data

def convert_chemical_reaction_file(filename:str):
    """convert_chemical_reaction_file _summary_

    _extended_summary_

    Parameters
    ----------
    filename : str
        _description_
    """

    # # Read the content of the input text file
    # with open('user_model_example.txt', 'r') as file:
    #     reaction_equation = file.read()

    # Empty list of all reactions
    chemical_system = []
    
    # Read the content of the input text file line by line
    with open(filename, 'r') as file:
        while line := file.readline():
            reaction_equation = line.rstrip()

            chemical_system.append(format_line(reaction_equation))

    # Write the JSON data to an output file
    with open('chemical_reaction_system.json', 'w') as output_file:
        json.dump(chemical_system, output_file, indent=2)

    print("Conversion to JSON format complete.")


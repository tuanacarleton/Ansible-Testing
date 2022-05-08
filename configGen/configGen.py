#####################################################################################
#  Script that ingests data from YAML variables and renders the configuration
#  with Jinja2 configuration templates. 
#####################################################################################
import sys
import csv
import yaml
import jinja2
from pathlib import Path

# Takes a CSV and device interface template and creates the appropriate interface configs 
def interfacesFromCSV(source_file, interface_template_file):
    # String that will hold final full configuration of all interfaces
    interface_configs = ""

# Open up the Jinja template file (as text) and then create a Jinja Template Object 
    with open(interface_template_file) as f:
        interface_template = jinja2.Template(f.read(), keep_trailing_newline=True)

    # Open up the CSV file containing the data 
    with open(source_file) as f:
        # Use DictReader to access data from CSV 
        reader = csv.DictReader(f)
        # For each row in the CSV, generate an interface configuration using the jinja template 
        for row in reader:
            interface_config = interface_template.render(
                interface = row["Interface"],
                vlan = row["VLAN"],
                server = row["Server"],
                link = row["Link"],
                purpose = row["Purpose"]
            )

            # Append this interface configuration to the full configuration 
            interface_configs += interface_config

    return interface_configs

def main():
    # We will be using the sys.argv method to collect the arguments passed
    # Also to have the values as proper systems Paths and not worry about termination
    # based on filesystem, we are leveraging the Path object from pathlib
    variables_file = Path(sys.argv[1])
    index_file = Path(sys.argv[2])
    source_file = "data/switch-ports.csv"
    interface_template_file = "templates/switchport-interface-template.j2"
    configuration_data = ''

    # Get the config data from file
    with open(variables_file, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    # Open the index file and load the defined templates
    with open(index_file, "r") as f:
        index = f.readlines()
        for i in index:

            # Get the template data from file
            with open(i.strip(), "r") as f:
                template_data = f.read()

                # Generate template object
                template = jinja2.Template(template_data)

                # Render the template
                configuration_data += template.render(data)

    configuration_data += interfacesFromCSV(source_file, interface_template_file)

    # Save the configuration to output file
    output_file = "build/conf.txt"
    with open(output_file, "w") as f:
        f.write(configuration_data)

    print("Created {}".format(output_file))
    return


if __name__ == "__main__":
    main()
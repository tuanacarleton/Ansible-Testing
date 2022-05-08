#####################################################################################
#  Script that ingests data from YAML variables and renders the configuration
#  with Jinja2 configuration templates. 
#####################################################################################
import sys
import yaml
import jinja2
from pathlib import Path


def main():
    # We will be using the sys.argv method to collect the arguments passed
    # Also to have the values as proper systems Paths and not worry about termination
    # based on filesystem, we are leveraging the Path object from pathlib
    variables_file = Path(sys.argv[1])
    index_file = Path(sys.argv[2])
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

    # Save the configuration to output file
    output_file = "build/conf.txt"
    with open(output_file, "w") as f:
        f.write(configuration_data)

    print("Created {} File! -->".format(output_file))
    print(configuration_data)
    return


if __name__ == "__main__":
    main()
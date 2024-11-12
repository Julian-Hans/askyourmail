from typing import List, Tuple
import yaml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class PromptBlueprint:
    """Class for retrieving prompt blueprints based on agent class names and versions."""

    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def get_blueprint(cls, class_name: str, version: str = "v1") -> List[Tuple[str, str]]:
        """Retrieve and return the prompt blueprint for a given class and version.

        Args:
            class_name (str): The class name of the agent whose blueprint is required.
            version (str): The version of the blueprint to retrieve (default is "v1").

        Raises:
            FileNotFoundError: If the blueprint file does not exist.
            KeyError: If the specified version is not found in the blueprint file.
            ValueError: If any other issues occur while fetching the blueprint.

        Returns:
            List[Tuple[str, str]]: A list of tuples, each containing (type, prompt).
        """
        filename = os.path.join(cls.SCRIPT_DIR, f"{class_name}Prompt.yaml")
        
        if not os.path.exists(filename):
            log.error(f"blueprint file {filename} not found.")
            raise FileNotFoundError(f"blueprint file {filename} not found.")

        try:
            with open(filename, 'r') as file:
                blueprints = yaml.safe_load(file)

            if version not in blueprints:
                log.error(f"Version '{version}' not found in {filename}.")
                raise KeyError(f"Version '{version}' not found in {filename}.")

            blueprint_list = blueprints[version]
            return [(item['type'], item['prompt']) for item in blueprint_list]

        except yaml.YAMLError as e:
            log.error(f"Error parsing YAML in {filename}: {e}")
            raise ValueError(f"Error parsing YAML in {filename}: {e}")

        except Exception as e:
            log.error(f"An unexpected error occurred while retrieving the blueprint: {e}")
            raise ValueError(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        blueprint = PromptBlueprint.get_blueprint("MethodAnalyserAgent", "v2")
        print(blueprint)
    except Exception as e:
        log.error(f"Error retrieving blueprint: {e}")

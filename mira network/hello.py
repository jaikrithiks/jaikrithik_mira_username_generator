from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
import os
import glob
from mira_sdk import MiraClient


client = MiraClient(config={"API_KEY": "sb-cf43d104d1e7a63553979a3305f0eb73"})
# Load environment variables
load_dotenv()

# Initialize Mira client with API key from .env file
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})


def deploy_flows():
    """
    Deploy all flows defined in YAML files in the `flows` directory.
    """
    # Get all YAML files in the `flows` directory
    flow_files = glob.glob("flows/*.yaml")

    for flow_file in flow_files:
        try:
            print(f"Deploying flow: {flow_file}")
            
            # Create flow from YAML file
            flow = Flow(source=flow_file)

            # Deploy flow to the Mira platform
            client.flow.deploy(flow)

            # Extract flow name from file name and construct flow ID
            flow_name = os.path.splitext(os.path.basename(flow_file))[0]
            flow_id = f"Jaikrithik/{flow_name}"  # Adjust to match your namespace
            print(f"Flow deployed successfully with ID: {flow_id}")

        except FlowError as e:
            print(f"FlowError while deploying {flow_file}: {e}")
        except Exception as e:
            print(f"Unexpected error with {flow_file}: {e}")

def test_flow(flow_id, inputs):
    """
    Test a deployed flow by executing it with the provided inputs.
    """
    try:
        print(f"Testing flow with ID: {flow_id}")
        
        # Execute the flow with given inputs
        result = client.flow.execute(flow_id, inputs)
        return result

    except FlowError as e:
        print(f"FlowError while testing flow {flow_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while testing flow {flow_id}: {e}")
        return None

def main():
    """
    Main function to deploy flows and test the `username-generator-project` flow.
    """
    # Deploy the flow(s)
    print("Deploying flow...")
    deploy_flows()

    # Test the `cusername-generator-project` flow
    code_sample = """
    def add(a, b):
        return a + b  # No type hints or error handling
    """
    print("\nTesting `username-generator` flow...")
    
    # Test inputs for the username-generator-project flow
    result = test_flow("Jaikrithik/Username-generator-project", {
    "text1": "jai krithik",
    "text2": "github"
})


    if result:
        print("\nusername-generator-project Output:")
        print(result)
    else:
        print("\nFailed to test the username-generator-project flow.")

if __name__ == "__main__":
    main()

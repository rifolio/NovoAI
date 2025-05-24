import torch

def inspect_pth_file(file_path):
    """
    Loads a .pth file and prints the names and shapes of its parameters.

    Args:
        file_path (str): The path to the .pth file.
    """
    print(f"--- Inspecting: {file_path} ---")
    try:
        checkpoint = torch.load(file_path, map_location=torch.device('cpu'))

        state_dict = None
        if isinstance(checkpoint, dict):

            possible_keys = ['state_dict', 'model_state_dict', 'model', 'net']
            for key in possible_keys:
                if key in checkpoint and isinstance(checkpoint[key], dict):
                    state_dict = checkpoint[key]
                    print(f"Found state_dict under key: '{key}'")
                    break

            if state_dict is None:
                state_dict = checkpoint
                print("Assuming the loaded object is the state_dict itself.")
        elif isinstance(checkpoint, dict):
             state_dict = checkpoint
             print("Loaded object is a dictionary, assuming it's the state_dict.")
        else:
            print("Warning: Loaded object is not a dictionary. Attempting to treat as state_dict, but might fail.")

            state_dict = checkpoint

        if not hasattr(state_dict, 'items'):
             print("Error: Could not find or interpret the state_dict in the file.")
             print(f"File contains object of type: {type(checkpoint)}")
             return

        print("\nParameters found:")
        total_params = 0
        for name, param in state_dict.items():
            print(f"  {name:<60} | Shape: {param.shape}")
            total_params += param.numel()

        print(f"\nTotal number of parameters in the state_dict: {total_params}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred while inspecting {file_path}: {e}")
    print("-" * (len(file_path) + 20) + "\n")


detr_model_path = 'path/to/your/detr_model.pth' # <--- CHANGE THIS
tatr_model_path = 'path/to/your/tatr_model.pth' # <--- CHANGE THIS

# --- Inspect the files ---
inspect_pth_file(detr_model_path)
inspect_pth_file(tatr_model_path)
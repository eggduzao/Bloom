import os
import sys
import subprocess
from pathlib import Path

def run_on_remote_node(node: str, script_path: str, conda_env: str):
    """
    Runs the specified Python script on a remote node via SSH.
    
    Parameters:
    -----------
    node : str
        Hostname of the node to run the script on (e.g., "compute02").
    script_path : str
        Absolute path of the Python script on the remote node.
    """

    script_path = Path(script_path).resolve()
    script_directory = script_path.parent
    script_name = Path(script_path).name

    command = (
        f"nohup bash -c 'source /sw/miniconda3/etc/profile.d/conda.sh && "
        f"source /home/egusmao/.bashrc && "
        f"cd {script_directory} && "
        f"conda activate {conda_env} && "
        f"python {script_name}' "
        f"> {script_directory}/{node}_info.txt 2>&1 &"
    )

    ssh_command = ["ssh", node, command]

    print(f"Running remotely on node {node}: {command}")
    subprocess.run(ssh_command)

def merge_node_outputs(output_dir: str, merged_filename: str = "cluster_summary.txt"):
    """
    Merge node-specific output files into one summary file.

    Parameters:
    -----------
    output_dir : str
        Directory containing the node output files (e.g., "node1_info.txt").
    """
    output_dir = Path(output_dir)
    merged_output = output_dir / merged_filename

    with merged_output.open('w') as outfile:
        for file in sorted(output_dir.glob("no*_info.txt")):
            node_name = file.stem.replace("_info", "")
            outfile.write(f"=== Node: {node_name} ===\n")
            outfile.write(file.read_text() + "\n\n")
        for file in sorted(output_dir.glob("no*_info.txt")):
            file_to_delete = Path(file)
            file_to_delete.unlink()

# Example of usage:
if __name__ == "__main__":

    # Parameters
    compute_nodes = ["node1", "node2", "node3", "node4"]
    script = "/storage2/egusmao/projects/Bloom/scripts/check_cluster_nodes.py"
    conda_env = "ml"

    # Running for each node
    #for compute_node in compute_nodes:
    #    run_on_remote_node(compute_node, script, conda_env)

    merge_node_outputs(".", merged_filename="cluster_summary.txt")

# rm no*_info.txt
# mv /home/egusmao/*_info.txt .


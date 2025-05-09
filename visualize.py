import pandas as pd
import matplotlib.pyplot as plt
import io  # Required to read string data as a file

# CSV data provided by the user
csv_data = """Search Type,Depth,Nodes Expanded,Max Queue Size
Manhattan,2,3,5
Manhattan,3,4,4
Manhattan,18,145,101
Manhattan,26,2521,1409
Manhattan,31,7132,3573
Misplaced,2,3,5
Misplaced,3,4,4
Misplaced,18,1093,664
Misplaced,26,28016,12620
Misplaced,31,124658,24434
UCS,2,8,8
UCS,3,12,14
UCS,18,23130,11644
UCS,26,119826,24054
UCS,31,127788,25134
"""


def create_plots_from_data(data):
    """
    Generates and saves two plots from the provided puzzle solver data:
    1. Nodes Expanded vs. Depth
    2. Max Queue Size vs. Depth

    Args:
        data (str): A string containing the CSV data.
    """
    try:
        # Use io.StringIO to treat the string data as a file
        df = pd.read_csv(io.StringIO(data))
    except Exception as e:
        print(f"Error reading CSV data: {e}")
        return

    # Ensure required columns are present
    required_columns = {"Search Type", "Depth", "Nodes Expanded", "Max Queue Size"}
    if not required_columns.issubset(df.columns):
        print(
            f"Error: CSV data must contain the columns: {', '.join(required_columns)}"
        )
        print(f"Found columns: {', '.join(df.columns)}")
        return

    # Get unique search types for iterating and labeling
    search_types = df["Search Type"].unique()

    # --- Plot 1: Nodes Expanded vs. Depth ---
    plt.figure(figsize=(10, 6))  # Define figure size

    for search_type in search_types:
        # Filter data for the current search type
        subset = df[df["Search Type"] == search_type].sort_values(by="Depth")
        if not subset.empty:
            plt.plot(
                subset["Depth"],
                subset["Nodes Expanded"],
                marker="o",
                linestyle="-",
                label=search_type,
            )
        else:
            print(
                f"Warning: No data found for search type '{search_type}' for Nodes Expanded plot."
            )

    plt.title("Nodes Expanded vs. Solution Depth", fontsize=16)
    plt.xlabel("Solution Depth", fontsize=12)
    plt.ylabel("Number of Nodes Expanded", fontsize=12)
    plt.xticks(
        sorted(df["Depth"].unique())
    )  # Ensure all depth points are marked on x-axis
    plt.legend(fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()  # Adjust layout

    # Save the first plot
    nodes_expanded_plot_path = "nodes_expanded_vs_depth_plot.png"
    try:
        plt.savefig(nodes_expanded_plot_path)
        print(f"Plot 1: Nodes Expanded vs. Depth saved as '{nodes_expanded_plot_path}'")
    except Exception as e:
        print(f"Error saving Nodes Expanded plot: {e}")
    # plt.show() # Uncomment to display plot interactively

    # --- Plot 2: Max Queue Size vs. Depth ---
    plt.figure(figsize=(10, 6))  # Define figure size for the second plot

    for search_type in search_types:
        # Filter data for the current search type
        subset = df[df["Search Type"] == search_type].sort_values(by="Depth")
        if not subset.empty:
            plt.plot(
                subset["Depth"],
                subset["Max Queue Size"],
                marker="s",
                linestyle="--",
                label=search_type,
            )  # Different marker/linestyle
        else:
            print(
                f"Warning: No data found for search type '{search_type}' for Max Queue Size plot."
            )

    plt.title("Maximum Queue Size vs. Solution Depth", fontsize=16)
    plt.xlabel("Solution Depth", fontsize=12)
    plt.ylabel("Maximum Queue Size", fontsize=12)
    plt.xticks(
        sorted(df["Depth"].unique())
    )  # Ensure all depth points are marked on x-axis
    plt.legend(fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()  # Adjust layout

    # Save the second plot
    max_queue_plot_path = "max_queue_size_vs_depth_plot.png"
    try:
        plt.savefig(max_queue_plot_path)
        print(f"Plot 2: Max Queue Size vs. Depth saved as '{max_queue_plot_path}'")
    except Exception as e:
        print(f"Error saving Max Queue Size plot: {e}")
    # plt.show() # Uncomment to display plot interactively


if __name__ == "__main__":
    # Call the function with the CSV data string
    create_plots_from_data(csv_data)

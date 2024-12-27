import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
import io
import contextlib
import matplotlib.pyplot as plt

def main():
    # Set the page configuration
    st.set_page_config(page_title="Code Editor with Visualization", layout="wide")

    # Page title
    st.title("Interactive Code Editor with Database Access and Visualization")

    # Instructions
    st.markdown(
        """
        Welcome to the interactive code editor! Here you can write Python code, edit it, and run it directly.
        The Lego dataset has been preloaded and is available as a pandas DataFrame named `lego_data`.

        1. Write your code in the editor below.
        2. Use `lego_data` to analyze the dataset.
        3. Generate visualizations using libraries like matplotlib.
        4. Click the 'Run Code' button to execute it.
        5. View the output and graphs below.
        """
    )

    # Load the dataset
    try:
        data_path = "lego_block_dataset_with_availability.csv"
        lego_data = pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")
        return

    # Default code in the editor
    default_code = """# Analyze the Lego dataset\n\n# The dataset is loaded as 'lego_data'.\n# Example: Display the first 5 rows\nprint(lego_data.head())\n\n# Visualization example\nimport matplotlib.pyplot as plt\n\n# Group the data by color and calculate the total quantity\ncolor_group = lego_data.groupby('Block Color')['Available Quantity'].sum()\n\n# Create a bar chart\nplt.figure(figsize=(10, 6))\ncolor_group.plot(kind='bar', color=['red', 'blue', 'yellow', 'green', 'black', 'gray'])\nplt.title('Total Quantity of Lego Blocks by Color')\nplt.xlabel('Block Color')\nplt.ylabel('Available Quantity')\nplt.xticks(rotation=45)\nplt.tight_layout()\n\n# Show the plot\nst.pyplot(plt)\n"""

    # Create the code editor
    code = st_ace(
        value=default_code,
        language="python",
        theme="monokai",
        key="ace_editor",
        height=300
    )

    # Run the code
    if st.button("Run Code"):
        try:
            # Capture the output of the executed code
            output_buffer = io.StringIO()
            exec_globals = {"lego_data": lego_data, "st": st, "plt": plt}
            with contextlib.redirect_stdout(output_buffer):
                exec(code, exec_globals)
            output = output_buffer.getvalue()
            st.text_area("Output", value=output, height=200)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()

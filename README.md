# GraphRAG

👉 [Use the GraphRAG Accelerator solution](https://github.com/Azure-Samples/graphrag-accelerator) <br/>
👉 [Microsoft Research Blog Post](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)<br/>
👉 [Read the docs](https://microsoft.github.io/graphrag)<br/>
👉 [GraphRAG Arxiv](https://arxiv.org/pdf/2404.16130)

<div align="left">
  <a href="https://pypi.org/project/graphrag/">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/graphrag">
  </a>
  <a href="https://pypi.org/project/graphrag/">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/graphrag">
  </a>
  <a href="https://github.com/microsoft/graphrag/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/microsoft/graphrag">
  </a>
  <a href="https://github.com/microsoft/graphrag/discussions">
    <img alt="GitHub Discussions" src="https://img.shields.io/github/discussions/microsoft/graphrag">
  </a>
</div>

## Overview

The GraphRAG project is a data pipeline and transformation suite that is designed to extract meaningful, structured data from unstructured text using the power of LLMs.

To learn more about GraphRAG and how it can be used to enhance your LLM's ability to reason about your private data, please visit the <a href="https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/" target="_blank">Microsoft Research Blog Post.</a>

## Instructions for GraphRAG

### Step 1: Clone the Repository Using GitHub Desktop

1. Download GitHub Desktop from [here](https://desktop.github.com/download/) and install it.
2. Open GitHub Desktop, log in to your GitHub account, and go to **File > Clone repository**.
3. Choose the **URL** tab and paste the following link:
   ```
   https://github.com/xtxxxxxtx/graphrag.git
   ```
4. Select a local path where you would like to save the repository. Remember this location, as you’ll need it in the following steps.
   > **Note:** An example is shown below.
   
   > <img src="https://github.com/user-attachments/assets/34fcc0e6-7655-4195-a7a2-c977cca50d0c" alt="image" width="600"/>

### Step 2: Navigate to the GraphRAG Directory

1. Open **Terminal** and navigate to the ```graphrag``` directory you just cloned. Use the following command, replacing ```...``` with your local path:
   ```
   cd ...
   ```
   **Example:**
   ```
   cd /Users/xu/Desktop/graphrag
   ```

### Step 3: Start the GraphRAG Environment

1. **Skip this installation** if you already have ```poetry``` installed. Otherwise, copy and paste the commands below into Terminal to install it:

   **On MacOS/Linux:** For Mac/Linux user, you will need [brew](https://brew.sh/) be installed first.
   ```
   brew install pipx
   pipx ensurepath
   ```
   **On Windows:** For Windows user, you will need [scoop](https://scoop.sh/) be installed first.
   ```
   scoop install pipx
   pipx ensurepath
   ```
   > **Note:** For more information about ```pipx```, you can visit [the pipx documentation](https://pipx.pypa.io/stable/installation/).
3. With ```pipx``` installed, you can now install ```poetry```:
   ```
   pipx install poetry
   ```
4. Run the following command to activate the required environment:
   ```
   poetry shell
   ```

### Step 4: Download Test Papers

1. Visit [the link](https://wustl.box.com/s/wvi9z297a90d6ymdn3swas4fzezwliia) and download the ```ragtest``` folder, which contains the six sample papers.
2. Place the ```ragtest``` folder inside the main ```graphrag``` folder.
   > **Note:** There is a secondary ```graphrag``` folder within the main one. Make sure to place ```ragtest``` inside the main graphrag folder.
   

### Step 5: Test a Query

Run the following command in Terminal, modifying the query text as needed:
```
PYTHONPATH="$(pwd)" python ad_graphrag/query/__main__.py --root ragtest --method global "What is the main topic in these papers?"
```
> **Note:** Feel free to change the query text within the quotation marks to test different questions.

In default, relevant score, all related communities, entities, relationship, and selected text chunks will be print out 
for each intermediate response. If you only want final answer, as the original GraphRAG, just do:
```
PYTHONPATH="$(pwd)" python ad_graphrag/query/__main__.py --root ragtest --no_reverse --method global "What is the main topic in these papers?"
```

If you want to see the relevant information for the final answer, run as the follow:
```
PYTHONPATH="$(pwd)" python ad_graphrag/query/__main__.py --root ragtest --final_response --method global "What is the main topic in these papers?"
```

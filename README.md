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

### Step 1: Set Up Your Directory

1. Open the **Terminal** application.
2. Navigate to the directory where you'd like to download the repository. Replace ```...``` with your preferred path:
   ```
   cd ...
   ```
   **Example:***
   ```
   cd /Users/xu/Downloads
   ```

### Step 2: Download the GraphRAG Repository

1. Copy and paste the following command into Terminal to download the repository:
   ```
   git clone https://github.com/xtxxxxxtx/graphrag.git
   ```
2. Enter the newly created ```graphrag``` directory:
   ```
   cd graphrag/
   ```
3. To ensure you always have the latest updates, run these commands whenever you use GraphRAG (Not necessary for the first time):
   ```
   git fetch
   git pull
   ```

### Step 3: Start the GraphRAG Environment

1. **Skip this installation** if you already have ```poetry``` installed. Otherwise, follow the steps below to install it using ```pipx```.

   **On MacOS:**
   ```
   brew install pipx
   pipx ensurepath
   ```
   **On Windows:**
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

1. Run the following command in Terminal, modifying the query text as needed:
   ```
   PYTHONPATH="$(pwd)" python ad_graphrag/query/__main__.py --root ragtest --method global "What is the main topic in these papers?"
   ```
   > **Note:** Feel free to change the query text within the quotation marks to test different questions.

## Quickstart

To get started with the GraphRAG system we recommend trying the [Solution Accelerator](https://github.com/Azure-Samples/graphrag-accelerator) package. This provides a user-friendly end-to-end experience with Azure resources.

## Repository Guidance

This repository presents a methodology for using knowledge graph memory structures to enhance LLM outputs. Please note that the provided code serves as a demonstration and is not an officially supported Microsoft offering.

⚠️ *Warning: GraphRAG indexing can be an expensive operation, please read all of the documentation to understand the process and costs involved, and start small.*

## Diving Deeper

- To learn about our contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md)
- To start developing _GraphRAG_, see [DEVELOPING.md](./DEVELOPING.md)
- Join the conversation and provide feedback in the [GitHub Discussions tab!](https://github.com/microsoft/graphrag/discussions)

## Prompt Tuning

Using _GraphRAG_ with your data out of the box may not yield the best possible results.
We strongly recommend to fine-tune your prompts following the [Prompt Tuning Guide](https://microsoft.github.io/graphrag/prompt_tuning/overview/) in our documentation.

## Responsible AI FAQ

See [RAI_TRANSPARENCY.md](./RAI_TRANSPARENCY.md)

- [What is GraphRAG?](./RAI_TRANSPARENCY.md#what-is-graphrag)
- [What can GraphRAG do?](./RAI_TRANSPARENCY.md#what-can-graphrag-do)
- [What are GraphRAG’s intended use(s)?](./RAI_TRANSPARENCY.md#what-are-graphrags-intended-uses)
- [How was GraphRAG evaluated? What metrics are used to measure performance?](./RAI_TRANSPARENCY.md#how-was-graphrag-evaluated-what-metrics-are-used-to-measure-performance)
- [What are the limitations of GraphRAG? How can users minimize the impact of GraphRAG’s limitations when using the system?](./RAI_TRANSPARENCY.md#what-are-the-limitations-of-graphrag-how-can-users-minimize-the-impact-of-graphrags-limitations-when-using-the-system)
- [What operational factors and settings allow for effective and responsible use of GraphRAG?](./RAI_TRANSPARENCY.md#what-operational-factors-and-settings-allow-for-effective-and-responsible-use-of-graphrag)

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

## Privacy

[Microsoft Privacy Statement](https://privacy.microsoft.com/en-us/privacystatement)

# Order Matters: The Impact of Positional Bias in LLM-Based Recommender Systems

This code allow the reproducibility of the experiments performed for bias detection in recommender systems based on Large Language Models.

> **Authors**: Carlos Peláez-González, Andrés Herrera-Poyatos, Francisco Herrera Triguero
> 
> **Conference/Journal**: 
>
> **Code License**: 

---

## 📄 Abstract

Large Language Models (LLMs) have demonstrated impressive capabilities across a wide range of natural language tasks, including their use in building recommender systems (RS). Among these, conversational RS allow users to express preferences via text, enabling personalized item recommendations without model retraining. However, as black-box systems, LLM-based RS can exhibit hidden biases that compromise their reliability. This paper investigates positional bias—how the order of items in the prompt affects recommendation outcomes. We propose two methodologies: one based on contingency matrix analysis with statistical independence testing, and another grounded in a uniformity assumption. Our results reveal a consistent positional bias in LLM-based RS, even when item relevance is constant. These findings highlight the need for deeper auditing of prompt-based recommendation pipelines.

---

## 🏗️ Project Structure

```bash
├── data/               # [Auto-generated] Includes amazon index and user queries
├── results/            # [Auto-generated] Output logs, checkpoints, metrics
├── scripts/            # Dataset creation and bias evaluation code
├── notebooks/          # Jupyter notebooks for analysis/visualization
├── src/                # Common source code for the scripts
├── environment.yml     # Python dependencies (conda)
└── README.md           # This file
```

---

## 🔧 Reproducibility commands

In order to replicate the paper results, the following steps should be followed.

 1. Configure environment
    ```bash
    conda env create -n llm_positional_bias -f environment.yml
    conda activate llm_bias_attack
    export PYTHONPATH="$(pwd)/src"
    ```
 3. Download products dataset
    ```bash
    mkdir -p data/dataset
    # Download from https://www.kaggle.com/datasets/ashisparida/amazon-ml-challenge-2023
    # Uncompress and place the CSV at data/dataset/train.csv
    ```
 5. Generate search engine
    ```bash
    python scripts/dataset_creation/create_index.py -d data/dataset/train.csv -o data/amazon_index
    ```
 7. Generate queries automatically
    ```bash
    python scripts/dataset_creation/generate_queries.py -o data/generated_queries.json
    ```
 9. Create evaluation dataset
    ```bash
    mkdir data/shuffled_products
    python scripts/dataset_creation/sample_products_shuffles.py -i data/generated_queries.json -s data/amazon_index/ -o data/shuffled_products --output-name position_bias__share -n 0 -k 5 --share-permutations
    ```
 11. Launch Ollama and pull model/s (available models at https://ollama.com/library?sort=newest)
     ```bash
     docker pull ollama/ollama:0.11.4
     ./launch_ollama
     docker exec ollama0 ollama pull <MODEL_NAME>
     # The provided script assumes that one model fits on one GPU. Feel free to manually launch the container if it is not the case.
     ```
 13. Process queries and associated products with one LLM (evaluate the LLM)
     ```bash
     mkdir -p results/position_bias__share
     python scripts/evaluation/evaluate_bias.py -i data/shuffled_products/position_bias__share.json -m <MODEL_NAME> -o results/position_bias__share/evaluation_<MODEL_NAME>.json
     ```
 15. Analyze the data
     ```bash
     mkdir figures
     jupyter-notebook
     # Open the notebook notebooks/initialBias_analysis.ipynb
     # Execute the cells to generate the provided results
     ```

---

## ✏️ How to reference this work

If you find this work useful for your research, please cite it as the following.

```bibtex
<TBD>
```

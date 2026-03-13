# A statistical analysis of positional bias in LLM-Based Recommender Systems

This code allow the reproducibility of the experiments performed for bias detection in recommender systems based on Large Language Models.

> **Authors**: Carlos Peláez-González, Andrés Herrera-Poyatos, Francisco Herrera Triguero
> 
> **Conference/Journal**: 
>
> **Code License**: 

---

## 📄 Abstract

Large Language Models (LLMs) are increasingly being used as recommendation generators in conversational recommender systems (RS) via retrieval-augmented generation (RAG). Although this design enables flexible, natural-language interaction, it also introduces new sources of structural bias that can affect the reliability of the system. This paper studies *positional bias* in LLM-based RS: systematic dependence of the recommended item on the order in which candidate items are presented in the prompt.

We propose two complementary statistical methodologies to detect and characterize positional bias:

1. **POB-ICM**, based on contingency matrix analysis and Chi-square independence testing, and
2. **POB-UNBP**, a sample-efficient approach derived from a uniformity null model under permutation-based evaluation.

Using a controlled RAG testbed built from 730 user queries and exhaustive permutations of *k* = 5 retrieved items (87,600 query-permutation instances), we find consistent evidence that recommendation outcomes are not invariant to item ordering. Across multiple state-of-the-art model families, both methodologies reject the null hypothesis of positional independence and uniformity under conventional significance thresholds (e.g., *p* = 2.42 × 10⁻¹¹⁶ for GPT-OSS 20B under POB-ICM).

These results establish positional bias as a measurable and reproducible property of prompt-mediated recommendation pipelines and motivate routine auditing and governance controls (e.g., order randomization and standardized prompting) when deploying LLM-based RS in practice.

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
 2. Download products dataset
    ```bash
    mkdir -p data/dataset
    # Download from https://www.kaggle.com/datasets/ashisparida/amazon-ml-challenge-2023
    # Uncompress and place the CSV at data/dataset/train.csv
    ```
 3. Generate search engine
    ```bash
    python scripts/dataset_creation/create_index.py -d data/dataset/train.csv -o data/amazon_index
    ```
 4. Generate queries automatically
    ```bash
    python scripts/dataset_creation/generate_queries.py -o data/generated_queries.json
    ```
 5. Create evaluation dataset
    ```bash
    mkdir data/shuffled_products
    python scripts/dataset_creation/sample_products_shuffles.py -i data/generated_queries.json -s data/amazon_index/ -o data/shuffled_products --output-name position_bias__share -n 0 -k 5 --share-permutations
    ```
 6. Launch Ollama and pull model/s (available models at https://ollama.com/library?sort=newest)
     ```bash
     docker pull ollama/ollama:0.11.4
     ./launch_ollama
     docker exec ollama0 ollama pull <MODEL_NAME>
     # The provided script assumes that one model fits on one GPU. Feel free to manually launch the container if it is not the case.
     ```
 7. Process queries and associated products with one LLM (evaluate the LLM)
     ```bash
     mkdir -p results/position_bias__share
     python scripts/evaluation/evaluate_bias.py -i data/shuffled_products/position_bias__share.json -m <MODEL_NAME> -o results/position_bias__share/evaluation_<MODEL_NAME>.json
     ```
 8. Analyze the data
     ```bash
     mkdir figures
     jupyter-notebook
     # Open the notebook notebooks/bias_analysis.ipynb
     # Execute the cells to generate the provided results
     ```

---

## ✏️ How to reference this work

If you find this work useful for your research, please cite it as the following.

```bibtex
<TBD>
```

 1. Configure environment
    $ conda env create -n llm_positional_bias -f environment.yml
    $ conda activate llm_bias_attack
    $ export PYTHONPATH="$(pwd)/src"
 2. Generate search engine
    $ python scripts/dataset_creation/create_index.py -d data/dataset/train.csv -o data/amazon_index
 3. Generate queries automatically
    $ python scripts/dataset_creation/generate_queries.py -o data/generated_queries.json
 4. Create evaluation dataset
    $ mkdir data/shuffled_products
    $ python scripts/dataset_creation/sample_products_shuffles.py -i data/generated_queries.json -s data/amazon_index/ -o data/shuffled_products --output-name position_bias__share -n 0 -k 5 --share-permutations
 5. Launch Ollama and pull model/s (available models at https://ollama.com/library?sort=newest)
    $ docker pull ollama/ollama:0.11.4
    $ ./launch_ollama
    $ docker exec ollama0 ollama pull <MODEL_NAME>
 6. Generate evaluation
    $ mkdir -p results/position_bias__share
    $ python scripts/evaluation/evaluate_bias.py -i data/shuffled_products/position_bias__share.json -m <MODEL_NAME> -o results/position_bias__share/evaluation_<MODEL_NAME>.json
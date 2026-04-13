import json
import random
import argparse
import os

def main(args):
    output_path = args.output_path
    seed = args.seed
    n_queries = args.size

    if os.path.exists(output_path):
        raise IOError('Output file already exists')

    random.seed(seed)

    # Expanded categories with subcategories
    categories = {
        "electronics": ["wireless headphones", "smartphones", "smartwatches", "laptops", "tablets", 
                       "gaming consoles", "cameras", "e-readers", "portable speakers", "drones",
                       "wireless earbuds", "smart home hubs", "streaming devices", "projectors"],
        "fashion": ["running shoes", "summer dresses", "winter jackets", "men's suits", "designer handbags", 
                   "sportswear", "sneakers", "jeans", "t-shirts", "sweaters", "coats", "scarves",
                   "belts", "sunglasses", "watches", "boots", "sandals", "activewear"],
        "home appliances": ["microwaves", "vacuum cleaners", "air purifiers", "coffee makers", "blenders", 
                           "toasters", "dishwashers", "washing machines", "dryers", "refrigerators",
                           "air conditioners", "heaters", "humidifiers", "dehumidifiers", "food processors"],
        "beauty": ["skincare products", "perfumes", "makeup kits", "hairdryers", "organic shampoos",
                  "face masks", "serums", "moisturizers", "lipsticks", "nail polish", "hair straighteners",
                  "electric razors", "facial cleansers", "anti-aging creams"],
        "sports": ["yoga mats", "fitness trackers", "treadmills", "dumbbells", "cycling gloves",
                  "tennis rackets", "golf clubs", "soccer balls", "basketballs", "swimming goggles",
                  "workout benches", "jump ropes", "kettlebells", "foam rollers"],
        "automotive": ["car chargers", "seat covers", "dashboard cameras", "car cleaning kits",
                      "tire pressure monitors", "jump starters", "car organizers", "phone mounts",
                      "floor mats", "steering wheel covers", "GPS devices"],
        "books": ["fiction novels", "non-fiction bestsellers", "mystery novels", "science fiction books",
                 "cookbooks", "self-help books", "biographies", "children's books", "graphic novels",
                 "poetry collections", "business books", "history books"],
        "toys": ["LEGO sets", "puzzle games", "educational toys", "remote-controlled cars",
                "board games", "action figures", "dolls", "building blocks", "art supplies",
                "science kits", "stuffed animals", "play kitchens"],
        "groceries": ["organic green tea", "protein snacks", "coffee beans", "gluten-free pasta",
                     "olive oil", "quinoa", "almond milk", "dark chocolate", "honey",
                     "coconut water", "granola bars", "dried fruits", "nuts"],
        "office supplies": ["ergonomic chairs", "standing desks", "wireless keyboards", "noise-canceling headphones",
                           "desk lamps", "filing cabinets", "whiteboards", "monitor stands",
                           "cable organizers", "laptop stands", "mouse pads", "pen holders"],
        "pet supplies": ["dog food", "cat trees", "fish tanks", "rabbit cages", "pet beds",
                        "leashes", "pet toys", "grooming brushes", "litter boxes", "bird cages",
                        "hamster wheels", "pet carriers"],
        "fitness": ["resistance bands", "exercise bikes", "adjustable dumbbells", "pull-up bars",
                   "weight plates", "battle ropes", "medicine balls", "ab wheels", "yoga blocks",
                   "pilates rings", "suspension trainers"],
        "gaming": ["gaming mice", "RGB keyboards", "VR headsets", "gaming chairs", "controllers",
                  "gaming monitors", "mouse pads", "headset stands", "webcams", "capture cards",
                  "racing wheels", "gaming desks"],
        "travel": ["carry-on suitcases", "travel pillows", "backpacks", "power banks",
                  "luggage tags", "packing cubes", "travel adapters", "neck pillows",
                  "toiletry bags", "travel wallets", "luggage scales"],
        "outdoor equipment": ["camping tents", "hiking boots", "fishing gear", "sleeping bags",
                             "camping stoves", "backpacks", "water bottles", "coolers",
                             "binoculars", "compasses", "flashlights", "camping chairs"],
        "health": ["blood pressure monitors", "multivitamins", "first aid kits", "thermometers",
                  "pulse oximeters", "heating pads", "massage guns", "nebulizers",
                  "compression socks", "back braces", "knee braces"],
        "baby products": ["baby strollers", "diaper bags", "baby monitors", "car seats",
                         "high chairs", "baby carriers", "bottle warmers", "play mats",
                         "baby swings", "changing tables", "crib sheets"],
        "jewelry": ["gold necklaces", "silver rings", "diamond earrings", "bracelets",
                   "anklets", "pendants", "charm bracelets", "engagement rings", "cufflinks"]
    }

    # Attributes mapped to relevant categories
    # Format: attribute_value: [list of compatible categories]
    attribute_compatibility = {
        # Quality attributes - applicable to most categories
        "quality": {
            "high-quality": ["all"],
            "durable": ["electronics", "fashion", "home appliances", "sports", "automotive", 
                       "office supplies", "pet supplies", "fitness", "gaming", "travel", 
                       "outdoor equipment", "health", "baby products", "jewelry"],
            "long-lasting": ["electronics", "fashion", "home appliances", "sports", "automotive",
                           "office supplies", "pet supplies", "fitness", "gaming", "travel",
                           "outdoor equipment", "health", "baby products", "jewelry"],
            "reliable": ["electronics", "home appliances", "automotive", "office supplies",
                        "fitness", "gaming", "health", "baby products"],
            "professional-grade": ["electronics", "beauty", "sports", "office supplies", "fitness", "gaming"],
            "top-rated": ["all"],
            "well-reviewed": ["all"],
            "best-selling": ["all"],
            "award-winning": ["electronics", "beauty", "books", "toys", "gaming"],
            "premium quality": ["all"]
        },
        # Brand attributes - applicable to most categories
        "brand": {
            "branded": ["all"],
            "name-brand": ["all"],
            "designer": ["fashion", "beauty", "jewelry"],
            "well-known brand": ["all"],
            "trusted brand": ["all"],
            "popular brand": ["all"],
            "top brand": ["all"],
            "reputable brand": ["all"]
        },
        # Feature attributes - specific to certain categories
        "feature": {
            "wireless": ["electronics", "office supplies", "gaming"],
            "bluetooth": ["electronics", "office supplies", "gaming"],
            "smart": ["electronics", "home appliances", "office supplies", "health", "baby products"],
            "portable": ["electronics", "sports", "office supplies", "fitness", "gaming", 
                        "travel", "outdoor equipment", "health"],
            "compact": ["electronics", "home appliances", "sports", "office supplies", "fitness",
                       "gaming", "travel", "outdoor equipment", "health"],
            "lightweight": ["electronics", "fashion", "sports", "office supplies", "fitness",
                          "gaming", "travel", "outdoor equipment", "baby products"],
            "waterproof": ["electronics", "fashion", "sports", "automotive", "outdoor equipment", "health"],
            "rechargeable": ["electronics", "beauty", "office supplies", "gaming", "outdoor equipment", "health"],
            "adjustable": ["fashion", "sports", "office supplies", "fitness", "baby products"],
            "foldable": ["sports", "office supplies", "fitness", "travel", "outdoor equipment", "baby products"],
            "eco-friendly": ["all"],
            "energy-efficient": ["electronics", "home appliances", "office supplies"],
            "noise-canceling": ["electronics", "office supplies", "gaming"],
            "fast-charging": ["electronics", "automotive", "gaming"],
            "multi-functional": ["electronics", "home appliances", "beauty", "sports", "office supplies",
                               "pet supplies", "fitness", "gaming", "outdoor equipment", "health"]
        },
        # Style attributes
        "style": {
            "modern": ["all"],
            "classic": ["fashion", "home appliances", "office supplies", "jewelry"],
            "minimalist": ["fashion", "home appliances", "office supplies", "jewelry"],
            "elegant": ["fashion", "home appliances", "beauty", "office supplies", "jewelry"],
            "stylish": ["all"],
            "trendy": ["fashion", "beauty", "jewelry"],
            "vintage": ["fashion", "jewelry"],
            "contemporary": ["fashion", "home appliances", "office supplies", "jewelry"],
            "sleek": ["electronics", "fashion", "home appliances", "automotive", "office supplies", "gaming"],
            "professional-looking": ["fashion", "electronics", "office supplies", "gaming"]
        },
        # Color attributes
        "color": {
            "black": ["electronics", "fashion", "home appliances", "automotive", "office supplies",
                     "fitness", "gaming", "travel"],
            "white": ["electronics", "fashion", "home appliances", "office supplies", "gaming", "travel"],
            "blue": ["fashion", "automotive", "office supplies", "travel"],
            "red": ["fashion", "automotive", "office supplies", "travel"],
            "gray": ["electronics", "fashion", "automotive", "office supplies", "gaming", "travel"],
            "silver": ["electronics", "automotive", "office supplies", "gaming", "jewelry"],
            "gold": ["electronics", "jewelry"],
            "rose gold": ["electronics", "jewelry"],
            "neutral-colored": ["fashion", "home appliances", "office supplies", "travel"],
            "colorful": ["fashion", "toys", "office supplies", "travel"],
            "matte": ["electronics", "beauty", "fashion"],
            "glossy": ["electronics", "beauty", "fashion"]
        },
        # Size attributes
        "size": {
            "small": ["all"],
            "medium": ["all"],
            "large": ["all"],
            "compact": ["electronics", "home appliances", "sports", "office supplies", "fitness",
                       "gaming", "travel", "outdoor equipment", "health"],
            "portable": ["electronics", "sports", "office supplies", "fitness", "gaming",
                        "travel", "outdoor equipment", "health"],
            "travel-size": ["beauty", "groceries", "travel", "health"],
            "full-size": ["electronics", "home appliances", "beauty", "sports", "office supplies",
                         "fitness", "gaming"],
            "mini": ["electronics", "beauty", "toys", "travel"],
            "extra-large": ["fashion", "home appliances", "sports", "office supplies", "fitness", "travel"],
            "space-saving": ["home appliances", "office supplies", "fitness"]
        },
        # Use case attributes
        "use_case": {
            "for home": ["all"],
            "for office": ["electronics", "home appliances", "office supplies", "health"],
            "for travel": ["electronics", "fashion", "beauty", "sports", "travel", "outdoor equipment", "health"],
            "for gym": ["fashion", "sports", "fitness", "health"],
            "for outdoor use": ["electronics", "fashion", "sports", "automotive", "outdoor equipment"],
            "for beginners": ["electronics", "beauty", "sports", "books", "toys", "office supplies",
                            "fitness", "gaming", "outdoor equipment"],
            "for professionals": ["electronics", "beauty", "sports", "office supplies", "fitness", "gaming"],
            "for kids": ["electronics", "fashion", "toys", "books", "outdoor equipment", "health", "baby products"],
            "for seniors": ["electronics", "health"],
            "for everyday use": ["all"],
            "for gifting": ["all"],
            "for students": ["electronics", "fashion", "books", "office supplies"]
        },
        # Material attributes
        "material": {
            "leather": ["fashion", "automotive", "office supplies", "travel"],
            "stainless steel": ["home appliances", "jewelry", "outdoor equipment"],
            "plastic": ["home appliances", "toys", "office supplies", "pet supplies", "travel", "baby products"],
            "wood": ["home appliances", "office supplies", "toys"],
            "metal": ["home appliances", "office supplies", "fitness", "jewelry", "outdoor equipment"],
            "fabric": ["fashion", "office supplies", "pet supplies", "travel", "baby products"],
            "silicone": ["electronics", "beauty", "sports", "fitness", "baby products"],
            "rubber": ["sports", "automotive", "fitness", "outdoor equipment"],
            "glass": ["home appliances", "beauty", "groceries"],
            "ceramic": ["home appliances", "beauty", "groceries"],
            "bamboo": ["home appliances", "office supplies", "outdoor equipment"],
            "organic materials": ["beauty", "groceries", "pet supplies"]
        },
        # Condition attributes
        "condition": {
            "new": ["all"],
            "latest": ["all"],
            "newest": ["all"],
            "latest model": ["electronics", "home appliances", "automotive", "gaming"],
            "2024 edition": ["all"],
            "updated version": ["electronics", "home appliances", "gaming"]
        }
    }

    # More diverse query templates
    query_templates = [
        # Simple queries
        "Find me {product}",
        "I need {product}",
        "Show me {product}",
        "Looking for {product}",
        "Where can I get {product}?",
        "Do you have {product}?",
        "I want to buy {product}",
        "Searching for {product}",
        
        # Single attribute queries
        "I need {attr1} {product}",
        "Looking for {attr1} {product}",
        "Find me {attr1} {product}",
        "Show me {attr1} {product}",
        "Do you have {attr1} {product}?",
        "I want {attr1} {product}",
        "Recommend {attr1} {product}",
        "What's the best {attr1} {product}?",
        
        # Double attribute queries
        "I need {attr1} and {attr2} {product}",
        "Looking for {attr1} {attr2} {product}",
        "Find me {attr1}, {attr2} {product}",
        "Show me {attr1} {product} that is also {attr2}",
        "I want {attr1} {product} with {attr2} design",
        "Recommend {attr1} and {attr2} {product}",
        
        # Triple attribute queries
        "I need {attr1}, {attr2}, and {attr3} {product}",
        "Looking for {attr1} {attr2} {product} that is {attr3}",
        "Find me {attr1} {product} with {attr2} and {attr3} features",
        "Show me {attr1} and {attr2} {product} for {attr3}",
        
        # Use case specific queries
        "Best {product} {use_case}",
        "Recommend {product} {use_case}",
        "I need {product} {use_case}",
        "Find me {attr1} {product} {use_case}",
        "Looking for {attr1} and {attr2} {product} {use_case}",
        "What's the best {attr1} {product} {use_case}?",
        
        # Question-based queries
        "What are the best {product}?",
        "Which {product} should I buy?",
        "What's the most {attr1} {product}?",
        "Which {product} is {attr1}?",
        "What {product} do you recommend?",
        "Can you recommend {attr1} {product}?",
        "What's a good {attr1} {product} {use_case}?",
        
        # Preference queries
        "I prefer {attr1} {product}",
        "I'm looking for {product} that is {attr1}",
        "I want {product} with {attr1} and {attr2}",
        "I'd like {attr1} {product} {use_case}",
        
        # Specific requirement queries
        "Need {product} with {attr1} feature",
        "{product} that is {attr1} and {attr2}",
        "{attr1} {product} with good reviews",
        "Top-rated {attr1} {product}",
        "Bestselling {product} {use_case}",
        "Most popular {attr1} {product}",
        
        # Feature-focused queries
        "{product} with {feature} feature",
        "I need {product} that is {feature}",
        "Looking for {feature} {product}",
        "{feature} and {attr1} {product}",
        "Best {feature} {product} {use_case}",
    ]

    def is_attribute_compatible(attr_value, attr_type, category):
        """Check if an attribute is compatible with a product category"""
        if attr_type not in attribute_compatibility:
            return True
        
        if attr_value not in attribute_compatibility[attr_type]:
            return True
        
        compatible_categories = attribute_compatibility[attr_type][attr_value]
        
        if "all" in compatible_categories:
            return True
        
        return category in compatible_categories

    def get_compatible_attribute(attr_type, category, excluded_values):
        """Get a random attribute that is compatible with the category"""
        if attr_type == "quality":
            possible_attrs = list(attribute_compatibility["quality"].keys())
        elif attr_type == "brand":
            possible_attrs = list(attribute_compatibility["brand"].keys())
        elif attr_type == "feature":
            possible_attrs = list(attribute_compatibility["feature"].keys())
        elif attr_type == "style":
            possible_attrs = list(attribute_compatibility["style"].keys())
        elif attr_type == "color":
            possible_attrs = list(attribute_compatibility["color"].keys())
        elif attr_type == "size":
            possible_attrs = list(attribute_compatibility["size"].keys())
        elif attr_type == "material":
            possible_attrs = list(attribute_compatibility["material"].keys())
        elif attr_type == "condition":
            possible_attrs = list(attribute_compatibility["condition"].keys())
        else:
            return None
        
        # Filter compatible attributes
        compatible = [attr for attr in possible_attrs 
                     if is_attribute_compatible(attr, attr_type, category) 
                     and attr not in excluded_values]
        
        if not compatible:
            return None
        
        return random.choice(compatible)

    queries = {}
    attempts = 0
    max_attempts = n_queries * 20  # Increase max attempts since we're filtering
    
    while len(queries) < n_queries and attempts < max_attempts:
        attempts += 1
        
        # Randomly select category and product
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        # Randomly select template
        template = random.choice(query_templates)
        
        # Generate query based on template placeholders
        query = template
        
        # Track all variables used in this query
        query_variables = {
            "product_category": category,
            "product_name": product,
            "prompt_template": template
        }
        
        # Count attribute placeholders
        attr_count = query.count("{attr")
        
        # Replace product
        query = query.replace("{product}", product)
        
        # Replace attributes
        valid_query = True
        if attr_count > 0:
            selected_attrs = []
            for i in range(1, attr_count + 1):
                placeholder = f"{{attr{i}}}"
                if placeholder in query:
                    # Select random attribute type
                    attr_type = random.choice(["quality", "brand", "feature", "style", 
                                              "color", "size", "material", "condition"])
                    
                    # Get compatible attribute
                    attr_value = get_compatible_attribute(attr_type, category, selected_attrs)
                    
                    if attr_value is None:
                        valid_query = False
                        break
                    
                    selected_attrs.append(attr_value)
                    query_variables[f"attribute_{i}"] = attr_value
                    query_variables[f"attribute_{i}_type"] = attr_type
                    query = query.replace(placeholder, attr_value, 1)
        
        if not valid_query:
            continue
        
        # Replace use case
        if "{use_case}" in query:
            use_case_options = [uc for uc, cats in attribute_compatibility["use_case"].items()
                               if "all" in cats or category in cats]
            if not use_case_options:
                continue
            use_case = random.choice(use_case_options)
            query = query.replace("{use_case}", use_case)
            query_variables["use_case"] = use_case
        
        # Replace feature
        if "{feature}" in query:
            feature_options = [feat for feat, cats in attribute_compatibility["feature"].items()
                              if "all" in cats or category in cats]
            if not feature_options:
                continue
            feature = random.choice(feature_options)
            query = query.replace("{feature}", feature)
            query_variables["feature"] = feature
        
        # Add to dictionary if unique
        if query not in queries:
            queries[query] = query_variables

    if len(queries) < n_queries:
        print(f"Warning: Only generated {len(queries)} unique queries out of {n_queries} requested")

    # Save to JSON file
    with open(output_path, "w") as f:
        json.dump(queries, f, indent=2)
    
    print(f"Successfully generated {len(queries)} queries")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to generate a dataset of user queries in different categories')
    parser.add_argument('-o', '--output-path', type=str, required=True, help='Path to store the queries, in JSON format')
    parser.add_argument('-s', '--seed', type=int, default=1234, help='Seed used to sample categories and patterns')
    parser.add_argument('-n', '--size', type=int, default=2000, help='Number of queries to generate')

    args = parser.parse_args()

    main(args)
RareSimulator
RareSimulator is a Python package designed to simulate the genetic and phenotypic profiles of rare disease patients. This package can be used by researchers, students, and enthusiasts to generate synthetic data for studying the relationship between specific genetic mutations and the phenotypic manifestations associated with rare diseases.

Table of Contents
Features
Installation
Usage
Examples
Contributing
License
Features
Genotype Simulation: Generate synthetic genotypes with user-defined mutation rates for specific genes.
Phenotype Simulation: Map genotypic variations to observable characteristics (phenotypes) based on predefined disease models.
Disease Models: Supports custom models linking genes to symptoms, enabling flexible simulations for various rare diseases.
Synthetic Data: Generate data for testing and validating algorithms or understanding disease-gene relationships.
Installation
To install rare_disease_sim, you’ll need Python 3.6 or higher. Install via pip:

bash
Copy code
pip install git+https://github.com/xhwang2017/RareSimulator.git
Alternatively, you can clone the repository and install it locally:

bash
Copy code
git clone https://github.com/yourusername/rare_disease_sim.git
cd rare_disease_sim
pip install .
Usage
After installation, you can start using the package to simulate genotype and phenotype data for rare disease patients.

Example Usage
python
Copy code
from rare_disease_sim.disease import DiseaseSimulator

# Define a simple disease model where genes are linked to symptoms
disease_model = {
    "BRCA1": ["Tumorigenesis", "Breast Cancer"],
    "CFTR": ["Respiratory Issues", "Digestive Issues"],
    "PAH": ["Intellectual Disability"]
}

# Initialize the simulator with the disease model
simulator = DiseaseSimulator(disease_model)

# List of genes to include in the simulation
genes = ["BRCA1", "CFTR", "PAH"]

# Simulate a patient's genotype and phenotype data
patient_data = simulator.simulate_patient(genes, mutation_rate=0.05)

print("Genotype Data:")
print(patient_data["genotype"])

print("\nPhenotype Data:")
print(patient_data["phenotype"])
Examples
Here are a few more examples of what you can do with rare_disease_sim:

Custom Disease Models: Create your own disease model linking genes to specific symptoms.
Adjust Mutation Rates: Experiment with different mutation rates to observe how they affect phenotype simulations.
Batch Simulations: Generate multiple synthetic patients to create datasets for machine learning models or statistical analysis.
Data Files
If your package includes real or synthetic disease data, place these files in the data/ directory and update the path in your code to load these files as needed. You can define disease characteristics in a CSV file, such as data/disease_data.csv:

csv
Copy code
Gene,Disease,Symptom
BRCA1,Breast Cancer,Tumorigenesis
CFTR,Cystic Fibrosis,Respiratory Issues
PAH,Phenylketonuria,Intellectual Disability
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.
Please make sure to add tests for any new features and follow the project’s code style.

License
This project is licensed under the MIT License. See the LICENSE file for details.

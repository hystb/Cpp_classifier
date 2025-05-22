# 🧠 Cpp_classifier: Classifying C++ Functions with CodeBERT

This project demonstrates how to classify C++ programs using a fine-tuned CodeBERT model on a subset of the CodeNet dataset.

## 📂 Project Structure

- `data/`: Contains the `codenet_c++_100_jsonl` dataset.
- `notebooks/`: Jupyter notebooks for model training.
- `src/`: Source code for data processing.
- `label_map.json`: Mapping of problem IDs to integer labels.

## 🧰 Dependencies

All required Python packages are listed in `requirements.txt` exept pytorch got to [pytorch](https://pytorch.org/get-started/locally/) to install the version corresponding to your hardware

## 📊 Dataset

The dataset is a subset of the `CodeNet dataset` focusing on 100 C++ problems. Each entry is a JSON object:

```json
{"func": "<C++ function code>", "label": <integer label>}
```

The `label` corresponds to a problem ID, mapped using `label_map.json`.

## 🧪 Data Preprocessing

We define a custom `CodeDataset` class to handle data loading and preprocessing. Each function is tokenized using `RobertaTokenizer` from the `microsoft/codebert-base` model.

## 🏗️ Model Architecture

We utilize `RobertaForSequenceClassification` from Hugging Face's Transformers library, initialized with the `microsoft/codebert-base` weights. This model is fine-tuned for multi-class classification tasks.

## ⚙️ Training Configuration

Training is managed using Hugging Face's `Trainer` API.

## 📈 Evaluation Metrics

We use accuracy as the primary evaluation metric, computed during training and validation phases.

## 🧪 Testing

After training, the model is evaluated on a separate test set. We utilize `classification_report` from scikit-learn to obtain precision, recall, and F1-score for each class.

## 📉 Confusion Matrix

A confusion matrix is generated to visualize the model's performance across different classes, helping identify areas where the model may be misclassifying functions.

## 🔮 Next Steps

- 📦 Extend the classifier to support all 1000 C++ problem classes from the CodeNet dataset.
- 🧠 Switch from raw source code to control flow graph (CFG) and SSA-based representations extracted from binaries.  
  This shift in feature engineering will require adopting a Graph Neural Network (GNN) architecture instead of CodeBERT.


## 🚀 Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/hystb/Cpp_classifier.git
   cd Cpp_classifier
   ```

2. Install dependencies:
expample for my config with cuda 12.6 and pytorch 2.7.0
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
   ```
   ```bash
   pip install -r requirements.txt
   ```

## 🙌 Acknowledgments

Thanks to `IBM's Project CodeNet` for providing the dataset and to the Hugging Face team for their excellent Transformers library.

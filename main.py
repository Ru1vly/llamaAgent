from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

def train_model():
    # 1. Modeli ve tokenizer'ı yükle
    model_name = "meta/llama-2-7b"  # Örneğin 7B parametreli model
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 2. Veri kümesini yükle (Hugging Face datasets veya yerel veri)
    dataset = load_dataset("path_to_your_dataset")  # Burada kendi veri kümenizi kullanın
    
    # 3. Tokenizasyon
    def tokenize_function(examples):
        return tokenizer(examples['text'], padding='max_length', truncation=True)
    
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # 4. Eğitim parametrelerini ayarla
    training_args = TrainingArguments(
        output_dir="./results",          # Modelin kaydedileceği dizin
        evaluation_strategy="epoch",     # Her epoch'ta modelin değerlendirilmesi
        learning_rate=2e-5,             # Öğrenme oranı
        per_device_train_batch_size=4,  # Eğitim sırasında her cihazda kullanılacak batch boyutu
        num_train_epochs=3,             # Eğitim epok sayısı
        weight_decay=0.01,              # Ağırlık düşüşü
    )

    # 5. Trainer ile eğitim işlemi başlat
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],   # Eğitim verisi
        eval_dataset=tokenized_datasets["test"],     # Değerlendirme verisi
    )

    # 6. Eğitim başlat
    trainer.train()

    # 7. Modeli kaydet
    trainer.save_model("./fine_tuned_llama")  # Eğitim bitiminde model kaydedilir
    tokenizer.save_pretrained("./fine_tuned_llama")

if __name__ == "__main__":
    train_model()

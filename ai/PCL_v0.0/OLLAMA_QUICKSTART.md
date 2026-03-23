# Quick Start: PCL Model in Ollama

## 🚀 One-Command Export (Recommended)

```bash
# Install dependencies first
pip install torch transformers --break-system-packages

# Then run the complete pipeline
python ollama_export_complete.py --quick
```

That's it! This will:
1. ✅ Train a small PCL model
2. ✅ Export to HuggingFace format
3. ✅ Convert to GGUF
4. ✅ Import to Ollama
5. ✅ Test the model

**Time**: ~5-10 minutes for quick mode

---

## 📋 Step-by-Step (If you prefer manual control)

### Step 1: Train Model
```bash
python train_pcl_for_ollama.py --epochs 10
```

**Output**: `pcl_model.pt` and `pcl_model_config.json`

---

### Step 2: Export to HuggingFace
```bash
python export_to_huggingface.py
```

**Output**: `pcl_model_hf/` directory

---

### Step 3: Convert to GGUF

First, get llama.cpp:
```bash
git clone https://github.com/ggerganov/llama.cpp.git
```

Then convert:
```bash
python llama.cpp/convert-hf-to-gguf.py pcl_model_hf \
  --outfile pcl_model.gguf \
  --outtype f16
```

**Output**: `pcl_model.gguf`

---

### Step 4: Create Modelfile

```bash
cat > Modelfile << 'EOF'
FROM ./pcl_model.gguf

PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9

SYSTEM """You are a helpful AI assistant with Phase Control Layers."""
EOF
```

---

### Step 5: Import to Ollama

```bash
ollama create pcl-minigpt -f Modelfile
```

---

### Step 6: Test It!

```bash
# Interactive chat
ollama run pcl-minigpt

# Single prompt
ollama run pcl-minigpt "Hello! Tell me about phase control."
```

---

## ⚡ Quick Mode vs Full Mode

### Quick Mode (for testing)
```bash
python ollama_export_complete.py --quick
```
- Vocab: 1,000 tokens
- Model: 4 layers, 256 dim
- Training: 5 epochs
- Size: ~10 MB
- Time: ~5 minutes

### Full Mode (for real use)
```bash
python ollama_export_complete.py
```
- Vocab: 32,000 tokens
- Model: 8 layers, 512 dim
- Training: 20 epochs
- Size: ~500 MB
- Time: ~30-60 minutes

---

## 🔧 Troubleshooting

### "ollama not found"
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Or on macOS
brew install ollama
```

### "transformers not installed"
```bash
pip install transformers --break-system-packages
```

### "pcl_corrected.py not found"
Make sure you're in the same directory as `pcl_corrected.py`

### "Conversion failed"
```bash
# Make sure llama.cpp is cloned
git clone https://github.com/ggerganov/llama.cpp.git

# Check Python path
which python
python --version
```

### Model doesn't respond well
This is a tiny model trained on synthetic data. For better results:
1. Train longer (`--epochs 50`)
2. Use real text data
3. Increase model size
4. Fine-tune on your specific task

---

## 📊 What You Get

After successful import:

```bash
$ ollama list
NAME                ID              SIZE
pcl-minigpt        abc123def       10 MB

$ ollama run pcl-minigpt
>>> Hello!
Hello! I'm an AI assistant with Phase Control Layers. How can I help you?

>>> What are phase control layers?
Phase Control Layers (PCL) are a neural network technique that...
```

---

## 🎯 Next Steps

### Test the Model
```bash
# Chat interactively
ollama run pcl-minigpt

# Run specific prompts
ollama run pcl-minigpt "Explain PCL in simple terms"

# Check model info
ollama show pcl-minigpt
```

### Fine-tune on Real Data
1. Collect your dataset
2. Modify `train_pcl_for_ollama.py` to use it
3. Train longer
4. Export again

### Scale Up
```bash
# Larger model
python train_pcl_for_ollama.py \
  --dim 1024 \
  --layers 12 \
  --epochs 50
```

### Share Your Model
```bash
# Save to file
ollama save pcl-minigpt

# Push to Ollama registry (if you have access)
ollama push your-username/pcl-minigpt
```

---

## 💡 Tips

1. **Start with --quick** to test the pipeline
2. **Use GPU** if available (much faster training)
3. **Monitor training** - watch the loss decrease
4. **Test generation** before exporting (in training script)
5. **Keep checkpoints** - you can export different versions

---

## 🐛 Known Issues

### PCL Features in GGUF
- ⚠️ GGUF doesn't natively support custom layers
- 🔧 PCL layers are "baked in" during export
- ⚡ Dynamic gating is preserved in the weights
- ✅ Inference still works, just not as flexible

### Quantization
- F16 preserves most accuracy
- Q4/Q8 may affect PCL's norm preservation
- Test different quantization levels

### Model Size
- Small models (<100M params) won't be very capable
- PCL shines with 350M+ parameters
- This is a proof-of-concept, not production-ready

---

## 📞 Support

If you hit issues:
1. Check the detailed guide: `ollama_export_guide.md`
2. Verify dependencies are installed
3. Try --quick mode first
4. Check Ollama is running: `ollama serve`

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Model trained successfully
- [ ] Exported to HuggingFace
- [ ] Converted to GGUF
- [ ] Imported to Ollama
- [ ] Model responds to prompts

Once all checked, you have a working PCL model in Ollama! 🎉

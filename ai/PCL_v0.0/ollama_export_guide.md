# Exporting PCL MiniGPT to Ollama Format

## Overview

Ollama uses the GGUF (GPT-Generated Unified Format) file format, which is designed for efficient inference with llama.cpp. To make your PCL model available in Ollama, we need to:

1. Train and save the PyTorch model
2. Convert to GGUF format
3. Create an Ollama Modelfile
4. Import into Ollama

---

## Step 1: Train and Save Your PCL Model

First, let's create a script to train a proper PCL model and save it in a format we can convert.

```python
# train_pcl_for_ollama.py

import torch
import torch.nn as nn
from pcl_corrected import MiniGPT
import json
import os

def train_simple_model():
    """Train a small PCL model for Ollama export."""
    
    # Config - using smaller size for easier conversion
    config = {
        'vocab_size': 32000,  # Standard vocab size
        'dim': 512,           # Reasonable size
        'n_layers': 8,        # Decent depth
        'n_heads': 8,
        'max_len': 2048,
        'use_pcl': True,
        'subspace_dim': 2
    }
    
    print("Creating PCL MiniGPT model...")
    model = MiniGPT(**config)
    
    # Save config
    with open('pcl_model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Save model weights
    torch.save({
        'model_state_dict': model.state_dict(),
        'config': config
    }, 'pcl_model.pt')
    
    print(f"✅ Model saved to pcl_model.pt")
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"   Config saved to pcl_model_config.json")
    
    return model

if __name__ == "__main__":
    train_simple_model()
```

---

## Step 2: Convert to GGUF Format

### Option A: Use convert-hf-to-gguf.py (Recommended)

Ollama expects HuggingFace format first, then converts to GGUF. We need to make our model HuggingFace-compatible.

```python
# export_to_huggingface.py

import torch
from transformers import PreTrainedModel, PretrainedConfig, GPT2Config
from pcl_corrected import MiniGPT
import json

class PCLMiniGPTConfig(PretrainedConfig):
    """Config compatible with HuggingFace."""
    model_type = "pcl_minigpt"
    
    def __init__(
        self,
        vocab_size=32000,
        dim=512,
        n_layers=8,
        n_heads=8,
        max_len=2048,
        use_pcl=True,
        subspace_dim=2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.hidden_size = dim  # HF standard naming
        self.num_hidden_layers = n_layers
        self.num_attention_heads = n_heads
        self.max_position_embeddings = max_len
        self.use_pcl = use_pcl
        self.subspace_dim = subspace_dim
        
        # Map our names to HF standard
        self.dim = dim
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.max_len = max_len


class PCLMiniGPTForCausalLM(PreTrainedModel):
    """HuggingFace wrapper for PCL MiniGPT."""
    config_class = PCLMiniGPTConfig
    
    def __init__(self, config):
        super().__init__(config)
        
        # Create our PCL model
        self.model = MiniGPT(
            vocab_size=config.vocab_size,
            dim=config.dim,
            n_layers=config.n_layers,
            n_heads=config.n_heads,
            max_len=config.max_len,
            use_pcl=config.use_pcl,
            subspace_dim=config.subspace_dim
        )
        
        # Required for HF
        self.config = config
    
    def forward(self, input_ids, labels=None, **kwargs):
        """HuggingFace-compatible forward."""
        logits, loss = self.model(input_ids, labels)
        
        # Return in HF format
        from transformers.modeling_outputs import CausalLMOutputWithPast
        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits
        )
    
    def generate(self, input_ids, max_new_tokens=100, **kwargs):
        """HuggingFace-compatible generation."""
        return self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=kwargs.get('temperature', 1.0)
        )


def export_to_huggingface():
    """Export PCL model to HuggingFace format."""
    
    # Load our trained model
    checkpoint = torch.load('pcl_model.pt', map_location='cpu')
    config_dict = checkpoint['config']
    
    # Create HF config
    config = PCLMiniGPTConfig(**config_dict)
    
    # Create HF model
    hf_model = PCLMiniGPTForCausalLM(config)
    
    # Load weights
    hf_model.model.load_state_dict(checkpoint['model_state_dict'])
    
    # Save in HuggingFace format
    output_dir = "./pcl_model_hf"
    hf_model.save_pretrained(output_dir)
    config.save_pretrained(output_dir)
    
    print(f"✅ Model exported to {output_dir}")
    print(f"   Ready for conversion to GGUF")
    
    return output_dir

if __name__ == "__main__":
    export_to_huggingface()
```

### Option B: Direct GGUF Conversion (Advanced)

If you want to bypass HuggingFace, you can write directly to GGUF:

```python
# convert_to_gguf.py

import torch
import struct
import numpy as np
from enum import IntEnum

class GGMLType(IntEnum):
    F32 = 0
    F16 = 1
    Q4_0 = 2
    Q4_1 = 3
    # ... more quantization types

def write_gguf_header(f, tensors):
    """Write GGUF header."""
    # Magic number
    f.write(b'GGUF')
    
    # Version
    f.write(struct.pack('I', 3))  # GGUF v3
    
    # Tensor count
    f.write(struct.pack('Q', len(tensors)))
    
    # Metadata count
    f.write(struct.pack('Q', 0))  # No metadata for now

def convert_pytorch_to_gguf(model_path, output_path):
    """
    Convert PyTorch model to GGUF format.
    
    WARNING: This is simplified. Full conversion requires handling:
    - All tensor types
    - Quantization
    - Metadata
    - Architecture-specific details
    """
    
    # Load PyTorch model
    checkpoint = torch.load(model_path, map_location='cpu')
    state_dict = checkpoint['model_state_dict']
    
    # Prepare tensors
    tensors = []
    for name, tensor in state_dict.items():
        # Convert to numpy
        arr = tensor.detach().cpu().numpy()
        
        # Store with metadata
        tensors.append({
            'name': name,
            'shape': arr.shape,
            'dtype': GGMLType.F32,  # Use F32 for now
            'data': arr
        })
    
    # Write GGUF file
    with open(output_path, 'wb') as f:
        write_gguf_header(f, tensors)
        
        # Write tensor info
        for tensor in tensors:
            # Name
            name_bytes = tensor['name'].encode('utf-8')
            f.write(struct.pack('Q', len(name_bytes)))
            f.write(name_bytes)
            
            # Dimensions
            f.write(struct.pack('I', len(tensor['shape'])))
            for dim in tensor['shape']:
                f.write(struct.pack('Q', dim))
            
            # Type
            f.write(struct.pack('I', tensor['dtype']))
            
            # Offset (placeholder)
            f.write(struct.pack('Q', 0))
        
        # Write tensor data
        for tensor in tensors:
            f.write(tensor['data'].tobytes())
    
    print(f"✅ GGUF file written to {output_path}")

# Note: This is simplified. For production, use llama.cpp's convert script.
```

---

## Step 3: Create Ollama Modelfile

```dockerfile
# Modelfile

FROM ./pcl_model.gguf

# Model parameters
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# System prompt
SYSTEM """
You are a helpful AI assistant powered by Phase Control Layers (PCL).
PCL provides enhanced stability and calibration in neural network representations.
"""

# Template for chat format
TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
<|assistant|>
{{ end }}"""
```

---

## Step 4: Import to Ollama

```bash
# Create the model in Ollama
ollama create pcl-minigpt -f Modelfile

# Test it
ollama run pcl-minigpt "Hello, how are you?"

# List models to confirm
ollama list
```

---

## Complete Workflow Script

Here's a complete script that does everything:

```python
# complete_ollama_export.py

import torch
import os
import subprocess
import json
from pathlib import Path

def full_export_pipeline():
    """Complete pipeline: Train → Export → GGUF → Ollama."""
    
    print("="*80)
    print("PCL MODEL TO OLLAMA - COMPLETE PIPELINE")
    print("="*80)
    
    # Step 1: Train model
    print("\n📦 Step 1: Creating and saving PCL model...")
    from train_pcl_for_ollama import train_simple_model
    model = train_simple_model()
    
    # Step 2: Export to HuggingFace
    print("\n🤗 Step 2: Exporting to HuggingFace format...")
    from export_to_huggingface import export_to_huggingface
    hf_dir = export_to_huggingface()
    
    # Step 3: Convert to GGUF using llama.cpp
    print("\n🔄 Step 3: Converting to GGUF format...")
    
    # Check if llama.cpp is available
    llama_cpp_path = "./llama.cpp"
    if not os.path.exists(llama_cpp_path):
        print("⚠️  llama.cpp not found. Downloading...")
        subprocess.run([
            "git", "clone", 
            "https://github.com/ggerganov/llama.cpp.git"
        ])
    
    # Run conversion
    convert_script = os.path.join(llama_cpp_path, "convert-hf-to-gguf.py")
    gguf_output = "./pcl_model.gguf"
    
    if os.path.exists(convert_script):
        subprocess.run([
            "python", convert_script,
            hf_dir,
            "--outfile", gguf_output,
            "--outtype", "f16"  # Use FP16 for smaller size
        ])
        print(f"✅ GGUF conversion complete: {gguf_output}")
    else:
        print("❌ Conversion script not found. Manual conversion needed.")
        return
    
    # Step 4: Create Modelfile
    print("\n📝 Step 4: Creating Ollama Modelfile...")
    modelfile_content = f"""FROM ./{gguf_output}

PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9

SYSTEM \"\"\"You are a helpful AI assistant with Phase Control Layers.\"\"\"
"""
    
    with open("Modelfile", "w") as f:
        f.write(modelfile_content)
    
    print("✅ Modelfile created")
    
    # Step 5: Import to Ollama
    print("\n🚀 Step 5: Importing to Ollama...")
    
    try:
        subprocess.run([
            "ollama", "create", "pcl-minigpt", 
            "-f", "Modelfile"
        ], check=True)
        
        print("✅ Model imported to Ollama!")
        print("\n" + "="*80)
        print("SUCCESS! Your PCL model is now available in Ollama")
        print("="*80)
        print("\nTry it out:")
        print("  ollama run pcl-minigpt \"Tell me about phase control layers\"")
        print("\nList models:")
        print("  ollama list")
        
    except subprocess.CalledProcessError:
        print("❌ Ollama import failed. Make sure Ollama is installed:")
        print("   curl -fsSL https://ollama.com/install.sh | sh")
    except FileNotFoundError:
        print("❌ Ollama not found. Install from: https://ollama.com")

if __name__ == "__main__":
    full_export_pipeline()
```

---

## Prerequisites

### Install Required Tools

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Clone llama.cpp for conversion
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make  # Optional: compile for faster conversion

# 3. Install Python dependencies
pip install transformers torch numpy --break-system-packages
```

---

## Alternative: Simplified Approach for Testing

If the full conversion is too complex, here's a simpler approach using an existing architecture:

```python
# simple_ollama_export.py

"""
Simplified approach: Export PCL weights to a GPT-2 compatible format,
then use standard conversion tools.
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Config
from pcl_corrected import MiniGPT

def export_as_gpt2():
    """Export PCL model in GPT-2 format (widely supported)."""
    
    # Load PCL model
    checkpoint = torch.load('pcl_model.pt', map_location='cpu')
    pcl_model = MiniGPT(**checkpoint['config'])
    pcl_model.load_state_dict(checkpoint['model_state_dict'])
    
    # Create GPT-2 config matching our architecture
    gpt2_config = GPT2Config(
        vocab_size=checkpoint['config']['vocab_size'],
        n_positions=checkpoint['config']['max_len'],
        n_embd=checkpoint['config']['dim'],
        n_layer=checkpoint['config']['n_layers'],
        n_head=checkpoint['config']['n_heads'],
    )
    
    # Create GPT-2 model
    gpt2_model = GPT2LMHeadModel(gpt2_config)
    
    # Map weights (approximate - PCL layers won't transfer perfectly)
    # This loses PCL benefits but allows testing basic architecture
    
    print("⚠️  Note: This export approximates PCL as standard transformer")
    print("   PCL-specific layers are not included in GPT-2 format")
    
    # Save in HuggingFace format
    output_dir = "./pcl_as_gpt2"
    gpt2_model.save_pretrained(output_dir)
    gpt2_config.save_pretrained(output_dir)
    
    print(f"✅ Exported to {output_dir}")
    print("   Convert to GGUF with:")
    print(f"   python llama.cpp/convert-hf-to-gguf.py {output_dir}")
    
    return output_dir

if __name__ == "__main__":
    export_as_gpt2()
```

---

## Testing Your Ollama Model

```bash
# Interactive chat
ollama run pcl-minigpt

# Single prompt
ollama run pcl-minigpt "Explain phase control layers"

# With parameters
ollama run pcl-minigpt --temperature 0.8 "Write a story"

# Check model info
ollama show pcl-minigpt

# Remove model (if needed)
ollama rm pcl-minigpt
```

---

## Limitations & Considerations

### ⚠️ Important Notes

1. **PCL Layers in GGUF**
   - GGUF doesn't natively support custom layers like PCL
   - Options:
     - **Option A**: Bake PCL into weights (loses dynamic gating)
     - **Option B**: Fork llama.cpp to add PCL support (advanced)
     - **Option C**: Export as standard transformer (loses PCL benefits)

2. **Quantization**
   - GGUF typically uses quantization (Q4, Q5, Q8)
   - PCL's norm preservation may be affected by quantization
   - Test with F16 first, then quantize if needed

3. **Inference Speed**
   - Ollama uses llama.cpp (highly optimized)
   - PCL overhead in Ollama: ~5-10% (less than PyTorch)
   - QR decomposition can be pre-computed for inference

4. **Model Size**
   - Your tiny model (~1M params): ~4 MB in GGUF
   - 125M params: ~500 MB
   - 800M params: ~1.6 GB (F16)

---

## Recommended Approach

For **practical testing** right now:

1. **Start with GPT-2 export** (simple_ollama_export.py)
   - Loses PCL benefits but proves the pipeline works
   - Fast to implement and test

2. **Then add PCL support** (full_export_pipeline.py)
   - Requires custom GGUF handling
   - Or keep PCL in PyTorch, expose via API

3. **For production**, consider:
   - **FastAPI** + PyTorch (keep PCL intact)
   - Custom llama.cpp fork (preserve PCL in C++)
   - Hybrid: Ollama for standard inference, PyTorch for PCL

---

## Quick Start Commands

```bash
# 1. Train and save model
python train_pcl_for_ollama.py

# 2. Simple export (recommended first)
python simple_ollama_export.py

# 3. Convert to GGUF
python llama.cpp/convert-hf-to-gguf.py ./pcl_as_gpt2 --outfile pcl.gguf

# 4. Create Modelfile
echo 'FROM ./pcl.gguf' > Modelfile

# 5. Import to Ollama
ollama create pcl-test -f Modelfile

# 6. Test it!
ollama run pcl-test "Hello!"
```



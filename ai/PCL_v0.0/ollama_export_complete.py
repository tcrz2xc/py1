#!/usr/bin/env python3
"""
One-Command Ollama Export
==========================

This script handles the entire pipeline:
1. Train PCL model
2. Export to HuggingFace
3. Convert to GGUF
4. Create Modelfile
5. Import to Ollama

Usage:
    python ollama_export_complete.py

Or with custom settings:
    python ollama_export_complete.py --quick  # Fast training
    python ollama_export_complete.py --full   # Full training
"""

import torch
import json
import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    issues = []
    
    # Check PyTorch
    try:
        import torch
        print(f"   ✅ PyTorch {torch.__version__}")
    except ImportError:
        issues.append("PyTorch not installed")
    
    # Check transformers
    try:
        import transformers
        print(f"   ✅ Transformers {transformers.__version__}")
    except ImportError:
        issues.append("transformers not installed: pip install transformers")
    
    # Check pcl_corrected
    if not os.path.exists('pcl_corrected.py'):
        issues.append("pcl_corrected.py not found in current directory")
    else:
        print(f"   ✅ pcl_corrected.py found")
    
    # Check Ollama
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Ollama installed")
        else:
            issues.append("Ollama not working properly")
    except FileNotFoundError:
        issues.append("Ollama not installed: https://ollama.com")
    
    # Check llama.cpp (optional)
    if os.path.exists('llama.cpp'):
        print(f"   ✅ llama.cpp found")
    else:
        print(f"   ⚠️  llama.cpp not found (will download if needed)")
    
    if issues:
        print(f"\n❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    print(f"✅ All dependencies OK!\n")
    return True


def train_model(quick=False):
    """Train the PCL model."""
    print("="*80)
    print("STEP 1: TRAINING PCL MODEL")
    print("="*80)
    
    from train_pcl_for_ollama import train_pcl_model
    
    if quick:
        print("\n⚡ Quick training mode (for testing)")
        model, config = train_pcl_model(
            vocab_size=1000,    # Small vocab
            dim=256,            # Small model
            n_layers=4,
            n_heads=4,
            n_epochs=5,
            batch_size=16
        )
    else:
        print("\n🏋️  Full training mode")
        model, config = train_pcl_model(
            vocab_size=32000,
            dim=512,
            n_layers=8,
            n_heads=8,
            n_epochs=20,
            batch_size=16
        )
    
    print("\n✅ Training complete!")
    return model, config


def export_hf():
    """Export to HuggingFace format."""
    print("\n" + "="*80)
    print("STEP 2: EXPORTING TO HUGGINGFACE FORMAT")
    print("="*80 + "\n")
    
    from export_to_huggingface import export_to_huggingface
    
    output_dir = export_to_huggingface(
        checkpoint_path='pcl_model.pt',
        output_dir='./pcl_model_hf'
    )
    
    print("\n✅ HuggingFace export complete!")
    return output_dir


def setup_llama_cpp():
    """Download and setup llama.cpp if needed."""
    print("\n" + "="*80)
    print("STEP 3: SETTING UP LLAMA.CPP")
    print("="*80 + "\n")
    
    llama_dir = Path('llama.cpp')
    
    if llama_dir.exists():
        print("✅ llama.cpp already exists")
        return str(llama_dir)
    
    print("📥 Downloading llama.cpp...")
    try:
        subprocess.run([
            'git', 'clone', 
            'https://github.com/ggerganov/llama.cpp.git'
        ], check=True)
        print("✅ llama.cpp downloaded!")
    except subprocess.CalledProcessError:
        print("❌ Failed to download llama.cpp")
        print("   Please clone manually:")
        print("   git clone https://github.com/ggerganov/llama.cpp.git")
        sys.exit(1)
    
    return str(llama_dir)


def convert_to_gguf(hf_dir, llama_dir):
    """Convert HuggingFace model to GGUF."""
    print("\n" + "="*80)
    print("STEP 4: CONVERTING TO GGUF FORMAT")
    print("="*80 + "\n")
    
    convert_script = Path(llama_dir) / 'convert-hf-to-gguf.py'
    
    if not convert_script.exists():
        print(f"❌ Conversion script not found at {convert_script}")
        print("   Please ensure llama.cpp is properly cloned")
        sys.exit(1)
    
    output_gguf = 'pcl_model.gguf'
    
    print(f"🔄 Converting {hf_dir} to GGUF...")
    print(f"   This may take a few minutes...")
    
    try:
        subprocess.run([
            sys.executable,
            str(convert_script),
            hf_dir,
            '--outfile', output_gguf,
            '--outtype', 'f16'
        ], check=True)
        
        print(f"\n✅ GGUF conversion complete!")
        print(f"   Output: {output_gguf}")
        
        # Check file size
        file_size = os.path.getsize(output_gguf) / (1024 * 1024)
        print(f"   Size: {file_size:.1f} MB")
        
        return output_gguf
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GGUF conversion failed: {e}")
        sys.exit(1)


def create_modelfile(gguf_path):
    """Create Ollama Modelfile."""
    print("\n" + "="*80)
    print("STEP 5: CREATING OLLAMA MODELFILE")
    print("="*80 + "\n")
    
    modelfile_content = f"""# PCL MiniGPT Model
FROM ./{gguf_path}

# Model parameters
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER stop "<|end|>"

# System message
SYSTEM \"\"\"You are a helpful AI assistant powered by Phase Control Layers (PCL).

PCL provides:
- Enhanced stability in representations
- Better calibration of predictions
- Reduced feature interference

How can I help you today?\"\"\"

# Chat template
TEMPLATE \"\"\"{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
<|assistant|>
{{ end }}\"\"\"
"""
    
    modelfile_path = 'Modelfile'
    with open(modelfile_path, 'w') as f:
        f.write(modelfile_content)
    
    print(f"✅ Modelfile created: {modelfile_path}")
    print(f"\nModelfile contents:")
    print("-" * 40)
    print(modelfile_content)
    print("-" * 40)
    
    return modelfile_path


def import_to_ollama(modelfile, model_name='pcl-minigpt'):
    """Import model into Ollama."""
    print("\n" + "="*80)
    print("STEP 6: IMPORTING TO OLLAMA")
    print("="*80 + "\n")
    
    print(f"📥 Importing model as '{model_name}'...")
    
    try:
        subprocess.run([
            'ollama', 'create', model_name,
            '-f', modelfile
        ], check=True)
        
        print(f"\n✅ Model successfully imported to Ollama!")
        return model_name
        
    except subprocess.CalledProcessError:
        print(f"❌ Failed to import to Ollama")
        print(f"   Make sure Ollama is running:")
        print(f"   ollama serve")
        sys.exit(1)


def test_model(model_name):
    """Test the imported model."""
    print("\n" + "="*80)
    print("STEP 7: TESTING MODEL")
    print("="*80 + "\n")
    
    print(f"🧪 Testing model '{model_name}'...")
    
    test_prompts = [
        "Hello! What are phase control layers?",
        "Count from 1 to 10",
        "What can you do?"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Prompt: {prompt}")
        print(f"Response: ", end='', flush=True)
        
        try:
            result = subprocess.run([
                'ollama', 'run', model_name,
                prompt
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print(f"[Error: {result.stderr.strip()}]")
                
        except subprocess.TimeoutExpired:
            print("[Timeout]")
        except Exception as e:
            print(f"[Error: {e}]")
    
    print("\n✅ Testing complete!")


def main():
    parser = argparse.ArgumentParser(
        description='Complete PCL to Ollama export pipeline'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick training mode (small model, fast)'
    )
    parser.add_argument(
        '--skip-train',
        action='store_true',
        help='Skip training (use existing pcl_model.pt)'
    )
    parser.add_argument(
        '--skip-test',
        action='store_true',
        help='Skip testing after import'
    )
    parser.add_argument(
        '--model-name',
        type=str,
        default='pcl-minigpt',
        help='Name for model in Ollama'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("PCL MODEL TO OLLAMA - COMPLETE PIPELINE")
    print("="*80 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    try:
        # Step 1: Train (unless skipped)
        if not args.skip_train:
            train_model(quick=args.quick)
        else:
            print("⏭️  Skipping training (using existing model)")
            if not os.path.exists('pcl_model.pt'):
                print("❌ No existing model found!")
                sys.exit(1)
        
        # Step 2: Export to HuggingFace
        hf_dir = export_hf()
        
        # Step 3: Setup llama.cpp
        llama_dir = setup_llama_cpp()
        
        # Step 4: Convert to GGUF
        gguf_path = convert_to_gguf(hf_dir, llama_dir)
        
        # Step 5: Create Modelfile
        modelfile = create_modelfile(gguf_path)
        
        # Step 6: Import to Ollama
        model_name = import_to_ollama(modelfile, args.model_name)
        
        # Step 7: Test (unless skipped)
        if not args.skip_test:
            test_model(model_name)
        else:
            print("\n⏭️  Skipping tests")
        
        # Success!
        print("\n" + "="*80)
        print("🎉 SUCCESS! YOUR PCL MODEL IS NOW IN OLLAMA!")
        print("="*80)
        
        print(f"\n📋 Summary:")
        print(f"   Model name: {model_name}")
        print(f"   GGUF file:  {gguf_path}")
        print(f"   Model size: {os.path.getsize(gguf_path) / (1024*1024):.1f} MB")
        
        print(f"\n🚀 Usage:")
        print(f"   ollama run {model_name}")
        print(f"   ollama run {model_name} 'Your prompt here'")
        
        print(f"\n📊 Other commands:")
        print(f"   ollama list                  # List all models")
        print(f"   ollama show {model_name}     # Show model info")
        print(f"   ollama rm {model_name}       # Remove model")
        
        print(f"\n✅ All done!")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

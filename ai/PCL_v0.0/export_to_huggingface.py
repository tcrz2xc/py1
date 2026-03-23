"""
Export PCL Model to HuggingFace Format
=======================================

This script converts the trained PCL model to HuggingFace format,
which can then be converted to GGUF for Ollama.
"""

import torch
import json
import os
import sys

try:
    from transformers import PreTrainedModel, PretrainedConfig
    from transformers.modeling_outputs import CausalLMOutputWithPast
except ImportError:
    print("❌ Error: transformers not installed")
    print("   Install with: pip install transformers --break-system-packages")
    sys.exit(1)

try:
    from pcl_corrected import MiniGPT
except ImportError:
    print("❌ Error: pcl_corrected.py not found")
    sys.exit(1)


class PCLConfig(PretrainedConfig):
    """
    HuggingFace-compatible configuration for PCL MiniGPT.
    
    This allows the model to be saved/loaded using HuggingFace's
    standard interfaces.
    """
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
        
        # Our custom params
        self.vocab_size = vocab_size
        self.dim = dim
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.max_len = max_len
        self.use_pcl = use_pcl
        self.subspace_dim = subspace_dim
        
        # HuggingFace standard naming (for compatibility)
        self.hidden_size = dim
        self.num_hidden_layers = n_layers
        self.num_attention_heads = n_heads
        self.max_position_embeddings = max_len


class PCLForCausalLM(PreTrainedModel):
    """
    HuggingFace wrapper for PCL MiniGPT.
    
    This makes our model compatible with HuggingFace's ecosystem,
    allowing use of their conversion tools, pipelines, etc.
    """
    config_class = PCLConfig
    
    def __init__(self, config):
        super().__init__(config)
        
        # Create our PCL model with the config
        self.transformer = MiniGPT(
            vocab_size=config.vocab_size,
            dim=config.dim,
            n_layers=config.n_layers,
            n_heads=config.n_heads,
            max_len=config.max_len,
            use_pcl=config.use_pcl,
            subspace_dim=config.subspace_dim
        )
        
        # Required by HuggingFace
        self.config = config
        
        # For generation
        self.generation_config = None
    
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        labels=None,
        **kwargs
    ):
        """
        Forward pass compatible with HuggingFace.
        
        Args:
            input_ids: Token IDs [batch_size, seq_len]
            attention_mask: Attention mask (unused in our simple model)
            labels: Target tokens for loss computation
            
        Returns:
            CausalLMOutputWithPast with logits and optional loss
        """
        # Our model's forward pass
        logits, loss = self.transformer(input_ids, labels)
        
        # Return in HuggingFace format
        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=None,  # We don't use KV cache yet
            hidden_states=None,
            attentions=None
        )
    
    def generate(self, input_ids, max_new_tokens=100, **kwargs):
        """
        Generation compatible with HuggingFace.
        
        Note: This is a simple wrapper. For full HuggingFace generation
        features (beam search, etc.), we'd need to implement more methods.
        """
        temperature = kwargs.get('temperature', 1.0)
        return self.transformer.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature
        )
    
    def prepare_inputs_for_generation(self, input_ids, **kwargs):
        """Required for HuggingFace generation."""
        return {"input_ids": input_ids}


def export_to_huggingface(
    checkpoint_path='pcl_model.pt',
    output_dir='./pcl_model_hf'
):
    """
    Export trained PCL model to HuggingFace format.
    
    Args:
        checkpoint_path: Path to saved PyTorch checkpoint
        output_dir: Directory to save HuggingFace model
        
    Returns:
        output_dir: Path where model was saved
    """
    
    print("="*80)
    print("EXPORTING PCL MODEL TO HUGGINGFACE FORMAT")
    print("="*80)
    
    # Load checkpoint
    print(f"\n📂 Loading checkpoint from {checkpoint_path}...")
    
    if not os.path.exists(checkpoint_path):
        print(f"❌ Error: Checkpoint not found at {checkpoint_path}")
        print("   Run train_pcl_for_ollama.py first!")
        sys.exit(1)
    
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    config_dict = checkpoint['config']
    state_dict = checkpoint['model_state_dict']
    
    print(f"✅ Checkpoint loaded")
    print(f"   Parameters: {sum(p.numel() for p in state_dict.values()):,}")
    
    # Create HuggingFace config
    print(f"\n⚙️  Creating HuggingFace config...")
    config = PCLConfig(**config_dict)
    
    # Create HuggingFace model
    print(f"🏗️  Creating HuggingFace model...")
    hf_model = PCLForCausalLM(config)
    
    # Load weights into the transformer part
    hf_model.transformer.load_state_dict(state_dict)
    
    print(f"✅ Model created and weights loaded")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save in HuggingFace format
    print(f"\n💾 Saving to {output_dir}...")
    hf_model.save_pretrained(output_dir)
    config.save_pretrained(output_dir)
    
    print(f"✅ Model saved successfully!")
    
    # Save additional metadata
    metadata = {
        'model_type': 'pcl_minigpt',
        'version': '1.0',
        'config': config_dict,
        'training_info': checkpoint.get('training_info', {}),
        'notes': 'PCL (Phase Control Layer) MiniGPT model'
    }
    
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"   Metadata: {metadata_path}")
    
    # Verify the model can be loaded
    print(f"\n🔍 Verifying model can be loaded...")
    try:
        loaded_model = PCLForCausalLM.from_pretrained(output_dir)
        print(f"✅ Model loads successfully!")
        
        # Quick test
        test_input = torch.tensor([[0, 1, 2, 3, 4]])
        with torch.no_grad():
            output = loaded_model(test_input)
            print(f"   Test forward pass: logits shape = {output.logits.shape}")
    
    except Exception as e:
        print(f"⚠️  Warning: Model verification failed: {e}")
    
    print("\n" + "="*80)
    print("EXPORT COMPLETE")
    print("="*80)
    
    print(f"\n📁 HuggingFace model saved to: {output_dir}")
    print(f"\nNext steps:")
    print(f"1. Install llama.cpp:")
    print(f"   git clone https://github.com/ggerganov/llama.cpp.git")
    print(f"")
    print(f"2. Convert to GGUF:")
    print(f"   python llama.cpp/convert-hf-to-gguf.py {output_dir} \\")
    print(f"     --outfile pcl_model.gguf \\")
    print(f"     --outtype f16")
    print(f"")
    print(f"3. Create Modelfile:")
    print(f"   echo 'FROM ./pcl_model.gguf' > Modelfile")
    print(f"")
    print(f"4. Import to Ollama:")
    print(f"   ollama create pcl-minigpt -f Modelfile")
    print(f"")
    print(f"5. Test:")
    print(f"   ollama run pcl-minigpt")
    
    return output_dir


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Export PCL model to HuggingFace')
    parser.add_argument(
        '--checkpoint',
        type=str,
        default='pcl_model.pt',
        help='Path to PyTorch checkpoint'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./pcl_model_hf',
        help='Output directory for HuggingFace model'
    )
    
    args = parser.parse_args()
    
    export_to_huggingface(args.checkpoint, args.output)

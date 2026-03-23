"""
Train PCL MiniGPT for Ollama Export
====================================

This script trains a small PCL model suitable for export to Ollama.
Uses a tiny dataset for quick training and demonstration.
"""

import torch
import torch.nn as nn
import json
import os
import sys

# Import our PCL model
try:
    from pcl_corrected import MiniGPT
except ImportError:
    print("❌ Error: pcl_corrected.py not found")
    print("   Make sure you're in the same directory as pcl_corrected.py")
    sys.exit(1)


def create_tiny_dataset(vocab_size=32000, seq_len=128, n_samples=1000):
    """Create a tiny synthetic dataset for quick training."""
    print(f"📊 Creating dataset: {n_samples} samples, seq_len={seq_len}")
    
    # Simple patterns: counting, repeating, fibonacci-like
    data = []
    for i in range(n_samples):
        pattern = i % 3
        if pattern == 0:
            # Count up
            seq = torch.arange(seq_len) % vocab_size
        elif pattern == 1:
            # Repeat pattern
            base = torch.randint(0, vocab_size, (10,))
            seq = base.repeat((seq_len // 10) + 1)[:seq_len]
        else:
            # Random (to learn general distribution)
            seq = torch.randint(0, vocab_size, (seq_len,))
        
        data.append(seq)
    
    return torch.stack(data)


def train_pcl_model(
    vocab_size=32000,
    dim=512,
    n_layers=8,
    n_heads=8,
    max_len=2048,
    n_epochs=10,
    batch_size=16,
    learning_rate=3e-4
):
    """Train a PCL model ready for Ollama export."""
    
    print("="*80)
    print("TRAINING PCL MODEL FOR OLLAMA")
    print("="*80)
    
    # Configuration
    config = {
        'vocab_size': vocab_size,
        'dim': dim,
        'n_layers': n_layers,
        'n_heads': n_heads,
        'max_len': max_len,
        'use_pcl': True,
        'subspace_dim': 2  # k=2 for efficiency
    }
    
    print(f"\n📦 Model Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Create model
    print(f"\n🏗️  Creating model...")
    model = MiniGPT(**config)
    
    n_params = sum(p.numel() for p in model.parameters())
    print(f"   Parameters: {n_params:,}")
    print(f"   Model size: ~{n_params * 4 / 1024 / 1024:.1f} MB (FP32)")
    
    # Create dataset
    dataset = create_tiny_dataset(vocab_size, seq_len=128, n_samples=1000)
    
    # Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    
    # Training loop
    print(f"\n🏋️  Training for {n_epochs} epochs...")
    model.train()
    
    best_loss = float('inf')
    
    for epoch in range(n_epochs):
        epoch_loss = 0
        n_batches = len(dataset) // batch_size
        
        for batch_idx in range(n_batches):
            # Get batch
            start_idx = batch_idx * batch_size
            end_idx = start_idx + batch_size
            batch = dataset[start_idx:end_idx]
            
            # Input and target (shifted by 1)
            x = batch[:, :-1]
            y = batch[:, 1:]
            
            # Forward
            optimizer.zero_grad()
            logits, loss = model(x, y)
            
            # Backward
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            epoch_loss += loss.item()
        
        avg_loss = epoch_loss / n_batches
        
        if avg_loss < best_loss:
            best_loss = avg_loss
        
        if (epoch + 1) % 2 == 0:
            print(f"   Epoch {epoch+1:2d}/{n_epochs}: Loss = {avg_loss:.4f}")
    
    print(f"\n✅ Training complete!")
    print(f"   Final loss: {avg_loss:.4f}")
    print(f"   Best loss:  {best_loss:.4f}")
    
    # Save model
    output_path = 'pcl_model.pt'
    print(f"\n💾 Saving model to {output_path}...")
    
    torch.save({
        'model_state_dict': model.state_dict(),
        'config': config,
        'training_info': {
            'final_loss': avg_loss,
            'best_loss': best_loss,
            'n_epochs': n_epochs,
            'vocab_size': vocab_size,
            'n_params': n_params
        }
    }, output_path)
    
    # Save config separately for easy access
    config_path = 'pcl_model_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Model saved successfully!")
    print(f"   Checkpoint: {output_path}")
    print(f"   Config:     {config_path}")
    
    # Test generation
    print(f"\n🎲 Testing generation...")
    model.eval()
    with torch.no_grad():
        prompt = torch.tensor([[0, 1, 2, 3, 4]])
        generated = model.generate(prompt, max_new_tokens=20)
        print(f"   Prompt:    {prompt[0].tolist()}")
        print(f"   Generated: {generated[0].tolist()}")
    
    print("\n" + "="*80)
    print("READY FOR EXPORT")
    print("="*80)
    print("\nNext steps:")
    print("1. Run: python export_to_huggingface.py")
    print("2. Convert to GGUF using llama.cpp")
    print("3. Import to Ollama with Modelfile")
    print("\nOr use the quick export:")
    print("  python simple_ollama_export.py")
    
    return model, config


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train PCL model for Ollama')
    parser.add_argument('--vocab-size', type=int, default=32000, help='Vocabulary size')
    parser.add_argument('--dim', type=int, default=512, help='Model dimension')
    parser.add_argument('--layers', type=int, default=8, help='Number of layers')
    parser.add_argument('--heads', type=int, default=8, help='Number of attention heads')
    parser.add_argument('--epochs', type=int, default=10, help='Training epochs')
    parser.add_argument('--batch-size', type=int, default=16, help='Batch size')
    parser.add_argument('--lr', type=float, default=3e-4, help='Learning rate')
    
    args = parser.parse_args()
    
    model, config = train_pcl_model(
        vocab_size=args.vocab_size,
        dim=args.dim,
        n_layers=args.layers,
        n_heads=args.heads,
        n_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr
    )

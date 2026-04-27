"""
Training script for the Custom LLM

This script trains the neural network on the training data and tests the results.
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm.client import CustomProvider


async def train_and_test():
    """Train the custom LLM and test it"""
    
    print("=" * 60)
    print("Cognitive Engine - Custom LLM Training")
    print("=" * 60)
    
    # Initialize the custom provider
    provider = CustomProvider()
    
    print(f"\nTraining data loaded: {len(provider.training_data)} examples")
    
    if len(provider.training_data) == 0:
        print("No training data found. Creating initial dataset...")
        # The training data should already exist in llm_training_data.json
        print("Please ensure llm_training_data.json exists with training examples.")
        return
    
    # Train the model
    print("\nTraining neural network...")
    losses = provider.train_model(epochs=50)
    
    print(f"\nTraining completed!")
    print(f"Initial loss: {losses[0]:.4f}")
    print(f"Final loss: {losses[-1]:.4f}")
    print(f"Improvement: {losses[0] - losses[-1]:.4f}")
    
    # Test the trained model
    print("\n" + "=" * 60)
    print("Testing Trained Model")
    print("=" * 60)
    
    test_prompts = [
        "hello",
        "what is the cognitive engine",
        "how do you work",
        "what is a thought",
        "tell me about deliberation"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        response = await provider.generate(prompt, mode='response')
        print(f"Response: {response}")
        print("-" * 40)
    
    print("\nTraining and testing complete!")


if __name__ == "__main__":
    asyncio.run(train_and_test())

# Custom LLM Training Guide

This guide covers training a custom LLM for the Cognitive Engine.

## Overview

The Cognitive Engine includes a custom LLM provider that can be trained on domain-specific data. This allows the system to:
- Learn from your specific use cases
- Adapt to your terminology
- Improve performance on your tasks
- Reduce dependency on external APIs

## Training Script

The training script is located at `train_llm.py`.

### Basic Usage

```bash
python train_llm.py
```

This will:
1. Load training data from `llm_training_data.json`
2. Train the neural network
3. Test the trained model
4. Save the trained weights to `neural_network_weights.npz`

## Training Data

### Data Format

Training data should be in JSON format:

```json
{
  "examples": [
    {
      "prompt": "What is artificial intelligence?",
      "response": "AI is the simulation of human intelligence in machines..."
    },
    {
      "prompt": "How do neural networks learn?",
      "response": "Neural networks learn through backpropagation..."
    }
  ]
}
```

### Creating Training Data

Create or edit `llm_training_data.json`:

```python
import json

training_data = {
    "examples": [
        {
            "prompt": "Your question here",
            "response": "Your answer here"
        }
    ]
}

with open('llm_training_data.json', 'w') as f:
    json.dump(training_data, f, indent=2)
```

### Data Quality Guidelines

- **Variety**: Include diverse examples
- **Accuracy**: Ensure responses are correct
- **Consistency**: Maintain consistent style
- **Relevance**: Focus on your domain
- **Quantity**: More examples generally improve performance

## Training Process

### Neural Network Architecture

The custom LLM uses a neural network with:
- Input layer: Tokenized prompts
- Hidden layers: Multiple processing layers
- Output layer: Generated responses

### Training Parameters

Default training parameters in `train_llm.py`:

```python
provider.train_model(epochs=50)
```

You can adjust parameters by modifying the training script:

```python
# More epochs for better training
provider.train_model(epochs=100)

# Learning rate
provider.train_model(epochs=50, learning_rate=0.001)

# Batch size
provider.train_model(epochs=50, batch_size=32)
```

### Monitoring Training

The training script outputs:
- Initial loss
- Final loss
- Improvement metrics

Example output:
```
Training neural network...
Initial loss: 2.3456
Final loss: 0.1234
Improvement: 2.2222
```

## Testing the Trained Model

### Built-in Testing

The training script includes automatic testing:

```bash
python train_llm.py
```

Test prompts included:
- "hello"
- "what is the cognitive engine"
- "how do you work"
- "what is a thought"
- "tell me about deliberation"

### Manual Testing

Test the trained model programmatically:

```python
from llm.client import CustomProvider

provider = CustomProvider()
provider.load_weights('neural_network_weights.npz')

response = await provider.generate("Your question", mode='response')
print(response)
```

## Using the Custom LLM

### Configuration

Enable the custom LLM in your configuration:

```python
from llm.client import CustomProvider
from core.config import Config

# Use custom provider
config = Config(default_llm_provider='custom')

# Or set environment variable
DEFAULT_LLM_PROVIDER=custom
```

### Integration with Cognitive Engine

```python
from core.engine import CognitiveEngine
from llm.client import CustomProvider

# Initialize custom provider
custom_provider = CustomProvider()
custom_provider.load_weights('neural_network_weights.npz')

# Use in engine
engine = CognitiveEngine()
engine.llm_client.provider = custom_provider
```

## Advanced Training

### Transfer Learning

Start with pre-trained weights and fine-tune:

```python
provider = CustomProvider()
provider.load_weights('pretrained_weights.npz')
provider.train_model(epochs=10)  # Fine-tune
```

### Continuous Learning

Add new data and retrain periodically:

```python
# Add new examples to training data
# Retrain with more epochs
provider.train_model(epochs=20)
```

### Evaluation Metrics

Evaluate model performance:

```python
provider = CustomProvider()
provider.load_weights('neural_network_weights.npz')

# Test on validation set
test_results = provider.evaluate(validation_data)
print(f"Accuracy: {test_results['accuracy']}")
print(f"Loss: {test_results['loss']}")
```

## Troubleshooting

### No Training Data

**Issue**: "No training data found"

**Solution**:
```bash
# Ensure llm_training_data.json exists
ls llm_training_data.json

# Create if missing
echo '{"examples":[]}' > llm_training_data.json
```

### Poor Training Results

**Issue**: Model doesn't learn well

**Solutions**:
- Increase training epochs
- Add more diverse training data
- Check data quality
- Adjust learning rate
- Normalize input data

### Out of Memory

**Issue**: Training fails due to memory

**Solutions**:
- Reduce batch size
- Use fewer training examples
- Reduce model complexity
- Use GPU if available

### Slow Training

**Issue**: Training takes too long

**Solutions**:
- Reduce epochs
- Use smaller dataset
- Use GPU acceleration
- Optimize data loading

## Best Practices

1. **Data Quality**
   - Ensure accurate responses
   - Maintain consistent formatting
   - Remove duplicates
   - Balance categories

2. **Training Strategy**
   - Start with small dataset
   - Gradually increase complexity
   - Monitor loss curves
   - Save checkpoints

3. **Evaluation**
   - Use separate test set
   - Measure multiple metrics
   - Test on real queries
   - Compare with baseline

4. **Deployment**
   - Version your models
   - Test before deployment
   - Monitor performance
   - Rollback if needed

## Performance Tips

- Use GPU acceleration if available
- Batch similar queries
- Cache frequent responses
- Optimize data loading
- Use mixed precision training

## File Locations

- Training script: `train_llm.py`
- Training data: `llm_training_data.json`
- Model weights: `neural_network_weights.npz`
- Custom provider: `llm/client.py` (CustomProvider class)

## Support

For training issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check training logs for errors
- Verify training data format

# Traffic - cs50-ai NN project

Write an AI to identify which traffic sign appears in a photograph. 

Developing a computer vision model, allowing cars to understand their environment from digital images (we use the German Traffic Sign Recognition Benchmark (GTSRB) dataset)

## Experimentation process

I started with a base scenario that I copied from the handwriting CNN model. The model looked like:

| Layer 1| Layer 2| Layer 3| Layer 4|
|-|-|-|-|
| Convolutional layer, learning 32 filters using 3x3 kernel | Max-pooling layer using 2x2 pool size | Hidden layer with 128 nodes (50% dropout) | Output layer for all traffic sign categories |


## Results

| Scenario | Modification                                                                | Testing Accuracy |
|----------|-----------------------------------------------------------------------------|------------------|
| 1        | none                                                                        | 0.0514           |
| 2        | Adding convolutional layer (64 filters) and Max-pooling layer after layer 2 | 0.9692           |
| 3        | Adding convolutional layer (64 filters) after layer 2                       | 0.9757           |
| 4        | Adding 2 convolutional layers (64 filters and 128 filters) after layer 2    | 0.9838           |


## What worked well?

Adding convolutional layers to the model allowed me to reach a significantly better accuracy.
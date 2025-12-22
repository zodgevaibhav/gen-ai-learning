from genaibook.core import get_device

def main():
    device = get_device()
    print(f"Detected device: {device}")
    # mps -> metal
    # CPU, GPU, TPU
    # Tensor : 3D Array kind of DS
    # TensorFlow <-- Library, Tensor DS computation easy
    # PyTorch <-- Library, Tensor DS computation easy
    # Torch : PyTorch Library
     # Tensor : Computation
        # Matrix Multiplication
        # Addition/Subtraction
        # Reshape : meaning 
            # - Mannitude change : Values/Depth/Color
            # - Dimension/Scaling change : Shape
            #  - Rotate

if __name__ == "__main__":
    main()
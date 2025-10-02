# gan_mnist_hf.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import torchvision
import matplotlib.pyplot as plt
import numpy as np
from datasets import load_dataset

# --------------------------
# 1. Hyperparameters
# --------------------------
latent_dim = 100
hidden_dim = 256
image_size = 28*28  # MNIST images are 28x28
batch_size = 64
epochs = 50
lr = 0.0002

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --------------------------
# 2. Load HuggingFace MNIST dataset
# --------------------------
hf_dataset = load_dataset("mnist")  # loads train + test

# Transform: convert to tensor & normalize [-1,1]
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# Custom PyTorch Dataset wrapper
class MNISTDataset(Dataset):
    def __init__(self, hf_dataset_split, transform=None):
        self.dataset = hf_dataset_split
        self.transform = transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img = self.dataset[idx]["image"]
        label = self.dataset[idx]["label"]
        if self.transform:
            img = self.transform(img)
        return img, label

train_dataset = MNISTDataset(hf_dataset["train"], transform=transform)
dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# --------------------------
# 3. Generator
# --------------------------
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim*2),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim*2, image_size),
            nn.Tanh()
        )

    def forward(self, z):
        return self.model(z)

# --------------------------
# 4. Discriminator
# --------------------------
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(image_size, hidden_dim*2),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim*2, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, img):
        return self.model(img)

# --------------------------
# 5. Initialize models + loss + optimizers
# --------------------------
generator = Generator().to(device)
discriminator = Discriminator().to(device)

criterion = nn.BCELoss()
optimizer_G = optim.Adam(generator.parameters(), lr=lr)
optimizer_D = optim.Adam(discriminator.parameters(), lr=lr)

# --------------------------
# 6. Training Loop
# --------------------------
fixed_noise = torch.randn(16, latent_dim, device=device)

for epoch in range(epochs):
    for real_imgs, _ in dataloader:
        real_imgs = real_imgs.view(-1, image_size).to(device)
        batch_size_curr = real_imgs.size(0)

        # Labels
        real_labels = torch.ones(batch_size_curr, 1, device=device)
        fake_labels = torch.zeros(batch_size_curr, 1, device=device)

        # -------------------
        # Train Generator
        # -------------------
        optimizer_G.zero_grad()
        z = torch.randn(batch_size_curr, latent_dim, device=device)
        fake_imgs = generator(z)
        output = discriminator(fake_imgs)
        g_loss = criterion(output, real_labels)  # trick D
        g_loss.backward()
        optimizer_G.step()

        # -------------------
        # Train Discriminator
        # -------------------
        optimizer_D.zero_grad()
        real_loss = criterion(discriminator(real_imgs), real_labels)
        fake_loss = criterion(discriminator(fake_imgs.detach()), fake_labels)
        d_loss = (real_loss + fake_loss) / 2
        d_loss.backward()
        optimizer_D.step()

    # -------------------
    # Show progress
    # -------------------
    with torch.no_grad():
        fake_samples = generator(fixed_noise).view(-1, 1, 28, 28).cpu()
    grid = torchvision.utils.make_grid(fake_samples, nrow=4, normalize=True)
    plt.imshow(np.transpose(grid, (1,2,0)))
    plt.title(f"Epoch {epoch+1}/{epochs}")
    plt.show()

    print(f"Epoch [{epoch+1}/{epochs}]  D_loss: {d_loss.item():.4f}  G_loss: {g_loss.item():.4f}")

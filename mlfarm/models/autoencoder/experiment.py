import torch
from torch import nn
from torch.nn import functional as F
import pytorch_lightning as pl
from torchvision import transforms
import data

class Autoencoder(pl.LightningModule):
    def __init__(self, encoder, decoder, loss, optimizer_builders, train_dataset_builder, train_data_loader_builder, lr_scheduler_builders=None):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.loss = loss
        self.optimizer_builders = optimizer_builders
        self.lr_scheduler_builders = lr_scheduler_builders
        self.train_dataset_builder = train_dataset_builder
        self.train_data_loader_builder = train_data_loader_builder

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def training_step(self, batch, batch_idx):
        y = batch['image']
        y_hat = self(y)
        loss = self.loss(y_hat, y)
        return { 'loss': loss }

    def configure_optimizers(self):
        args = {
            'params': self.parameters()
        }

        optims = [ob(args) for ob in self.optimizer_builders]
        if self.lr_scheduler_builders:
            return optims, [lb({'optimizer': opt}) for lb, opt in zip(self.lr_scheduler_builders, optims)]
        elif len(optims) == 1:
            return optims[0]
        return optims
    
    def train_dataloader(self):
        dataset = self.train_dataset_builder()
        loader = self.train_data_loader_builder({'dataset': dataset})
        return loader
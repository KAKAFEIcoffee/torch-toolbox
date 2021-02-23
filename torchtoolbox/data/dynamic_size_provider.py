__all__ = ['DynamicBatchSampler', 'DynamicSizeImageFolder']
from torch.utils.data import BatchSampler
from torchvision.datasets import ImageFolder


class DynamicBatchSampler(BatchSampler):
    """DynamicBatchSampler

    Args:
        info_generate_fn (callable): give batch samples extra info.
    """
    def __init__(self, sampler, batch_size: int, drop_last: bool, info_generate_fn) -> None:
        super().__init__(sampler, batch_size, drop_last)
        self.generate_fn = info_generate_fn

    def __iter__(self):
        batch = []
        info = self.generate_fn()
        for idx in self.sampler:
            batch.append([idx, info])
            if len(batch) == self.batch_size:
                yield batch
                batch = []
                info = self.generate_fn()
        if len(batch) > 0 and not self.drop_last:
            yield batch


class DynamicSizeImageFolder(ImageFolder):
    def __getitem__(self, index_info):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        index, size = index_info
        path, target = self.samples[index]
        sample = self.loader(path)
        if self.transform is not None:
            sample = self.transform(sample, size)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target

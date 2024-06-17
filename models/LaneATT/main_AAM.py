import logging
import argparse
import os
import random
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

from lib.config import Config
from lib.runner import Runner
from lib.experiment import Experiment


def parse_args():
    parser = argparse.ArgumentParser(description="Train lane detector")
    parser.add_argument("mode", choices=["train", "test"], help="Train or test?")
    parser.add_argument("--exp_name", help="Experiment name", required=True)
    parser.add_argument("--cfg", help="Config file")
    parser.add_argument("--resume", action="store_true", help="Resume training")
    parser.add_argument("--epoch", type=int, help="Epoch to test the model on")
    parser.add_argument("--cpu", action="store_true", help="(Unsupported) Use CPU instead of GPU")
    parser.add_argument("--save_predictions", action="store_true", help="Save predictions to pickle file")
    parser.add_argument("--view", choices=["all", "mistakes"], help="Show predictions")
    parser.add_argument("--deterministic",
                        action="store_true",
                        help="set cudnn.deterministic = True and cudnn.benchmark = False")
    args = parser.parse_args()
    if args.cfg is None and args.mode == "train":
        raise Exception("If you are training, you have to set a config file using --cfg /path/to/your/config.yaml")
    if args.resume and args.mode == "test":
        raise Exception("args.resume is set on `test` mode: can't resume testing")
    if args.epoch is not None and args.mode == 'train':
        raise Exception("The `epoch` parameter should not be set when training")
    if args.view is not None and args.mode != "test":
        raise Exception('Visualization is only available during evaluation')
    if args.cpu:
        raise Exception("CPU training/testing is not supported: the NMS procedure is only implemented for CUDA")

    return args


class HAARepository:
    def __init__(self, haa_folder):
        self.haa_folder = haa_folder
        self.haa_images = self.load_haa_images()

    def load_haa_images(self):
        # 从haa_folder加载图片
        haa_images = []
        for file in os.listdir(self.haa_folder):
            if file.endswith(".png"): 
                img = Image.open(os.path.join(self.haa_folder, file))
                haa_images.append(transforms.ToTensor()(img))
        return haa_images

    def sample(self):
        # 随机抽取一个高注意力区域图片
        return random.choice(self.haa_images)


def compute_attention_map(model, inputs):
    """计算给定输入的注意力图"""
    model.eval()
    with torch.no_grad():
        outputs = model(inputs)
        attention_map = F.relu(torch.sum(outputs, dim=1, keepdim=True))
    return attention_map


def apply_aam(images, attention_maps, haa_repository):
    mixed_images = []
    for img, attn_map in zip(images, attention_maps):
        high_attention_area = haa_repository.sample()
        augmented_image = img * (1 - attn_map) + high_attention_area * attn_map
        mixed_images.append(augmented_image)
    return torch.stack(mixed_images)


def main():
    args = parse_args()
    exp = Experiment(args.exp_name, args, mode=args.mode)
    if args.cfg is None:
        cfg_path = exp.cfg_path
    else:
        cfg_path = args.cfg
    cfg = Config(cfg_path)
    exp.set_cfg(cfg, override=False)
    device = torch.device('cpu') if not torch.cuda.is_available() or args.cpu else torch.device('cuda')
    runner = Runner(cfg, exp, device, view=args.view, resume=args.resume, deterministic=args.deterministic)

    haa_repository = HAARepository('./data/haa_images/')

    if args.mode == 'train':
        try:
            for epoch in range(cfg['epochs']):
                for inputs, targets in runner.train_loader:
                    attention_maps = compute_attention_map(runner.model, inputs)
                    mixed_inputs = apply_aam(inputs, attention_maps, haa_repository)

                    # 使用混合输入训练模型
                    outputs = runner.model(mixed_inputs)
                    loss = runner.criterion(outputs, targets)
                    runner.optimizer.zero_grad()
                    loss.backward()
                    runner.optimizer.step()
        except KeyboardInterrupt:
            logging.info('Training interrupted.')
    runner.eval(epoch=args.epoch or exp.get_last_checkpoint_epoch(), save_predictions=args.save_predictions)


if __name__ == '__main__':
    main()

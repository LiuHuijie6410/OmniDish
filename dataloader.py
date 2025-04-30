from PIL import Image
import os
import json

class DishEditingDataset():
    def __init__(self, data_root, pair_list_file, transform=None):
        self.data_root = data_root
        self.data = []
        with open(pair_list_file) as f:
            for i, line in enumerate(f):

                line = line.strip()
                cur_meta = json.loads(line)
                cur_dict = {}
                cur_dict['pair_id'] = i + 1
               
                cur_dict['image_src'] = f"{data_root}/{i+1}-src.png"
                cur_dict['image_tgt'] = f"{data_root}/{i+1}-target.png"
                cur_dict['meta'] = cur_meta
                self.data.append(cur_dict)
            
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        pair_info = self.data[idx]

        img_a = self._load_image(pair_info["image_src"])
        img_b = self._load_image(pair_info["image_tgt"])

        meta = pair_info.get("meta", {})
        
        return {
            "image_src": img_a,
            "image_tgt": img_b,
            "meta": meta,
            "pair_id": pair_info["pair_id"]
        }

    def _load_image(self, rel_path):
        full_path = os.path.join(self.data_root, rel_path)
        image = Image.open(full_path).convert("RGB")  # 统一转为RGB格式
        return image

if __name__ == "__main__":

    dataset = DishEditingDataset(
        data_root="datasets/png_imgs",
        pair_list_file="datasets/txt.txt",
    )

    for i in range(len(dataset)):  
        sample = dataset[i]  
        print("Data ID:", i+1)
        sample['image_src'].save(f'./{i+1}-source_image.png')
        sample['image_tgt'].save(f'./{i+1}-target_image.png')
        print(f"Source image saved to {f'{i+1}-source_image.png'}")
        print(f"Target image saved to {f'{i+1}-target_image.png'}")
        for k, v in sample['meta'].items():
            print(f"{k}:\t{v}")
        if i == 5:
            break

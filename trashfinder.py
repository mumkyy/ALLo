import torch

class trash_finder:
    
    def __init__(self,yolo_dir,model_dir):
        self.model = torch.hub.load(yolo_dir, 'custom', path=model_dir, source='local')

    def find_trash(self,img):
        results = self.model([img], size=640) # batch of images
        return results

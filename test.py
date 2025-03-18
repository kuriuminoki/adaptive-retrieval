import torch
print('GPU の利用状況 :', torch.cuda.is_available())
print('CUDA のバージョン :', torch.version.cuda)
print('cuDNN のバージョン :', torch.backends.cudnn.version())

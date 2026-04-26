import numpy as np
import matplotlib.pyplot as plt

# 示例：展示 clims 的作用
data = np.array([[50, 100, 150],
                 [200, 250, 10],
                 [180, 75, 225]], dtype=np.uint8)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# 默认情况（自动缩放）
im1 = axes[0].imshow(data, cmap='gray')
axes[0].set_title('默认 clims\n(min-max自动缩放)')
axes[0].axis('off')
plt.colorbar(im1, ax=axes[0])

# 手动设置 clims 为 0-255（标准8位图像范围）
im2 = axes[1].imshow(data, cmap='gray', vmin=0, vmax=255)
axes[1].set_title('固定 clims\n(0-255)')
axes[1].axis('off')
plt.colorbar(im2, ax=axes[1])

# 手动设置 clims 为数据的实际范围
im3 = axes[2].imshow(data, cmap='gray', vmin=data.min(), vmax=data.max())
axes[2].set_title(f'动态 clims\n({data.min()}-{data.max()})')
axes[2].axis('off')
plt.colorbar(im3, ax=axes[2])

plt.tight_layout()
plt.show()
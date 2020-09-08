from scene_detector.scene_detect_script import find_scenes
from PIL import Image
import cv2
from kmean_cluster.cluster_utility import ClusterUtility
from kmean_cluster.stats.key_frame import KeyFrame


res = find_scenes("test.mov")


imgs = []
bars = []
for i in res:
    width = int(i.shape[1] * 0.1)
    height = int(i.shape[0] * 0.1)
    dim = (width, height)
    image = cv2.resize(i, dim, Image.ANTIALIAS)
    bar, colors_info = ClusterUtility.kmeans_cluster(image, 5)
    imgs.append(KeyFrame(colors_info))
    bars.append(bar)
print(imgs)
print(len(imgs))

for i in bars:
    cv2.imshow('image',i)
    cv2.waitKey(0)

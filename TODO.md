#Todo list
### 1. Error arouse when test scene detect, some lib miss:

Error message:

```python
/usr/bin/python2.7 /home/jacky/Documents/git/github/FilmColorSearch/src/scene_detector/scene_detect_script.py
Traceback (most recent call last):
  File "/home/jacky/Documents/git/github/FilmColorSearch/src/scene_detector/scene_detect_script.py", line 14, in <module>
    from scenedetect.video_manager import VideoManager
  File "/home/jacky/.local/lib/python2.7/site-packages/scenedetect/__init__.py", line 52, in <module>
    from scenedetect.scene_manager import SceneManager
  File "/home/jacky/.local/lib/python2.7/site-packages/scenedetect/scene_manager.py", line 67, in <module>
    from scenedetect.thirdparty.simpletable import SimpleTableCell, SimpleTableImage
  File "/home/jacky/.local/lib/python2.7/site-packages/scenedetect/thirdparty/simpletable.py", line 57, in <module>
    from urllib.parse import quote
ImportError: No module named parse
```

### 2. testing
    1. use kmean-cluster to process the test pics
    2. pickle locally
    3. test parallel search 
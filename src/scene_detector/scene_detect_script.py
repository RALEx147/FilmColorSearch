"""Scene Detect Script

File to initiate automation of scene detection. Uses hardcoded parameters.
Saves out to images and python objects.

"""

import os
import math
from string import Template
import numpy as np
import cv2

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors.content_detector import ContentDetector
from scenedetect.platform import get_cv2_imwrite_params
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.platform import get_and_create_path

def find_scenes(video_path, generate_images=False):
    """
    This method slicing a video to a list of scenes, each scene will have a similar color distributions.
    This function allows to generate images for each scene.
    :param video_path: The path to the video for finding scenes
    :param generate_images: whether to generate images or not
    :return: a list of scenes
    """
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)

    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    stats_file_path = '%s.stats.csv' % video_path

    scene_list = []

    try:
        if os.path.exists(stats_file_path):
            with open(stats_file_path, 'r') as stats_file:
                stats_manager.load_from_csv(stats_file, base_timecode)

        video_manager.set_downscale_factor()
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(base_timecode)

        if generate_images:
            print("Starting to generate images from scenelist")
            num_images = 2

            if not scene_list:
                return

            available_extensions = get_cv2_imwrite_params()
            image_extension = "jpg"


            imwrite_param = [available_extensions[image_extension], 100]

            video_manager.release()
            video_manager.reset()
            video_manager.set_downscale_factor(1)
            video_manager.start()

            completed = True
            print('Generating output images (%d per scene)...', num_images)

            filename_template = Template("$VIDEO_NAME-Scene-$SCENE_NUMBER-$IMAGE_NUMBER")


            scene_num_format = '%0'
            scene_num_format += str(max(3, math.floor(math.log(len(scene_list), 10)) + 1)) + 'd'
            image_num_format = '%0'
            image_num_format += str(math.floor(math.log(num_images, 10)) + 2) + 'd'

            timecode_list = dict()

            fps = scene_list[0][0].framerate

            timecode_list = [
                [
                    FrameTimecode(int(f), fps=fps) for f in [
                        a[len(a)//2] if (0 < j < num_images-1) or num_images == 1
                        else min(a[0] + 0, a[-1]) if j == 0
                        else max(a[-1] - 0, a[0])
                        for j, a in enumerate(np.array_split(r, num_images))
                    ]
                ]
                for i, r in enumerate([
                        r
                        if r.stop-r.start >= num_images
                        else list(r) + [r.stop-1] * (num_images - len(r))
                        for r in (
                            range(start.get_frames(), end.get_frames())
                            for start, end in scene_list
                        )
                ])
            ]

            image_filenames = { i: [] for i in range(len(timecode_list)) }

            for i, tl in enumerate(timecode_list):
                for j, image_timecode in enumerate(tl):
                    video_manager.seek(image_timecode)
                    video_manager.grab()
                    ret_val, frame_im = video_manager.retrieve()
                    if ret_val:
                        file_path = '%s.%s' % (filename_template.safe_substitute(
                            VIDEO_NAME=video_path,
                            SCENE_NUMBER=scene_num_format % (i + 1),
                            IMAGE_NUMBER=image_num_format % (j + 1),
                            FRAME_NUMBER=image_timecode.get_frames()),
                                               image_extension)
                        image_filenames[i].append(file_path)
                        abs_file_path = get_and_create_path(file_path, "output")
                        print(abs_file_path)
                        cv2.imwrite(abs_file_path, frame_im, imwrite_param)
                    else:
                        completed = False
                        break

            if not completed:
                print('Could not generate all output images.')


    finally:
        video_manager.release()

    return scene_list

if __name__ == '__main__':
    print(find_scenes("test.mp4", True))
    # print(find_scenes("test.mp4"))

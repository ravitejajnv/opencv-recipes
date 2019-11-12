# Program To Stack Videos side by side for comparision
import os
import glob
import cv2
import re
from tqdm import tqdm
from pathlib import Path
import argparse


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def StackVideos(path1, path2, use_flag, output_fname = None, extesnion = 'jpg', frame_rate = 25, width = None, height = None):
    '''
    Function to stack and write frames for quick comparision

    Arguments:
        path1: path for videos or frames of 1st video
        path2: path for videos or frames of 2nd video
        output_fname: output filename (optional)
    '''

    if output_fname is None:
        output_fname = 'stacked_video_1_2.mp4'

    print('Output video path is {}'.format(output_fname))

    if use_flag == 'frames':
        file_list_1 = glob.glob(os.path.join(path1, '*.'+extesnion))
        file_list_2 = glob.glob(os.path.join(path2, '*.'+extesnion))
        file_list_1 = natural_sort (file_list_1)
        file_list_2 = natural_sort (file_list_2)

        frame = cv2.imread(file_list_1[0])
        h, w, c = frame.shape

        if height is None:
            height = h
        if width is None:
            width = w

        out = cv2.VideoWriter(str(output_fname), cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (width*2, height))

        for i,(file1, file2) in enumerate(zip(file_list_1,file_list_2)):
            img1 = cv2.imread(file1)
            img2 = cv2.imread(file2)
            img1 = cv2.resize(img1,(width,height))
            img2 = cv2.resize(img2,(width,height))
            img_out = cv2.hconcat([img1, img2])
            out.write(img_out)

    if use_flag == 'videos':
        cap1 = cv2.VideoCapture(str(path1))
        cap2 = cv2.VideoCapture(str(path2))

        w = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if height is None:
            height = h
        if width is None:
            width = w

        out = cv2.VideoWriter(str(output_fname), cv2.VideoWriter_fourcc(*"mp4v"), (frame_rate), (width*2, height))
        while True:
            ret1, img1 = cap1.read()
            ret2, img2 = cap2.read()
            
            if not (ret1 and ret2):
                break
            img1 = cv2.resize(img1,(width,height))
            img2 = cv2.resize(img2,(width,height))
            
            img_out = cv2.hconcat([img1, img2])
            out.write(img_out)

    out.release()
    return

    
def main():
    
    parser = argparse.ArgumentParser(description="stack frames from two videos side by side for comparision")

    parser.add_argument(
        "--video-file-1",
        dest="video_file_1",
        default=None,
        metavar="FILE",
        help="path to first video file",
        type=str,
    )

    parser.add_argument(
        "--video-file-2",
        dest="video_file_2",
        default=None,
        metavar="FILE",
        help="path to second video file",
        type=str,
    )

    parser.add_argument(
        "--frame-path-1",
        dest="frame_path_1",
        default=None,
        metavar="Dir",
        help="path to first frames folder",
        type=str,
    )

    parser.add_argument(
        "--frame-path-2",
        dest="frame_path_2",
        default=None,
        metavar="Dir",
        help="path to second frames folder",
        type=str,
    )

    parser.add_argument(
        "--frame-extension",
        dest="frame_extension",
        default='jpg',
        metavar="Extension",
        help="File extension of frames jpg/png",
        type=str,
    )

    parser.add_argument(
        "--use_frames",
        dest="use_frames",
        help="Make this true when you have folders with frames",
        default=False,
        type=bool,
    )

    parser.add_argument(
        "--use_videos",
        dest="use_videos",
        help="Make this true when you have files as video files",
        default=False,
        type=bool,
    )

    parser.add_argument(
        "--output_fname",
        dest="output_video_file",
        default=None,
        metavar="FILE",
        help="path to video file",
        type=str,
    )

    parser.add_argument(
        "--frame-rate",
        dest="frame_rate",
        default=25,
        help="Desired frame rate of the output video",
        type=float,
    )

    parser.add_argument(
        "--height",
        dest="height",
        default=None,
        help="Desired height of output video, optional argument",
        type=int,
    )

    parser.add_argument(
        "--width",
        dest="width",
        default=None,
        help="Desired height of output video, video will be double the given width due to stacking, optional argument",
        type=int,
    )

    args = parser.parse_args()

    use_frames = args.use_frames
    use_videos = args.use_videos
    extesnion = args.frame_extension
    frame_rate = args.frame_rate
    width = args.width
    height = args.height

    if (use_frames and use_videos) or ( (not use_frames) and (not use_videos) ):
        print("Error, use_frames and use_videos both can't be True simultaneously")
        sys.exit(0)
    
    # get the variables
    if use_videos:
        path1 = Path(args.video_file_1)
        path2 = Path(args.video_file_2)
    
    if use_frames:
        path1 = Path(args.frame_path_1)
        path2 = Path(args.frame_path_2)


    use_flag = 'frames' if use_frames else 'videos'

    if args.output_video_file is not None:
        output_fname = Path(args.output_video_file)
        output_fname.parents[0].mkdir(parents=True, exist_ok=True)
    else:
        output_fname = None
        
    # call the driver program
    StackVideos(path1, path2, use_flag, output_fname, extesnion, frame_rate, width, height)
    return 

# Driver Code 
if __name__ == '__main__': 

	# Calling the function 
    main()



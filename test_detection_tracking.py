"""
baseline for 3rd Anti-UAV
https://anti-uav.github.io/
"""
from __future__ import absolute_import
import os
import glob
import json
import cv2
import numpy as np
from tqdm import tqdm

from detection_siamfc import TrackerSiamFC


def iou(bbox1, bbox2):
    """
    Calculates the intersection-over-union of two bounding boxes.
    Args:
        bbox1 (numpy.array, list of floats): bounding box in format x,y,w,h.
        bbox2 (numpy.array, list of floats): bounding box in format x,y,w,h.
    Returns:
        int: intersection-over-onion of bbox1, bbox2
    """
    bbox1 = [float(x) for x in bbox1]
    bbox2 = [float(x) for x in bbox2]

    (x0_1, y0_1, w1_1, h1_1) = bbox1
    (x0_2, y0_2, w1_2, h1_2) = bbox2
    x1_1 = x0_1 + w1_1
    x1_2 = x0_2 + w1_2
    y1_1 = y0_1 + h1_1
    y1_2 = y0_2 + h1_2
    # get the overlap rectangle
    overlap_x0 = max(x0_1, x0_2)
    overlap_y0 = max(y0_1, y0_2)
    overlap_x1 = min(x1_1, x1_2)
    overlap_y1 = min(y1_1, y1_2)

    # check if there is an overlap
    if overlap_x1 - overlap_x0 <= 0 or overlap_y1 - overlap_y0 <= 0:
        return 0

    # if yes, calculate the ratio of the overlap to each ROI size and the unified size
    size_1 = (x1_1 - x0_1) * (y1_1 - y0_1)
    size_2 = (x1_2 - x0_2) * (y1_2 - y0_2)
    size_intersection = (overlap_x1 - overlap_x0) * (overlap_y1 - overlap_y0)
    size_union = size_1 + size_2 - size_intersection

    return size_intersection / size_union


def not_exist(pred):
    return (len(pred) == 1 and pred[0] == 0) or len(pred) == 0


def eval(out_res, label_res):
    measure_per_frame = []
    penalty_measure = []  # penalty for frames where the target exists but is not detected
    for _pred, _gt, _exist in zip(out_res, label_res['gt_rect'], label_res['exist']):
        measure_per_frame.append(not_exist(_pred) if not _exist else iou(_pred, _gt) if len(_pred) > 1 else 0)
        if _exist:
            if (len(_pred) > 1 and iou(_pred, _gt) > 1e-5):
                penalty_measure.append(0)
            else:
                penalty_measure.append(1)
    # 检查 measure_per_frame 的长度
    if len(measure_per_frame) == 0:
        measure_per_frame_mean = 0
    else:
        measure_per_frame_mean = np.mean(measure_per_frame)

    # 检查 penalty_measure 的长度
    if len(penalty_measure) == 0:
        penalty_measure_mean = 0
    else:
        penalty_measure_mean = np.mean(penalty_measure)

    # 计算最终结果
    return  measure_per_frame_mean - 0.2 * (penalty_measure_mean ** 0.3)
    # return np.mean(measure_per_frame) - 0.2 * np.mean(penalty_measure)**0.3

def main(mode='IR', visulization=False):
    assert mode in ['IR', 'RGB'], 'Only Support IR or RGB to evalute'
    # setup tracker
    net_path = 'model.pth'
    tracker = TrackerSiamFC(net_path=net_path)
    # tracker.name은 Yolo_SiamFC로 정의 될 것.
    yolo_model = tracker.initialize_yolo()

    # setup experiments
    video_paths = glob.glob(os.path.join(r'D:\DataSet\UAV\track2_test', '*'))
    video_num = len(video_paths)
    output_dir = os.path.join('results', tracker.name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    overall_performance = []

    # run tracking experiments and report performance
    for video_id, video_path in enumerate(video_paths, start=1):
        video_name = os.path.basename(video_path) # 파일 경로에서 마지막 구성 요소만 추출 \\ 제일 마지막꺼
        video_file = os.path.join(video_path, '%s.mp4'%mode)
        frame_files = sorted(
            [f for f in os.listdir(video_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))])  # 得到视频帧路径list

        res_file = os.path.join(r"D:\DataSet\Label\track2_test_labels",video_name, '%s_label.json'%mode)
        with open(res_file, 'r') as f:
            label_res = json.load(f)

        output_file = os.path.join(output_dir, '%s.txt' % video_name)
        # capture = cv2.VideoCapture(video_file)
        if os.path.exists(output_file): #存在
            # print("-1", output_file)
            with open(output_file, 'r') as file:
                # 读取文件内容
                content = file.read()
                # 将内容解析为JSON对象
                data = json.loads(content)
                # 提取res字段
                out_res = data['res']
        else:
            frame_id = 0
            out_res = []
            pred_bbox = [0] # no prection

            for frame_file in frame_files:
                frame_path = os.path.join(video_path, frame_file)
                frame = cv2.imread(frame_path)

                im_vis = frame.copy()
                if len(pred_bbox) == 1:
                    pred_bbox, im_vis = tracker.init(frame, yolo_model)  # initialization
                    out_res.append(pred_bbox)

                    cv2.putText(im_vis, str(frame_id), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    if len(pred_bbox) == 1:
                        cv2.putText(im_vis, 'Fail to detect the UAV', (100, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                    2)
                    else:
                        pred_bbox = list(map(int, pred_bbox))
                        cv2.rectangle(im_vis, (pred_bbox[0], pred_bbox[1]),
                                      (pred_bbox[0] + pred_bbox[2], pred_bbox[1] + pred_bbox[3]), (0, 0, 255), 3)
                else:
                    pred_bbox = tracker.update(frame)  # tracking
                    pred_bbox = list(map(int, pred_bbox))
                    out_res.append(pred_bbox)
                    cv2.rectangle(im_vis, (pred_bbox[0], pred_bbox[1]),
                                  (pred_bbox[0] + pred_bbox[2], pred_bbox[1] + pred_bbox[3]), (0, 0, 255), 3)
                    cv2.putText(im_vis, str(frame_id), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                if visulization:
                    cv2.imshow(video_name, im_vis)
                    cv2.waitKey(1)

                frame_id += 1
            if visulization:
                cv2.destroyAllWindows()
            # save result
            output_file = os.path.join(output_dir, '%s.txt' % video_name)
            with open(output_file, 'w') as f:
                json.dump({'res': out_res}, f)

        mixed_measure = eval(out_res, label_res)
        overall_performance.append(mixed_measure)
        print('[%03d/%03d] %20s %5s Fixed Measure: %.03f' % (video_id, video_num, video_name, mode, mixed_measure))

    print('[Overall] %5s Mixed Measure: %.03f\n' % (mode, np.mean(overall_performance)))


if __name__ == '__main__':
    main(mode='IR', visulization=False)

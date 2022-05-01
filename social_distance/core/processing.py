import math
import os
from typing import Any, Tuple, List, Dict

import cv2 as cv
import numpy as np

NETWORK_NAMES = ['YOLOv4', 'YOLOv4-TINY', 'YOLOv3']
NETWORK_FILENAMES = ['yolov4', 'yolov4-tiny', 'yolov3']

data_prefix = 'data/'

from disjoint_set import DisjointSet


def get_file_path(filename):
    return os.path.join(data_prefix, filename)


def draw_bb(frame: np.ndarray, is_safe: List[bool], boxes: Any) -> None:
    for color_id, box in zip(is_safe, boxes):
        x1, y1, w, h = box
        x2, y2 = x1 + w, y1 + h
        color = safe_flag_to_color(color_id)
        thickness = min(int(frame.shape[0] / 300), 2)
        cv.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        rect_bottom = box_center_bottom(box)
        cv.circle(frame, tuple(rect_bottom), thickness * 3, color, -1)


def box_center_bottom(box):
    x1, y1, w, h = box
    return x1 + w // 2, y1 + h


def safe_flag_to_color(is_safe: bool) -> Tuple[int, int, int]:
    return ((0, 0, 230), (0, 230, 0))[is_safe]


def classify_safe_unsafe(points, radius):
    is_safe = [True] * len(points)
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if j >= i:
                break
            if np.linalg.norm(p1 - p2) < radius:
                is_safe[i] = False
                is_safe[j] = False
                break
    return is_safe


def filter_except_person(class_ids, boxes):
    return [box for class_id, box in zip(class_ids, boxes) if class_id == 0]


def filter_except_in_polygon(boxes, polygon):
    return [bb for bb in boxes if
            cv.pointPolygonTest(contour=polygon, pt=np.asarray(bb_point(bb), np.float32), measureDist=False) >= 0]


def bb_point(box):
    x1, y1, w, h = box
    return x1 + w // 2, y1 + h


def bb_points(boxes):
    return [bb_point(bb) for bb in boxes]


def project_points(image_points, perspective_matrix):
    if not image_points:
        return []
    return cv.perspectiveTransform(np.asarray([image_points], np.float32), perspective_matrix)[0]


def draw_polygon(frame, polygon) -> np.ndarray:
    if polygon is None:
        return
    img_red = np.zeros_like(frame)
    img_red[:, :, -1] = 255
    mask = np.full_like(frame, (1, 1, 1), dtype=np.float32)
    mask = cv.fillPoly(mask, [polygon], (0, 0, 0), lineType=cv.LINE_AA)
    result = cv.add(frame * (1 - mask), img_red * mask).astype(np.uint8)
    alpha = 0.2
    return cv.addWeighted(frame, 1 - alpha, result, alpha, 0)


def calc_statistics(ground_points, safe_distance, is_safe) -> Dict[str, int]:
    violations = 0
    ds = DisjointSet()

    visited = set()
    for i, p1 in enumerate(ground_points):
        for j, p2 in enumerate(ground_points):
            if i == j or (j, i) in visited:
                continue
            visited.add((i, j))
            p1x, p1y = p1
            p2x, p2y = p2
            distance = math.hypot(p1x - p2x, p1y - p2y)
            if distance < safe_distance:
                ds.union(i, j)
                violations += 1

    safe_count = sum(is_safe)
    return {
        'Total': len(ground_points),
        'Safe': safe_count,
        'Unsafe': len(ground_points) - safe_count,
        'Violations': violations,
        'Violation Clusters': len(list(ds.itersets()))
    }

import cv2
import json
import numpy as np
from pathlib import Path

root = Path(__file__).parent
for name, size in [('op-title-white-4k60.mp4', (3840, 2160)), ('op-title-white-1080p60.mp4', (1920, 1080))]:
    cap = cv2.VideoCapture(str(root / name))
    assert cap.isOpened(), name
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    times, corner_values, motion_changes = [], [], []
    previous = None
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        times.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        corner_values.append(frame[0, 0].tolist())
        small = cv2.resize(frame, (480, 270), interpolation=cv2.INTER_AREA)
        if previous is not None and .20 <= i / 60 <= 1.80:
            motion_changes.append(float(np.mean(np.abs(small.astype(np.int16) - previous.astype(np.int16)))))
        previous = small
        if i == 144 and width == 3840:
            cv2.imencode('.png', frame)[1].tofile(str(root / 'assets' / 'frame-final-4k.png'))
        i += 1
    cap.release()
    gaps = np.diff(times)
    assert (width, height) == size
    assert fps == 60 and i == 312
    assert np.max(np.abs(gaps - 1000 / 60)) < .05, gaps.tolist()
    # The source is #FFFFFF; allow up to three RGB levels from lossy H.264 quantization.
    assert all(min(c) >= 252 for c in corner_values), corner_values[0]
    assert min(motion_changes) > 0, 'Unexpected repeated frame during entrance'
    print(json.dumps({'file': name, 'size': [width, height], 'fps': fps, 'decoded_frames': i, 'max_gap_ms': float(max(gaps)), 'background_corner_rgb': corner_values[0][::-1], 'min_motion_change': min(motion_changes)}, ensure_ascii=False))

from pathlib import Path
import cv2
root = Path(__file__).parent
for p in root.glob('*.mp4'):
    cap = cv2.VideoCapture(str(p))
    assert cap.isOpened(), p.name
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    times = []
    while True:
        ok, frame = cap.read()
        if not ok: break
        times.append(cap.get(cv2.CAP_PROP_POS_MSEC))
    cap.release()
    gap = max(abs((b-a)-1000/60) for a,b in zip(times,times[1:]))
    assert len(times) == 228 and abs(fps-60) < .001 and gap < .05, (p.name,len(times),fps,gap)
    print(p.name, size, len(times), 'frames; uniform 60 fps')

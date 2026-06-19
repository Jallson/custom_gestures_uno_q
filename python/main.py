from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection

from datetime import datetime, UTC
import time

# ============================================================
# UI + DETECTION
# ============================================================

ui = WebUI()

detection_stream = VideoObjectDetection(
    confidence=0.6,
    debounce_sec=0.0
)

# ============================================================
# SERVO CONFIGURATION
# ============================================================

# PAN SERVO
PAN_MIN = 10
PAN_MAX = 170

# TILT SERVO
TILT_MIN = 90
TILT_MAX = 160

# CLAW SERVO
CLAW_OPEN = 40
CLAW_CLOSE = 100

# ============================================================
# INITIAL SERVO POSITIONS
# ============================================================

last_pan = 90
last_tilt = 120
last_claw = CLAW_OPEN

# ============================================================
# SMOOTHING
# ============================================================

SMOOTHING = 0.65

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clamp(val, min_val, max_val):
    return max(min_val, min(max_val, val))


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / \
           (in_max - in_min) + out_min


def smooth(current, target):
    return current + (target - current) * SMOOTHING

# ============================================================
# MAIN DETECTION CALLBACK
# ============================================================

def process_detections(detections):

    global last_pan
    global last_tilt
    global last_claw

    best_obj = None
    best_area = 0

    # ========================================================
    # FIND LARGEST DETECTED OBJECT
    # ========================================================

    for label in ["neut", "open", "close"]:

        if label not in detections:
            continue

        objs = detections[label]

        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:

            if "bounding_box_xyxy" not in obj:
                continue

            x1, y1, x2, y2 = obj["bounding_box_xyxy"]

            width = x2 - x1
            height = y2 - y1

            area = width * height

            if area > best_area:

                best_area = area

                best_obj = {
                    "label": label,
                    "bbox": (x1, y1, x2, y2),
                    "area": area
                }

    # ========================================================
    # NO DETECTION
    # ========================================================

    if best_obj is None:
        return

    label = best_obj["label"]

    x1, y1, x2, y2 = best_obj["bbox"]

    # ========================================================
    # TRACKING ONLY WHEN "neut" DETECTED
    # ========================================================

    if label == "neut":

        # ====================================================
        # PAN CONTROL
        # ====================================================

        center_x = (x1 + x2) / 2

        target_pan = map_range(
            center_x,
            80,
            560,
            PAN_MIN,
            PAN_MAX
        )

        target_pan = clamp(
            target_pan,
            PAN_MIN,
            PAN_MAX
        )

        # ====================================================
        # TILT CONTROL USING BBOX AREA
        # ====================================================

        width = x2 - x1
        height = y2 - y1

        area = width * height

        target_tilt = map_range(
            area,
            8500,
            49000,
            TILT_MIN,
            TILT_MAX
        )

        target_tilt = clamp(
            target_tilt,
            TILT_MIN,
            TILT_MAX
        )

        # ====================================================
        # SMOOTH MOVEMENT
        # ====================================================

        last_pan = smooth(
            last_pan,
            target_pan
        )

        last_tilt = smooth(
            last_tilt,
            target_tilt
        )

        # ====================================================
        # DEBUG
        # ====================================================

        print(
            f"TRACKING | "
            f"X={center_x:.1f} "
            f"AREA={area} "
            f"PAN={int(last_pan)} "
            f"TILT={int(last_tilt)}"
        )

    # ========================================================
    # CLAW CONTROL
    # ========================================================

    if label == "open":

        last_claw = smooth(
            last_claw,
            CLAW_OPEN
        )

        print("CLAW OPEN")

    elif label == "close":

        last_claw = smooth(
            last_claw,
            CLAW_CLOSE
        )

        print("CLAW CLOSE")

    # ========================================================
    # FINAL INTEGER VALUES
    # ========================================================

    pan = int(last_pan)
    tilt = int(last_tilt)
    claw = int(last_claw)

    # ========================================================
    # SEND TO ARDUINO
    # ========================================================

    Bridge.call(
        "set_arm",
        pan,
        tilt,
        claw
    )

    # ========================================================
    # SEND TO WEB UI
    # ========================================================

    entry = {
        "gesture": label,
        "timestamp": datetime.now(UTC).isoformat()
    }

    ui.send_message(
        "detection",
        message=entry
    )

    # ========================================================
    # SMALL DELAY FOR STABILITY
    # ========================================================

    time.sleep(0.005)

# ============================================================
# REGISTER CALLBACK
# ============================================================

detection_stream.on_detect_all(
    process_detections
)

# ============================================================
# START APP
# ============================================================

App.run()
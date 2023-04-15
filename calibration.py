#!/usr/bin/env python

import argparse
import numpy as np
import cv2
import sys


def detect_charuco_board(img, board, dictionary, draw_axis=True):
    
    square_corners, ids, _, _ = board.charuco_detector.detectBoard(img)
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame
import sys
import os

pygame.init()

class ScoobaDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
        self.detector = vision.HandLandmarker.create_from_options(options)

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Scooba - Detector de Gatos")

        self.video_path = "scooba_video.mp4"
        self.video_cap = cv2.VideoCapture(self.video_path)
        self.video_frames = []
        self.load_video()

        self.video_index = 0
        self.video_speed = 1
        self.video_counter = 0
        self.showing_video = False
        self.video_timer = 0
        self.video_duration = 10

        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def load_video(self):
        if os.path.exists(self.video_path):
            ret, frame = self.video_cap.read()
            while ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
                self.video_frames.append(surface)
                ret, frame = self.video_cap.read()
            self.video_cap.release()
            self.video_cap = cv2.VideoCapture(self.video_path)
            print(f"Loaded {len(self.video_frames)} frames from video")
        else:
            print("Video not found!")

    def is_scooba_gesture(self, hand_landmarks):
        thumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]
        
        dx = thumb_tip.x - index_tip.x
        dy = thumb_tip.y - index_tip.y
        distance = (dx**2 + dy**2)**0.5

        extended = []
        for i in [8, 12, 16, 20]:
            extended.append(hand_landmarks[i].y < hand_landmarks[i-2].y)

        if distance < 0.08 and sum(extended) >= 2:
            return True
        return False

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    self.video_cap.release()
                    pygame.quit()
                    sys.exit()

            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            results = self.detector.detect(mp_image)

            scooba_detected = False

            if results and results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    if self.is_scooba_gesture(hand_landmarks):
                        scooba_detected = True

            if scooba_detected:
                self.showing_video = True
                self.video_timer = self.video_duration
            elif self.video_timer > 0:
                self.video_timer -= 1
            else:
                self.showing_video = False

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            frame_surface = pygame.transform.rotate(frame_surface, 90)
            frame_surface = pygame.transform.flip(frame_surface, False, True)

            self.screen.fill((0, 0, 0))
            self.screen.blit(frame_surface, (0, 0))

            if self.showing_video and self.video_frames:
                self.video_counter += 1
                if self.video_counter >= self.video_speed:
                    self.video_counter = 0
                    self.video_index = (self.video_index + 1) % len(self.video_frames)

                video_frame = self.video_frames[self.video_index]
                video_scaled = pygame.transform.scale(video_frame, (300, 300))
                self.screen.blit(video_scaled, (80, 20))

            pygame.display.flip()
            self.clock.tick(30)

        cap.release()
        self.video_cap.release()
        pygame.quit()

if __name__ == "__main__":
    app = ScoobaDetector()
    app.run()
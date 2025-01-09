import pygame

pygame.mixer.init()

AUDIO_DIR = "audio"

sounds = {
    "flap": pygame.mixer.Sound(f"{AUDIO_DIR}/wing.wav"),
    "die": pygame.mixer.Sound(f"{AUDIO_DIR}/hit.wav")
}

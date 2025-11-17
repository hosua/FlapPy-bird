import pygame

pygame.mixer.init()

AUDIO_DIR = "audio"

sounds = {
    "flap": pygame.mixer.Sound(f"{AUDIO_DIR}/wing.ogg"),
    "die": pygame.mixer.Sound(f"{AUDIO_DIR}/hit.ogg")
}

for k, v in sounds.items():
    v.set_volume(.25)

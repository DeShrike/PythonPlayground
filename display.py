#!/usr/bin/python

import os
import pygame
import time

def FindImageFilename():
  for filename in os.listdir("."):
    if filename.lower().endswith(".bmp") : return filename
    if filename.lower().endswith(".gif") : return filename
    if filename.lower().endswith(".jpg") : return filename
    if filename.lower().endswith(".png") : return filename
  return ""

def FindDisplayDriver():
  for driver in ["fbcon", "directfb", "svgalib"]:
    if not os.getenv("SDL_VIDEODRIVER"):
      os.putenv("SDL_VIDEODRIVER", driver)
    try:
      pygame.display.init()
      print(driver)
      return True
    except pygame.error:
      pass
  return False

def Main():
  filename = FindImageFilename()
  if filename == "":
    print("No image file found")
  else:
    pygame.init()
    if not FindDisplayDriver():
      print("Failed to initialise display driver")
    else:
      width  = pygame.display.Info().current_w
      height = pygame.display.Info().current_h
      screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
      pygame.mouse.set_visible(False)
      image = pygame.image.load(filename)
      if True: # Stretch image to fit screen
        image = pygame.transform.smoothscale(image, (width,height))
      screen.blit(image,(0,0))
      pygame.display.update()
      time.sleep(10)
    pygame.quit()

if __name__ == "__main__":
  Main()

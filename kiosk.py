# kiosk.py
#
# wjt
# 3-5 mar 2007
#
# http://digitalhistoryhacks.blogspot.com
#
# based on ideas and code in
#
# http://technobabbler.com/?p=22
# http://gumuz.looze.net/wordpress/index.php/archives/2005/06/06/python-webcam-fun-motion-detection/

from VideoCapture import Device
from PIL import Image
import sys, time, pygame
import ImageGrab
from pygame.locals import *

# camera resolution
camera_width = 640
camera_height = 480
camera_resolution = (camera_width,camera_height)

# screen resolution
screen_width = 1120
screen_height = 480
screen_resolution = (screen_width,screen_height)

# offset camera image within screen image
camera_offset = (480,0)

# frames in interface
frame_color = (141,112,52)

# preview window
preview_width = 478
preview_height = 478
preview_dimensions = (preview_width,preview_height)

# for demo purposes, set motion capture region to second photo from left
# (relative to camera image)
detector_left = 132
detector_upper = 2
detector_right = 252
detector_lower = 122

# detect change of at least pix_threshold in img_threshold percent of pixels
def diff_image(img1, img2, pix_threshold=5, img_threshold=30):
    if not img1 or not img2:
        return False
    img1 = img1.getdata()
    img2 = img2.getdata()
    pixel_count = len(img1)
    pixdiff = 0
    for i in range(pixel_count):
        if abs(sum(img1[i]) - sum(img2[i])) >= pix_threshold:
            pixdiff += 1
    diffperc = pixdiff / (pixel_count/100.0)
    if diffperc > img_threshold:
        # motion detected
        return True

# capture a screen shot
def screen_shot():
    shot = ImageGrab.grab()
    filename = str(time.time()) + ".jpg"
    shot.save(filename)

# resize a photo so longest dimension equals max
def resize_photo(p, photo_maxdim=120):
    (w, h) = p.size
    if w > h: p = p.resize((photo_maxdim,int(round((h * photo_maxdim) / w))))
    else: p = p.resize((int(round((w * photo_maxdim) / h)),photo_maxdim))        
    return p

# photo windows (demo)
photo_width = 120
photo_height = 120
photo_locations = [486, 612, 738, 864, 990]
photo0 = resize_photo(Image.open('mccord/1895-025-199.jpg'))
photo1 = resize_photo(Image.open('mccord/1910-025-1030.jpg'))
photo2 = resize_photo(Image.open('mccord/1915-025-1087.jpg'))
photo3 = resize_photo(Image.open('mccord/1920-025-1041.jpg'))
photo4 = resize_photo(Image.open('mccord/1931-025-203.jpg'))

# preview has two states: JPEG image and solid rectangle (demo)
preview_images = (resize_photo(Image.open('mccord/1910-025-1030.jpg'), 478),
                  Image.new("RGB", (478,478), (0,0,0)))
        
# switch between preview ON and OFF
toggle = 1

# 0 = transparent, 255 = opaque
photo_transparency = 200

# initialization
pygame.init()
cam = Device()
cam.setResolution(camera_width,camera_height)
screen = pygame.display.set_mode(screen_resolution)
pygame.display.set_caption('Kiosk in a Cabinet')
pygame.mouse.set_visible(0)

while 1:

    # grab two images and clip button region to do motion detection
    img1 = cam.getImage()
    detect1 = img1.crop((detector_left,detector_upper,detector_right,detector_lower))
    img2 = cam.getImage()
    detect2 = img2.crop((detector_left,detector_upper,detector_right,detector_lower))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    keyinput = pygame.key.get_pressed()
    if keyinput[K_s]: screen_shot()

    # compose images on a temporary surface s
    s = pygame.Surface(screen.get_size())
    s = s.convert()
    
    # render webcam image
    img = cam.getImage()
    camera_surface = pygame.image.frombuffer(img.tostring(), camera_resolution, "RGB")
    s.blit(camera_surface, camera_offset)
    
    # render interface frames
    pygame.draw.rect(s, frame_color, [2,2,preview_width,preview_height], 1)
    for i in photo_locations:
        pygame.draw.rect(s, frame_color, [i,2,photo_width,photo_height], 1)

    # render demo photos (for actual application, replace this with image flow)
    photo_surface0 = pygame.image.frombuffer(photo0.tostring(), photo0.size, "RGB")
    photo_surface0.set_alpha(photo_transparency)
    s.blit(photo_surface0, [photo_locations[0],2])
    photo_surface1 = pygame.image.frombuffer(photo1.tostring(), photo1.size, "RGB")
    photo_surface1.set_alpha(photo_transparency)
    s.blit(photo_surface1, [photo_locations[1],2])
    photo_surface2 = pygame.image.frombuffer(photo2.tostring(), photo2.size, "RGB")
    photo_surface2.set_alpha(photo_transparency)
    s.blit(photo_surface2, [photo_locations[2],2])
    photo_surface3 = pygame.image.frombuffer(photo3.tostring(), photo3.size, "RGB")
    photo_surface3.set_alpha(photo_transparency)
    s.blit(photo_surface3, [photo_locations[3],2])
    photo_surface4 = pygame.image.frombuffer(photo4.tostring(), photo4.size, "RGB")
    photo_surface4.set_alpha(photo_transparency)
    s.blit(photo_surface4, [photo_locations[4],2])
            
    # has photo been chosen?
    if diff_image(detect1, detect2):
        toggle = 1 - toggle

    # render preview
    preview_surface = pygame.image.frombuffer(preview_images[toggle].tostring(), preview_images[toggle].size, "RGB")
    s.blit(preview_surface, [2,2])
            
    # render temporary surface on the screen
    screen.blit(s, (0, 0))
    
    # finally make the buffer visible
    pygame.display.flip()



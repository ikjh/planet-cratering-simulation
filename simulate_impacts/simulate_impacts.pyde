import math
import os
    #TODO
    #data graphs
    #commenting / documentation
    #changing one variable
    
#erase according to overlap rule, stop simulation according to underlap rule

# PROGRAM VARS #
crater_info         = []
all_craters         = []
images              = []
idx                 = 0
years               = 0
visible_craters     = 0
underlap_streak     = 0
outfile             = None
resets              = 0
img_idx             = 1

# CONSTANTS #
RESULTSFILE_PATH    = "..%sanalyze%sresults.txt" % (os.path.sep, os.path.sep)
DATAFILE_PATH       = "..%sdata%sdata.txt" % (os.path.sep, os.path.sep)
IMAGE_PATH          = "..%simg%ssim" % (os.path.sep, os.path.sep)
IMAGE_COUNT         = 4
SIDE_LENGTH         = 500 # (km)
STOP_THRESHOLD      = 2000 #
BASE_THRESHOLD      = STOP_THRESHOLD
FRAMERATE           = 100
COLOR_BG            = 51

#this function is run one time, to set up the display parameters and gather the data.
def setup():
    global outfile, FRAMERATE, COLOR_BG, SIDE_LENGTH, RESULTSFILE_PATH, DATAFILE_PATH 
    
    #set background attrs
    size(SIDE_LENGTH,SIDE_LENGTH)
    background(COLOR_BG)
    frameRate(FRAMERATE)
    
    #get impact sizes (diameter, km) from data.txt
    crater_sizes = []
    with open(DATAFILE_PATH, 'r') as datafile:
        for entry in datafile:
            crater_sizes.append(int(entry.strip()))
            
    #open the output file for simulation data collection
    outfile = open(RESULTSFILE_PATH, 'w+')
    outfile.write("visible_craters,time\n")
    
    #create crater info from given sizes, and generate random locations (x,y) within the square for each crater
    for i in range(len(crater_sizes)):
        crater = {}
        crater["ID"] = i
        crater["Location"] = (int(random(0, SIDE_LENGTH - 1)), int(random(0, SIDE_LENGTH - 1)))
        crater["Diameter"] = crater_sizes[i]
        crater["Radius"] = crater["Diameter"] / 2.0
        crater["Area"] = math.pi * (crater["Radius"] ** 2)
        crater_info.append(crater)
    print(crater_info)

#run this procedure repeatedly until told to stop (noLoop())
def draw():
    global idx, years, all_craters, visible_craters, underlap_streak, outfile, BASE_THRESHOLD, STOP_THRESHOLD, resets, img_idx, IMAGE_COUNT

    new_crater = crater_info[idx]
    crater_radius = new_crater["Radius"]
    crater_area = new_crater["Area"]
    crater_X = new_crater["Location"][0]
    crater_Y = new_crater["Location"][1]
    overlap = False
    underlap = False
    
    #impact the surface with a crater
    ellipse(crater_X, crater_Y, crater_radius, crater_radius)
    visible_craters += 1
    
    #If the new impact covers the center of an older, smaller crater, remove the covered 
    #crater from the array
    if all_craters:
        for old_crater in all_craters:
            if isOverlapped(old_crater, new_crater):
                visible_craters -= 1
                overlap = True
                all_craters.remove({"Radius": old_crater["Radius"], "Area" : old_crater["Area"], "Location" : (old_crater["Location"][0], old_crater["Location"][1])})
            if isUnderlapped(old_crater, new_crater):
                underlap = True
        
    all_craters.append({"Radius": crater_radius, "Area" : crater_area, "Location" : (crater_X, crater_Y)})
    #print("visible craters: %d\nlist size: %d\n" % (visible_craters, len(all_craters)))
          
    #redraw surviving craters
    for survivor in all_craters:
        ellipse(survivor["Location"][0], survivor["Location"][1], survivor["Radius"], survivor["Radius"])

    #count of consecutive impact underlaps determines how far along the simulation is; underlap_streak resets to zero if the new crater touches no other craters on impact
    #underlap_streak = underlap_streak + 1 if underlap else 0
    
    if underlap:
        underlap_streak += 1
    else:
        if underlap_streak >= STOP_THRESHOLD / 2:
            STOP_THRESHOLD /= 2
        underlap_streak = 0
        resets += 1
    
    print("\nunderlap streak: %d\nresets: %d\nthreshold: %d\nvisible craters: %d\nyears: %d\nidx: %d" % (underlap_streak, resets, STOP_THRESHOLD, visible_craters, years, idx))
    outfile.write("%d,%d\n" % (visible_craters, years))
    
    #take a picture every 100 craters
    if idx % 100 == 0:
        image_name = "%s_%d.png" % (IMAGE_PATH, img_idx)
        save(image_name)
        images.append(image_name)
        img_idx += 1
    
    #simulation stop condition, 2000 continuous underlaps
    if underlap_streak >= STOP_THRESHOLD:
        #save final image
        image_name = "%s_%d.png" % (IMAGE_PATH, img_idx)
        save(image_name)
        images.append(image_name)
        
        #calculate which images to keep
        bin = len(images)
        bin_diff = bin % IMAGE_COUNT
        cut_bin = bin - bin_diff
        inc = cut_bin / IMAGE_COUNT
        token = bin
        
        save_imgs = [bin - inc*i for i in range(0, IMAGE_COUNT)]
        print(save_imgs)
        
        for img in images:
            img_num = img.split('_')[1]
            img_num = int(img_num.split('.png')[0])
            if img_num not in save_imgs:
                os.remove(img)
        
        outfile.close()
        noLoop()

    idx += 1
    years = idx * 1000

#overlap method: detects which craters should be deleted. Overlaps occur when the center of a small crater is within a larger, newer crater
def isOverlapped(old_crater, new_crater):
    return new_crater["Radius"] > old_crater["Radius"] and dist(old_crater["Location"][0], old_crater["Location"][1], new_crater["Location"][0], new_crater["Location"][1]) <= new_crater["Radius"]

#underlap method: detects if old_crater is underlapped (covered) in any way by new_crater. A slightly different calculation where if the distance between the craters' centers minus the the radius of the 
#old crater is less than the radius of the new crater, an old crater underlaps the new crater.
def isUnderlapped(old_crater, new_crater):
    return dist(old_crater["Location"][0], old_crater["Location"][1], new_crater["Location"][0], new_crater["Location"][1]) - old_crater["Radius"] < new_crater["Radius"]

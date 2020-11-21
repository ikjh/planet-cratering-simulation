import math

crater_info = []
all_craters = []
idx = 0
years = 0
visible_craters = 0
covered_area = 0
total_area = 250000 # 500x500 km
overlap_streak = 0
overlap = False

#this function is run one time, to set up the display parameters and gather the data.
def setup():
    #set background attrs
    size(500,500)
    background(51)
    frameRate(30)
    
    #get impact sizes (diameter, km) from data.txt
    crater_sizes = []
    with open("data.txt") as datafile:
        for entry in datafile:
            crater_sizes.append(int(entry.strip()))
    
    #create crater info from given sizes, and generate random locations (x,y) within the square for each crater
    for i in range(len(crater_sizes)):
        crater = {}
        crater["ID"] = i
        crater["Location"] = (int(random(0,499)), int(random(0,499)))
        crater["Diameter"] = crater_sizes[i]
        crater["Radius"] = crater["Diameter"] / 2.0
        crater["Area"] = math.pi * (crater["Radius"] ** 2)
        crater_info.append(crater)
    print(crater_info)

#run this procedure repeatedly until told to stop (noLoop())
def draw():
    global idx, years, all_craters, visible_craters, covered_area, total_area, overlap, overlap_streak

    new_crater = crater_info[idx]
    crater_radius = new_crater["Radius"]
    crater_area = new_crater["Area"]
    crater_X = new_crater["Location"][0]
    crater_Y = new_crater["Location"][1]
    
    #impact the surface with a crater
    ellipse(crater_X, crater_Y, crater_radius, crater_radius)
    visible_craters += 1
    covered_area += crater_area
    
    #If the new impact covers the center of an older, smaller crater, remove the covered 
    #crater from the array
    if all_craters:
        for old_crater in all_craters:
            if crater_radius > old_crater["Radius"]:
                if isOverlapped(old_crater, new_crater):
                    visible_craters -= 1
                    covered_area -= old_crater["Area"]
                    overlap = True
                    all_craters.remove({"Radius": old_crater["Radius"], "Area" : old_crater["Area"], "Location" : (old_crater["Location"][0], old_crater["Location"][1])})
                    #print("***OVERLAP***")
    all_craters.append({"Radius": crater_radius, "Area" : crater_area, "Location" : (crater_X, crater_Y)})
    #print("covered area: %d\nvisible craters: %d\nlist size: %d\n" % (covered_area, visible_craters, len(all_craters)))
          
    #redraw surviving craters
    for survivor in all_craters:
        ellipse(survivor["Location"][0], survivor["Location"][1], survivor["Radius"], survivor["Radius"])
    if overlap:
        overlap_streak += 1
    else:
        overlap_streak = 0
    if overlap_streak > 30:
        noLoop()
    print(overlap_streak)
    overlap = False
    #print("frame: %d" % idx)
    idx += 1
    years += 10000
    #TODO
    #how to make crater size distribution
    #store each crater into a list
    #delete craters with overlapped 
    
    
def isOverlapped(old_crater, new_crater):
    return dist(old_crater["Location"][0], old_crater["Location"][1], new_crater["Location"][0], new_crater["Location"][1]) < new_crater["Radius"]

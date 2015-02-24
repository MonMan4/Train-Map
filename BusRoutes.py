import json
import urllib2
import pygame, sys
pygame.init()
screen = pygame.display.set_mode([640,480])
white = [255, 255, 255]
def get_data(api):
    get = urllib2.urlopen(api).read()
    data = json.loads(get)

    return data

def find_bus(bus_name, data):
  for bus_id, bus_info in data.iteritems():
    if bus_info['routeTag'] == bus_name:
      return bus_info


def get_map(latitude, longitude):
  size = '640x640'
  zoom = '16'
  url = "http://maps.google.com/maps/api/staticmap?size=%s&maptype=roadmap&markers=size:mid|color:red|%s,%s&sensor=false&zoom=%s"

  return url % (size, latitude, longitude, zoom)

def find_address(address):
    data = get_data("https://maps.googleapis.com/maps/api/geocode/json?address="+ address)
    return data['results'][0]['geometry']['location']



def updateMap():
    api = "https://publicdata-transit.firebaseio.com/sf-muni/vehicles.json"
    data = get_data(api)

    # for routes that are just numbers the input parameter 
    # should be int instead of string
    number = 'N'
    location = find_bus(number, data)

    latitude = location['lat']
    longitude = location['lon']

    map_url = get_map(latitude, longitude)
    map_image = urllib2.urlopen(map_url).read()
    output = open("file01.png","wb")
    output.write(map_image)
    output.close()
    #load in pygame
    my_ball = pygame.image.load("file01.png")
    screen.blit(my_ball, [0, 0])
    pygame.display.update()
#innout
address = "333+Jefferson+Street+San+Francisco+CA"
location = find_address(address)
latitude = location['lat']
longitude = location['lng']
map_url2 = get_map(latitude, longitude)

running = True

updateMap()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(5000) #pause for 5000 milliseconds
#update the entire display
    updateMap()
pygame.quit()





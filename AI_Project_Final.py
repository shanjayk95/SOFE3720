import requests
import json
import http.client, urllib.parse
from queue import PriorityQueue
import sys
import webbrowser

def get_time_matrix(lng,lat):
    coordinate=[]
    for i in range(len(lng)):
        coordinate.append([lng[i],lat[i]]) #make coordinate list [longitude, latitude]

    body = {"locations":coordinate} #Api body

    #Api header
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248ba591b5a9d6841fa8fac6503147cf58c',
        'Content-Type': 'application/json; charset=utf-8'
    }
    # Call Api
    call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
    #return duration matrix
    return call.json()['durations']

def get_shortest_path(path, address_array):  # A* alg goes here and should use lat and long array elements to do calculations
    goal = len(address_array)-1
    global Queue #make global Queue 
    for i in range(len(Time_matrix)):
        tempPath=path.copy()
        if i not in path:
            tempPath.append(i)
            Queue.put((Time_matrix[path[-1]][i],0,tempPath)) #add nodes in priority queue in terms of time

    # get_shortest_path(curr,goal,path)
    while(path!=goal and len(path) != len(Time_matrix)): #if we reach goal and visited all addresses in the path it stops
        _,_,path=Queue.get() #uses the high piroty value from queue
        #only stores path since thats what were interested in
        
        get_shortest_path(path,address_array) #calls function again
    else:
        print("\nShortest path using A* Algorithm:")
        url = 'https://www.google.com/maps/dir/'
        for p in path:
            print(p+1, end=': ')
            print(address_array[p])
            split = address_array[p].split()
            for z in range(len(split)):
                url = url + split[z]
                url = url + '+'
            url = url + '/'
        print('\nOpening route on Google Maps...')
        webbrowser.open(url)
        sys.exit(0)

def get_coordinates(address):  # gets latitude & longitude of the given address via an api call
    conn = http.client.HTTPConnection('geocode.xyz')

    params = urllib.parse.urlencode({
        'auth': '536361396685382879794x51993',
        'locate': address,
        'region': 'CA',
        'json': 1,
    })

    conn.request('GET', '/?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    output = json.loads(data)
    lati = output['latt']
    longi = output['longt']

    address_array.append(address)
    latitude_array.append(lati)
    longitude_array.append(longi)


address_array = []
latitude_array = []
longitude_array = []

num = int(input("How many stops will you be making between your start and end destination?: "))
num = num + 2
for x in range(num):
    if x == 0:
        address = str(input("Please enter your start address: "))
    elif x == (num - 1):
        address = str(input("Please enter your end address: "))
    else:
        address = str(input("Please enter any stop address: "))
    get_coordinates(address)

for x in range(num):  # Check to see if values were properly stored in their arrays
    print("Address: ", address_array[x])
    print("Latitude: ", latitude_array[x])
    print("Longitude: ", longitude_array[x])


Time_matrix=get_time_matrix(longitude_array,latitude_array) #Get time matrix from each location

print('\nTime Matrix')
#print Time Matrix
for tm in Time_matrix:
    print(tm)

Queue=PriorityQueue() #use piriority queue for solving A*
Path = [0]
get_shortest_path(Path, address_array) # function to find shortest distance


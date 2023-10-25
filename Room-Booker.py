import sys, os
#import config
import discord
import requests
import json
import numbers
from datetime import datetime, timedelta

#GetEvents() is important

eid_arr = {
    "101A" : 43398,
    "101B" : 54868,
    "101C" : 54869,
    "108A" : 55287,
    "108B" : 55289,
    "112A" : 55292
}

booking_count = 1

times ={}

session = requests.Session()

def book_room(room, startTime, name):
    global booking_count
    #add room here
    eid = -1

    if isinstance(room, numbers.Number):
        eid = room
    else:
        eid = eid_arr.get(room)

    if not (eid in eid_arr.values()):
        return "An invalid room was given"

    print(times)

    if times[eid].get(startTime) == None:
        return "an invalid start time was given"

    url = "https://oberlin.libcal.com/spaces/availability/booking/add"
    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://oberlin.libcal.com",
    "Referer": "https://oberlin.libcal.com/reserve/mudd-main-level-study-rooms",
    "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
    }
    data = {
        "add[eid]": str(eid),
        "add[gid]": "11326",
        "add[lid]": "6052",
        "add[start]": startTime,
        "add[checksum]": times.get(eid).get(startTime).get("checksum"),
        "lid": "6052",
        "gid": "11326",
        "start": startTime[:10],
        "end": (datetime.strptime(startTime[:10], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    }

    response = session.post(url, headers=headers, data=data)
    print("Add returned a", response.status_code)
    checksum = ""

    #gets the checksum if the add is a sucess
    if response.text == "{\"error\":\"Sorry, the selected times have become unavailable.\",\"isRefreshRequired\":true}":
        print("the selected booking is unavaliable")
    else:
        response_json = response.json()
        bookings = response_json.get('bookings')
        checksum = bookings[0]['checksum']
        print(bookings)
        print("checksum:", checksum)
        #print("The text was", response.text)

        #book room here
        url = "https://oberlin.libcal.com/ajax/space/book"
        headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://oberlin.libcal.com",
        "Referer": "https://oberlin.libcal.com/reserve/mudd-main-level-study-rooms",
        "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
        }
        print("startTime: " + startTime)
        print ("end " +  (datetime.strptime(startTime[-8:], "%H:%M:%S") + timedelta(hours=1)).strftime("%H:%M"))
        data = {
        "session": "36627955",
        "fname": name,
        "lname": "(booked using obiesourcebot)",
        "email": str(booking_count) + "@oberlin.edu",
        "q6507": "Study",
        "q8617": "",
        "bookings": json.dumps([{
            "id": 1,
            "eid": eid,
            "seat_id": 0,
            "gid": 11326,
            "lid": 6052,
            "start": startTime,
            "end": startTime[:11] + (datetime.strptime(startTime[-8:], "%H:%M:%S") + timedelta(hours=1)).strftime("%H:%M"),
            "checksum": checksum
        }]),
        "returnUrl": "/reserve/mudd-main-level-study-rooms",
        "pickupHolds": "",
        "method": "11"
        }

        #print(json.dumps(data))
        response = session.post(url, headers=headers, data=data)

        if response.status_code == 200:
            booking_count += 1


        print(response.status_code)
        print(response.text)
        print(startTime[:11])


def get_rooms(date):
    
    url = "https://oberlin.libcal.com/spaces/availability/grid"

    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://oberlin.libcal.com",
    "Referer": "https://oberlin.libcal.com/reserve/mudd-main-level-study-rooms",
    "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
    }
    print((datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))
    data = {
        "lid": 6052,
        "gid": 11326,
        "eid": -1,
        "seat": 0,
        "seatId": 0,
        "zone": 0,
        "start": date,
        "end": (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
        "pageIndex": 0,
        "pageSize": 18
    }

    response = session.post(url, headers=headers, data=data)
    response_json = response.json()

    #print(response.text)
    for i in response_json.get("slots"):
        if times.get(i.get("itemId")) == None:
            times.update({i.get("itemId"): {i.get("start"): i}})
        else:
            times.get(i.get("itemId")).update({i.get("start"): i})
    
    #print(times.get(43398))


#MUDD_url_req = requests.get('https://oberlin.libcal.com/reserve/mudd-main-level-study-rooms')
#MUDD_soup = BeautifulSoup(MUDD_url_req.text, 'html.parser')

#print(MUDD_soup.title.text)

#book_room()
get_rooms("2023-10-25")
print(book_room("101B", "2023-10-25 22:00:00", "test"))

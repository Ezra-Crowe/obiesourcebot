import sys, os
#import config
import discord
import requests
import json
import numbers
from datetime import datetime, timedelta


eid_arr = {
    "101A" : 43398,
    "101B" : 54868,
    "101C" : 54869,
    "108A" : 55287,
    "108B" : 55289,
    "112A" : 55292
}

booking_count = 2

times ={}

session = requests.Session()

def book_room(room, startTime, endTime, name):
    global booking_count

    #add room here
    eid = -1

    #Transfers any room numbers given to their corresponding eid
    if isinstance(room, numbers.Number):
        eid = room
    else:
        eid = eid_arr.get(room)

    if not (eid in eid_arr.values()):
        return "An invalid room was given"
    
    if times.get(eid) == None:
        return "get_rooms was not called or failed to generate rooms"

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
        "end": (datetime.strptime(startTime[:10], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d") #Turns the start time to a Date object, adds a day to it, then turns it back into a string
    }

    response = session.post(url, headers=headers, data=data)
    response_json = ""
    try:
        response_json = response.json()
    except:
        return "There was an error adding the selected room\nAdd says " + response.text
    print("Add returned a", response.status_code)

    if response_json.get("error") == "Sorry, the selected times have become unavailable.":
        return "The selected booking is already taken :("

    #updates the booking to be of the requested time
    updateChecksum = ""
    if response_json.get("bookings") != None:
        j = 0
        #Loops through the other time options and finds the end time requested
        for i in response_json.get("bookings")[0].get("options"): #We have to say bookings[0] becuase add always returns an array of bookings despite not being able to make more than 1 booking at a time
            if datetime.strptime(i, "%Y-%m-%d %H:%M:%S") == datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S"):
                updateChecksum = response_json.get("bookings")[0].get("optionChecksums")[j]  
            j += 1
    else:
        return "There was an issue adding your booking"

    if updateChecksum == "":
        return "The requested end time is not valid"

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
        "update[id]": response_json.get("bookings")[0].get("id"),
        "update[checksum]": updateChecksum,
        "update[end]": endTime,
        "add[eid]": str(eid),
        "add[gid]": "11326",
        "add[lid]": "6052",
        "add[start]": startTime,
        "add[checksum]": times.get(eid).get(startTime).get("checksum"),
        "lid": "6052",
        "gid": "11326",
        "start": startTime[:10],
        "end": (datetime.strptime(startTime[:10], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d") #Turns the start time to a Date object, adds a day to it, then turns it back into a string
    }

    response = session.post(url, headers=headers, data=data)
    try:
        response_json = response.json()
    except:
        return "there was an issue updating the added booking\nUpdate add says " + response.text
    print("Add Update returned a", response.status_code)
    checksum = ""
    end = ""

    #gets the checksum if the add is a sucess
    if response.text == "{\"error\":\"Sorry, the selected times have become unavailable.\",\"isRefreshRequired\":true}":
        return "the selected booking is unavaliable"
    else:
        response_json = response.json()
        bookings = response_json.get('bookings')
        checksum = bookings[0]['checksum']
        end = bookings[0]['end']
        print("checksum:", checksum)

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
            "end": end,
            "checksum": checksum
        }]),
        "returnUrl": "/reserve/mudd-main-level-study-rooms",
        "pickupHolds": "",
        "method": "11"
        }

        response = session.post(url, headers=headers, data=data)

        if response.text == "<p>Mudd 101A: This booking is too close to a previous booking you have made. This category has a limit of 1 hour between bookings.</p>":
            booking_count += 1
            return book_room(room, startTime, endTime, name)

        if response.status_code == 200:
            booking_count += 1
        else:
            return "There was an error booking the room\nThe response says " + response.text


        print("Book returned a " + str(response.status_code))
        return "Your room was booked successfully"

#Get all the avaliable rooms and loads them into a dictionary called times
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

    data = {
        "lid": 6052,
        "gid": 11326,
        "eid": -1,
        "seat": 0,
        "seatId": 0,
        "zone": 0,
        "start": date,
        "end": (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"), #turns the date string into a date object, adds a day then turns the date object back into a string
        "pageIndex": 0,
        "pageSize": 18
    }

    response = session.post(url, headers=headers, data=data)
    response_json = response.json()

    #Adds all the avaliable times to times
    for i in response_json.get("slots"):
        if times.get(i.get("itemId")) == None:
            times.update({i.get("itemId"): {i.get("start"): i}})
        else:
            times.get(i.get("itemId")).update({i.get("start"): i})
    
get_rooms("2023-10-30")
print(book_room("101A", "2023-10-30 09:30:00", "2023-10-30 01:15:00", "Josh Toker"))

#Discord UI sucks so we are gonna prompt the user for when they want to book the room
#The first response should have 3 drop down menus. One for a date, one for a Time and one for how many rooms they want to book. There should also be be 3 buttons that adjust the increments of time in the drop down menu.
#The drop down menu should defualt to hour increments but there should be a 15 minute button and a 30 minute button.
#Once a date and time are selected we should respond to them with 2 drop down menus. The first should be of all the avaliable rooms at their selected time and in parenthesis how long they can be booked for.
#The second should be how long they want to book the selected room for. Finally their should be a sumbit button that finishes the booking.
#Later 
class RoomView(discord.ui.View):
    async def display_times():
        print("Not yet implemented")

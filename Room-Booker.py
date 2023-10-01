import sys, os
#import config
import discord
import requests
import json

def book_room():
    #add room here
    session = requests.Session()

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
        "add[eid]": "54868",
        "add[gid]": "11326",
        "add[lid]": "6052",
        "add[start]": "2023-10-1 10:00",
        "add[checksum]": "bfbafdf865a97d36e4a515b46afcf948",
        "lid": "6052",
        "gid": "11326",
        "start": "2023-10-1" ,
        "end": "2023-10-02"
    }

    response = session.post(url, headers=headers, data=data)
    print("Add returned a", response.status_code)
    #print("The text was", response.text)

    #Add Times here

    url = "https://oberlin.libcal.com/ajax/space/times"
    headers = {
    "Accept": "text/html, */*; q=0.01",
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43",
    "X-Requested-With": "XMLHttpRequest"
}
    data = {
        "patron": "",
        "patronHash": "",
        "bookings[0][id]": "1",
        "bookings[0][eid]": "54868",
        "bookings[0][seat_id]": "0",
        "bookings[0][gid]": "11326",
        "bookings[0][lid]": "6052",
        "bookings[0][start]": "2023-10-01 10:00",
        "bookings[0][end]": "2023-10-01 11:00",
        "bookings[0][checksum]": "b9a259da461232b02f2697852fa714c0"
    }
    #data_str = urllib.parse.urlencode(data)
    #response = session.post(url, headers=headers, data=data)
    print("Times returned a", response.status_code)
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
    
    data = {
    "session": "36627955",
    "fname": "test",
    "lname": "student",
    "email": "ab@oberlin.edu",
    "q6507": "Study",
    "q8617": "",
    "bookings": json.dumps([{
        "id": 1,
        "eid": 43398,
        "seat_id": 0,
        "gid": 11326,
        "lid": 6052,
        "start": "2023-10-01 10:00",
        "end": "2023-10-01 11:00",
        "checksum": "c1e5ab282d6a1c38bed05bc8cbe4958a"
    }]),
    "returnUrl": "/reserve/mudd-main-level-study-rooms",
    "pickupHolds": "",
    "method": "11"
    }

    print(json.dumps(data))
    response = session.post(url, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

book_room()

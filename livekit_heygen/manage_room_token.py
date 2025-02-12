#RKYTAHEMPMDBTGQXZSTARRDF

# import asyncio
#
# import requests
# from livekit.api import LiveKitAPI, CreateRoomRequest, ListRoomsRequest, DeleteRoomRequest
# from livekit import api
# import os


# livekit_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibXkgbmFtZSIsInZpZGVvIjp7InJvb21Kb2luIjp0cnVlLCJyb29tIjoibXktcm9vbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWV9LCJzdWIiOiJpZGVudGl0eSIsImlzcyI6IkFQSWs3Tk1LSnBNUlJjdyIsIm5iZiI6MTczODc0OTAyOCwiZXhwIjoxNzM4NzcwNjI4fQ.y20oKz_RWyqKnzIIs--AK8YUbaqnrUKFD6Tx2gPB2CY'
# base_url = 'https://api.heygen.com/v1'
# HEYGEN_API_KEY = "NDIwN2M1MjQwNTJiNGM0MTgwOGVjOGZlMzY5MzZjZGUtMTczODY3NjgxMw=="
# LIVEKIT_SERVER = 'wss://heygenstream-lnczb0yw.livekit.cloud'
# LIVEKIT_API_KEY = 'APIk7NMKJpMRRcw'
# LIVEKIT_API_SECRET = 'XDj8JHYEA1QBykyoYJQeZvbXNavuU3mennKPRtohk4Z'





#-----------------------------------------------------------------
import asyncio
import json
import re

import aiohttp
import requests
import time
import cv2
import pyvirtualcam
import websockets
from aiortc import RTCConfiguration, RTCIceServer, RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from livekit import api, rtc



token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibXkgbmFtZSIsInZpZGVvIjp7InJvb21Kb2luIjp0cnVlLCJyb29tIjoibXktcm9vbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWV9LCJzdWIiOiJpZGVudGl0eSIsImlzcyI6IkFQSWs3Tk1LSnBNUlJjdyIsIm5iZiI6MTczODc0OTAyOCwiZXhwIjoxNzM4NzcwNjI4fQ.y20oKz_RWyqKnzIIs--AK8YUbaqnrUKFD6Tx2gPB2CY'
LIVEKIT_SERVER_URL = "https://first-pka0inn5.livekit.cloud"
LIVEKIT_SERVER_URL_wss = "wss://first-pka0inn5.livekit.cloud/v1/rtc"
LIVEKIT_API_KEY = 'APIAQgcK5767baz'
LIVEKIT_API_SECRET = 'aJKwEeBszxgezsDTLZlXZ7RhfjNEiWfktdRHTHsgeNMA'
heygen_api_key = 'MDI0YTQ0MjEzOWNkNDEwNzhkNzlmNzE1NzhjOGI5NGQtMTczOTE4OTcxMQ=='

#generate token
def getToken():
  token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET).with_identity("identity").with_name("my name").with_grants(api.VideoGrants(room_join=True, room="my-room"))
  return token.to_jwt()


def create_room(room_name, token):
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibXkgbmFtZSIsInZpZGVvIjp7InJvb21Kb2luIjp0cnVlLCJyb29tIjoibXktcm9vbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWV9LCJzdWIiOiJpZGVudGl0eSIsImlzcyI6IkFQSWs3Tk1LSnBNUlJjdyIsIm5iZiI6MTczODc0OTAyOCwiZXhwIjoxNzM4NzcwNjI4fQ.y20oKz_RWyqKnzIIs--AK8YUbaqnrUKFD6Tx2gPB2CY'
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{LIVEKIT_SERVER_URL}/room", headers=headers, json={"name": room_name})
    print(response.text)
    return response.text


def list_sessions(session_id):
    url = "https://api.heygen.com/v1/streaming.list"
    headers = {
        "accept": "application/json",
        # "x-api-key": "NDIwN2M1MjQwNTJiNGM0MTgwOGVjOGZlMzY5MzZjZGUtMTczODY3NjgxMw=="
        "x-api-key": heygen_api_key
    }

    response = requests.get(url, headers=headers)

    print('this is list sessions function', response.text)
    from_list_data = response.json()

    try:
        for session in from_list_data["data"]["sessions"]:
            if session["session_id"] == session_id:
                return session["status"]
    except (KeyError, ValueError):
        print("Error retrieving session status.")

    return "unknown"


def create_session():
    url = "https://api.heygen.com/v1/streaming.new"

    payload = {
        "quality": "medium",
        "voice": {"rate": 1},
        "video_encoding": "VP8",
        "disable_idle_timeout": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": heygen_api_key
    }

    response = requests.post(url, json=payload, headers=headers)
    print('session created.', response.json())
    data1 = response.json()
    session_id = data1.get("data", {}).get("session_id", {})
    sdp_data = data1.get("data", {}).get("sdp", {}).get("sdp", {})
    sdp_type = data1.get("data", {}).get("sdp", {}).get("type", {})
    sdp_ice_servers2 = data1.get("data", {}).get("ice_servers2", {})
    return session_id, sdp_data, sdp_type, sdp_ice_servers2

def start_session(session_id, sdp_type):
    url = "https://api.heygen.com/v1/streaming.start"
    payload = {
        "session_id": session_id,
        "sdp": {
            "type": sdp_type,
            # "sdp": sdp_data
        }
    }

    header = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": heygen_api_key
    }
    wait_for_session = wait_for_session_ready(session_id)
    if wait_for_session:
        response = requests.post(url, json=payload, headers=header)
        print(f"Start session response: {response.text}")
        return response.json()
    else:
        print('failed to start session')



def wait_for_session_ready(session_id):
    for _ in range(20):
        status = list_sessions(session_id)
        print(f"Session {session_id} status: {status}")

        if status == "open" or status == "connected":
            print('wait for session status ready:', status)
            return True

        time.sleep(10)

    print("Session did not become ready in time.")
    return False


def send_task(session_id):
    url = "https://api.heygen.com/v1/streaming.task"
    payload = {
        "session_id": session_id,
        "text": "Of course, I’m here to help you with any task or question you have, no matter how simple or complex"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": heygen_api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    print('send task function', response.text)


async def establish_rtc_connection(session_id, sdp_data, sdp_type, heygen_ice_servers):
    # Set ICE servers (using Heygen response)
    ice_servers = [
        {
            "urls": server["urls"],
            "username": server.get("username", ""),
            "credential": server.get("credential", "")
        }
        for server in heygen_ice_servers
        if isinstance(server, dict) and "urls" in server
    ]
    configuration = RTCConfiguration([RTCIceServer(**server) for server in ice_servers])
    pc = RTCPeerConnection(configuration)

    candidate_lines = re.findall(r"a=candidate:(.*)", sdp_data)
    username = ice_servers.pop().get('username', "")
    for candidate_line in candidate_lines:
        send_candidate_to_heygen(session_id,username, candidate_line)


    # @pc.on("icecandidate")
    # def on_ice_candidate(candidate):
    #     print("ICE Candidate Handler Triggered")
    #     if candidate:
    #         print(f"ICE Candidate: {candidate}")
    #     else:
    #         print("No ICE candidate received or ICE gathering completed.")

    # Set Heygen's SDP as remote description
    heygen_offer = RTCSessionDescription(sdp_data, sdp_type)
    await pc.setRemoteDescription(heygen_offer)

    # Create Local Answer for Heygen
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    print("Sending Answer to Heygen:", answer.sdp)

    # Send Answer back to Heygen
    heygen_response = send_answer_to_heygen(session_id, answer.sdp)

    if heygen_response:
        print("Session Started Successfully ")
        start_session(session_id, answer.sdp)
        send_task(session_id)
    else:
        print("Session Failed")


def send_candidate_to_heygen(session_id, username, candidate):
    url = "https://api.heygen.com/v1/streaming.ice"

    parts = candidate.split()

    if len(parts) < 8:
        print(f"Skipping invalid candidate: {parts}")
        return

    payload = {
        "session_id": session_id,
        "candidate": {
            "candidate":  f"candidate:{candidate}",
            "sdpMid": parts[1],
            "sdpMLineIndex": int(parts[1]),
            "usernameFragment": username
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "MDI0YTQ0MjEzOWNkNDEwNzhkNzlmNzE1NzhjOGI5NGQtMTczOTE4OTcxMQ=="
    }

    response = requests.post(url, json=payload, headers=headers)

    print('send candidate to heygen', response.text)
    return response.text


def send_answer_to_heygen(session_id, sdp_answer):
    url = f"https://api.heygen.com/v1/webrtc/session/{session_id}/answer"
    headers = {
        "Authorization": f"Bearer {heygen_api_key}",
        "Content-Type": "application/json"
    }
    data = {"sdp": sdp_answer, "type": "answer"}

    response = requests.post(url, json=data, headers=headers)
    return response.text




# async def setup_livekit_listeners(sdp_offer, candidate):
#     token = getToken()
#     room = rtc.Room()
#     @room.on("track_subscribed")
#     def on_track_subscribed(track: rtc.Track, publication, participant):
#         print(f"Track subscribed: {track.kind} from {participant.identity}")
#         if track.kind == rtc.TrackKind.KIND_AUDIO:
#             asyncio.create_task(handle_audio_track(track))
#
#
#
#     await room.connect(LIVEKIT_SERVER_URL, token)
#     print("Connected to LiveKit room!")
#     sid = await room.sid
#     print(f"Room SID: {sid}")
#
#
#     # Keep the script running
#     await asyncio.Future()


# async def handle_audio_track(track):
#     print("Handling audio track...")
#     # Process the audio track

def stream_to_virtual_cam():
    cap = cv2.VideoCapture(0)

    with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
        print("Streaming video to virtual camera...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cam.send(frame)
            cam.sleep_until_next_frame()


def stop_session(session_id):
    url = "https://api.heygen.com/v1/streaming.stop"
    payload = {"session_id": session_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": heygen_api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    return response.text

#---------------------------------------
async def connect_to_livekit(token):
    pc = RTCPeerConnection()

    # Connect to LiveKit WebSocket
    async with websockets.connect(LIVEKIT_SERVER_URL_wss) as ws:
        # Send Join Room Message
        join_message = {
            'type': 'join',
            'token': token
        }
        await ws.send(json.dumps(join_message))

        # Wait for server response
        response = await ws.recv()
        print('Connected to LiveKit:', response)

        # Offer and Answer Exchange for WebRTC
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        offer_message = {
            'type': 'offer',
            'sdp': pc.localDescription.sdp
        }
        await ws.send(json.dumps(offer_message))

        # Receive Answer from LiveKit
        answer = await ws.recv()
        answer_data = json.loads(answer)
        remote_sdp = answer_data.get('sdp')
        await pc.setRemoteDescription(RTCSessionDescription(remote_sdp, 'answer'))

        print("Connected Heygen to LiveKit Room!")



async def main():
    # generate token
    token = getToken()

    room_name = "new_zoom-room1"
    # #create room
    create_room(room_name, token)

    # # heygen token
    # heygen_token = generate_heygen_session_token()

    # # create session
    session_id, sdp_data, sdp_type, sdp_ice_servers2 = create_session()
    start_session(session_id, sdp_data)
    send_task(session_id)

    # connection = await establish_rtc_connection(session_id,sdp_data, sdp_type, sdp_ice_servers2)
    # print('this is response from astablish rtc connection function', connection)
    # livekit_sdp = await publish_to_livekit(sdp_data)
    # if livekit_sdp:
    #     start_session(session_id, livekit_sdp, sdp_type='answer')
    #     send_task(session_id)
    # else:
    #     print('no livekit sdp')


    # #play on zoom
    # stream_to_virtual_cam()


if __name__ == "__main__":
    asyncio.run(main())



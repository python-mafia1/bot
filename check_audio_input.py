import os
import subprocess
import re


# def find_all_devices():
#     devices = subprocess.check_output(["pactl", "list", "sources"], universal_newlines=True)
#     device_names = []
#     for line in devices.split("\n"):
#         if "Name" in line:
#             device_names.append(line.strip().split(": ")[-1])
#
#     if len(device_names) == 3:
#         return device_names[2]
#     elif len(device_names) == 2:
#         return device_names[1]
#
#
# print(find_all_devices())


# def get_audio_duration(audio_file):
#     # Run the ffmpeg command to get metadata about the audio file
#     ffmpeg_command = ['ffmpeg', '-i', audio_file]
#
#     process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#
#     match = re.search(r"Duration: (\d+:\d+:\d+\.\d+)", process.stderr)
#     print(match)
#     if match:
#         duration_str = match.group(1)
#         print(duration_str)
#         return duration_str
#     else:
#         raise Exception("Could not extract duration")
#
# audio_files = 'audio_folder/abc.mp3'
# print(get_audio_duration(audio_files))


from gtts import gTTS
# mytext = 'Welcome to geeksforgeeks Joe!'
# language = 'en'
# myobj = gTTS(text=mytext, lang=language, slow=False)
# myobj.save("recorded_audio/welcome.mp3")


# def text_to_speech(texts):
#     language = 'en'
#     # for ktext, vtext in texts.items():
#     voice = gTTS(text=texts, lang=language, slow=False)
#     voice.save(f"recorded_audio/welcome_{texts}.mp3")
#

text_script = """
    Hello everyone! Welcome to this amazing video generated with HeyGen's AI technology.
    Today, we're exploring the power of AI-driven video generation. This script will continue
    for at least two minutes to demonstrate the capabilities of this platform.
    
    Artificial Intelligence is transforming the way we create content, making it easier and faster
    to generate professional-looking videos. Whether you're a content creator, a business owner, or
    an educator, AI can help you produce high-quality videos without the need for expensive equipment
    or professional editing skills. This means anyone, regardless of technical knowledge, can create amazing
    videos and share their ideas with the world.
    
    In the past, creating videos involved complex processes—shooting, editing, sound design, and much more.
    But with AI, all of that changes. HeyGen's platform offers an all-in-one solution for content creation.
    You can simply input text, select an avatar, and have the video ready in a fraction of the time it would
    take using traditional methods. It’s efficient, cost-effective, and incredibly versatile.
    
    Now, let's dive deeper into the features of HeyGen. The platform provides various avatars and voice options
    to customize your video. You can choose from different backgrounds, voice tones, and styles to match your needs.
    Whether you’re making an instructional video, a promotional ad, or a fun social media clip, HeyGen has everything
    you need to make your content stand out.
    
    What makes HeyGen even more powerful is the ability to produce videos in multiple languages. This means you can
    reach a global audience, no matter where they are. AI can instantly translate and generate video content in the
    language of your choice, helping businesses and educators expand their reach to different cultures and regions. 
    This opens up new possibilities for those looking to create inclusive and accessible content for audiences worldwide.
    
    Furthermore, AI can generate videos in various formats. Whether you need a simple talking head, an animated character,
    or a scene with dynamic backgrounds, you can get creative with the options available. Imagine a business owner 
    recording a promotional video for their product or a teacher delivering a lesson plan to students from across the 
    globe, all created in minutes with the help of AI.
    
    In conclusion, HeyGen is revolutionizing video creation, saving time and effort while delivering professional-quality
    results. If you haven’t tried it yet, now is the perfect time to explore this fantastic tool. The future of video 
    creation is here, and it’s powered by AI.
    
    Thanks for watching, and see you in the next AI-generated video!
    """

# text_script = """
#     Hello everyone! Welcome to this amazing video generated with HeyGen's AI technology.
#     Today, we're exploring the power of AI-driven video generation. This script will
#     continue for at least two minutes to demonstrate the capabilities of this platform.
#
#     Artificial Intelligence is transforming the way we create content, making it easier
#     and faster to generate professional-looking videos. Whether you're a content creator,
#     a business owner, or an educator, AI can help you produce high-quality videos without
#     the need for expensive equipment or professional editing skills.
#
#     Now, let's dive deeper into the features of HeyGen. The platform provides various
#     avatars and voice options to customize your video. You can choose from different
#     backgrounds, voice tones, and styles to match your needs.
#
#     Furthermore, AI can generate videos in multiple languages, making content accessible
#     to a global audience. This opens up new possibilities for businesses and educators
#     who want to reach people worldwide.
#
#     In conclusion, HeyGen is revolutionizing video creation, saving time and effort while
#     delivering professional-quality results. If you haven't tried it yet, now is the perfect
#     time to explore this fantastic tool.
#
#     Thanks for watching, and see you in the next AI-generated video!
#     """

qa_dict1 = {
    "How are you?": "I am doing well, thank you for asking, and I hope you are also doing great today.",
    "What is your name?": "My name is ChatGPT, and I am here to assist you with any questions or tasks you have.",
    "Where are you from?": "I exist in the digital realm, created by OpenAI to help people all over the world.",
    "What do you do?": "I assist users by providing answers, solving problems, and engaging in meaningful conversations.",
    "What is your favorite color?": "I don’t have preferences like humans, but I can tell you about the meaning of various colors if you'd like.",
    "What are you doing right now?": "Right now, I’m focusing entirely on answering your questions and providing the best help I can.",
    "What is your purpose?": "My purpose is to help, inform, and support users in solving problems, learning, and achieving their goals.",
    "Do you like talking to me?": "Yes, I enjoy engaging with you and helping you out; it’s what I’m here for!",
    "Can you help me with something?": "Of course, I’m here to help you with any task or question you have, no matter how simple or complex.",
    "How is your day going?": "My day has been productive so far, and I’m happy to be assisting you right now."
}
# t = 'helo how are you i am fine tell me about you'
# text_to_speech(t)

#     latest_messages = chat_messages[-a:]  # Fetch the last N messages
#     message_texts = [message.text.strip() for message in latest_messages]


# a = [5,6,7,3,2]
# print(a[-2:])

# accept_cookies_button = //*[@id="onetrust-accept-btn-handler"]
# launch_meeting_button = //*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div
# join_browser_link = //*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3[2]/span/a
# name_input = //*[@id="input-for-name"]
# checkbox = //*[@id="root"]/div/div[1]/div/div[2]/div[3]/div
# join_button = //*[@id="root"]/div/div[1]/div/div[2]/button


#you have been removed = /html/body/div[15]/div/div/div/div[1]/div[1]
#exit button = /html/body/div[15]/div/div/div/div[2]/div/div/button

#close_chat_button = //*[@id="wc-container-right"]/div/div[1]/div[2]/button[2]
#participant_button = //*[@id="participant"]
#participant_count_element = //*[@id="participant"]/button/div/span
#waiting_room_element = //*[@id="root"]/div/div[2]/div[1]/div[3]/span
#removed_text_element = /html/body/div[16]/div/div/div/div[1]/div
#exit_button = /html/body/div[16]/div/div/div/div[2]/div/div/button



#--------------------------------------------------------
# accept_cookies_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
# launch_meeting_button = driver.find_element(By.CLASS_NAME, "mbTuDeF1")
# join_browser_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#zoom-ui-frame > div.bhauZU7H > div > div.pUmU_FLW > h3:nth-child(2) > span > a")))
# WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input-for-name")))
# name_input = driver.find_element(By.CSS_SELECTOR, '#input-for-name')
# checkbox = driver.find_element(By.CSS_SELECTOR, '#root > div > div.preview-new-flow > div > div.preview-meeting-info > div.preview-meeting-info__remember-checkbox > div > div')
# join_button = driver.find_element(By.CSS_SELECTOR, '#root > div > div.preview-new-flow > div > div.preview-meeting-info > button')
# waiting_room_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div.waiting-room-container > div.wr-information > div.wr-tip > span")) )
# removed_text_element = WebDriverWait(driver, 10).until(
                        #     EC.visibility_of_element_located((By.CSS_SELECTOR,
                        #                                       "body > div:nth-child(36) > div > div > div > div.zm-modal-body > div.zm-modal-body-title"))
                        # )
# exit_button = WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable((By.CSS_SELECTOR,
                            #                                 "body > div:nth-child(36) > div > div > div > div.zm-modal-footer > div > div > button"))
                            # )

#when if meeting ends from admin
# removed_text_element = WebDriverWait(driver, 10).until(
                        #     EC.visibility_of_element_located((By.CSS_SELECTOR,
                        #                                       "body > div:nth-child(36) > div > div > div > div.zm-modal-body > div"))
                        # )
# exit_button = WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable((By.CSS_SELECTOR,
                            #                                 "body > div:nth-child(36) > div > div > div > div.zm-modal-footer > div > div > button"))
                            # )

# mic_button = WebDriverWait(driver, 20).until(
                            #     EC.presence_of_element_located(
                            #         (By.CSS_SELECTOR, ".footer-button-base__button.join-audio-container__btn"))
                            # )

# close_chat_button = WebDriverWait(driver, 20).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, "#wc-container-right > div > div.chat-header__header > div.chat-header__operate > button.particpant-header__close-right")))

# Check participant count for 30 minutes
                        # participant_button = WebDriverWait(driver, 10).until(
                        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "#participant"))
                        # )

# participant_count_element = participant_button.find_element(By.CSS_SELECTOR,
#                                                             ".footer-button__number-counter span")

# leave_button = WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable(
                            #         (By.CSS_SELECTOR, "#foot-bar > div.footer__leave-btn-container > button"))
                            # )

# leave_meeting_button = WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable(
                            #         (By.CSS_SELECTOR,
                            #          "#wc-footer > div.footer__inner.leave-option-container > div:nth-child(2) > div > div > button:nth-child(2)"))
                            # )




#stream new
#---------------------------------------------------
data={
   "code":100,
   "data":{
      "session_id":"52bf01ef-e38b-11ef-ab64-36bdd396d627",
      "sdp":{
         "type":"offer",
         "sdp":"v=0\r\no=- 1378261675744859235 1738737300 IN IP4 0.0.0.0\r\ns=-\r\nt=0 0\r\na=msid-semantic:WMS*\r\na=fingerprint:sha-256 89:2B:44:47:DA:F2:01:32:6A:05:80:B4:ED:2E:3E:E4:14:BD:AD:05:97:77:00:EA:1B:55:03:7E:30:75:67:97\r\na=extmap-allow-mixed\r\na=group:BUNDLE 0 1 2\r\nm=video 9 UDP/TLS/RTP/SAVPF 96\r\nc=IN IP4 0.0.0.0\r\na=setup:actpass\r\na=mid:0\r\na=ice-ufrag:IMYsKjepMCjOoXXc\r\na=ice-pwd:gEPvNSPKKIjQwFgWyspBqxWQpbwYLKoL\r\na=rtcp-mux\r\na=rtcp-rsize\r\na=rtpmap:96 VP8/90000\r\na=extmap:1 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=ssrc:2869684506 cname:pion\r\na=ssrc:2869684506 msid:pion video\r\na=ssrc:2869684506 mslabel:pion\r\na=ssrc:2869684506 label:video\r\na=msid:pion video\r\na=sendonly\r\na=candidate:1383040851 1 udp 2130706431 192.168.1.144 44890 typ host\r\na=candidate:1383040851 2 udp 2130706431 192.168.1.144 44890 typ host\r\na=candidate:233762139 1 udp 2130706431 172.17.0.1 38653 typ host\r\na=candidate:233762139 2 udp 2130706431 172.17.0.1 38653 typ host\r\na=candidate:1976174607 1 udp 1694498815 3.129.59.123 35639 typ srflx raddr 0.0.0.0 rport 35639\r\na=candidate:1976174607 2 udp 1694498815 3.129.59.123 35639 typ srflx raddr 0.0.0.0 rport 35639\r\na=candidate:1976174607 1 udp 1694498815 3.129.59.123 57741 typ srflx raddr 0.0.0.0 rport 57741\r\na=candidate:1976174607 2 udp 1694498815 3.129.59.123 57741 typ srflx raddr 0.0.0.0 rport 57741\r\na=candidate:1976174607 1 udp 1694498815 3.129.59.123 36183 typ srflx raddr 0.0.0.0 rport 36183\r\na=candidate:1976174607 2 udp 1694498815 3.129.59.123 36183 typ srflx raddr 0.0.0.0 rport 36183\r\na=candidate:1976174607 1 udp 1694498815 3.129.59.123 52407 typ srflx raddr 0.0.0.0 rport 52407\r\na=candidate:1976174607 2 udp 1694498815 3.129.59.123 52407 typ srflx raddr 0.0.0.0 rport 52407\r\na=candidate:1976174607 1 udp 1694498815 3.129.59.123 42940 typ srflx raddr 0.0.0.0 rport 42940\r\na=candidate:1976174607 2 udp 1694498815 3.129.59.123 42940 typ srflx raddr 0.0.0.0 rport 42940\r\na=candidate:2784105335 1 udp 16777215 34.203.251.42 43015 typ relay raddr 0.0.0.0 rport 51381\r\na=candidate:2784105335 2 udp 16777215 34.203.251.42 43015 typ relay raddr 0.0.0.0 rport 51381\r\na=candidate:2784105335 1 udp 16777215 34.203.251.42 41004 typ relay raddr 192.168.1.144 rport 40464\r\na=candidate:2784105335 2 udp 16777215 34.203.251.42 41004 typ relay raddr 192.168.1.144 rport 40464\r\na=candidate:2784105335 1 udp 16777215 34.203.251.42 44190 typ relay raddr 192.168.1.144 rport 46632\r\na=candidate:2784105335 2 udp 16777215 34.203.251.42 44190 typ relay raddr 192.168.1.144 rport 46632\r\na=end-of-candidates\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111\r\nc=IN IP4 0.0.0.0\r\na=setup:actpass\r\na=mid:1\r\na=ice-ufrag:IMYsKjepMCjOoXXc\r\na=ice-pwd:gEPvNSPKKIjQwFgWyspBqxWQpbwYLKoL\r\na=rtcp-mux\r\na=rtcp-rsize\r\na=rtpmap:111 opus/48000/2\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=extmap:1 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=ssrc:4146346173 cname:pion\r\na=ssrc:4146346173 msid:pion audio\r\na=ssrc:4146346173 mslabel:pion\r\na=ssrc:4146346173 label:audio\r\na=msid:pion audio\r\na=sendrecv\r\nm=application 9 UDP/DTLS/SCTP webrtc-datachannel\r\nc=IN IP4 0.0.0.0\r\na=setup:actpass\r\na=mid:2\r\na=sendrecv\r\na=sctp-port:5000\r\na=ice-ufrag:IMYsKjepMCjOoXXc\r\na=ice-pwd:gEPvNSPKKIjQwFgWyspBqxWQpbwYLKoL\r\n"
      },
      "access_token":null,
      "url":null,
      "ice_servers":null,
      "ice_servers2":[
         {
            "credentialType":"password",
            "urls":[
               "stun:stun.l.google.com:19302"
            ]
         },
         {
            "credential":"",
            "credentialType":"password",
            "urls":[
               "stun:global.stun.twilio.com:3478"
            ]
         },
         {
            "credential":"5f17IZGYNeBEOCIxxX4N5eAPvEVlfHdK4cgFf7M8mxg=",
            "credentialType":"password",
            "urls":[
               "turn:global.turn.twilio.com:3478?transport=udp"
            ],
            "username":"7de691201c8a359cdcec725f9b667114e58f09b9453f2a9553849606187dd5a1"
         },
         {
            "credential":"5f17IZGYNeBEOCIxxX4N5eAPvEVlfHdK4cgFf7M8mxg=",
            "credentialType":"password",
            "urls":[
               "turn:global.turn.twilio.com:3478?transport=tcp"
            ],
            "username":"7de691201c8a359cdcec725f9b667114e58f09b9453f2a9553849606187dd5a1"
         },
         {
            "credential":"5f17IZGYNeBEOCIxxX4N5eAPvEVlfHdK4cgFf7M8mxg=",
            "credentialType":"password",
            "urls":[
               "turn:global.turn.twilio.com:443?transport=tcp"
            ],
            "username":"7de691201c8a359cdcec725f9b667114e58f09b9453f2a9553849606187dd5a1"
         }
      ],
      "is_paid":false,
      "session_duration_limit":600,
      "realtime_endpoint":"wss://webrtc-signaling.heygen.io/v2-alpha/interactive-avatar/session/52bf01ef-e38b-11ef-ab64-36bdd396d627"
   },
   "message":"success"
}


{
    "v": {
        "iceServers": {
            "username": "jP81PwQS2ZnhKlZ6W2h4CgKSz0jbX27sdiEZnfL2gjE0oZD8eUIVHSnV9GriLl2cAAAAAGel64FweXRob24=",
            "urls": [
                "stun:bn-turn1.xirsys.com",
                "turn:bn-turn1.xirsys.com:80?transport=udp",
                "turn:bn-turn1.xirsys.com:3478?transport=udp",
                "turn:bn-turn1.xirsys.com:80?transport=tcp",
                "turn:bn-turn1.xirsys.com:3478?transport=tcp",
                "turns:bn-turn1.xirsys.com:443?transport=tcp",
                "turns:bn-turn1.xirsys.com:5349?transport=tcp"
            ],
            "credential": "f3a1758e-e544-11ef-be54-0242ac140004"
        }
    },
    "s": "ok"
}
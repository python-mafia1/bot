import os
import subprocess
import time
import logging

from playsound import playsound
from gtts import gTTS
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import check_audio_input

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

class JoinZoomMeeting:
    def __init__(self, meeting_url):
        self.meeting_url = meeting_url

    @staticmethod
    def mouse_move(driver):
        ActionChains(driver).move_by_offset(0, 0).perform()
        time.sleep(2)

    @staticmethod
    def mouse_move1(driver, element):
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)

    @staticmethod
    def find_all_input_devices():
        devices = subprocess.check_output(["pactl", "list", "sources"], universal_newlines=True)
        device_names = []
        for line in devices.split("\n"):
            if "Name" in line:
                device_names.append(line.strip().split(": ")[-1])

        if len(device_names) == 3:
            return device_names[2]
        else:
            return device_names[1]


    # @staticmethod
    # def get_audio_file_duration(audio_file):
    #     ffmpeg_command =['ffmpeg', '-i', audio_file]
    #
    #     process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    #
    #     match = re.search(r"Duration: (\d+:\d+:\d+\.\d+)", process.stderr)
    #     if match:
    #         duration_str = match.group(1)
    #         return duration_str
    #     else:
    #         raise Exception("Could not extract duration")


    # def play_and_record_audio(self, index):
    #     folder_path = 'audio_folder/'
    #     output_folder = 'recorded_audio/'
    #
    #     if not os.path.exists(folder_path):
    #         logger.error(f"Folder '{folder_path}' does not exist.")
    #         return
    #
    #     # check output folder
    #     if not os.path.exists(output_folder):
    #         os.makedirs(output_folder)
    #
    #     files = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
    #
    #     if 0 <= index < len(files):
    #         audio_file = os.path.join(folder_path, files[index])
    #         output_file = os.path.join(output_folder, f"recorded_{index}.mp3")
    #
    #         try:
    #             logger.info(f"Recording audio while playing '{audio_file}'...")
    #             ffmpeg_command = [
    #                 "ffmpeg",
    #                 "-f", "pulse",
    #                 "-i", self.find_all_input_devices(),
    #                 "-y",
    #                 "-t", self.get_audio_file_duration(audio_file),
    #                 output_file
    #             ]
    #             process = subprocess.Popen(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #
    #             playsound(audio_file)
    #             process.communicate()
    #             logger.info(f"Recording saved to '{output_file}'.")
    #
    #
                # if os.path.exists(output_file):
                #     os.remove(output_file)
                #     logger.info(f"File deleted successfully: {output_file}")
                # else:
                #     logger.warning(f"File not exist: '{output_file}'.")

    #
    #         except Exception as e:
    #             logger.error(f"Error playing or recording audio file '{audio_file}': {e}")
    #     else:
    #         logger.error("Invalid file index.")

    def play_audio(self, file_name):
        folder_path = 'audio_folder/'

        # Check if the folder exists
        if not os.path.exists(folder_path):
            logger.error(f"Folder '{folder_path}' does not exist.")
            return

        # Construct the full file path
        audio_file = os.path.join(folder_path, f"{file_name}")

        # Check if the file exists
        if not os.path.exists(audio_file):
            logger.error(f"Audio file '{audio_file}' does not exist.")
            return

        try:
            logger.info(f"Playing audio file: '{audio_file}'...")
            playsound(audio_file)
            logger.info(f"Finished playing: '{audio_file}'.")

            if os.path.exists(audio_file):
                os.remove(audio_file)
                logger.info(f"File deleted successfully: {audio_file}")
            else:
                logger.warning(f"File not exist: '{audio_file}'.")

        except Exception as e:
            logger.error(f"Error playing audio file '{audio_file}': {e}")

    def text_to_speech(self, question):
        texts_dic = check_audio_input.qa_dict1
        language = 'en'
        for ktext, vtext in texts_dic.items():
            if ktext == question:
                voice = gTTS(text=vtext, lang=language, slow=False)
                voice.save(f"audio_folder/{ktext}.mp3")
                self.play_audio(f"{ktext}.mp3")

    def get_latest_message(self, driver):
        try:

            unread_badge = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#chat > div.footer-chat-button > button > div > span > span")
                    )
                )

            unread_count = 0
            if unread_badge.is_displayed():
                unread_count = int(unread_badge.text.strip())
                print('unread messages', unread_count)
            else:
                print('unread messages', unread_count)

            # Open the chat box (if it's not already opened)
            self.mouse_move(driver)
            chat_box_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="chat"]/div[1]/button'))
            )
            self.mouse_move1(driver, chat_box_button)
            logger.info('opening chat box')
            chat_box_button.click()
            logger.info("Chat box opened.")
            # time.sleep(5)

            # Wait for chat messages to load
            chat_messages = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#chat-list-content"))
            )

            # Get the latest message
            if chat_messages:
                all_messages = chat_messages[-1].text.strip()

                # Split the message text into a list of lines
                messages_list = all_messages.split("\n")
                latest_messages = messages_list[-unread_count:]

                # Return the list of lines
                logger.info(f"Latest message split into lines: {latest_messages}")

                return latest_messages
            else:
                logger.info("No messages found in the chat.")
                return []

        except Exception as e:
            logger.error(f"Error while retrieving the latest message: {e}")
            return []

    # def change_mic_state(self, driver, latest_message):
    #     self.mouse_move(driver)
    #     # mic button
    #     mic_button = WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located(
    #             (By.CSS_SELECTOR, ".footer-button-base__button.join-audio-container__btn"))
    #     )
    #
    #     aria_label = mic_button.get_attribute("aria-label").strip()
    #     logger.info("Detected aria-label:", aria_label)
    #
    #
    #     if "mute my microphone" == aria_label:
    #         logger.info("Mic is unmute.")
    #         self.text_to_speech(latest_message)
    #         self.mouse_move(driver)
    #         mic_button.click()
    #     elif "unmute my microphone" == aria_label:
    #         logger.info("Mic is already muted.")
    #         mic_button.click()
    #         self.text_to_speech(latest_message)
    #         self.mouse_move(driver)
    #         mic_button.click()
    #     else:
    #         logger.info("Unable to determine mic state.", aria_label)


    def join_zoom_meeting(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.notifications": 1,
        })
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(self.meeting_url)
            time.sleep(6)
            #accept cookies
            try:
                accept_cookies_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
                accept_cookies_button.click()
                logger.info("accepting cookies")
            except TimeoutException:
                logger.warning("Timed out waiting for cookies to become available")
                driver.quit()


            #lunch meeting
            try:
                launch_meeting_button = driver.find_element(By.XPATH, '//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div')
                launch_meeting_button.click()
                logger.info("click on launching meeting button")
            except TimeoutException:
                logger.warning("Timed out waiting for launching meeting button")
                driver.quit()


            #click on 'Join from your browser'
            try:
                join_browser_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3[2]/span/a')))
                join_browser_link.click()
                logger.info("click on joining zoom meeting link")
            except TimeoutException:
                logger.warning("Failed to click on joining zoom meeting link")
                driver.quit()


            #input field
            driver.switch_to.frame(0)
            try:

                WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="input-for-name"]')))
                name_input = driver.find_element(By.XPATH, '//*[@id="input-for-name"]')
                name_input.send_keys('Name')
                logger.info("fill the first name field")
            except TimeoutException:
                logger.warning("Timed out waiting for name field")
                driver.quit()

            #checkbox
            try:
                checkbox = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[3]/div')
                checkbox.click()
                logger.info("click on checkbox")
            except TimeoutException:
                logger.warning("Failed to check the checkbox")

            #join button
            try:
                join_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/button')
                join_button.click()
                logger.info("click on join button")
            except TimeoutException:
                logger.warning("Failed to click on the join button.")

            driver.switch_to.default_content()

            #enter in iframe
            driver.switch_to.frame(0)
            timeout = 1800
            start_time = time.time()

            while True:

                if driver.service.process is None or driver.service.process.poll() is not None:
                    logger.info("Browser closed. Stopping execution.")
                    break

                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    logger.warning("30 minutes passed")
                    break


                try:
                    # Waiting for the host to join the meeting
                    try:
                        waiting_room_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[3]/span'))
                        )
                        if waiting_room_element.is_displayed():
                            logger.info("Waiting for the host. Retrying in 5 seconds.")
                            time.sleep(5)
                            continue
                    except Exception:
                        logger.warning("The host has joined the meeting or the waiting room is no longer present.")


                    # leave meeting if removed from admin
                    try:

                        removed_text_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '/html/body/div[15]/div/div/div/div[1]/div[1]'))
                        )
                        removed_text = removed_text_element.text.strip()
                        print('>>>>>>>>>>>>>>>>', removed_text)
                        if "You have been removed" == removed_text:
                            logger.info("Detected 'You are removed' message. Leaving the meeting...")

                            exit_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '/html/body/div[15]/div/div/div/div[2]/div/div/button'))
                            )
                            exit_button.click()
                            break
                    except Exception as e:
                        logger.info("No 'You are removed' text found or timeout occurred:", e)



                    #leave meeting if meeting ends from admin
                    try:
                        removed_text_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '/html/body/div[16]/div/div/div/div[1]/div'))
                        )
                        removed_text = removed_text_element.text.strip()
                        if "This meeting has been ended by host" == removed_text:
                            logger.info("Detected 'meeting end from admin' message. Leaving the meeting...")

                            exit_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '/html/body/div[16]/div/div/div/div[2]/div/div/button'))
                            )
                            exit_button.click()
                            break
                    except Exception as e:
                        logger.info("No 'meeting end from admin' text found or timeout occurred:", e)


                    #read new msgs
                    try:
                        # play audio
                        self.mouse_move(driver)
                        latest_messages = self.get_latest_message(driver)
                        for latest_message in latest_messages:
                            self.mouse_move(driver)
                            #mic button

                            mic_button = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="foot-bar"]/div[1]/div[1]/button'))
                            )

                            aria_label = mic_button.get_attribute("aria-label").strip()
                            logger.info("Detected aria-label:", aria_label)

                            if "mute my microphone" == aria_label:
                                logger.info("Mic is unmute.")
                                self.text_to_speech(latest_message)
                                self.mouse_move(driver)
                                mic_button.click()
                            elif "unmute my microphone" == aria_label:
                                logger.info("Mic is already muted.")
                                self.mouse_move1(driver, mic_button)
                                mic_button.click()
                                self.text_to_speech(latest_message)
                                self.mouse_move(driver)
                                mic_button.click()
                            else:
                                logger.info("Unable to determine mic state.", aria_label)


                        close_chat_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="wc-container-right"]/div/div[1]/div[2]/button[2]')))

                        close_chat_button.click()
                        logger.info("Successfully closed chat.")

                    except TimeoutException:
                        print('cant open the chatbox')

                    # Leave the meeting if all participants
                    try:
                        self.mouse_move(driver)
                        participant_button = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="participant"]'))
                        )

                        participant_count_element = participant_button.find_element(By.XPATH, '//*[@id="participant"]/button/div/span')
                        participant_count = int(participant_count_element.text.strip())
                        logger.info(f"Participant count: {participant_count}")

                        # Leave if only 1 participant remains (yourself)
                        if participant_count == 1:
                            print("Only you are in the meeting. Leaving the meeting.")

                            leave_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '// * [ @ id = "foot-bar"] / div[5]'))
                            )
                            self.mouse_move1(driver, leave_button)
                            leave_button.click()

                            leave_meeting_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//*[@id="wc-footer"]/div[2]/div[2]/div/div/button[1]'))
                            )
                            leave_meeting_button.click()
                            break
                        else:
                            print("Other participants are still in the meeting. try again...")
                    except Exception as e:
                        logger.error("An error occurred while checking participant count:", e)


                except Exception as e:
                    logger.error("An unexpected error occurred:", e)
                    break


            driver.switch_to.default_content()
        except Exception as e:
            logger.error('Unexpected error occurred:', e)

        finally:
            # Close the browser
            driver.quit()
            logger.info('browser closed.')


meeting_url = "https://us05web.zoom.us/j/81927147841?pwd=QUZJi3Wj2DsAMXb0gLeJVaTXB0j4Zf.1"
meeting = JoinZoomMeeting(meeting_url)
meeting.join_zoom_meeting()


from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def switch_to_iframe(func):
    """Decorator to ensure the function operates within the iframe context."""
    def wrapper(self, *args, **kwargs):
        self.driver.switch_to.frame(0)
        result = func(self, *args, **kwargs)
        self.driver.switch_to.default_content()
        return result
    return wrapper


class ZoomAutomation:
    def __init__(self, meeting_url, name="Your Name"):
        self.meeting_url = meeting_url
        self.name = name
        self.driver = self._initialize_driver()

    @staticmethod
    def _initialize_driver():
        """Initialize the Chrome WebDriver with necessary options."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.notifications": 1,
        })
        return webdriver.Chrome(options=options)

    def _click_element(self, by, value, timeout=10):
        """Click an element specified by a locator strategy."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
            element.click()
            print(f"Clicked element: {value}")
        except Exception as e:
            print(f"Failed to click element: {value}. Error: {e}")

    def join_meeting(self):
        """Navigate to the meeting URL and perform initial setup."""
        self.driver.get(self.meeting_url)

        # Accept cookies
        self._click_element(By.ID, "onetrust-accept-btn-handler")

        # Launch meeting
        self._click_element(By.CLASS_NAME, "mbTuDeF1")

        # Join from browser
        self._click_element(By.CSS_SELECTOR, "#zoom-ui-frame > div.bhauZU7H > div > div.pUmU_FLW > h3:nth-child(2) > span > a")

        # Enter name and join meeting
        self._enter_name_and_join()

    @switch_to_iframe
    def _enter_name_and_join(self):
        """Enter the name and click the join button."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input-for-name")))
        name_input = self.driver.find_element(By.CSS_SELECTOR, '#input-for-name')
        name_input.send_keys(self.name)

        checkbox = self.driver.find_element(By.CSS_SELECTOR, '#root > div > div.preview-new-flow > div > div.preview-meeting-info > div.preview-meeting-info__remember-checkbox > div > div')
        checkbox.click()

        join_button = self.driver.find_element(By.CSS_SELECTOR, '#root > div > div.preview-new-flow > div > div.preview-meeting-info > button')
        join_button.click()

    def monitor_meeting(self, timeout=1800):
        """Monitor the meeting for specific conditions."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self._handle_waiting_room()
                self._mute_mic()
                self._handle_removal()
                self._check_participants()
                time.sleep(10)  # Polling interval
            except Exception as e:
                print("An unexpected error occurred:", e)
                break
        print("Exiting monitoring after timeout.")
        self.driver.quit()

    @switch_to_iframe
    def _handle_waiting_room(self, timeout=1800, check_interval=5):
        """Check if the user is in the waiting room for a specified duration."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                waiting_room_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "#root > div > div.waiting-room-container > div.wr-information > div.wr-tip > span"))
                )
                if waiting_room_element.is_displayed():
                    print("Still in the waiting room. Retrying in 5 seconds.")
                    time.sleep(check_interval)
                else:
                    print("The host has joined or the waiting room is no longer present.")
                    break
            except Exception:
                print("The host has joined or the waiting room is no longer present.")
                break
        else:
            print("Timeout reached. Host did not join the meeting.")
    @switch_to_iframe
    def _mute_mic(self):
        """Mute the microphone if it is not already muted."""
        try:
            ActionChains(self.driver).move_by_offset(0, 0).perform()
            time.sleep(1)
            mic_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".footer-button-base__button.join-audio-container__btn"))
            )
            aria_label = mic_button.get_attribute("aria-label").strip()
            print("Detected aria-label:", aria_label)

            if "mute my microphone" == aria_label.lower():
                print("Mic is unmuted. Muting the mic.")
                mic_button.click()
            elif "unmute my microphone" == aria_label.lower():
                print("Mic is already muted. Leaving it off.")
        except Exception:
            print("Unable to determine mic state.")

    @switch_to_iframe
    def _handle_removal(self):
        """Leave the meeting if removed by the admin."""
        try:
            removed_text_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "body > div:nth-child(36) > div > div > div > div.zm-modal-body > div.zm-modal-body-title"))
            )
            removed_text = removed_text_element.text.strip()
            if "You have been removed" == removed_text:
                print("Detected removal message. Leaving the meeting...")
                exit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(36) > div > div > div > div.zm-modal-footer > div > div > button"))
                )
                exit_button.click()
        except Exception:
            print("No 'You are removed' text found or timeout occurred.")

    @switch_to_iframe
    def _check_participants(self):
        """Leave the meeting if all participants except the user have left."""
        try:
            ActionChains(self.driver).move_by_offset(0, 0).perform()  # Make participant count visible
            time.sleep(1)

            participant_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#participant"))
            )
            participant_count_element = participant_button.find_element(By.CSS_SELECTOR, ".footer-button__number-counter span")
            participant_count = int(participant_count_element.text.strip())
            print(f"Participant count: {participant_count}")

            if participant_count == 1:
                print("Only you are in the meeting. Leaving the meeting.")
                self._leave_meeting()
        except Exception as e:
            print("An error occurred while checking participant count:", e)

    def _leave_meeting(self):
        time.sleep(2)
        """Click the leave meeting button."""
        leave_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#foot-bar > div.footer__leave-btn-container > button"))
        )
        leave_button.click()

        leave_meeting_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wc-footer > div.footer__inner.leave-option-container > div:nth-child(2) > div > div > button:nth-child(2)"))
        )
        leave_meeting_button.click()


# Example usage
meeting_url = "https://us05web.zoom.us/j/81408554530?pwd=WEERWjrC4V1yH9UQCKR3oNRmC5UmMD.1"
zoom = ZoomAutomation(meeting_url)
zoom.join_meeting()
zoom.monitor_meeting()

from flask import Flask, request, render_template
    import requests
    import warnings
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    app = Flask(__name__)

    @app.route('/')
    def home():
      return render_template('index.html')

    @app.route('/start-bot', methods=['POST'])
    def start_bot():
      twitch_username = request.form.get('twitch_username')
      proxy_count = int(request.form.get('proxy_count'))
      proxy_url = request.form.get('proxy_url')

      # Initialize Selenium WebDriver
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
      chrome_options.add_argument('--disable-logging')
      chrome_options.add_argument('--log-level=3')
      chrome_options.add_argument('--disable-extensions')
      chrome_options.add_argument('--headless')
      chrome_options.add_argument("--mute-audio")
      chrome_options.add_argument('--disable-dev-shm-usage')
      driver = webdriver.Chrome(options=chrome_options)

      driver.get(proxy_url)

      for _ in range(proxy_count):
        driver.execute_script("window.open('" + proxy_url + "')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(proxy_url)

        text_box = driver.find_element(By.ID, 'url')
        text_box.send_keys(f'www.twitch.tv/{twitch_username}')
        text_box.send_keys(Keys.RETURN)

      driver.quit()
      return "Bot started successfully!"

    if __name__ == '__main__':
      app.run(debug=True)

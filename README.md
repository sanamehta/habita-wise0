# habita - wise
Habita-Wise is an AI-powered tenant advocacy platform designed to empower renters by addressing systemic challenges in the rental housing market. The app helps tenants navigate landlord disputes, understand their legal rights, and access actionable resources for resolving rental issues. Combining data-driven insights with advanced automation, Habita-Wise provides tools like personalized legal guidance, automated document generation, and seamless communication support, such as making calls or filing complaints.

Key features include:



- AI-Driven Guidance: Through conversational interaction, the app collects tenant issues, retrieves insights from a database of historical landlord-tenant cases, and predicts the likelihood of success in legal disputes.

- Legal Resource Retrieval: An integrated Researcher agent fetches location-specific, up-to-date filing procedures, forms, and contact details.

- Automated Action Tools: Features like email drafting, report generation, and voice-enabled calls save time and reduce stress for tenants.

- Tenant Empowerment: The platform simplifies complex legal jargon, ensuring users understand their rights and are equipped to take informed action.

- Scalability: While the app initially focuses on California, it is designed to scale nationally to address the broader rental market.

* 💬 OpenAI Assistants API chat UI
* 🛠️ It works easily by setting the ASSISTANT IDs
* 📁 Supports file upload and file download
* 🏃 Supports Streaming API
* 👥 Supports multiple Assistant profiles in one place
* 🪟 Support to Azure OpenAI

<img width="1459" alt="スクリーンショット 2023-11-20 2 23 51" src="https://github.com/ryo-ma/gpt-assistants-api-ui/assets/6661165/5c288d51-196a-4919-bc4d-dc508146f58a">

## 🌟 Quick Start

1. 👤 Create an assistant on the OpenAI site & Get assistant ID (https://platform.openai.com/assistants)
2. 🔑 Get the API key from OpenAI (https://platform.openai.com/api-keys)
3. ⬇️ Clone the repository

    ```bash
    $ git clone https://github.com/ryo-ma/gpt-assistants-api-ui.git
    ```

4. 📦 Install dependencies

    ```bash
    $ poetry install
    ```

5. ⚙️ Set environment variables file `.env`

    ```bash
    # OpenAI settings
    OPENAI_API_KEY="sk-xxx"
    APP_ENABLED_FILE_UPLOAD_MESSAGE="Upload a file" # Leave empty to disable

    AUTHENTICATION_REQUIRED="False" # Must change to True if you require authentication

    # When using only one assistant, set the following, unset the OPENAI_ASSISTANTS variable.
    ASSISTANT_ID="asst_xxx"
    ASSISTANT_TITLE="Assistants API UI" # This is for the single agent title

    # When using multiple assistants, set the following.
    OPENAI_ASSISTANTS='[{"id": "asst_xxx", "title": "Assistants XXX UI"}, {"id": "asst_yyy", "title": "Assistants YYY UI"}]'
    ```
    If you use azure instead, set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_KEY`

6. 🔑 Set Authentication configuration (optional)

    To set up authentication, create a [secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) file `.streamlit/secrets.toml`  as below:

    ```toml
    [credentials]
    usernames = { jsmith = {failed_login_attempts = 0,  logged_in = false, name = "John Smith", password = "abc"}, rbriggs = {failed_login_attempts = 0,  logged_in = false, name = "R Briggs", password = "abc"}}

    [cookie]
    expiry_days = 30
    key = "some_signature_key"  # Must be string
    name = "some_cookie_name"
    ```
    Reference:  [Deploying Streamlit-Authenticator via Streamlit Community Cloud](https://discuss.streamlit.io/t/deploying-streamlit-authenticator-via-streamlit-community-cloud/39085)

## 🏃‍️ Run the app using Streamlit


```bash
$ poetry shell
$ streamlit run app.py
```

## 🐳 Run the app using Docker

1. 💽 Build image

    ```bash
    $ docker compose build
    ```

2. 🏃‍️ Run the app

    ```bash
    $ docker compose up
    ```
Access to [http://localhost:8501](http://localhost:8501).

## 🌐 Deploy to Streamlit Cloud
You can fork this repository and deploy the app to https://share.streamlit.io/. No need to run the app on your local machine.

> Don't forget to choose 3.10 as the Python version and set environment variables in the "Advanced settings" during deployment.

To use authentication with Streamlit Cloud, please use this TOML format:

```toml
# Environment variables
# OpenAI settings
OPENAI_API_KEY="sk-xxx"
APP_ENABLED_FILE_UPLOAD_MESSAGE="Upload a file" # Leave empty to disable

AUTHENTICATION_REQUIRED="False" # Must change to True if you require authentication

# When using only one assistant, set the following, unset the OPENAI_ASSISTANTS variable.
ASSISTANT_ID="asst_xxx"
ASSISTANT_TITLE="Assistants API UI" # This is for the single agent title

# When using multiple assistants, set the following.
OPENAI_ASSISTANTS='[{"id": "asst_xxx", "title": "Assistants XXX UI"}, {"id": "asst_yyy", "title": "Assistants YYY UI"}]'

# Authentication secrets
[credentials]
usernames = { jsmith = {failed_login_attempts = 0,  logged_in = false, name = "John Smith", password = "abc"}, rbriggs = {failed_login_attempts = 0,  logged_in = false, name = "R Briggs", password = "abc"}}

[cookie]
expiry_days = 30
key = "some_signature_key"  # Must be string
name = "some_cookie_name"
```

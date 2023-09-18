# demo_le
## Running the App

### a) Locally:

1. **Install Virtual Environment Tool**:
   - First, you need to have `virtualenv` installed. If you don't have it, you can install it using pip:
     ```bash
     pip install virtualenv
     ```

2. **Create a Virtual Environment**:
   - Navigate to your project directory called “demo_le” as part of the folders submitted and create a virtual environment.
     ```bash
     cd path/to/your/demo_le
     virtualenv venv
     ```

3. **Activate the Virtual Environment**:
   - Depending on your operating system, the command to activate the virtual environment will differ:
     - **WINDOWS**:
       ```bash
       .\venv\Scripts\activate
       ```
     - **MACOS AND LINUX**:
       ```bash
       source venv/bin/activate
       ```

   - Once activated, your terminal or command prompt should show the name of the virtual environment, indicating that it's currently active.

4. **Install Dependencies**:
   - Install all the dependencies and their versions listed on the `requirements.txt` file in your project directory "demo_le" using:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run Your Streamlit App**:
   - With the virtual environment activated and all dependencies installed, you can run your Streamlit app:
     ```bash
     streamlit run main.py
     ```

6. **Deactivate the Virtual Environment**:
   - Once you're done working on your Streamlit app, you can deactivate the virtual environment:
     ```bash
     deactivate
     ```

### b) Globally on Streamlit Host:

1. **Prepare Your App**:
   - Ensure your Streamlit app works locally without any issues. Test it by running:
     ```bash
     streamlit run main.py
     ```

2. **Push Your App to GitHub**:
   - Streamlit Sharing deploys apps directly from GitHub repositories. Create a new repository on GitHub and push your Streamlit app folder called "demo_le" to it. Ensure your repository is public.

3. **Sign Up for Streamlit Sharing**:
   - Go to [Streamlit Sharing](https://share.streamlit.io/) and sign up using your GitHub account.

4. **Deploy Your App**:
   - Once you have access, go to the Streamlit Sharing dashboard, click on the NEW APP button, select the appropriate GitHub repository and branch, choose the main file, and click on DEPLOY.

5. **Access and Share Your App**:
   - Once deployed, you'll receive a unique URL for your app. Share this URL to give others access.

6. **Updating Your App**:
   - Push changes to your GitHub repository. Streamlit Sharing will automatically redeploy your app.

7. **Additional Configuration**:
   - **REQUIREMENTS**: Ensure `requirements.txt` in your GitHub repository lists necessary packages.
   - **DATA FILES**: Push external data files to the same GitHub repository.
   - **SECRETS**: Add secrets via the app's settings in the Streamlit Sharing dashboard.

8. **Monitor Usage**:
   - View metrics on app usage from the Streamlit Sharing dashboard.

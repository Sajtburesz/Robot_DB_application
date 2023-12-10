# Robot Framework database application
## Install
Prerequisites:
- Install docker

Steps:
- Clone repository
- Stand in Root directory of application (Robot_Result_app)
- Edit docker-compose.yaml for your liking
- Build application: 'docker build'
- Deploy application: 'docker compose up'

With default config application will run on local host address(127.0.0.1). To expose application on local or global network additional port forwarding and routing configurations need to be done on local network. That part is the endusers task to figure out.

Developing application:
Prerequisites:
- Running Postgresql instance on default port 5437

Steps:
- Clone repository
- Stand in Root directory of application (Robot_Result_app)
- Create virtual python environment(venv)
- Install requirements.txt content
- Install npm package manager
- Move to frontend directory and execute 'npm install' command
- Run Django migrations if necessary: 'python3 manage.py migrate'
- Standing in application root directory start Django dev server with: 'python3 manage.py runserver'
- Standing in application frontend directory start Vue.js dev server with: 'npm run serve'

The two devservers are connected to eachother and feature hot loading capabilities, meaning no server reload is required on code change. Dev server runs on localhost(127.0.0.1:8000) and Vue.js devserver on(127.0.0.1:8080). Both ports need to be empty or port usage has to be edited in root/config/settings.py and root/frontend/vue.config.js.

Application is available on backend dev server access 127.0.0.1:8000.

## Testing
Unit Tests for backend changes are necesary!
Unit Tests for frontend are advised but manual testing is acceptable.
Robot Framework platform tests if the estimated time allows.

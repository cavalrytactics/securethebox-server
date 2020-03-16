# Kill this service running on port 5000
sudo lsof -t -i tcp:5000  | xargs kill
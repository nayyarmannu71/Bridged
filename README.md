# Bridged

Prerequisites
1. Ubuntu OS
2. Python 2
3. Install redis-server using the following commands:
        sudo apt update
        sudo apt install redis-server
        
Clone the repository and follow below instructions.


Running the program
1. Run command "redis-server" to start redis server.
2. Run command "pip install -r requirements.txt".
3. Run command "python pass_data.py".
4. Open as many terminal as you like and run command "rq worker" to start the crawling process.

NOTE: To view queue data, run the following commands "rq-dashboard --port=5000" and navigate to localhost:5000 in you browser to view rq-dashboard.

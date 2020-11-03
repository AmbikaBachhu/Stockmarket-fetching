from datetime import datetime
from nsetools import Nse
from apscheduler.schedulers.blocking import BlockingScheduler
nse = Nse()
def job_function():
    top = nse.get_top_gainers()
    print(top)
sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(job_function, 'interval', seconds=30)

sched.start()

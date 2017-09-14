#bash
#python /app/src/main.py >>/var/log/cron.log 2>&1

# export environment variables to the crontab environment
# [This issue](stackoverflow.com/questions/27771781)
env > /etc/environment
cron -f
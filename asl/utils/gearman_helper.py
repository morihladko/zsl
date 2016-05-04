import gearman
import json

def schedule_german_task(app, path, data):
    gm_client = gearman.GearmanClient(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])
    gm_client.submit_job(app.config['GEARMAN_TASK_NAME'], json.dumps({ 'path': path, 'data': data }), wait_until_complete=False, background=True)

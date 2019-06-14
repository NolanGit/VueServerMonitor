from flask import Flask, render_template,jsonify
from monitor_model import system_disk_monitor, system_uptime
app = Flask(__name__,
static_folder = "../server-monitor/dist",
static_url_path="",
template_folder = "../server-monitor/dist")

@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/systemMonitor', methods=['GET'])
def systemMonitor():
	result = {}
	
	system_disk_monitor_query = system_disk_monitor.select().order_by(
		-system_disk_monitor.id).limit(1).dicts()
	result['disk']={}
	for row in system_disk_monitor_query:
		result['disk']['size'] = row['size']
		result['disk']['used'] = row['used']
		result['update_time']=row['update_time']
		result['update_time']=row['update_time']
			
	system_uptime_query = system_uptime.select().order_by(-system_uptime.id).limit(
            60).dicts()
	i = 0
	result['uptime']={}
	result['uptime']['average']=[]
	result['uptime']['time']=[]
	for row in system_uptime_query:
		result['uptime']['average'].append(row['average'])
		result['uptime']['time'].append(
			row['update_time'].strftime('%H:%M'))
		i += 1
		if i==1:
			result['user']=row['user']

	return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
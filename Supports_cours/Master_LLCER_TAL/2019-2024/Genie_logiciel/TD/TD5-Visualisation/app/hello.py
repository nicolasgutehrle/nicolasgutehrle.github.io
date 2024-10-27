# Importing required functions 
import random 

from flask import Flask, render_template 
from bokeh.embed import components 
from bokeh.plotting import figure 

# Flask constructor 
app = Flask(__name__) 

# Root endpoint 
@app.route('/') 
def homepage(): 

	# First Chart - Scatter Plot 
	p1 = figure(height=350, sizing_mode="stretch_width") 
	p1.circle( 
		[i for i in range(10)], 
		[random.randint(1, 50) for j in range(10)], 
		size=20, 
		color="navy", 
		alpha=0.5
	) 

	# Second Chart - Line Plot 
	language = ['Python', 'JavaScript', 'C++', 'C#', 'Java', 'Golang'] 
	popularity = [85, 91, 63, 58, 80, 77] 

	p2 = figure( 
		x_range=language, 
		height=350, 
		title="Popularity", 
	) 
	p2.vbar(x=language, top=popularity, width=0.5) 
	p2.xgrid.grid_line_color = None
	p2.y_range.start = 0

	# Third Chart - Line Plot 
	p3 = figure(height=350, sizing_mode="stretch_width") 
	p3.line( 
		[i for i in range(10)], 
		[random.randint(1, 50) for j in range(10)], 
		line_width=2, 
		color="olive", 
		alpha=0.5
	) 

	script1, div1 = components(p1) 
	script2, div2 = components(p2) 
	script3, div3 = components(p3) 

	# Return all the charts to the HTML template 
	return render_template( 
		template_name_or_list='charts.html', 
		script=[script1, script2, script3],
		div=[div1, div2, div3], 
	) 


# Main Driver Function 
if __name__ == '__main__': 
	# Run the application on the local development server 
	app.run() 

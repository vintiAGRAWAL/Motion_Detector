from Basics import dFrame
from bokeh.plotting import figure, show, output_file, Figure
from bokeh.models import HoverTool, ColumnDataSource

dFrame["Start_string"] = dFrame["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
dFrame["End_string"] = dFrame["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(dFrame)

p = figure(x_axis_type='datetime', height=100, width=500,
           sizing_mode="scale_width", title="Motion Graph")
p.yaxis.minor_tick_line_color = None
#p.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(
    tooltips=[("Start", "@Start_String"), ("End", "@End_String")])
p.add_tools(hover)

q = p.quad(left="Start", right="End", bottom=0,
           top=1, color="blue", source=cds)
output_file("Graph.html")
show(p)

from basic import *	
from coupler import *

length = 250
width = 1.0

dx = 0.4
spec={'layer':1}
bend_r = 20

rate = 10

w_gap = rate*width

cell_m = gdspy.Cell('test')

coupler_df((0,0), 2, np.pi/4.0, 100, 1.0, 0.8, cell_m, 1, 10)

gdspy.LayoutViewer()
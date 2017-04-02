from coupler import *

origin=(0,0)
width = 1.3
gap=3
bend=20
dx = 0.45
radius_disk=40

p=(gap+width)*0.5
cell = gp.Cell('test')
cell.add(coupler(origin,width,np.pi*0.25,10,0.8,1.2,gap))
cell.add(coupler((250,0),width,np.pi*0.25,10,0.8,1.2,gap))

path1=gp.Path(gap, (origin[0]+p,origin[1]))
path1.arc(bend-p,np.pi,np.pi*0.5).segment(210).arc(bend-p,np.pi*0.5,0)
cell.add(path1)

path2=gp.Path(gap, (origin[0]-p,origin[1]))
path2.arc(bend+p,np.pi,np.pi*0.5).segment(210).arc(bend+p,np.pi*0.5,0)

origin_disk=(origin[0]+125, origin[1]+dx+width*0.5+radius_disk+bend)
path2=gp.fast_boolean(path2,gp.Round(origin_disk,radius_disk),'not')
cell.add(path2)

ring=gp.Round(
        origin_disk,
        radius_disk+gap,
        inner_radius=radius_disk),

cell.add(gp.fast_boolean(
	ring,
	gp.Path(width+2*gap,
		(origin[0]+125-100,origin[1]+bend)).segment(2*100),
	'not'))

# gp.LayoutViewer()
gp.gds_print('disk.gds', unit=1.0e-6, precision=1.0e-9)

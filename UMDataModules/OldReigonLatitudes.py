# Stores latitude boundaries in form (min long (deg E), max long(deg E), min lat, max lat) where lons are East longitudes and lats are -v for SH, +v for NH, both in degrees

RegionLonsLats = {'US':(235.,290.,30.,50.),
    'Europe_Approx':(336.,30.,36.,66. ), # may need to treat differently because Europe lies over 0 degree longitude
    'Europe':(350.,40.,35.,70.),
    'NHML':(0.,360.,30.,60. ),
    'China':(80.,120.,20.,50. ),
    'East_Asia':(105.,145.,20.,45. ),
    'India': (70.,90.,10.,30. ),
    'Asia': (60.,140.,10.,50.),
    'Arabia': (30.,85.,0.,40.),
    'Global':(0.,360.,-90.,90.),
    'NH':(0.,360.,0.,90.),
    'SH':(0.,360.,-90.,90.),
    'Africa':(360.-20.,50.,-35.,35.),
    'South_America':(360.-80.,360.-35.,-50.,10.),
    'NHML_ext':(0.,360.,20.,70.),
    'Tropics':(0.,360.,-30.,30.),
    'SHML':(0.,360.,-60.,-30.),
    'SHML_ext':(0.,360.,-70.,-20.),
    'NHHL':(0.,360.,60.,90.),
    'SHHL':(0.,360.,-90.,60.),
    #'NP':(0.,360.,66.,90.),     # defined by arctic circle
    'SP':(0.,360.,-90.,-66.), 
    'NorwSea':(10.,70.,70.,80.),    # Small blob in Norweigan sea appears influential
    'Sahel':(360.-17.,38.,9.,19.),
    'North_America':(360.-129.,260.-77.,32.,60.),
    'India/Bangladesh':(71.,94.,15.,28.), # Same as Shindel et al
    'Southwest_China/SE_Asia':(98.,110.,11.,30.),
    'Southwestern_US':(360-120.,360.-103.,32.,37),
    'Eastern_US':(360.-95., 360-77.,34. ,44. ),
    'Pacific_Northwest': (360.-129 ,360.-115,42 ,60.),
    'Arctic':(0.,360.,66.,90.),
    'Austrailia':(95.,155.,-40.,-10.)
    }

RegionList = ['US','Europe','China','East_Asia','India','Arabia','Asia','Africa','South_America']
for reg in RegionList:
    ext_reg = reg+'_ext'
    (xmin,xmax,ymin,ymax) = RegionLonsLats[reg]
    RegionLonsLats[ext_reg] = ( xmin-10.,xmax+10.,ymin-10.,ymax+10.)

print(RegionLonsLats)

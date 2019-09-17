
RegionLonsLats = {'Arctic':(0.,360.,66.,90.),
        'NorthAmerica':(230.,300.,10.,66.),
        'NorthPacific':(145.  ,230.,10.,66.),
        'SouthPacific':(180., 360.-80., -50.,10.),
        'SouthAmerica':(360.-80.,360.-35.,-50.,10.),
        'Antarctic':(0.,360.,-90.,-66.),
        'SouthernOcean':(0.,360.,-66.,-50.),
        'SouthAtlantic':(360.-35.,10. ,-50.,10.),
        'NorthAtlantic':(300.,340.,10.,66.),
        'NorthernAfrica':(340.,50.,10.,35.), # would prefer this to start at 5 deg?
        'SouthernAfrica':(10.,50.,-50.,10.),
        'Europe':(340.,50.,35.,66.),
        'Russia':(50.,  100. ,35.,66.),
        'SouthAsia':(50.,100.,0.,35.),
        'IndianOcean':(50.,100.  ,-50. ,0.),
        'Oceania':(100.,180. ,-50., 10.),
        'EastAsia':(100.,145.,10.,66. ),
        'Global':(0.,360.,-90.,90.),
        'NH':(0.,360.,0.,90.),
        'SH':(0.,360.,-90.,90.),
        'NHML':(0.,360.,30.,60.),
        'SHML':(0.,360.,-60.,-30.),
        'NHHL':(0.,360.,60.,90.),
        'SHHL':(0.,360.,-90.,-60.),
        'Tropics':(0.,360.,-30.,30.)
}

RegionsList = list(RegionLonsLats.keys())

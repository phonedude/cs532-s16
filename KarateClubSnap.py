import snap

UGraph = snap.GenRndGnm(snap.PUNGraph, 100, 1000)
CmtyV = snap.TCnComV()
modularity = snap.CommunityGirvanNewman(UGraph, CmtyV)
for Cmty in CmtyV:
    print "Community: "
    for NI in Cmty:
        print NI
print "The modularity of the network is %f" % modularity
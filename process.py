import psutil

conn_counts = {}
totalConns = 0

def buildBaseline():
    for p in psutil.pids():
        try:
            proc = psutil.Process(p)
            name = proc.name()
            hasConns = int(len(proc.connections()) > 0)
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                conn_counts[name] = (connected+hasConns,total+1)
            else:
                conn_counts[name] = (hasConns,1)
        except:
            continue

    return '\n'.join(map(lambda x: f"{x[0]} ", conn_counts.items()))


threshold = .5
def checkConnections():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = len(proc.connections()) > 0
        if hasConns:
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                prob = connected/total
                if prob < threshold:
                    return("Process %s has network connection at %f probability" % (name,prob))
            else:
                return("New process %s has network connection" % name)
        else:
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                prob = 1-(connected/total)
                if prob < threshold:
                    return("Process %s doesn't have network connection at %f probability" % (name, prob))

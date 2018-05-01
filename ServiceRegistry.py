import datetime
from nose.tools import assert_equals, assert_raises

class Address(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return self.ip+self.port

class Service(object):

    def __init__(self, serviceId, serviceName, address, health=100):
        self.serviceId = serviceId
        self.serviceName = serviceName
        self.address = address
        self.health = health
        self.lastHeartBeat = datetime.datetime.now().time()

    def updateHeartBeat(self):
        self.lastHeartBeat = datetime.datetime.now().time()

    def getInstanceId(self):
        return getInstanceId(self.serviceId, self.address.ip, self.address.port)

    def __str__(self):
        return str(self.serviceId)+self.serviceName+self.address.__str__()+str(self.health)+str(self.lastHeartBeat)

def getInstanceId(serviceId, ip, port):
    return str(serviceId)+'|'+ip+'|'+port

class ServiceRegistry(object):

    def __init__(self):
        self.serviceDict = dict()
        self.bestInstanceDict = dict()

    def registerService(self, serviceId, serviceName, address, health=100):

        # Create instance of new service
        service = Service(serviceId, serviceName, address, health)
        instanceId = service.getInstanceId()

        # Create entries for service if no instance already exists
        if service.serviceId not in self.serviceDict:
            self.serviceDict[service.serviceId] = dict()
            self.bestInstanceDict[service.serviceId] = instanceId

        # Add instance to cluster and update best instance of service
        self.serviceDict[service.serviceId][instanceId] = service
        if self.serviceDict[service.serviceId][self.bestInstanceDict[service.serviceId]].health < service.health:
            self.bestInstanceDict[service.serviceId] = instanceId

        return True

    def deRegisterService(self, serviceId, address):

        # Raise exception if service doesn't exist
        if serviceId not in self.serviceDict:
            raise Exception("Service doesn't exist")

        # Raise exception if instance isn't registered
        instances = self.serviceDict[serviceId]
        instanceId = getInstanceId(serviceId, address.ip, address.port)
        if instanceId not in instances:
            raise Exception("Instance isn't registered")

        # Delete the instance from records
        del self.serviceDict[serviceId][instanceId]

        # Update bestInstance of the service if needed
        if self.bestInstanceDict[serviceId] == instanceId:
            bestHealth = 0
            for instanceId1 in self.serviceDict[serviceId]:
                if self.serviceDict[serviceId][instanceId1].health > bestHealth:
                    bestHealth = self.serviceDict[serviceId][instanceId1].health
                    self.bestInstanceDict[serviceId] = instanceId1

        # Delete record for entire service if this is the only instance of the service
        if len(self.serviceDict[serviceId].keys()) == 0:
            del self.serviceDict[serviceId]
            del self.bestInstanceDict[serviceId]

        return True

    def getInstance(self, serviceId):

        # Raise exception if service doesn't exist
        if serviceId not in self.serviceDict:
            raise Exception("Service doesn't exist")

        return self.serviceDict[serviceId][self.bestInstanceDict[serviceId]]

    def heartbeat(self, serviceId, address, health):

        # Raise exception if service doesn't exist
        if serviceId not in self.serviceDict:
            raise Exception("Service doen't exist")

        # Raise exception if instance isn't registered
        instanceId = getInstanceId(serviceId, address.ip, address.port)
        if instanceId not in self.serviceDict[serviceId]:
            raise Exception("Instance isn't registered")

        # Update health and heartbeat of instance
        self.serviceDict[serviceId][instanceId].health = health
        self.serviceDict[serviceId][instanceId].updateHeartBeat()

        # Update bestInstance of the service if needed
        bestHealth = 0
        for instanceId1 in self.serviceDict[serviceId]:
            if self.serviceDict[serviceId][instanceId1].health > bestHealth:
                bestHealth = self.serviceDict[serviceId][instanceId1].health
                self.bestInstanceDict[serviceId] = instanceId1

    def __str__(self):
        return "Service dictionary: " + str(self.serviceDict) + "\n" + \
            "Best instance dictionary: " + str(self.bestInstanceDict)

if __name__ == '__main__':

    serviceRegistry = ServiceRegistry()

    print (serviceRegistry)

    serviceRegistry.registerService(1, "Shamanyu", Address('192.168.1.1', '8083'), 98)

    print (serviceRegistry)

    serviceRegistry.registerService(2, "Sameer", Address('192.168.1.2', '8084'))

    print (serviceRegistry)

    serviceRegistry.registerService(1, "Arissss", Address('192.168.1.3', '8084'))

    print (serviceRegistry)

    serviceRegistry.deRegisterService(1, Address('192.168.1.3', '8084'))

    print (serviceRegistry)

    print (serviceRegistry.getInstance(1))

    print (serviceRegistry.getInstance(2))

    serviceRegistry.registerService(2, "Doshi", Address('192.168.1.2', '8087'), 81)

    print (serviceRegistry)

    serviceRegistry.heartbeat(2, Address('192.168.1.2', '8084'), 79)

    print (serviceRegistry)

    # print (serviceRegistry.getInstance(3))
